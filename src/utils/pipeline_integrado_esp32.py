#!/usr/bin/env python3
"""
Pipeline Integrado - Sistema IoT Monitoring Sprint 3
Integra as três entregas em um pipeline executável completo:
- Coleta/ingestão de dados do ESP32 (Wokwi/VSCode/PlatformIO)
- Processamento e armazenamento em banco de dados
- Machine Learning e detecção de anomalias
- Dashboard e alertas em tempo real

Autor: Enterprise Challenge - Sprint 3 - Reply
Data: 2024
"""

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import time
import json
import logging
import threading
import queue
import paho.mqtt.client as mqtt
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import mysql.connector
from mysql.connector import Error
import joblib
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns
from dotenv import load_dotenv

# Importar módulos do projeto
from src.models.modelos_ia import ModeloEnsemble
from src.utils.kpis_negocio import KPIsNegocio
from src.monitoring.monitoramento_drift import MonitoramentoDrift
from src.evaluation.metricas_validacao_detalhadas import MetricasValidacaoDetalhadas

# Carregar variáveis de ambiente
load_dotenv()

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("pipeline_integrado.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("Pipeline Integrado")

class PipelineIntegradoESP32:
    """
    Pipeline integrado para coleta, processamento e análise de dados IoT
    """
    
    def __init__(self, config_path: str = "configs/config_pipeline.json"):
        """
        Inicializa o pipeline integrado
        
        Args:
            config_path: Caminho para arquivo de configuração
        """
        self.config = self._carregar_configuracao(config_path)
        self.fila_dados = queue.Queue(maxsize=1000)
        self.fila_alertas = queue.Queue(maxsize=100)
        
        # Componentes do pipeline
        self.modelo_ml = None
        self.scaler = None
        self.kpis_negocio = KPIsNegocio()
        self.monitor_drift = MonitoramentoDrift()
        self.metricas_validacao = MetricasValidacaoDetalhadas()
        
        # Conexões
        self.mqtt_client = None
        self.db_connection = None
        
        # Controle de execução
        self.executando = False
        self.threads = []
        
        # Estatísticas
        self.stats = {
            'dados_recebidos': 0,
            'dados_processados': 0,
            'anomalias_detectadas': 0,
            'alertas_enviados': 0,
            'inicio_execucao': None
        }
        
        logger.info("Pipeline Integrado ESP32 inicializado")
    
    def _carregar_configuracao(self, config_path: str) -> Dict:
        """Carrega configuração do pipeline"""
        config_padrao = {
            "mqtt": {
                "broker": "broker.hivemq.com",
                "port": 1883,
                "topic": "industrial/sensors/data",
                "client_id": "pipeline_integrado_esp32",
                "username": None,
                "password": None
            },
            "database": {
                "host": "localhost",
                "port": 3306,
                "database": "iot_monitoring",
                "username": "root",
                "password": "password"
            },
            "ml": {
                "modelo_path": "ml/modelo_anomalia_iot_completo.pkl",
                "scaler_path": "ml/scaler_iot.pkl",
                "threshold_anomalia": 0.5,
                "retreinar_intervalo_horas": 24
            },
            "monitoramento": {
                "drift_threshold": 0.05,
                "kpi_update_intervalo_minutos": 5,
                "dashboard_update_intervalo_segundos": 30
            },
            "alertas": {
                "email_enabled": False,
                "email_smtp": "smtp.gmail.com",
                "email_port": 587,
                "email_user": "",
                "email_password": "",
                "email_to": []
            }
        }
        
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    config_custom = json.load(f)
                config_padrao.update(config_custom)
                logger.info(f"Configuração carregada de {config_path}")
            except Exception as e:
                logger.warning(f"Erro ao carregar configuração: {e}. Usando configuração padrão.")
        else:
            # Salvar configuração padrão
            with open(config_path, 'w') as f:
                json.dump(config_padrao, f, indent=2)
            logger.info(f"Configuração padrão salva em {config_path}")
        
        return config_padrao
    
    def conectar_mqtt(self) -> bool:
        """Conecta ao broker MQTT"""
        try:
            self.mqtt_client = mqtt.Client(self.config["mqtt"]["client_id"])
            
            if self.config["mqtt"]["username"]:
                self.mqtt_client.username_pw_set(
                    self.config["mqtt"]["username"], 
                    self.config["mqtt"]["password"]
                )
            
            # Callbacks
            self.mqtt_client.on_connect = self._on_mqtt_connect
            self.mqtt_client.on_message = self._on_mqtt_message
            self.mqtt_client.on_disconnect = self._on_mqtt_disconnect
            
            # Conectar
            self.mqtt_client.connect(
                self.config["mqtt"]["broker"], 
                self.config["mqtt"]["port"], 
                60
            )
            
            # Iniciar loop em thread separada
            self.mqtt_client.loop_start()
            
            logger.info("Conectado ao broker MQTT")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao conectar MQTT: {e}")
            return False
    
    def _on_mqtt_connect(self, client, userdata, flags, rc):
        """Callback de conexão MQTT"""
        if rc == 0:
            logger.info("MQTT conectado com sucesso")
            # Subscrever ao tópico
            client.subscribe(self.config["mqtt"]["topic"])
            logger.info(f"Subscrito ao tópico: {self.config['mqtt']['topic']}")
        else:
            logger.error(f"Falha na conexão MQTT. Código: {rc}")
    
    def _on_mqtt_message(self, client, userdata, msg):
        """Callback de mensagem MQTT recebida"""
        try:
            # Decodificar mensagem JSON
            dados = json.loads(msg.payload.decode())
            
            # Adicionar timestamp de recebimento
            dados['timestamp_recebimento'] = datetime.now().isoformat()
            
            # Adicionar à fila de processamento
            if not self.fila_dados.full():
                self.fila_dados.put(dados)
                self.stats['dados_recebidos'] += 1
                logger.debug(f"Dados recebidos: {dados}")
            else:
                logger.warning("Fila de dados cheia. Dados descartados.")
                
        except Exception as e:
            logger.error(f"Erro ao processar mensagem MQTT: {e}")
    
    def _on_mqtt_disconnect(self, client, userdata, rc):
        """Callback de desconexão MQTT"""
        logger.warning("MQTT desconectado")
    
    def conectar_banco_dados(self) -> bool:
        """Conecta ao banco de dados MySQL"""
        try:
            self.db_connection = mysql.connector.connect(
                host=self.config["database"]["host"],
                port=self.config["database"]["port"],
                database=self.config["database"]["database"],
                user=self.config["database"]["username"],
                password=self.config["database"]["password"]
            )
            
            if self.db_connection.is_connected():
                logger.info("Conectado ao banco de dados MySQL")
                return True
            else:
                logger.error("Falha na conexão com banco de dados")
                return False
                
        except Error as e:
            logger.error(f"Erro ao conectar banco de dados: {e}")
            return False
    
    def carregar_modelo_ml(self) -> bool:
        """Carrega modelo de ML treinado"""
        try:
            modelo_path = self.config["ml"]["modelo_path"]
            scaler_path = self.config["ml"]["scaler_path"]
            
            if os.path.exists(modelo_path):
                self.modelo_ml = joblib.load(modelo_path)
                logger.info(f"Modelo ML carregado: {modelo_path}")
            else:
                logger.warning(f"Modelo ML não encontrado: {modelo_path}")
                return False
            
            if os.path.exists(scaler_path):
                self.scaler = joblib.load(scaler_path)
                logger.info(f"Scaler carregado: {scaler_path}")
            else:
                logger.warning(f"Scaler não encontrado: {scaler_path}")
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Erro ao carregar modelo ML: {e}")
            return False
    
    def processar_dados(self, dados: Dict) -> Dict:
        """
        Processa dados recebidos do ESP32
        
        Args:
            dados: Dados recebidos do ESP32
            
        Returns:
            dict: Dados processados com predições
        """
        try:
            # Preparar features para ML
            features = self._extrair_features(dados)
            
            # Normalizar features
            if self.scaler:
                features_scaled = self.scaler.transform([features])
            else:
                features_scaled = [features]
            
            # Fazer predição de anomalia
            if self.modelo_ml:
                predicao_anomalia = self.modelo_ml.predict(features_scaled)[0]
                probabilidade_anomalia = self.modelo_ml.predict_proba(features_scaled)[0][1]
            else:
                predicao_anomalia = 0
                probabilidade_anomalia = 0.0
            
            # Adicionar resultados ao dados
            dados_processados = dados.copy()
            dados_processados.update({
                'predicao_anomalia': int(predicao_anomalia),
                'probabilidade_anomalia': float(probabilidade_anomalia),
                'timestamp_processamento': datetime.now().isoformat(),
                'features_utilizadas': features
            })
            
            # Detectar se é anomalia
            if predicao_anomalia == 1:
                self.stats['anomalias_detectadas'] += 1
                logger.warning(f"Anomalia detectada! Probabilidade: {probabilidade_anomalia:.3f}")
                
                # Adicionar à fila de alertas
                if not self.fila_alertas.full():
                    self.fila_alertas.put(dados_processados)
            
            self.stats['dados_processados'] += 1
            return dados_processados
            
        except Exception as e:
            logger.error(f"Erro ao processar dados: {e}")
            return dados
    
    def _extrair_features(self, dados: Dict) -> List[float]:
        """Extrai features dos dados para ML"""
        features = []
        
        # Features primárias
        features.extend([
            dados.get('temperature', 0.0),
            dados.get('pressure', 0.0),
            dados.get('vibration', 0.0),
            dados.get('level', 0.0),
            dados.get('accel_x', 0.0),
            dados.get('accel_y', 0.0),
            dados.get('accel_z', 0.0)
        ])
        
        # Features derivadas
        if 'temperature' in dados and 'pressure' in dados:
            features.append(dados['temperature'] / max(dados['pressure'], 0.001))
        else:
            features.append(0.0)
        
        if 'vibration' in dados and 'level' in dados:
            features.append(dados['vibration'] * dados['level'])
        else:
            features.append(0.0)
        
        # Adicionar features de tempo (hora do dia, dia da semana)
        timestamp = dados.get('timestamp', time.time())
        dt_obj = datetime.fromtimestamp(timestamp)
        features.extend([
            dt_obj.hour / 24.0,  # Hora normalizada
            dt_obj.weekday() / 7.0,  # Dia da semana normalizado
            dt_obj.month / 12.0  # Mês normalizado
        ])
        
        return features
    
    def salvar_dados_banco(self, dados: Dict) -> bool:
        """Salva dados processados no banco de dados"""
        try:
            cursor = self.db_connection.cursor()
            
            # Inserir dados na tabela leituras_sensores
            query = """
            INSERT INTO leituras_sensores 
            (id_sensor, timestamp_unix, timestamp_datetime, valor_numerico, 
             anomalia_detectada, data_coleta, qualidade_dados)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            
            # Assumir sensor ID 1 para simplicidade
            sensor_id = 1
            timestamp_unix = dados.get('timestamp', int(time.time()))
            timestamp_datetime = datetime.fromtimestamp(timestamp_unix)
            valor_numerico = dados.get('temperature', 0.0)  # Usar temperatura como valor principal
            anomalia_detectada = dados.get('predicao_anomalia', 0)
            data_coleta = datetime.now()
            qualidade_dados = 1.0  # Assumir qualidade boa
            
            cursor.execute(query, (
                sensor_id, timestamp_unix, timestamp_datetime, valor_numerico,
                anomalia_detectada, data_coleta, qualidade_dados
            ))
            
            self.db_connection.commit()
            cursor.close()
            
            logger.debug("Dados salvos no banco de dados")
            return True
            
        except Error as e:
            logger.error(f"Erro ao salvar dados no banco: {e}")
            return False
    
    def processar_alertas(self):
        """Processa alertas de anomalias detectadas"""
        while not self.fila_alertas.empty():
            try:
                dados_alerta = self.fila_alertas.get_nowait()
                
                # Criar alerta
                alerta = {
                    'timestamp': datetime.now().isoformat(),
                    'tipo': 'anomalia_detectada',
                    'severidade': 'alta' if dados_alerta['probabilidade_anomalia'] > 0.8 else 'media',
                    'dados': dados_alerta,
                    'mensagem': f"Anomalia detectada com probabilidade {dados_alerta['probabilidade_anomalia']:.3f}"
                }
                
                # Salvar alerta no banco
                self._salvar_alerta_banco(alerta)
                
                # Enviar notificação (se configurado)
                self._enviar_notificacao(alerta)
                
                self.stats['alertas_enviados'] += 1
                logger.warning(f"Alerta processado: {alerta['mensagem']}")
                
            except queue.Empty:
                break
            except Exception as e:
                logger.error(f"Erro ao processar alerta: {e}")
    
    def _salvar_alerta_banco(self, alerta: Dict) -> bool:
        """Salva alerta no banco de dados"""
        try:
            cursor = self.db_connection.cursor()
            
            query = """
            INSERT INTO alertas 
            (id_dispositivo, id_sensor, tipo_alerta, severidade, titulo, 
             descricao, valor_atual, timestamp_alerta, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            cursor.execute(query, (
                1,  # dispositivo_id
                1,  # sensor_id
                alerta['tipo'],
                alerta['severidade'],
                'Anomalia Detectada',
                alerta['mensagem'],
                alerta['dados'].get('probabilidade_anomalia', 0.0),
                datetime.now(),
                'ativo'
            ))
            
            self.db_connection.commit()
            cursor.close()
            
            return True
            
        except Error as e:
            logger.error(f"Erro ao salvar alerta no banco: {e}")
            return False
    
    def _enviar_notificacao(self, alerta: Dict):
        """Envia notificação de alerta"""
        # Implementar envio de email, SMS, etc.
        logger.info(f"Notificação enviada: {alerta['mensagem']}")
    
    def thread_processamento_dados(self):
        """Thread para processamento contínuo de dados"""
        logger.info("Thread de processamento de dados iniciada")
        
        while self.executando:
            try:
                # Processar dados da fila
                if not self.fila_dados.empty():
                    dados = self.fila_dados.get(timeout=1)
                    dados_processados = self.processar_dados(dados)
                    
                    # Salvar no banco
                    self.salvar_dados_banco(dados_processados)
                
                # Processar alertas
                self.processar_alertas()
                
                time.sleep(0.1)  # Pequena pausa para não sobrecarregar CPU
                
            except queue.Empty:
                continue
            except Exception as e:
                logger.error(f"Erro na thread de processamento: {e}")
                time.sleep(1)
    
    def thread_monitoramento_kpis(self):
        """Thread para monitoramento de KPIs"""
        logger.info("Thread de monitoramento de KPIs iniciada")
        
        while self.executando:
            try:
                # Calcular KPIs (simplificado)
                kpis = {
                    'dados_recebidos_total': self.stats['dados_recebidos'],
                    'dados_processados_total': self.stats['dados_processados'],
                    'anomalias_detectadas_total': self.stats['anomalias_detectadas'],
                    'alertas_enviados_total': self.stats['alertas_enviados'],
                    'uptime_horas': (datetime.now() - self.stats['inicio_execucao']).total_seconds() / 3600
                }
                
                # Registrar KPIs
                self.kpis_negocio.registrar_kpis(kpis)
                
                logger.info(f"KPIs atualizados: {kpis}")
                
                # Aguardar próximo ciclo
                time.sleep(self.config["monitoramento"]["kpi_update_intervalo_minutos"] * 60)
                
            except Exception as e:
                logger.error(f"Erro na thread de KPIs: {e}")
                time.sleep(60)
    
    def gerar_relatorio_status(self) -> Dict:
        """Gera relatório de status do pipeline"""
        uptime = datetime.now() - self.stats['inicio_execucao'] if self.stats['inicio_execucao'] else timedelta(0)
        
        return {
            'status': 'executando' if self.executando else 'parado',
            'uptime_segundos': uptime.total_seconds(),
            'estatisticas': self.stats.copy(),
            'fila_dados_tamanho': self.fila_dados.qsize(),
            'fila_alertas_tamanho': self.fila_alertas.qsize(),
            'conexoes': {
                'mqtt': self.mqtt_client.is_connected() if self.mqtt_client else False,
                'banco_dados': self.db_connection.is_connected() if self.db_connection else False
            },
            'modelo_ml_carregado': self.modelo_ml is not None,
            'timestamp': datetime.now().isoformat()
        }
    
    def iniciar_pipeline(self):
        """Inicia o pipeline integrado"""
        logger.info("Iniciando Pipeline Integrado ESP32...")
        
        # Conectar componentes
        if not self.conectar_mqtt():
            logger.error("Falha ao conectar MQTT. Pipeline não iniciado.")
            return False
        
        if not self.conectar_banco_dados():
            logger.error("Falha ao conectar banco de dados. Pipeline não iniciado.")
            return False
        
        if not self.carregar_modelo_ml():
            logger.warning("Modelo ML não carregado. Continuando sem ML.")
        
        # Iniciar execução
        self.executando = True
        self.stats['inicio_execucao'] = datetime.now()
        
        # Iniciar threads
        thread_processamento = threading.Thread(target=self.thread_processamento_dados)
        thread_kpis = threading.Thread(target=self.thread_monitoramento_kpis)
        
        thread_processamento.daemon = True
        thread_kpis.daemon = True
        
        thread_processamento.start()
        thread_kpis.start()
        
        self.threads = [thread_processamento, thread_kpis]
        
        logger.info("Pipeline Integrado ESP32 iniciado com sucesso!")
        return True
    
    def parar_pipeline(self):
        """Para o pipeline integrado"""
        logger.info("Parando Pipeline Integrado ESP32...")
        
        self.executando = False
        
        # Aguardar threads terminarem
        for thread in self.threads:
            thread.join(timeout=5)
        
        # Desconectar MQTT
        if self.mqtt_client:
            self.mqtt_client.loop_stop()
            self.mqtt_client.disconnect()
        
        # Fechar conexão banco
        if self.db_connection and self.db_connection.is_connected():
            self.db_connection.close()
        
        logger.info("Pipeline Integrado ESP32 parado.")
    
    def executar_dashboard_tempo_real(self):
        """Executa dashboard em tempo real"""
        try:
            import dash
            from dash import dcc, html, Input, Output
            import plotly.graph_objs as go
            import plotly.express as px
            
            app = dash.Dash(__name__)
            
            app.layout = html.Div([
                html.H1("Dashboard IoT Monitoring - Tempo Real"),
                html.Div(id='status-pipeline'),
                html.Div(id='graficos-tempo-real'),
                dcc.Interval(
                    id='interval-component',
                    interval=self.config["monitoramento"]["dashboard_update_intervalo_segundos"] * 1000,
                    n_intervals=0
                )
            ])
            
            @app.callback(Output('status-pipeline', 'children'),
                         Input('interval-component', 'n_intervals'))
            def atualizar_status(n):
                status = self.gerar_relatorio_status()
                return html.Div([
                    html.H3("Status do Pipeline"),
                    html.P(f"Status: {status['status']}"),
                    html.P(f"Uptime: {status['uptime_segundos']:.1f} segundos"),
                    html.P(f"Dados Recebidos: {status['estatisticas']['dados_recebidos']}"),
                    html.P(f"Anomalias Detectadas: {status['estatisticas']['anomalias_detectadas']}"),
                    html.P(f"Fila Dados: {status['fila_dados_tamanho']}"),
                    html.P(f"Fila Alertas: {status['fila_alertas_tamanho']}")
                ])
            
            @app.callback(Output('graficos-tempo-real', 'children'),
                         Input('interval-component', 'n_intervals'))
            def atualizar_graficos(n):
                # Aqui você implementaria gráficos em tempo real
                return html.Div([
                    html.H3("Gráficos em Tempo Real"),
                    html.P("Gráficos serão implementados aqui...")
                ])
            
            app.run_server(debug=False, host='0.0.0.0', port=8050)
            
        except ImportError:
            logger.warning("Dash não instalado. Dashboard não disponível.")
        except Exception as e:
            logger.error(f"Erro ao executar dashboard: {e}")


def main():
    """Função principal"""
    print("🚀 PIPELINE INTEGRADO ESP32 - SISTEMA IOT MONITORING")
    print("=" * 60)
    
    # Criar pipeline
    pipeline = PipelineIntegradoESP32()
    
    try:
        # Iniciar pipeline
        if pipeline.iniciar_pipeline():
            print("✅ Pipeline iniciado com sucesso!")
            print("📊 Monitorando dados do ESP32...")
            print("🔍 Detecção de anomalias ativa...")
            print("📈 KPIs sendo calculados...")
            print("\nPressione Ctrl+C para parar...")
            
            # Loop principal
            while True:
                time.sleep(10)
                
                # Mostrar status a cada 10 segundos
                status = pipeline.gerar_relatorio_status()
                print(f"\n📊 Status: {status['estatisticas']['dados_recebidos']} dados recebidos, "
                      f"{status['estatisticas']['anomalias_detectadas']} anomalias detectadas")
        
        else:
            print("❌ Falha ao iniciar pipeline")
            return 1
    
    except KeyboardInterrupt:
        print("\n🛑 Parando pipeline...")
        pipeline.parar_pipeline()
        print("✅ Pipeline parado com sucesso!")
        return 0
    
    except Exception as e:
        print(f"❌ Erro no pipeline: {e}")
        pipeline.parar_pipeline()
        return 1


if __name__ == "__main__":
    sys.exit(main())
