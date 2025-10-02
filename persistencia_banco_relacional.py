#!/usr/bin/env python3
"""
Sistema de Persistência no Banco Relacional - IoT Monitoring Sprint 3
Implementa persistência completa no banco MySQL modelado com 11 tabelas

Autor: Enterprise Challenge - Sprint 3 - Reply
Data: 2024
"""

import os
import sys
import json
import logging
import mysql.connector
from mysql.connector import Error, pooling
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any, Union
from contextlib import contextmanager
import threading
import time
from dataclasses import dataclass
from enum import Enum
import hashlib
import uuid

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger("PersistenciaBanco")

class QualidadeDados(Enum):
    EXCELENTE = "excelente"
    BOM = "bom"
    REGULAR = "regular"
    RUIM = "ruim"

class StatusDispositivo(Enum):
    ATIVO = "ativo"
    INATIVO = "inativo"
    MANUTENCAO = "manutencao"

class StatusSensor(Enum):
    ATIVO = "ativo"
    INATIVO = "inativo"
    FALHA = "falha"

class SeveridadeAlerta(Enum):
    BAIXA = "baixa"
    MEDIA = "media"
    ALTA = "alta"
    CRITICA = "critica"

class TipoLimite(Enum):
    MINIMO = "minimo"
    MAXIMO = "maximo"
    VARIACAO = "variacao"

@dataclass
class ConfiguracaoBanco:
    """Configuração de conexão com o banco de dados"""
    host: str = "localhost"
    port: int = 3306
    database: str = "iot_monitoring_db"
    username: str = "root"
    password: str = "password"
    pool_size: int = 10
    pool_name: str = "iot_pool"
    pool_reset_session: bool = True
    autocommit: bool = True
    charset: str = "utf8mb4"

class GerenciadorConexaoBanco:
    """
    Gerenciador de conexões com pool de conexões para MySQL
    """
    
    def __init__(self, config: ConfiguracaoBanco):
        self.config = config
        self.pool = None
        self._lock = threading.Lock()
        self._inicializar_pool()
    
    def _inicializar_pool(self):
        """Inicializa o pool de conexões"""
        try:
            self.pool = pooling.MySQLConnectionPool(
                pool_name=self.config.pool_name,
                pool_size=self.config.pool_size,
                pool_reset_session=self.config.pool_reset_session,
                host=self.config.host,
                port=self.config.port,
                database=self.config.database,
                user=self.config.username,
                password=self.config.password,
                charset=self.config.charset,
                autocommit=self.config.autocommit,
                use_unicode=True,
                sql_mode='TRADITIONAL'
            )
            logger.info(f"Pool de conexões inicializado: {self.config.pool_name}")
        except Error as e:
            logger.error(f"Erro ao inicializar pool de conexões: {e}")
            raise
    
    @contextmanager
    def obter_conexao(self):
        """Context manager para obter conexão do pool"""
        conexao = None
        try:
            conexao = self.pool.get_connection()
            yield conexao
        except Error as e:
            logger.error(f"Erro ao obter conexão: {e}")
            raise
        finally:
            if conexao and conexao.is_connected():
                conexao.close()
    
    def testar_conexao(self) -> bool:
        """Testa a conexão com o banco"""
        try:
            with self.obter_conexao() as conexao:
                cursor = conexao.cursor()
                cursor.execute("SELECT 1")
                resultado = cursor.fetchone()
                cursor.close()
                return resultado[0] == 1
        except Error as e:
            logger.error(f"Erro ao testar conexão: {e}")
            return False

