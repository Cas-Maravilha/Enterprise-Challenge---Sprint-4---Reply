#!/usr/bin/env python3
"""
Integração de Persistência ESP32 - Sistema IoT Monitoring Sprint 3
Integra o sistema de persistência com o pipeline ESP32 e coleta de dados

Autor: Enterprise Challenge - Sprint 3 - Reply
Data: 2024
"""

import os
import sys
import json
import time
import logging
import threading
import queue
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import paho.mqtt.client as mqtt
import numpy as np
from dataclasses import dataclass

# Importar módulos do projeto
from persistencia_banco_relacional import (
    PersistenciaBancoRelacional, 
    ConfiguracaoBanco,
    QualidadeDados,
    StatusDispositivo,
    StatusSensor
)

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger("IntegracaoPersistencia")

@dataclass
class ConfiguracaoMQTT:
    """Configuração MQTT para recebimento de dados"""
    broker: str = "broker.hivemq.com"
    port: int = 1883
    topic: str = "industrial/sensors/data"
    client_id: str = "persistencia_esp32"
    username: Optional[str] = None
    password: Optional[str] = None
    keepalive: int = 60

class IntegracaoPersistenciaESP32:
    """
    Sistema de integração entre coleta ESP32 e persistência no banco relacional
    """
    
    def __init__(self, config_banco: ConfiguracaoBanco, config_mqtt: ConfiguracaoMQTT):
        self.config_banco = config_banco
        self.config_mqtt = config_mqtt
        
        # Inicializa persistência
        self.persistencia = PersistenciaBancoRelacional(config_banco)
        
        # Configura MQTT
        self.client_mqtt = None
        self.fila_dados = queue.Queue(maxsize=1000)
        self.executando = False
        
        # Threads
        self.thread_processamento = None
        self.thread_mqtt = None
        
        # Estatísticas
        self.estatisticas = {
            'leituras_recebidas': 0,
            'leituras_processadas': 0,
            'leituras_erro': 0,
            'alertas_criados': 0,
            'inicio_execucao': datetime.now()
        }
        
        # Cache de dispositivos e sensores
        self.cache_dispositivos = {}
        self.cache_sensores = {}
        self._inicializar_cache()
    
    def _inicializar_cache(self):
        """Inicializa cache de dispositivos e sensores"""
        try:
            # Carrega dispositivos
            dispositivos = self.persistencia.listar_dispositivos()
            for dispositivo in dispositivos:
                self.cache_dispositivos[dispositivo['mac_address']] = dispositivo
            
            # Carrega sensores
            for dispositivo in dispositivos:
                sensores = self.persistencia.obter_sensores_por_dispositivo(dispositivo['id_dispositivo'])
                for sensor in sensores:
                    chave = f"{dispositivo['mac_address']}_{sensor['nome']}"
                    self.cache_sensores[chave] = sensor
            
            logger.info(f"Cache inicializado: {len(self.cache_dispositivos)} dispositivos, {len(self.cache_sensores)} sensores")
            
        except Exception as e:
            logger.error(f"Erro ao inicializar cache: {e}")
    
    def iniciar(self):
        """Inicia o sistema de integração"""
        try:
            logger.info("Iniciando sistema de integração ESP32-Persistência")
            
            # Inicia MQTT
            self._inicializar_mqtt()
            
            # Inicia thread de processamento
            self.executando = True
            self.thread_processamento = threading.Thread(target=self._processar_dados, daemon=True)
            self.thread_processamento.start()
            
            # Conecta MQTT
            self.client_mqtt.loop_start()
            
            logger.info("Sistema de integração iniciado com sucesso")
            
        except Exception as e:
            logger.error(f"Erro ao iniciar sistema: {e}")
            raise
    
    def parar(self):
        """Para o sistema de integração"""
        try:
            logger.info("Parando sistema de integração")
            
            self.executando = False
            
            # Para MQTT
            if self.client_mqtt:
                self.client_mqtt.loop_stop()
                self.client_mqtt.disconnect()
            
            # Aguarda thread de processamento
            if self.thread_processamento and self.thread_processamento.is_alive():
                self.thread_processamento.join(timeout=5)
            
            logger.info("Sistema de integração parado")
            
        except Exception as e:
            logger.error(f"Erro ao parar sistema: {e}")
    
    def _inicializar_mqtt(self):
        """Inicializa cliente MQTT"""
        try:
            self.client_mqtt = mqtt.Client(client_id=self.config_mqtt.client_id)
            
            if self.config_mqtt.username and self.config_mqtt.password:
                self.client_mqtt.username_pw_set(self.config_mqtt.username, self.config_mqtt.password)
            
            # Callbacks
            self.client_mqtt.on_connect = self._on_mqtt_connect
            self.client_mqtt.on_message = self._on_mqtt_message
            self.client_mqtt.on_disconnect = self._on_mqtt_disconnect
            
            # Conecta
            self.client_mqtt.connect(
                self.config_mqtt.broker,
                self.config_mqtt.port,
                self.config_mqtt.keepalive
            )
            
            logger.info(f"Cliente MQTT inicializado: {self.config_mqtt.broker}:{self.config_mqtt.port}")
            
        except Exception as e:
            logger.error(f"Erro ao inicializar MQTT: {e}")
            raise
    
    def _on_mqtt_connect(self, client, userdata, flags, rc):
        """Callback de conexão MQTT"""
        if rc == 0:
            logger.info("Conectado ao broker MQTT")
            client.subscribe(self.config_mqtt.topic)
            logger.info(f"Inscrito no tópico: {self.config_mqtt.topic}")
        else:
            logger.error(f"Falha na conexão MQTT: {rc}")
    
    def _on_mqtt_message(self, client, userdata, msg):
        """Callback de mensagem MQTT"""
        try:
            # Decodifica mensagem
            dados = json.loads(msg.payload.decode('utf-8'))
            
            # Adiciona à fila de processamento
            if not self.fila_dados.full():
                self.fila_dados.put(dados)
                self.estatisticas['leituras_recebidas'] += 1
            else:
                logger.warning("Fila de dados cheia, descartando mensagem")
            
        except Exception as e:
            logger.error(f"Erro ao processar mensagem MQTT: {e}")
            self.estatisticas['leituras_erro'] += 1
    
    def _on_mqtt_disconnect(self, client, userdata, rc):
        """Callback de desconexão MQTT"""
        logger.warning(f"Desconectado do broker MQTT: {rc}")
    
    def _processar_dados(self):
        """Thread de processamento de dados"""
        logger.info("Thread de processamento iniciada")
        
        while self.executando:
            try:
                # Processa dados da fila
                if not self.fila_dados.empty():
                    dados = self.fila_dados.get(timeout=1)
                    self._processar_leitura(dados)
                    self.fila_dados.task_done()
                else:
                    time.sleep(0.1)
                    
            except queue.Empty:
                continue
            except Exception as e:
                logger.error(f"Erro no processamento: {e}")
                time.sleep(1)
        
        logger.info("Thread de processamento finalizada")
    
    def _processar_leitura(self, dados: Dict[str, Any]):
        """Processa uma leitura de sensor"""
        try:
            # Valida dados básicos
            if not self._validar_dados_leitura(dados):
                return
            
            # Obtém informações do dispositivo e sensor
            dispositivo_info = self._obter_dispositivo_info(dados)
            if not dispositivo_info:
                logger.warning(f"Dispositivo não encontrado: {dados.get('mac_address')}")
                return
            
            sensor_info = self._obter_sensor_info(dados, dispositivo_info)
            if not sensor_info:
                logger.warning(f"Sensor não encontrado: {dados.get('sensor_nome')}")
                return
            
            # Processa leitura
            leitura = self._criar_leitura_sensor(dados, sensor_info)
            if leitura:
                # Insere no banco
                id_leitura = self.persistencia.inserir_leitura_sensor(leitura)
                self.estatisticas['leituras_processadas'] += 1
                
                # Verifica se criou alertas
                if self._verificar_alertas_criados(sensor_info['id_sensor']):
                    self.estatisticas['alertas_criados'] += 1
                
                logger.debug(f"Leitura processada: {id_leitura}")
            
        except Exception as e:
            logger.error(f"Erro ao processar leitura: {e}")
            self.estatisticas['leituras_erro'] += 1
    
    def _validar_dados_leitura(self, dados: Dict[str, Any]) -> bool:
        """Valida dados de leitura"""
        campos_obrigatorios = ['mac_address', 'sensor_nome', 'timestamp', 'valor']
        
        for campo in campos_obrigatorios:
            if campo not in dados:
                logger.warning(f"Campo obrigatório ausente: {campo}")
                return False
        
        return True
    
    def _obter_dispositivo_info(self, dados: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Obtém informações do dispositivo"""
        mac_address = dados['mac_address']
        
        # Verifica cache
        if mac_address in self.cache_dispositivos:
            return self.cache_dispositivos[mac_address]
        
        # Busca no banco
        try:
            dispositivos = self.persistencia.listar_dispositivos({'mac_address': mac_address})
            if dispositivos:
                dispositivo = dispositivos[0]
                self.cache_dispositivos[mac_address] = dispositivo
                return dispositivo
        except Exception as e:
            logger.error(f"Erro ao buscar dispositivo: {e}")
        
        return None
    
    def _obter_sensor_info(self, dados: Dict[str, Any], dispositivo_info: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Obtém informações do sensor"""
        chave = f"{dispositivo_info['mac_address']}_{dados['sensor_nome']}"
        
        # Verifica cache
        if chave in self.cache_sensores:
            return self.cache_sensores[chave]
        
        # Busca no banco
        try:
            sensores = self.persistencia.obter_sensores_por_dispositivo(dispositivo_info['id_dispositivo'])
            for sensor in sensores:
                if sensor['nome'] == dados['sensor_nome']:
                    self.cache_sensores[chave] = sensor
                    return sensor
        except Exception as e:
            logger.error(f"Erro ao buscar sensor: {e}")
        
        return None
    
    def _criar_leitura_sensor(self, dados: Dict[str, Any], sensor_info: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Cria estrutura de leitura para o banco"""
        try:
            # Converte timestamp
            timestamp_unix = float(dados['timestamp'])
            
            # Determina qualidade dos dados
            qualidade = self._determinar_qualidade_dados(dados)
            
            # Detecta anomalias
            anomalia = self._detectar_anomalia(dados, sensor_info)
            
            leitura = {
                'id_sensor': sensor_info['id_sensor'],
                'timestamp_unix': timestamp_unix,
                'valor_numerico': dados.get('valor'),
                'valor_booleano': dados.get('valor_booleano'),
                'valor_string': dados.get('valor_string'),
                'qualidade_dados': qualidade,
                'anomalia_detectada': anomalia
            }
            
            return leitura
            
        except Exception as e:
            logger.error(f"Erro ao criar leitura: {e}")
            return None
    
    def _determinar_qualidade_dados(self, dados: Dict[str, Any]) -> str:
        """Determina qualidade dos dados"""
        try:
            # Verifica se há ruído nos dados
            valor = dados.get('valor')
            if valor is None:
                return QualidadeDados.RUIM.value
            
            # Verifica se valor está dentro de faixas esperadas
            if isinstance(valor, (int, float)):
                if valor < -1000 or valor > 1000:  # Valores suspeitos
                    return QualidadeDados.RUIM.value
                elif abs(valor) > 500:  # Valores altos
                    return QualidadeDados.REGULAR.value
                else:
                    return QualidadeDados.BOM.value
            
            return QualidadeDados.BOM.value
            
        except Exception:
            return QualidadeDados.RUIM.value
    
    def _detectar_anomalia(self, dados: Dict[str, Any], sensor_info: Dict[str, Any]) -> bool:
        """Detecta anomalias nos dados"""
        try:
            valor = dados.get('valor')
            if valor is None or not isinstance(valor, (int, float)):
                return False
            
            # Verifica limites básicos
            if sensor_info.get('calibracao_min') and valor < sensor_info['calibracao_min']:
                return True
            
            if sensor_info.get('calibracao_max') and valor > sensor_info['calibracao_max']:
                return True
            
            # Verifica variação abrupta (simplificado)
            # Em um sistema real, usaria modelo ML mais sofisticado
            if abs(valor) > 100:  # Valores muito altos
                return True
            
            return False
            
        except Exception:
            return False
    
    def _verificar_alertas_criados(self, id_sensor: int) -> bool:
        """Verifica se foram criados alertas para o sensor"""
        try:
            # Verifica se há alertas ativos criados recentemente
            alertas = self.persistencia.obter_alertas_ativos()
            agora = datetime.now()
            
            for alerta in alertas:
                if (alerta['id_sensor'] == id_sensor and 
                    alerta['timestamp_alerta'] > agora - timedelta(minutes=1)):
                    return True
            
            return False
            
        except Exception:
            return False
    
    def obter_estatisticas(self) -> Dict[str, Any]:
        """Obtém estatísticas do sistema"""
        try:
            # Calcula tempo de execução
            tempo_execucao = datetime.now() - self.estatisticas['inicio_execucao']
            
            # Calcula taxa de processamento
            taxa_processamento = 0
            if tempo_execucao.total_seconds() > 0:
                taxa_processamento = self.estatisticas['leituras_processadas'] / tempo_execucao.total_seconds()
            
            # Obtém KPIs do banco
            kpis_banco = self.persistencia.obter_kpis_sistema()
            
            return {
                'tempo_execucao_segundos': tempo_execucao.total_seconds(),
                'leituras_recebidas': self.estatisticas['leituras_recebidas'],
                'leituras_processadas': self.estatisticas['leituras_processadas'],
                'leituras_erro': self.estatisticas['leituras_erro'],
                'alertas_criados': self.estatisticas['alertas_criados'],
                'taxa_processamento_por_segundo': taxa_processamento,
                'tamanho_fila': self.fila_dados.qsize(),
                'kpis_banco': kpis_banco
            }
            
        except Exception as e:
            logger.error(f"Erro ao obter estatísticas: {e}")
            return {}
    
    def configurar_limites_sensor(self, mac_address: str, sensor_nome: str, limites: List[Dict[str, Any]]) -> bool:
        """Configura limites para um sensor"""
        try:
            # Obtém informações do sensor
            dispositivo_info = self.cache_dispositivos.get(mac_address)
            if not dispositivo_info:
                logger.error(f"Dispositivo não encontrado: {mac_address}")
                return False
            
            sensores = self.persistencia.obter_sensores_por_dispositivo(dispositivo_info['id_dispositivo'])
            sensor_info = None
            
            for sensor in sensores:
                if sensor['nome'] == sensor_nome:
                    sensor_info = sensor
                    break
            
            if not sensor_info:
                logger.error(f"Sensor não encontrado: {sensor_nome}")
                return False
            
            # Configura limites
            return self.persistencia.configurar_limites_sensor(sensor_info['id_sensor'], limites)
            
        except Exception as e:
            logger.error(f"Erro ao configurar limites: {e}")
            return False

# =====================================================
# EXEMPLO DE USO
# =====================================================

def exemplo_uso():
    """Exemplo de uso do sistema de integração"""
    
    # Configurações
    config_banco = ConfiguracaoBanco(
        host="localhost",
        port=3306,
        database="iot_monitoring_db",
        username="root",
        password="password"
    )
    
    config_mqtt = ConfiguracaoMQTT(
        broker="broker.hivemq.com",
        port=1883,
        topic="industrial/sensors/data"
    )
    
    # Inicializa sistema
    integracao = IntegracaoPersistenciaESP32(config_banco, config_mqtt)
    
    try:
        # Inicia sistema
        integracao.iniciar()
        
        # Executa por 60 segundos
        print("Sistema executando... Pressione Ctrl+C para parar")
        time.sleep(60)
        
        # Mostra estatísticas
        stats = integracao.obter_estatisticas()
        print(f"Estatísticas: {json.dumps(stats, indent=2, default=str)}")
        
    except KeyboardInterrupt:
        print("Parando sistema...")
    finally:
        integracao.parar()

if __name__ == "__main__":
    exemplo_uso()

