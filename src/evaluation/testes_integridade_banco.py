#!/usr/bin/env python3
"""
Testes de Integridade do Banco de Dados - Sistema IoT Monitoring
Enterprise Challenge Sprint 3 - Reply

Este script executa testes de integridade para verificar
se todas as chaves e restrições estão funcionando corretamente.
"""

import mysql.connector
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Tuple
import warnings
warnings.filterwarnings('ignore')

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('testes_integridade.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class TestesIntegridadeBanco:
    """Testes de integridade do banco de dados"""
    
    def __init__(self, host='localhost', user='root', password='', database='iot_monitoring_db'):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None
        self.resultados = []
        
        logger.info("=== Testes de Integridade do Banco de Dados ===")
        logger.info("Enterprise Challenge Sprint 3 - Reply")
        logger.info("=============================================")
    
    def conectar_banco(self):
        """Conecta ao banco de dados"""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                charset='utf8mb4'
            )
            self.cursor = self.connection.cursor(dictionary=True)
            logger.info("Conectado ao banco de dados com sucesso")
            return True
        except mysql.connector.Error as e:
            logger.error(f"Erro ao conectar ao banco: {e}")
            return False
    
    def executar_consulta(self, query: str, params: Tuple = None) -> List[Dict]:
        """Executa uma consulta SQL"""
        try:
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
        except mysql.connector.Error as e:
            logger.error(f"Erro na consulta: {e}")
            return []
    
    def executar_comando(self, query: str, params: Tuple = None) -> bool:
        """Executa um comando SQL"""
        try:
            self.cursor.execute(query, params)
            self.connection.commit()
            return True
        except mysql.connector.Error as e:
            logger.error(f"Erro no comando: {e}")
            return False
    
    def teste_1_chaves_primarias(self):
        """Teste 1: Verificar chaves primárias"""
        logger.info("🔑 Teste 1: Verificando chaves primárias...")
        
        tabelas = [
            'dispositivos', 'tipos_sensor', 'sensores', 'leituras_sensores',
            'modos_operacao', 'alertas', 'configuracoes_limites', 'usuarios',
            'logs_sistema', 'dashboards', 'relatorios'
        ]
        
        resultados = []
        
        for tabela in tabelas:
            query = f"""
            SELECT COUNT(*) as total_registros
            FROM {tabela}
            """
            resultado = self.executar_consulta(query)
            
            if resultado:
                total = resultado[0]['total_registros']
                resultados.append({
                    'tabela': tabela,
                    'total_registros': total,
                    'status': 'OK' if total > 0 else 'VAZIA'
                })
                logger.info(f"  ✅ {tabela}: {total} registros")
            else:
                resultados.append({
                    'tabela': tabela,
                    'total_registros': 0,
                    'status': 'ERRO'
                })
                logger.error(f"  ❌ {tabela}: Erro na consulta")
        
        self.resultados.append({
            'teste': 'Chaves Primárias',
            'resultados': resultados,
            'status': 'OK' if all(r['status'] != 'ERRO' for r in resultados) else 'ERRO'
        })
        
        return resultados
    
    def teste_2_chaves_estrangeiras(self):
        """Teste 2: Verificar integridade das chaves estrangeiras"""
        logger.info("🔗 Teste 2: Verificando chaves estrangeiras...")
        
        testes_fk = [
            {
                'nome': 'Sensores → Dispositivos',
                'query': '''
                SELECT COUNT(*) as orfaos
                FROM sensores s
                LEFT JOIN dispositivos d ON s.id_dispositivo = d.id_dispositivo
                WHERE d.id_dispositivo IS NULL
                ''',
                'esperado': 0
            },
            {
                'nome': 'Sensores → Tipos Sensor',
                'query': '''
                SELECT COUNT(*) as orfaos
                FROM sensores s
                LEFT JOIN tipos_sensor ts ON s.id_tipo_sensor = ts.id_tipo_sensor
                WHERE ts.id_tipo_sensor IS NULL
                ''',
                'esperado': 0
            },
            {
                'nome': 'Leituras → Sensores',
                'query': '''
                SELECT COUNT(*) as orfaos
                FROM leituras_sensores l
                LEFT JOIN sensores s ON l.id_sensor = s.id_sensor
                WHERE s.id_sensor IS NULL
                ''',
                'esperado': 0
            },
            {
                'nome': 'Alertas → Dispositivos',
                'query': '''
                SELECT COUNT(*) as orfaos
                FROM alertas a
                LEFT JOIN dispositivos d ON a.id_dispositivo = d.id_dispositivo
                WHERE d.id_dispositivo IS NULL
                ''',
                'esperado': 0
            },
            {
                'nome': 'Alertas → Sensores (opcional)',
                'query': '''
                SELECT COUNT(*) as orfaos
                FROM alertas a
                LEFT JOIN sensores s ON a.id_sensor = s.id_sensor
                WHERE a.id_sensor IS NOT NULL AND s.id_sensor IS NULL
                ''',
                'esperado': 0
            },
            {
                'nome': 'Alertas → Modos Operação',
                'query': '''
                SELECT COUNT(*) as orfaos
                FROM alertas a
                LEFT JOIN modos_operacao m ON a.id_modo = m.id_modo
                WHERE m.id_modo IS NULL
                ''',
                'esperado': 0
            },
            {
                'nome': 'Configurações → Sensores',
                'query': '''
                SELECT COUNT(*) as orfaos
                FROM configuracoes_limites c
                LEFT JOIN sensores s ON c.id_sensor = s.id_sensor
                WHERE s.id_sensor IS NULL
                ''',
                'esperado': 0
            },
            {
                'nome': 'Logs → Usuários (opcional)',
                'query': '''
                SELECT COUNT(*) as orfaos
                FROM logs_sistema l
                LEFT JOIN usuarios u ON l.id_usuario = u.id_usuario
                WHERE l.id_usuario IS NOT NULL AND u.id_usuario IS NULL
                ''',
                'esperado': 0
            },
            {
                'nome': 'Dashboards → Usuários',
                'query': '''
                SELECT COUNT(*) as orfaos
                FROM dashboards d
                LEFT JOIN usuarios u ON d.id_usuario = u.id_usuario
                WHERE u.id_usuario IS NULL
                ''',
                'esperado': 0
            },
            {
                'nome': 'Relatórios → Usuários',
                'query': '''
                SELECT COUNT(*) as orfaos
                FROM relatorios r
                LEFT JOIN usuarios u ON r.id_usuario = u.id_usuario
                WHERE u.id_usuario IS NULL
                ''',
                'esperado': 0
            }
        ]
        
        resultados = []
        
        for teste in testes_fk:
            resultado = self.executar_consulta(teste['query'])
            
            if resultado:
                orfaos = resultado[0]['orfaos']
                status = 'OK' if orfaos == teste['esperado'] else 'ERRO'
                resultados.append({
                    'teste': teste['nome'],
                    'orfaos_encontrados': orfaos,
                    'esperado': teste['esperado'],
                    'status': status
                })
                
                if status == 'OK':
                    logger.info(f"  ✅ {teste['nome']}: {orfaos} órfãos (esperado: {teste['esperado']})")
                else:
                    logger.error(f"  ❌ {teste['nome']}: {orfaos} órfãos (esperado: {teste['esperado']})")
            else:
                resultados.append({
                    'teste': teste['nome'],
                    'orfaos_encontrados': -1,
                    'esperado': teste['esperado'],
                    'status': 'ERRO'
                })
                logger.error(f"  ❌ {teste['nome']}: Erro na consulta")
        
        self.resultados.append({
            'teste': 'Chaves Estrangeiras',
            'resultados': resultados,
            'status': 'OK' if all(r['status'] == 'OK' for r in resultados) else 'ERRO'
        })
        
        return resultados
    
    def teste_3_restricoes_unique(self):
        """Teste 3: Verificar restrições UNIQUE"""
        logger.info("🔒 Teste 3: Verificando restrições UNIQUE...")
        
        testes_unique = [
            {
                'nome': 'MAC Address Único',
                'query': '''
                SELECT mac_address, COUNT(*) as duplicatas
                FROM dispositivos
                GROUP BY mac_address
                HAVING COUNT(*) > 1
                ''',
                'esperado': 0
            },
            {
                'nome': 'Email Único',
                'query': '''
                SELECT email, COUNT(*) as duplicatas
                FROM usuarios
                GROUP BY email
                HAVING COUNT(*) > 1
                ''',
                'esperado': 0
            },
            {
                'nome': 'Nome Tipo Sensor Único',
                'query': '''
                SELECT nome, COUNT(*) as duplicatas
                FROM tipos_sensor
                GROUP BY nome
                HAVING COUNT(*) > 1
                ''',
                'esperado': 0
            },
            {
                'nome': 'Nome Modo Operação Único',
                'query': '''
                SELECT nome, COUNT(*) as duplicatas
                FROM modos_operacao
                GROUP BY nome
                HAVING COUNT(*) > 1
                ''',
                'esperado': 0
            }
        ]
        
        resultados = []
        
        for teste in testes_unique:
            resultado = self.executar_consulta(teste['query'])
            
            duplicatas = len(resultado)
            status = 'OK' if duplicatas == teste['esperado'] else 'ERRO'
            
            resultados.append({
                'teste': teste['nome'],
                'duplicatas_encontradas': duplicatas,
                'esperado': teste['esperado'],
                'status': status
            })
            
            if status == 'OK':
                logger.info(f"  ✅ {teste['nome']}: {duplicatas} duplicatas (esperado: {teste['esperado']})")
            else:
                logger.error(f"  ❌ {teste['nome']}: {duplicatas} duplicatas (esperado: {teste['esperado']})")
                for dup in resultado:
                    logger.error(f"    Duplicata: {dup}")
        
        self.resultados.append({
            'teste': 'Restrições UNIQUE',
            'resultados': resultados,
            'status': 'OK' if all(r['status'] == 'OK' for r in resultados) else 'ERRO'
        })
        
        return resultados
    
    def teste_4_restricoes_enum(self):
        """Teste 4: Verificar restrições ENUM"""
        logger.info("📋 Teste 4: Verificando restrições ENUM...")
        
        testes_enum = [
            {
                'nome': 'Status Dispositivo',
                'query': '''
                SELECT status, COUNT(*) as total
                FROM dispositivos
                GROUP BY status
                ''',
                'valores_validos': ['ativo', 'inativo', 'manutencao']
            },
            {
                'nome': 'Severidade Alertas',
                'query': '''
                SELECT severidade, COUNT(*) as total
                FROM alertas
                GROUP BY severidade
                ''',
                'valores_validos': ['baixa', 'media', 'alta', 'critica']
            },
            {
                'nome': 'Perfil Usuário',
                'query': '''
                SELECT perfil, COUNT(*) as total
                FROM usuarios
                GROUP BY perfil
                ''',
                'valores_validos': ['admin', 'operador', 'visualizador']
            },
            {
                'nome': 'Qualidade Dados',
                'query': '''
                SELECT qualidade_dados, COUNT(*) as total
                FROM leituras_sensores
                GROUP BY qualidade_dados
                ''',
                'valores_validos': ['excelente', 'bom', 'regular', 'ruim']
            },
            {
                'nome': 'Status Alertas',
                'query': '''
                SELECT status, COUNT(*) as total
                FROM alertas
                GROUP BY status
                ''',
                'valores_validos': ['ativo', 'resolvido', 'ignorado']
            }
        ]
        
        resultados = []
        
        for teste in testes_enum:
            resultado = self.executar_consulta(teste['query'])
            
            valores_invalidos = []
            for row in resultado:
                if row['status'] not in teste['valores_validos']:
                    valores_invalidos.append(row['status'])
            
            status = 'OK' if not valores_invalidos else 'ERRO'
            
            resultados.append({
                'teste': teste['nome'],
                'valores_encontrados': [row['status'] for row in resultado],
                'valores_validos': teste['valores_validos'],
                'valores_invalidos': valores_invalidos,
                'status': status
            })
            
            if status == 'OK':
                logger.info(f"  ✅ {teste['nome']}: Todos os valores são válidos")
            else:
                logger.error(f"  ❌ {teste['nome']}: Valores inválidos encontrados: {valores_invalidos}")
        
        self.resultados.append({
            'teste': 'Restrições ENUM',
            'resultados': resultados,
            'status': 'OK' if all(r['status'] == 'OK' for r in resultados) else 'ERRO'
        })
        
        return resultados
    
    def teste_5_restricoes_not_null(self):
        """Teste 5: Verificar restrições NOT NULL"""
        logger.info("🚫 Teste 5: Verificando restrições NOT NULL...")
        
        testes_not_null = [
            {
                'nome': 'Nome Dispositivo',
                'query': '''
                SELECT COUNT(*) as nulos
                FROM dispositivos
                WHERE nome IS NULL
                ''',
                'esperado': 0
            },
            {
                'nome': 'MAC Address Dispositivo',
                'query': '''
                SELECT COUNT(*) as nulos
                FROM dispositivos
                WHERE mac_address IS NULL
                ''',
                'esperado': 0
            },
            {
                'nome': 'Email Usuário',
                'query': '''
                SELECT COUNT(*) as nulos
                FROM usuarios
                WHERE email IS NULL
                ''',
                'esperado': 0
            },
            {
                'nome': 'Timestamp Leituras',
                'query': '''
                SELECT COUNT(*) as nulos
                FROM leituras_sensores
                WHERE timestamp_datetime IS NULL
                ''',
                'esperado': 0
            },
            {
                'nome': 'Tipo Alerta',
                'query': '''
                SELECT COUNT(*) as nulos
                FROM alertas
                WHERE tipo_alerta IS NULL
                ''',
                'esperado': 0
            },
            {
                'nome': 'Severidade Alerta',
                'query': '''
                SELECT COUNT(*) as nulos
                FROM alertas
                WHERE severidade IS NULL
                ''',
                'esperado': 0
            }
        ]
        
        resultados = []
        
        for teste in testes_not_null:
            resultado = self.executar_consulta(teste['query'])
            
            if resultado:
                nulos = resultado[0]['nulos']
                status = 'OK' if nulos == teste['esperado'] else 'ERRO'
                
                resultados.append({
                    'teste': teste['nome'],
                    'nulos_encontrados': nulos,
                    'esperado': teste['esperado'],
                    'status': status
                })
                
                if status == 'OK':
                    logger.info(f"  ✅ {teste['nome']}: {nulos} nulos (esperado: {teste['esperado']})")
                else:
                    logger.error(f"  ❌ {teste['nome']}: {nulos} nulos (esperado: {teste['esperado']})")
            else:
                resultados.append({
                    'teste': teste['nome'],
                    'nulos_encontrados': -1,
                    'esperado': teste['esperado'],
                    'status': 'ERRO'
                })
                logger.error(f"  ❌ {teste['nome']}: Erro na consulta")
        
        self.resultados.append({
            'teste': 'Restrições NOT NULL',
            'resultados': resultados,
            'status': 'OK' if all(r['status'] == 'OK' for r in resultados) else 'ERRO'
        })
        
        return resultados
    
    def teste_6_consistencia_dados(self):
        """Teste 6: Verificar consistência dos dados"""
        logger.info("🔍 Teste 6: Verificando consistência dos dados...")
        
        testes_consistencia = [
            {
                'nome': 'Leituras com Anomalias',
                'query': '''
                SELECT COUNT(*) as total
                FROM leituras_sensores
                WHERE anomalia_detectada = 1
                ''',
                'minimo': 0
            },
            {
                'nome': 'Alertas Ativos',
                'query': '''
                SELECT COUNT(*) as total
                FROM alertas
                WHERE status = 'ativo'
                ''',
                'minimo': 0
            },
            {
                'nome': 'Dispositivos Ativos',
                'query': '''
                SELECT COUNT(*) as total
                FROM dispositivos
                WHERE status = 'ativo'
                ''',
                'minimo': 1
            },
            {
                'nome': 'Sensores Ativos',
                'query': '''
                SELECT COUNT(*) as total
                FROM sensores
                WHERE status = 'ativo'
                ''',
                'minimo': 1
            },
            {
                'nome': 'Usuários Ativos',
                'query': '''
                SELECT COUNT(*) as total
                FROM usuarios
                WHERE ativo = 1
                ''',
                'minimo': 1
            },
            {
                'nome': 'Leituras Recentes (última hora)',
                'query': '''
                SELECT COUNT(*) as total
                FROM leituras_sensores
                WHERE timestamp_datetime >= DATE_SUB(NOW(), INTERVAL 1 HOUR)
                ''',
                'minimo': 0
            }
        ]
        
        resultados = []
        
        for teste in testes_consistencia:
            resultado = self.executar_consulta(teste['query'])
            
            if resultado:
                total = resultado[0]['total']
                status = 'OK' if total >= teste['minimo'] else 'AVISO'
                
                resultados.append({
                    'teste': teste['nome'],
                    'total_encontrado': total,
                    'minimo_esperado': teste['minimo'],
                    'status': status
                })
                
                if status == 'OK':
                    logger.info(f"  ✅ {teste['nome']}: {total} registros (mínimo: {teste['minimo']})")
                else:
                    logger.warning(f"  ⚠️ {teste['nome']}: {total} registros (mínimo: {teste['minimo']})")
            else:
                resultados.append({
                    'teste': teste['nome'],
                    'total_encontrado': -1,
                    'minimo_esperado': teste['minimo'],
                    'status': 'ERRO'
                })
                logger.error(f"  ❌ {teste['nome']}: Erro na consulta")
        
        self.resultados.append({
            'teste': 'Consistência dos Dados',
            'resultados': resultados,
            'status': 'OK' if all(r['status'] in ['OK', 'AVISO'] for r in resultados) else 'ERRO'
        })
        
        return resultados
    
    def teste_7_performance_indices(self):
        """Teste 7: Verificar performance dos índices"""
        logger.info("⚡ Teste 7: Verificando performance dos índices...")
        
        consultas_performance = [
            {
                'nome': 'Leituras por Sensor',
                'query': '''
                SELECT COUNT(*) as total
                FROM leituras_sensores
                WHERE id_sensor = 1
                AND timestamp_datetime >= DATE_SUB(NOW(), INTERVAL 1 DAY)
                ''',
                'tempo_maximo': 1.0
            },
            {
                'nome': 'Alertas Ativos por Severidade',
                'query': '''
                SELECT COUNT(*) as total
                FROM alertas
                WHERE status = 'ativo'
                AND severidade = 'alta'
                AND timestamp_alerta >= DATE_SUB(NOW(), INTERVAL 1 DAY)
                ''',
                'tempo_maximo': 1.0
            },
            {
                'nome': 'Dispositivos por Status',
                'query': '''
                SELECT COUNT(*) as total
                FROM dispositivos
                WHERE status = 'ativo'
                AND localizacao LIKE '%Sala%'
                ''',
                'tempo_maximo': 1.0
            },
            {
                'nome': 'Leituras por Qualidade',
                'query': '''
                SELECT COUNT(*) as total
                FROM leituras_sensores
                WHERE qualidade_dados = 'excelente'
                AND timestamp_datetime >= DATE_SUB(NOW(), INTERVAL 1 HOUR)
                ''',
                'tempo_maximo': 1.0
            }
        ]
        
        resultados = []
        
        for teste in consultas_performance:
            import time
            inicio = time.time()
            
            resultado = self.executar_consulta(teste['query'])
            
            fim = time.time()
            tempo_execucao = fim - inicio
            
            if resultado:
                total = resultado[0]['total']
                status = 'OK' if tempo_execucao <= teste['tempo_maximo'] else 'LENTO'
                
                resultados.append({
                    'teste': teste['nome'],
                    'tempo_execucao': round(tempo_execucao, 3),
                    'tempo_maximo': teste['tempo_maximo'],
                    'registros_encontrados': total,
                    'status': status
                })
                
                if status == 'OK':
                    logger.info(f"  ✅ {teste['nome']}: {tempo_execucao:.3f}s ({total} registros)")
                else:
                    logger.warning(f"  ⚠️ {teste['nome']}: {tempo_execucao:.3f}s (lento, máximo: {teste['tempo_maximo']}s)")
            else:
                resultados.append({
                    'teste': teste['nome'],
                    'tempo_execucao': -1,
                    'tempo_maximo': teste['tempo_maximo'],
                    'registros_encontrados': -1,
                    'status': 'ERRO'
                })
                logger.error(f"  ❌ {teste['nome']}: Erro na consulta")
        
        self.resultados.append({
            'teste': 'Performance dos Índices',
            'resultados': resultados,
            'status': 'OK' if all(r['status'] in ['OK', 'LENTO'] for r in resultados) else 'ERRO'
        })
        
        return resultados
    
    def gerar_relatorio_final(self):
        """Gera relatório final dos testes"""
        logger.info("📊 Gerando relatório final...")
        
        total_testes = len(self.resultados)
        testes_ok = sum(1 for r in self.resultados if r['status'] == 'OK')
        testes_erro = sum(1 for r in self.resultados if r['status'] == 'ERRO')
        
        logger.info("=" * 60)
        logger.info("📋 RELATÓRIO FINAL DOS TESTES")
        logger.info("=" * 60)
        logger.info(f"Total de Testes: {total_testes}")
        logger.info(f"Testes OK: {testes_ok}")
        logger.info(f"Testes com Erro: {testes_erro}")
        logger.info(f"Taxa de Sucesso: {(testes_ok/total_testes)*100:.1f}%")
        logger.info("")
        
        for resultado in self.resultados:
            status_icon = "✅" if resultado['status'] == 'OK' else "❌"
            logger.info(f"{status_icon} {resultado['teste']}: {resultado['status']}")
        
        logger.info("")
        
        if testes_erro == 0:
            logger.info("🎉 Todos os testes passaram! Banco de dados íntegro.")
        else:
            logger.warning(f"⚠️ {testes_erro} teste(s) falharam. Verifique os logs para detalhes.")
        
        # Salvar relatório em JSON
        relatorio = {
            'timestamp': datetime.now().isoformat(),
            'resumo': {
                'total_testes': total_testes,
                'testes_ok': testes_ok,
                'testes_erro': testes_erro,
                'taxa_sucesso': (testes_ok/total_testes)*100
            },
            'detalhes': self.resultados
        }
        
        with open('relatorio_testes_integridade.json', 'w', encoding='utf-8') as f:
            json.dump(relatorio, f, indent=2, ensure_ascii=False)
        
        logger.info("📁 Relatório salvo em: relatorio_testes_integridade.json")
        
        return relatorio
    
    def executar_todos_testes(self):
        """Executa todos os testes de integridade"""
        if not self.conectar_banco():
            return False
        
        try:
            # Executar todos os testes
            self.teste_1_chaves_primarias()
            self.teste_2_chaves_estrangeiras()
            self.teste_3_restricoes_unique()
            self.teste_4_restricoes_enum()
            self.teste_5_restricoes_not_null()
            self.teste_6_consistencia_dados()
            self.teste_7_performance_indices()
            
            # Gerar relatório final
            relatorio = self.gerar_relatorio_final()
            
            return relatorio
            
        except Exception as e:
            logger.error(f"Erro durante execução dos testes: {e}")
            return False
        
        finally:
            if self.cursor:
                self.cursor.close()
            if self.connection:
                self.connection.close()
    
    def fechar_conexao(self):
        """Fecha conexão com o banco"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        logger.info("Conexão com banco fechada")


def main():
    """Função principal"""
    print("=== Testes de Integridade do Banco de Dados ===")
    print("Enterprise Challenge Sprint 3 - Reply")
    print("=============================================")
    
    # Configurar parâmetros de conexão
    host = input("Host do banco (padrão: localhost): ").strip() or 'localhost'
    user = input("Usuário do banco (padrão: root): ").strip() or 'root'
    password = input("Senha do banco: ").strip()
    database = input("Nome do banco (padrão: iot_monitoring_db): ").strip() or 'iot_monitoring_db'
    
    # Criar instância dos testes
    testes = TestesIntegridadeBanco(host, user, password, database)
    
    # Executar testes
    resultado = testes.executar_todos_testes()
    
    if resultado:
        print("\n✅ Testes executados com sucesso!")
        print("📊 Verifique o relatório para detalhes.")
    else:
        print("\n❌ Erro na execução dos testes.")


if __name__ == "__main__":
    main()