class PersistenciaBancoRelacional:
    """
    Sistema completo de persistência no banco relacional modelado
    """
    
    def __init__(self, config: ConfiguracaoBanco):
        self.config = config
        self.gerenciador = GerenciadorConexaoBanco(config)
        self._lock = threading.Lock()
        self._inicializar_banco()
    
    def _inicializar_banco(self):
        """Inicializa o banco de dados e cria tabelas se necessário"""
        try:
            # Testa conexão
            if not self.gerenciador.testar_conexao():
                raise Exception("Não foi possível conectar ao banco de dados")
            
            # Verifica se as tabelas existem
            self._verificar_estrutura_banco()
            logger.info("Banco de dados inicializado com sucesso")
        except Exception as e:
            logger.error(f"Erro ao inicializar banco: {e}")
            raise
    
    def _verificar_estrutura_banco(self):
        """Verifica se a estrutura do banco está correta"""
        try:
            with self.gerenciador.obter_conexao() as conexao:
                cursor = conexao.cursor()
                
                # Verifica se as tabelas principais existem
                tabelas_necessarias = [
                    'dispositivos', 'tipos_sensor', 'sensores', 'leituras_sensores',
                    'modos_operacao', 'alertas', 'configuracoes_limites', 'usuarios',
                    'logs_sistema', 'dashboards', 'relatorios'
                ]
                
                cursor.execute("SHOW TABLES")
                tabelas_existentes = [tabela[0] for tabela in cursor.fetchall()]
                
                tabelas_faltando = [tabela for tabela in tabelas_necessarias if tabela not in tabelas_existentes]
                
                if tabelas_faltando:
                    logger.warning(f"Tabelas faltando: {tabelas_faltando}")
                    logger.info("Execute o script criar_tabelas_iot.sql para criar as tabelas")
                else:
                    logger.info("Estrutura do banco verificada com sucesso")
                
                cursor.close()
        except Error as e:
            logger.error(f"Erro ao verificar estrutura do banco: {e}")
            raise
    
    # =====================================================
    # OPERAÇÕES CRUD - DISPOSITIVOS
    # =====================================================
    
    def inserir_dispositivo(self, dispositivo: Dict[str, Any]) -> int:
        """Insere um novo dispositivo"""
        try:
            with self.gerenciador.obter_conexao() as conexao:
                cursor = conexao.cursor()
                
                query = """
                INSERT INTO dispositivos 
                (nome, mac_address, ip_address, localizacao, status, versao_firmware, observacoes)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                
                valores = (
                    dispositivo['nome'],
                    dispositivo['mac_address'],
                    dispositivo.get('ip_address'),
                    dispositivo.get('localizacao'),
                    dispositivo.get('status', StatusDispositivo.ATIVO.value),
                    dispositivo.get('versao_firmware'),
                    dispositivo.get('observacoes')
                )
                
                cursor.execute(query, valores)
                id_dispositivo = cursor.lastrowid
                
                # Log da operação
                self._log_operacao('INSERT', 'dispositivos', id_dispositivo, None, dispositivo)
                
                cursor.close()
                logger.info(f"Dispositivo inserido: {id_dispositivo}")
                return id_dispositivo
                
        except Error as e:
            logger.error(f"Erro ao inserir dispositivo: {e}")
            raise
    
    def obter_dispositivo(self, id_dispositivo: int) -> Optional[Dict[str, Any]]:
        """Obtém um dispositivo por ID"""
        try:
            with self.gerenciador.obter_conexao() as conexao:
                cursor = conexao.cursor(dictionary=True)
                
                query = "SELECT * FROM dispositivos WHERE id_dispositivo = %s"
                cursor.execute(query, (id_dispositivo,))
                
                resultado = cursor.fetchone()
                cursor.close()
                return resultado
                
        except Error as e:
            logger.error(f"Erro ao obter dispositivo: {e}")
            raise
    
    def listar_dispositivos(self, filtros: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Lista dispositivos com filtros opcionais"""
        try:
            with self.gerenciador.obter_conexao() as conexao:
                cursor = conexao.cursor(dictionary=True)
                
                query = "SELECT * FROM dispositivos WHERE 1=1"
                parametros = []
                
                if filtros:
                    if 'status' in filtros:
                        query += " AND status = %s"
                        parametros.append(filtros['status'])
                    
                    if 'localizacao' in filtros:
                        query += " AND localizacao LIKE %s"
                        parametros.append(f"%{filtros['localizacao']}%")
                
                query += " ORDER BY data_cadastro DESC"
                
                cursor.execute(query, parametros)
                resultados = cursor.fetchall()
                cursor.close()
                return resultados
                
        except Error as e:
            logger.error(f"Erro ao listar dispositivos: {e}")
            raise
    
    def atualizar_dispositivo(self, id_dispositivo: int, dados: Dict[str, Any]) -> bool:
        """Atualiza um dispositivo"""
        try:
            with self.gerenciador.obter_conexao() as conexao:
                cursor = conexao.cursor()
                
                # Obtém dados anteriores para log
                dados_anteriores = self.obter_dispositivo(id_dispositivo)
                
                # Constrói query de atualização
                campos = []
                valores = []
                
                for campo, valor in dados.items():
                    if campo != 'id_dispositivo':
                        campos.append(f"{campo} = %s")
                        valores.append(valor)
                
                if not campos:
                    return False
                
                query = f"UPDATE dispositivos SET {', '.join(campos)} WHERE id_dispositivo = %s"
                valores.append(id_dispositivo)
                
                cursor.execute(query, valores)
                linhas_afetadas = cursor.rowcount
                
                # Log da operação
                self._log_operacao('UPDATE', 'dispositivos', id_dispositivo, dados_anteriores, dados)
                
                cursor.close()
                logger.info(f"Dispositivo atualizado: {id_dispositivo}")
                return linhas_afetadas > 0
                
        except Error as e:
            logger.error(f"Erro ao atualizar dispositivo: {e}")
            raise
    
    # =====================================================
    # OPERAÇÕES CRUD - SENSORES
    # =====================================================
    
    def inserir_sensor(self, sensor: Dict[str, Any]) -> int:
        """Insere um novo sensor"""
        try:
            with self.gerenciador.obter_conexao() as conexao:
                cursor = conexao.cursor()
                
                query = """
                INSERT INTO sensores 
                (id_dispositivo, id_tipo_sensor, nome, pino_analogico, pino_digital, 
                 calibracao_min, calibracao_max, status, observacoes)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                
                valores = (
                    sensor['id_dispositivo'],
                    sensor['id_tipo_sensor'],
                    sensor['nome'],
                    sensor.get('pino_analogico'),
                    sensor.get('pino_digital'),
                    sensor.get('calibracao_min'),
                    sensor.get('calibracao_max'),
                    sensor.get('status', StatusSensor.ATIVO.value),
                    sensor.get('observacoes')
                )
                
                cursor.execute(query, valores)
                id_sensor = cursor.lastrowid
                
                # Log da operação
                self._log_operacao('INSERT', 'sensores', id_sensor, None, sensor)
                
                cursor.close()
                logger.info(f"Sensor inserido: {id_sensor}")
                return id_sensor
                
        except Error as e:
            logger.error(f"Erro ao inserir sensor: {e}")
            raise
    
    def obter_sensores_por_dispositivo(self, id_dispositivo: int) -> List[Dict[str, Any]]:
        """Obtém todos os sensores de um dispositivo"""
        try:
            with self.gerenciador.obter_conexao() as conexao:
                cursor = conexao.cursor(dictionary=True)
                
                query = """
                SELECT s.*, ts.nome as tipo_sensor_nome, ts.unidade_medida
                FROM sensores s
                JOIN tipos_sensor ts ON s.id_tipo_sensor = ts.id_tipo_sensor
                WHERE s.id_dispositivo = %s
                ORDER BY s.nome
                """
                
                cursor.execute(query, (id_dispositivo,))
                resultados = cursor.fetchall()
                cursor.close()
                return resultados
                
        except Error as e:
            logger.error(f"Erro ao obter sensores do dispositivo: {e}")
            raise
    
    # =====================================================
    # OPERAÇÕES CRUD - LEITURAS DE SENSORES
    # =====================================================
    
    def inserir_leitura_sensor(self, leitura: Dict[str, Any]) -> int:
        """Insere uma leitura de sensor"""
        try:
            with self.gerenciador.obter_conexao() as conexao:
                cursor = conexao.cursor()
                
                # Converte timestamp unix para datetime
                timestamp_datetime = datetime.fromtimestamp(leitura['timestamp_unix'])
                
                query = """
                INSERT INTO leituras_sensores 
                (id_sensor, timestamp_unix, timestamp_datetime, valor_numerico, 
                 valor_booleano, valor_string, qualidade_dados, anomalia_detectada)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
                
                valores = (
                    leitura['id_sensor'],
                    leitura['timestamp_unix'],
                    timestamp_datetime,
                    leitura.get('valor_numerico'),
                    leitura.get('valor_booleano'),
                    leitura.get('valor_string'),
                    leitura.get('qualidade_dados', QualidadeDados.BOM.value),
                    leitura.get('anomalia_detectada', False)
                )
                
                cursor.execute(query, valores)
                id_leitura = cursor.lastrowid
                
                # Atualiza última conexão do dispositivo
                self._atualizar_ultima_conexao_dispositivo(leitura['id_sensor'])
                
                # Verifica limites e cria alertas se necessário
                if leitura.get('valor_numerico') is not None:
                    self._verificar_limites_sensor(leitura['id_sensor'], leitura['valor_numerico'])
                
                cursor.close()
                logger.debug(f"Leitura inserida: {id_leitura}")
                return id_leitura
                
        except Error as e:
            logger.error(f"Erro ao inserir leitura: {e}")
            raise
    
    def inserir_multiplas_leituras(self, leituras: List[Dict[str, Any]]) -> List[int]:
        """Insere múltiplas leituras em lote"""
        try:
            with self.gerenciador.obter_conexao() as conexao:
                cursor = conexao.cursor()
                
                query = """
                INSERT INTO leituras_sensores 
                (id_sensor, timestamp_unix, timestamp_datetime, valor_numerico, 
                 valor_booleano, valor_string, qualidade_dados, anomalia_detectada)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
                
                valores_batch = []
                for leitura in leituras:
                    timestamp_datetime = datetime.fromtimestamp(leitura['timestamp_unix'])
                    valores_batch.append((
                        leitura['id_sensor'],
                        leitura['timestamp_unix'],
                        timestamp_datetime,
                        leitura.get('valor_numerico'),
                        leitura.get('valor_booleano'),
                        leitura.get('valor_string'),
                        leitura.get('qualidade_dados', QualidadeDados.BOM.value),
                        leitura.get('anomalia_detectada', False)
                    ))
                
                cursor.executemany(query, valores_batch)
                ids_leituras = list(range(cursor.lastrowid - len(leituras) + 1, cursor.lastrowid + 1))
                
                # Atualiza última conexão dos dispositivos
                dispositivos_atualizados = set()
                for leitura in leituras:
                    if leitura['id_sensor'] not in dispositivos_atualizados:
                        self._atualizar_ultima_conexao_dispositivo(leitura['id_sensor'])
                        dispositivos_atualizados.add(leitura['id_sensor'])
                
                cursor.close()
                logger.info(f"Inseridas {len(leituras)} leituras em lote")
                return ids_leituras
                
        except Error as e:
            logger.error(f"Erro ao inserir múltiplas leituras: {e}")
            raise
    
    def obter_leituras_sensor(self, id_sensor: int, limite: int = 100, 
                            data_inicio: Optional[datetime] = None, 
                            data_fim: Optional[datetime] = None) -> List[Dict[str, Any]]:
        """Obtém leituras de um sensor com filtros"""
        try:
            with self.gerenciador.obter_conexao() as conexao:
                cursor = conexao.cursor(dictionary=True)
                
                query = """
                SELECT * FROM leituras_sensores 
                WHERE id_sensor = %s
                """
                parametros = [id_sensor]
                
                if data_inicio:
                    query += " AND timestamp_datetime >= %s"
                    parametros.append(data_inicio)
                
                if data_fim:
                    query += " AND timestamp_datetime <= %s"
                    parametros.append(data_fim)
                
                query += " ORDER BY timestamp_datetime DESC LIMIT %s"
                parametros.append(limite)
                
                cursor.execute(query, parametros)
                resultados = cursor.fetchall()
                cursor.close()
                return resultados
                
        except Error as e:
            logger.error(f"Erro ao obter leituras do sensor: {e}")
            raise
    
    # =====================================================
    # OPERAÇÕES CRUD - ALERTAS
    # =====================================================
    
    def inserir_alerta(self, alerta: Dict[str, Any]) -> int:
        """Insere um novo alerta"""
        try:
            with self.gerenciador.obter_conexao() as conexao:
                cursor = conexao.cursor()
                
                query = """
                INSERT INTO alertas 
                (id_dispositivo, id_sensor, id_modo, tipo_alerta, severidade, 
                 titulo, descricao, valor_atual, valor_limite)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                
                valores = (
                    alerta['id_dispositivo'],
                    alerta.get('id_sensor'),
                    alerta['id_modo'],
                    alerta['tipo_alerta'],
                    alerta['severidade'],
                    alerta['titulo'],
                    alerta.get('descricao'),
                    alerta.get('valor_atual'),
                    alerta.get('valor_limite')
                )
                
                cursor.execute(query, valores)
                id_alerta = cursor.lastrowid
                
                # Log da operação
                self._log_operacao('INSERT', 'alertas', id_alerta, None, alerta)
                
                cursor.close()
                logger.info(f"Alerta inserido: {id_alerta}")
                return id_alerta
                
        except Error as e:
            logger.error(f"Erro ao inserir alerta: {e}")
            raise
    
    def obter_alertas_ativos(self, id_dispositivo: Optional[int] = None) -> List[Dict[str, Any]]:
        """Obtém alertas ativos"""
        try:
            with self.gerenciador.obter_conexao() as conexao:
                cursor = conexao.cursor(dictionary=True)
                
                query = """
                SELECT a.*, d.nome as dispositivo_nome, d.localizacao, 
                       s.nome as sensor_nome, mo.nome as modo_nome
                FROM alertas a
                JOIN dispositivos d ON a.id_dispositivo = d.id_dispositivo
                LEFT JOIN sensores s ON a.id_sensor = s.id_sensor
                JOIN modos_operacao mo ON a.id_modo = mo.id_modo
                WHERE a.status = 'ativo'
                """
                parametros = []
                
                if id_dispositivo:
                    query += " AND a.id_dispositivo = %s"
                    parametros.append(id_dispositivo)
                
                query += " ORDER BY a.timestamp_alerta DESC"
                
                cursor.execute(query, parametros)
                resultados = cursor.fetchall()
                cursor.close()
                return resultados
                
        except Error as e:
            logger.error(f"Erro ao obter alertas ativos: {e}")
            raise
    
    def resolver_alerta(self, id_alerta: int, usuario_resolucao: str, 
                       observacoes: Optional[str] = None) -> bool:
        """Resolve um alerta"""
        try:
            with self.gerenciador.obter_conexao() as conexao:
                cursor = conexao.cursor()
                
                query = """
                UPDATE alertas 
                SET status = 'resolvido', data_resolucao = NOW(), 
                    usuario_resolucao = %s, observacoes_resolucao = %s
                WHERE id_alerta = %s AND status = 'ativo'
                """
                
                cursor.execute(query, (usuario_resolucao, observacoes, id_alerta))
                linhas_afetadas = cursor.rowcount
                
                # Log da operação
                self._log_operacao('UPDATE', 'alertas', id_alerta, 
                                 {'status': 'ativo'}, {'status': 'resolvido'})
                
                cursor.close()
                logger.info(f"Alerta resolvido: {id_alerta}")
                return linhas_afetadas > 0
                
        except Error as e:
            logger.error(f"Erro ao resolver alerta: {e}")
            raise
    
    # =====================================================
    # OPERAÇÕES DE CONFIGURAÇÃO
    # =====================================================
    
    def configurar_limites_sensor(self, id_sensor: int, limites: List[Dict[str, Any]]) -> bool:
        """Configura limites para um sensor"""
        try:
            with self.gerenciador.obter_conexao() as conexao:
                cursor = conexao.cursor()
                
                # Remove configurações existentes
                cursor.execute("DELETE FROM configuracoes_limites WHERE id_sensor = %s", (id_sensor,))
                
                # Insere novas configurações
                query = """
                INSERT INTO configuracoes_limites 
                (id_sensor, tipo_limite, valor_limite, severidade, ativo, observacoes)
                VALUES (%s, %s, %s, %s, %s, %s)
                """
                
                for limite in limites:
                    valores = (
                        id_sensor,
                        limite['tipo_limite'],
                        limite['valor_limite'],
                        limite['severidade'],
                        limite.get('ativo', True),
                        limite.get('observacoes')
                    )
                    cursor.execute(query, valores)
                
                cursor.close()
                logger.info(f"Limites configurados para sensor: {id_sensor}")
                return True
                
        except Error as e:
            logger.error(f"Erro ao configurar limites: {e}")
            raise
    
    # =====================================================
    # OPERAÇÕES DE CONSULTA E ANÁLISE
    # =====================================================
    
    def obter_estatisticas_sensor(self, id_sensor: int, 
                                 data_inicio: datetime, 
                                 data_fim: datetime) -> Dict[str, Any]:
        """Obtém estatísticas de um sensor em um período"""
        try:
            with self.gerenciador.obter_conexao() as conexao:
                cursor = conexao.cursor()
                
                query = """
                SELECT 
                    COUNT(*) as total_leituras,
                    AVG(valor_numerico) as media,
                    MIN(valor_numerico) as minimo,
                    MAX(valor_numerico) as maximo,
                    STDDEV(valor_numerico) as desvio_padrao,
                    SUM(CASE WHEN anomalia_detectada = 1 THEN 1 ELSE 0 END) as anomalias,
                    SUM(CASE WHEN qualidade_dados = 'excelente' THEN 1 ELSE 0 END) as qualidade_excelente,
                    SUM(CASE WHEN qualidade_dados = 'bom' THEN 1 ELSE 0 END) as qualidade_bom,
                    SUM(CASE WHEN qualidade_dados = 'regular' THEN 1 ELSE 0 END) as qualidade_regular,
                    SUM(CASE WHEN qualidade_dados = 'ruim' THEN 1 ELSE 0 END) as qualidade_ruim
                FROM leituras_sensores 
                WHERE id_sensor = %s 
                AND timestamp_datetime BETWEEN %s AND %s
                AND valor_numerico IS NOT NULL
                """
                
                cursor.execute(query, (id_sensor, data_inicio, data_fim))
                resultado = cursor.fetchone()
                cursor.close()
                
                if resultado and resultado[0] > 0:
                    return {
                        'total_leituras': resultado[0],
                        'media': float(resultado[1]) if resultado[1] else 0,
                        'minimo': float(resultado[2]) if resultado[2] else 0,
                        'maximo': float(resultado[3]) if resultado[3] else 0,
                        'desvio_padrao': float(resultado[4]) if resultado[4] else 0,
                        'anomalias': resultado[5],
                        'qualidade_excelente': resultado[6],
                        'qualidade_bom': resultado[7],
                        'qualidade_regular': resultado[8],
                        'qualidade_ruim': resultado[9]
                    }
                else:
                    return {
                        'total_leituras': 0,
                        'media': 0,
                        'minimo': 0,
                        'maximo': 0,
                        'desvio_padrao': 0,
                        'anomalias': 0,
                        'qualidade_excelente': 0,
                        'qualidade_bom': 0,
                        'qualidade_regular': 0,
                        'qualidade_ruim': 0
                    }
                
        except Error as e:
            logger.error(f"Erro ao obter estatísticas: {e}")
            raise
    
    def obter_kpis_sistema(self) -> Dict[str, Any]:
        """Obtém KPIs do sistema"""
        try:
            with self.gerenciador.obter_conexao() as conexao:
                cursor = conexao.cursor()
                
                # Total de dispositivos
                cursor.execute("SELECT COUNT(*) FROM dispositivos WHERE status = 'ativo'")
                total_dispositivos = cursor.fetchone()[0]
                
                # Total de sensores
                cursor.execute("SELECT COUNT(*) FROM sensores WHERE status = 'ativo'")
                total_sensores = cursor.fetchone()[0]
                
                # Leituras nas últimas 24h
                cursor.execute("""
                    SELECT COUNT(*) FROM leituras_sensores 
                    WHERE timestamp_datetime >= DATE_SUB(NOW(), INTERVAL 24 HOUR)
                """)
                leituras_24h = cursor.fetchone()[0]
                
                # Alertas ativos
                cursor.execute("SELECT COUNT(*) FROM alertas WHERE status = 'ativo'")
                alertas_ativos = cursor.fetchone()[0]
                
                # Dispositivos offline (sem leitura nas últimas 2h)
                cursor.execute("""
                    SELECT COUNT(DISTINCT d.id_dispositivo) 
                    FROM dispositivos d
                    LEFT JOIN sensores s ON d.id_dispositivo = s.id_dispositivo
                    LEFT JOIN leituras_sensores ls ON s.id_sensor = ls.id_sensor
                    WHERE d.status = 'ativo' 
                    AND (ls.timestamp_datetime IS NULL OR ls.timestamp_datetime < DATE_SUB(NOW(), INTERVAL 2 HOUR))
                """)
                dispositivos_offline = cursor.fetchone()[0]
                
                cursor.close()
                
                return {
                    'total_dispositivos': total_dispositivos,
                    'total_sensores': total_sensores,
                    'leituras_24h': leituras_24h,
                    'alertas_ativos': alertas_ativos,
                    'dispositivos_offline': dispositivos_offline,
                    'timestamp': datetime.now().isoformat()
                }
                
        except Error as e:
            logger.error(f"Erro ao obter KPIs: {e}")
            raise
    
    # =====================================================
    # MÉTODOS AUXILIARES
    # =====================================================
    
    def _atualizar_ultima_conexao_dispositivo(self, id_sensor: int):
        """Atualiza a última conexão do dispositivo"""
        try:
            with self.gerenciador.obter_conexao() as conexao:
                cursor = conexao.cursor()
                
                query = """
                UPDATE dispositivos 
                SET ultima_conexao = NOW()
                WHERE id_dispositivo = (
                    SELECT id_dispositivo FROM sensores WHERE id_sensor = %s
                )
                """
                
                cursor.execute(query, (id_sensor,))
                cursor.close()
                
        except Error as e:
            logger.error(f"Erro ao atualizar última conexão: {e}")
    
    def _verificar_limites_sensor(self, id_sensor: int, valor: float):
        """Verifica limites e cria alertas se necessário"""
        try:
            with self.gerenciador.obter_conexao() as conexao:
                cursor = conexao.cursor()
                
                # Obtém configurações de limites ativas
                query = """
                SELECT tipo_limite, valor_limite, severidade, id_sensor
                FROM configuracoes_limites 
                WHERE id_sensor = %s AND ativo = TRUE
                """
                
                cursor.execute(query, (id_sensor,))
                limites = cursor.fetchall()
                
                for limite in limites:
                    tipo_limite, valor_limite, severidade, sensor_id = limite
                    
                    # Verifica se excedeu limite
                    if tipo_limite == 'maximo' and valor > valor_limite:
                        self._criar_alerta_limite(id_sensor, valor, valor_limite, severidade, 'maximo')
                    elif tipo_limite == 'minimo' and valor < valor_limite:
                        self._criar_alerta_limite(id_sensor, valor, valor_limite, severidade, 'minimo')
                
                cursor.close()
                
        except Error as e:
            logger.error(f"Erro ao verificar limites: {e}")
    
    def _criar_alerta_limite(self, id_sensor: int, valor_atual: float, 
                            valor_limite: float, severidade: str, tipo_limite: str):
        """Cria alerta de limite excedido"""
        try:
            # Obtém informações do sensor e dispositivo
            with self.gerenciador.obter_conexao() as conexao:
                cursor = conexao.cursor()
                
                query = """
                SELECT s.id_dispositivo, s.nome as sensor_nome, ts.nome as tipo_sensor
                FROM sensores s
                JOIN tipos_sensor ts ON s.id_tipo_sensor = ts.id_tipo_sensor
                WHERE s.id_sensor = %s
                """
                
                cursor.execute(query, (id_sensor,))
                resultado = cursor.fetchone()
                cursor.close()
                
                if resultado:
                    id_dispositivo, sensor_nome, tipo_sensor = resultado
                    
                    # Determina modo de operação baseado na severidade
                    id_modo = 2 if severidade in ['alta', 'critica'] else 1
                    
                    alerta = {
                        'id_dispositivo': id_dispositivo,
                        'id_sensor': id_sensor,
                        'id_modo': id_modo,
                        'tipo_alerta': tipo_sensor.lower(),
                        'severidade': severidade,
                        'titulo': f'Limite {tipo_limite} excedido: {sensor_nome}',
                        'descricao': f'Valor atual: {valor_atual:.2f} | Limite: {valor_limite:.2f}',
                        'valor_atual': valor_atual,
                        'valor_limite': valor_limite
                    }
                    
                    self.inserir_alerta(alerta)
                    
        except Error as e:
            logger.error(f"Erro ao criar alerta de limite: {e}")
    
    def _log_operacao(self, acao: str, tabela: str, id_registro: int, 
                     dados_anteriores: Optional[Dict], dados_novos: Optional[Dict]):
        """Registra log de operação"""
        try:
            with self.gerenciador.obter_conexao() as conexao:
                cursor = conexao.cursor()
                
                query = """
                INSERT INTO logs_sistema 
                (acao, tabela_afetada, id_registro_afetado, dados_anteriores, dados_novos)
                VALUES (%s, %s, %s, %s, %s)
                """
                
                dados_anteriores_json = json.dumps(dados_anteriores) if dados_anteriores else None
                dados_novos_json = json.dumps(dados_novos) if dados_novos else None
                
                cursor.execute(query, (acao, tabela, id_registro, dados_anteriores_json, dados_novos_json))
                cursor.close()
                
        except Error as e:
            logger.error(f"Erro ao registrar log: {e}")
    
    # =====================================================
    # MÉTODOS DE LIMPEZA E MANUTENÇÃO
    # =====================================================
    
    def limpar_dados_antigos(self, dias_manter: int = 30) -> int:
        """Remove dados antigos do banco"""
        try:
            with self.gerenciador.obter_conexao() as conexao:
                cursor = conexao.cursor()
                
                data_limite = datetime.now() - timedelta(days=dias_manter)
                
                # Remove leituras antigas
                query = "DELETE FROM leituras_sensores WHERE timestamp_datetime < %s"
                cursor.execute(query, (data_limite,))
                leituras_removidas = cursor.rowcount
                
                # Remove logs antigos
                query = "DELETE FROM logs_sistema WHERE timestamp_log < %s"
                cursor.execute(query, (data_limite,))
                logs_removidos = cursor.rowcount
                
                cursor.close()
                
                total_removido = leituras_removidas + logs_removidos
                logger.info(f"Dados antigos removidos: {total_removido} registros")
                return total_removido
                
        except Error as e:
            logger.error(f"Erro ao limpar dados antigos: {e}")
            raise
    
    def otimizar_banco(self) -> bool:
        """Otimiza o banco de dados"""
        try:
            with self.gerenciador.obter_conexao() as conexao:
                cursor = conexao.cursor()
                
                # Otimiza tabelas principais
                tabelas = ['leituras_sensores', 'alertas', 'logs_sistema']
                
                for tabela in tabelas:
                    cursor.execute(f"OPTIMIZE TABLE {tabela}")
                    logger.info(f"Tabela otimizada: {tabela}")
                
                cursor.close()
                logger.info("Banco de dados otimizado com sucesso")
                return True
                
        except Error as e:
            logger.error(f"Erro ao otimizar banco: {e}")
            raise

