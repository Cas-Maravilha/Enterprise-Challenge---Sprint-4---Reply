#!/usr/bin/env python3
"""
Integração ML com Pipeline ESP32 - Sistema IoT Monitoring Sprint 3
Integra o sistema de ML com o pipeline ESP32 e persistência no banco

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

# Importar módulos do projeto
from persistencia_banco_relacional import (
    PersistenciaBancoRelacional, 
    ConfiguracaoBanco
)
from integracao_persistencia_esp32 import (
    IntegracaoPersistenciaESP32,
    ConfiguracaoMQTT
)
from sistema_ml_completo import (
    SistemaMLCompleto,
    ConfiguracaoML
)

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger("IntegracaoMLPipeline")

class IntegracaoMLPipeline:
    """
    Sistema integrado de ML com pipeline ESP32 e persistência
    """
    
    def __init__(self, config_banco: ConfiguracaoBanco, 
                 config_mqtt: ConfiguracaoMQTT, 
                 config_ml: ConfiguracaoML):
        self.config_banco = config_banco
        self.config_mqtt = config_mqtt
        self.config_ml = config_ml
        
        # Inicializa sistemas
        self.persistencia = PersistenciaBancoRelacional(config_banco)
        self.integracao_esp32 = IntegracaoPersistenciaESP32(config_banco, config_mqtt)
        self.sistema_ml = SistemaMLCompleto(config_banco, config_ml)
        
        # Estado do sistema
        self.executando = False
        self.threads = {}
        
        # Fila de dados para ML
        self.fila_ml = queue.Queue(maxsize=1000)
        
        # Estatísticas integradas
        self.estatisticas = {
            'dados_recebidos': 0,
            'dados_processados': 0,
            'anomalias_detectadas': 0,
            'alertas_criados': 0,
            'inicio_execucao': datetime.now()
        }
        
        # Callbacks personalizados
        self._configurar_callbacks()
    
    def _configurar_callbacks(self):
        """Configura callbacks personalizados para integração ML"""
        # Sobrescreve callback de processamento de leitura
        self.integracao_esp32._processar_leitura = self._processar_leitura_com_ml
    
    def iniciar(self):
        """Inicia o sistema integrado completo"""
        try:
            logger.info("Iniciando sistema integrado ML + Pipeline ESP32")
            
            # Inicia persistência
            logger.info("Iniciando sistema de persistência...")
            # Persistência já inicializada no construtor
            
            # Inicia sistema ML
            logger.info("Iniciando sistema de ML...")
            self.sistema_ml.iniciar()
            
            # Inicia integração ESP32
            logger.info("Iniciando integração ESP32...")
            self.integracao_esp32.iniciar()
            
            # Inicia thread de processamento ML
            self.executando = True
            self.threads['processamento_ml'] = threading.Thread(
                target=self._thread_processamento_ml, daemon=True
            )
            self.threads['processamento_ml'].start()
            
            # Inicia thread de monitoramento
            self.threads['monitoramento'] = threading.Thread(
                target=self._thread_monitoramento, daemon=True
            )
            self.threads['monitoramento'].start()
            
            logger.info("Sistema integrado iniciado com sucesso")
            
        except Exception as e:
            logger.error(f"Erro ao iniciar sistema integrado: {e}")
            raise
    
    def parar(self):
        """Para o sistema integrado"""
        try:
            logger.info("Parando sistema integrado")
            
            self.executando = False
            
            # Para integração ESP32
            self.integracao_esp32.parar()
            
            # Para sistema ML
            self.sistema_ml.parar()
            
            # Aguarda threads
            for thread in self.threads.values():
                if thread.is_alive():
                    thread.join(timeout=5)
            
            logger.info("Sistema integrado parado")
            
        except Exception as e:
            logger.error(f"Erro ao parar sistema integrado: {e}")
    
    def _processar_leitura_com_ml(self, dados: Dict[str, Any]):
        """Processa leitura com ML integrado"""
        try:
            # Processa leitura original
            self.integracao_esp32._processar_leitura_original(dados)
            
            # Adiciona à fila de ML
            if not self.fila_ml.full():
                self.fila_ml.put(dados)
                self.estatisticas['dados_recebidos'] += 1
            else:
                logger.warning("Fila ML cheia, descartando dados")
            
        except Exception as e:
            logger.error(f"Erro no processamento com ML: {e}")
    
    def _thread_processamento_ml(self):
        """Thread de processamento ML"""
        logger.info("Thread de processamento ML iniciada")
        
        while self.executando:
            try:
                # Processa dados da fila ML
                if not self.fila_ml.empty():
                    dados = self.fila_ml.get(timeout=1)
                    self._processar_dados_ml(dados)
                    self.fila_ml.task_done()
                else:
                    time.sleep(0.1)
                    
            except queue.Empty:
                continue
            except Exception as e:
                logger.error(f"Erro no processamento ML: {e}")
                time.sleep(1)
        
        logger.info("Thread de processamento ML finalizada")
    
    def _thread_monitoramento(self):
        """Thread de monitoramento do sistema"""
        logger.info("Thread de monitoramento iniciada")
        
        while self.executando:
            try:
                # Mostra estatísticas a cada 30 segundos
                self._mostrar_estatisticas_integradas()
                time.sleep(30)
                
            except Exception as e:
                logger.error(f"Erro no monitoramento: {e}")
                time.sleep(5)
        
        logger.info("Thread de monitoramento finalizada")
    
    def _processar_dados_ml(self, dados: Dict[str, Any]):
        """Processa dados com ML"""
        try:
            # Valida dados
            if not self._validar_dados_ml(dados):
                return
            
            # Obtém informações do sensor
            dispositivo_info = self.integracao_esp32._obter_dispositivo_info(dados)
            if not dispositivo_info:
                return
            
            sensor_info = self.integracao_esp32._obter_sensor_info(dados, dispositivo_info)
            if not sensor_info:
                return
            
            # Prepara dados para ML
            dados_ml = self._preparar_dados_ml(dados, sensor_info)
            if not dados_ml:
                return
            
            # Faz inferência ML
            resultado_ml = self.sistema_ml.inferir_anomalia(dados_ml)
            
            # Atualiza estatísticas
            self.estatisticas['dados_processados'] += 1
            if resultado_ml.get('anomalia_detectada', False):
                self.estatisticas['anomalias_detectadas'] += 1
                
                # Cria alerta se necessário
                self._criar_alerta_ml(sensor_info, dados_ml, resultado_ml)
            
            # Atualiza banco com resultado ML
            self._atualizar_banco_ml(sensor_info, resultado_ml)
            
            logger.debug(f"Dados ML processados: {resultado_ml['anomalia_detectada']}")
            
        except Exception as e:
            logger.error(f"Erro no processamento ML: {e}")
    
    def _validar_dados_ml(self, dados: Dict[str, Any]) -> bool:
        """Valida dados para ML"""
        campos_necessarios = ['valor', 'sensor_nome']
        
        for campo in campos_necessarios:
            if campo not in dados:
                return False
        
        # Verifica se valor é numérico
        try:
            float(dados['valor'])
            return True
        except (ValueError, TypeError):
            return False
    
    def _preparar_dados_ml(self, dados: Dict[str, Any], sensor_info: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Prepara dados para ML"""
        try:
            # Mapeia dados do sensor para formato ML
            dados_ml = {
                'temperature': dados.get('temperature', 0.0),
                'humidity': dados.get('humidity', 0.0),
                'pressure': dados.get('pressure', 0.0),
                'vibration': dados.get('vibration', 0.0),
                'level': dados.get('level', 0.0),
                'luminosity': dados.get('luminosity', 0.0),
                'movement': dados.get('movement', 0)
            }
            
            # Adiciona dados específicos do sensor
            if 'temperatura' in sensor_info['nome'].lower():
                dados_ml['temperature'] = float(dados['valor'])
            elif 'umidade' in sensor_info['nome'].lower():
                dados_ml['humidity'] = float(dados['valor'])
            elif 'pressao' in sensor_info['nome'].lower():
                dados_ml['pressure'] = float(dados['valor'])
            elif 'vibracao' in sensor_info['nome'].lower():
                dados_ml['vibration'] = float(dados['valor'])
            elif 'nivel' in sensor_info['nome'].lower():
                dados_ml['level'] = float(dados['valor'])
            elif 'luminosidade' in sensor_info['nome'].lower():
                dados_ml['luminosity'] = float(dados['valor'])
            elif 'movimento' in sensor_info['nome'].lower():
                dados_ml['movement'] = int(dados['valor'])
            
            return dados_ml
            
        except Exception as e:
            logger.error(f"Erro ao preparar dados ML: {e}")
            return None
    
    def _criar_alerta_ml(self, sensor_info: Dict[str, Any], 
                        dados_ml: Dict[str, Any], 
                        resultado_ml: Dict[str, Any]):
        """Cria alerta baseado em resultado ML"""
        try:
            # Determina severidade baseada na probabilidade
            probabilidade = resultado_ml.get('probabilidade', 0.0)
            
            if probabilidade > 0.9:
                severidade = 'critica'
            elif probabilidade > 0.7:
                severidade = 'alta'
            elif probabilidade > 0.5:
                severidade = 'media'
            else:
                severidade = 'baixa'
            
            # Cria alerta
            alerta = {
                'id_dispositivo': sensor_info['id_dispositivo'],
                'id_sensor': sensor_info['id_sensor'],
                'id_modo': 2,  # Modo de falha
                'tipo_alerta': 'ml_anomalia',
                'severidade': severidade,
                'titulo': f'Anomalia ML detectada: {sensor_info["nome"]}',
                'descricao': f'ML detectou anomalia com probabilidade {probabilidade:.2f}',
                'valor_atual': dados_ml.get('valor', 0.0),
                'valor_limite': probabilidade
            }
            
            # Insere alerta no banco
            id_alerta = self.persistencia.inserir_alerta(alerta)
            self.estatisticas['alertas_criados'] += 1
            
            logger.info(f"Alerta ML criado: {id_alerta} - {severidade}")
            
        except Exception as e:
            logger.error(f"Erro ao criar alerta ML: {e}")
    
    def _atualizar_banco_ml(self, sensor_info: Dict[str, Any], resultado_ml: Dict[str, Any]):
        """Atualiza banco com resultado ML"""
        try:
            # Atualiza última leitura com resultado ML
            with self.persistencia.gerenciador.obter_conexao() as conexao:
                cursor = conexao.cursor()
                
                query = """
                UPDATE leituras_sensores 
                SET anomalia_detectada = %s, qualidade_dados = %s
                WHERE id_sensor = %s 
                ORDER BY timestamp_datetime DESC 
                LIMIT 1
                """
                
                qualidade = 'ruim' if resultado_ml.get('anomalia_detectada', False) else 'bom'
                
                cursor.execute(query, (
                    resultado_ml.get('anomalia_detectada', False),
                    qualidade,
                    sensor_info['id_sensor']
                ))
                
                cursor.close()
                
        except Exception as e:
            logger.error(f"Erro ao atualizar banco ML: {e}")
    
    def _mostrar_estatisticas_integradas(self):
        """Mostra estatísticas integradas do sistema"""
        try:
            # Estatísticas do pipeline ESP32
            stats_esp32 = self.integracao_esp32.obter_estatisticas()
            
            # Estatísticas do ML
            stats_ml = self.sistema_ml.obter_estatisticas()
            
            # Estatísticas integradas
            logger.info("=== ESTATÍSTICAS INTEGRADAS ===")
            logger.info(f"Dados recebidos: {self.estatisticas['dados_recebidos']}")
            logger.info(f"Dados processados: {self.estatisticas['dados_processados']}")
            logger.info(f"Anomalias detectadas: {self.estatisticas['anomalias_detectadas']}")
            logger.info(f"Alertas criados: {self.estatisticas['alertas_criados']}")
            logger.info(f"Fila ML: {self.fila_ml.qsize()}")
            
            # Estatísticas ESP32
            logger.info("=== ESTATÍSTICAS ESP32 ===")
            logger.info(f"Leituras recebidas: {stats_esp32.get('leituras_recebidas', 0)}")
            logger.info(f"Leituras processadas: {stats_esp32.get('leituras_processadas', 0)}")
            logger.info(f"Taxa processamento: {stats_esp32.get('taxa_processamento_por_segundo', 0):.2f}/s")
            
            # Estatísticas ML
            logger.info("=== ESTATÍSTICAS ML ===")
            logger.info(f"Modelo treinado: {stats_ml.get('modelo_treinado', False)}")
            logger.info(f"Inferências realizadas: {stats_ml.get('inferencias_realizadas', 0)}")
            logger.info(f"Taxa anomalias: {stats_ml.get('taxa_anomalias', 0):.2%}")
            
            logger.info("=" * 40)
            
        except Exception as e:
            logger.error(f"Erro ao mostrar estatísticas: {e}")
    
    def obter_estatisticas_completas(self) -> Dict[str, Any]:
        """Obtém estatísticas completas do sistema integrado"""
        try:
            stats_esp32 = self.integracao_esp32.obter_estatisticas()
            stats_ml = self.sistema_ml.obter_estatisticas()
            kpis_banco = self.persistencia.obter_kpis_sistema()
            
            return {
                'sistema_integrado': self.estatisticas,
                'pipeline_esp32': stats_esp32,
                'sistema_ml': stats_ml,
                'banco_dados': kpis_banco,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Erro ao obter estatísticas completas: {e}")
            return {}
    
    def forcar_retreinamento_ml(self):
        """Força retreinamento do modelo ML"""
        try:
            logger.info("Forçando retreinamento do modelo ML")
            self.sistema_ml.forcar_retreinamento()
            
        except Exception as e:
            logger.error(f"Erro no retreinamento forçado: {e}")
    
    def testar_sistema_completo(self) -> bool:
        """Testa o sistema integrado completo"""
        try:
            logger.info("Testando sistema integrado completo")
            
            # Dados de teste
            dados_teste = {
                'mac_address': 'AA:BB:CC:DD:EE:FF',
                'sensor_nome': 'DHT22-Temperatura',
                'timestamp': time.time(),
                'valor': 25.5,
                'temperature': 25.5,
                'humidity': 60.0,
                'pressure': 1.013,
                'vibration': 0.1,
                'level': 100.0,
                'luminosity': 500.0,
                'movement': 0
            }
            
            # Testa processamento
            self._processar_dados_ml(dados_teste)
            
            # Verifica se processou
            if self.estatisticas['dados_processados'] > 0:
                logger.info("Teste do sistema integrado: SUCESSO")
                return True
            else:
                logger.error("Teste do sistema integrado: FALHA")
                return False
                
        except Exception as e:
            logger.error(f"Erro no teste do sistema: {e}")
            return False

# =====================================================
# EXEMPLO DE USO
# =====================================================

def exemplo_uso():
    """Exemplo de uso do sistema integrado"""
    
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
    
    config_ml = ConfiguracaoML(
        modelo_path="modelos/",
        retreinar_intervalo_horas=24
    )
    
    # Inicializa sistema integrado
    sistema_integrado = IntegracaoMLPipeline(config_banco, config_mqtt, config_ml)
    
    try:
        # Inicia sistema
        sistema_integrado.iniciar()
        
        # Testa sistema
        if sistema_integrado.testar_sistema_completo():
            print("Sistema integrado funcionando corretamente!")
        
        # Executa por 60 segundos
        time.sleep(60)
        
        # Mostra estatísticas finais
        stats = sistema_integrado.obter_estatisticas_completas()
        print(f"Estatísticas finais: {json.dumps(stats, indent=2, default=str)}")
        
    except KeyboardInterrupt:
        print("Parando sistema...")
    finally:
        sistema_integrado.parar()

if __name__ == "__main__":
    exemplo_uso()