# =====================================================
# EXEMPLO DE USO
# =====================================================

def exemplo_uso():
    """Exemplo de uso do sistema de persistência"""
    
    # Configuração do banco
    config = ConfiguracaoBanco(
        host="localhost",
        port=3306,
        database="iot_monitoring_db",
        username="root",
        password="password"
    )
    
    # Inicializa sistema de persistência
    persistencia = PersistenciaBancoRelacional(config)
    
    # Exemplo: Inserir dispositivo
    dispositivo = {
        'nome': 'ESP32-Teste-01',
        'mac_address': 'AA:BB:CC:DD:EE:01',
        'ip_address': '192.168.1.100',
        'localizacao': 'Laboratório de Testes',
        'versao_firmware': 'v1.0.0'
    }
    
    id_dispositivo = persistencia.inserir_dispositivo(dispositivo)
    print(f"Dispositivo inserido: {id_dispositivo}")
    
    # Exemplo: Inserir sensor
    sensor = {
        'id_dispositivo': id_dispositivo,
        'id_tipo_sensor': 1,  # DHT22
        'nome': 'DHT22-Temperatura',
        'pino_digital': 2
    }
    
    id_sensor = persistencia.inserir_sensor(sensor)
    print(f"Sensor inserido: {id_sensor}")
    
    # Exemplo: Inserir leitura
    leitura = {
        'id_sensor': id_sensor,
        'timestamp_unix': time.time(),
        'valor_numerico': 25.5,
        'qualidade_dados': QualidadeDados.BOM.value
    }
    
    id_leitura = persistencia.inserir_leitura_sensor(leitura)
    print(f"Leitura inserida: {id_leitura}")
    
    # Exemplo: Obter KPIs
    kpis = persistencia.obter_kpis_sistema()
    print(f"KPIs do sistema: {kpis}")

if __name__ == "__main__":
    exemplo_uso()

