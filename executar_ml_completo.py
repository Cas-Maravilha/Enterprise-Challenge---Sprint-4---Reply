#!/usr/bin/env python3
"""
Executador do Sistema ML Completo - Sistema IoT Monitoring Sprint 3
Executa o sistema completo de ML com treino e inferência

Autor: Enterprise Challenge - Sprint 3 - Reply
Data: 2024
"""

import os
import sys
import json
import time
import logging
import argparse
import signal
import threading
from datetime import datetime
from typing import Dict, Any

# Importar módulos do projeto
from persistencia_banco_relacional import (
    PersistenciaBancoRelacional, 
    ConfiguracaoBanco
)
from sistema_ml_completo import (
    SistemaMLCompleto,
    ConfiguracaoML
)
from integracao_ml_pipeline import (
    IntegracaoMLPipeline,
    ConfiguracaoMQTT
)

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger("ExecutadorML")

class ExecutadorMLCompleto:
    """
    Executador do sistema completo de ML
    """
    
    def __init__(self, config_arquivo: str = "config_pipeline.json"):
        self.config_arquivo = config_arquivo
        self.config = self._carregar_configuracao()
        self.executando = False
        self.sistemas = {}
        
        # Configurar sinais para parada graceful
        signal.signal(signal.SIGINT, self._handler_sinal)
        signal.signal(signal.SIGTERM, self._handler_sinal)
    
    def _carregar_configuracao(self) -> Dict[str, Any]:
        """Carrega configuração do arquivo JSON"""
        try:
            if os.path.exists(self.config_arquivo):
                with open(self.config_arquivo, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                logger.warning(f"Arquivo de configuração não encontrado: {self.config_arquivo}")
                return self._configuracao_padrao()
        except Exception as e:
            logger.error(f"Erro ao carregar configuração: {e}")
            return self._configuracao_padrao()
    
    def _configuracao_padrao(self) -> Dict[str, Any]:
        """Configuração padrão do sistema"""
        return {
            "database": {
                "host": "localhost",
                "port": 3306,
                "database": "iot_monitoring_db",
                "username": "root",
                "password": "password"
            },
            "mqtt": {
                "broker": "broker.hivemq.com",
                "port": 1883,
                "topic": "industrial/sensors/data",
                "client_id": "ml_pipeline_esp32"
            },
            "ml": {
                "modelo_path": "modelos/",
                "retreinar_intervalo_horas": 24,
                "threshold_anomalia": 0.5,
                "min_amostras_treino": 1000
            },
            "monitoramento": {
                "intervalo_estatisticas_segundos": 30,
                "intervalo_limpeza_horas": 24,
                "dias_manter_dados": 30
            }
        }
    
    def _handler_sinal(self, signum, frame):
        """Handler para sinais de parada"""
        logger.info(f"Sinal recebido: {signum}")
        self.parar()
    
    def inicializar_sistemas(self):
        """Inicializa todos os sistemas"""
        try:
            logger.info("Inicializando sistemas de ML")
            
            # Configuração do banco
            config_banco = ConfiguracaoBanco(
                host=self.config['database']['host'],
                port=self.config['database']['port'],
                database=self.config['database']['database'],
                username=self.config['database']['username'],
                password=self.config['database']['password']
            )
            
            # Configuração MQTT
            config_mqtt = ConfiguracaoMQTT(
                broker=self.config['mqtt']['broker'],
                port=self.config['mqtt']['port'],
                topic=self.config['mqtt']['topic'],
                client_id=self.config['mqtt']['client_id']
            )
            
            # Configuração ML
            config_ml = ConfiguracaoML(
                modelo_path=self.config['ml']['modelo_path'],
                retreinar_intervalo_horas=self.config['ml']['retreinar_intervalo_horas'],
                threshold_anomalia=self.config['ml']['threshold_anomalia'],
                min_amostras_treino=self.config['ml']['min_amostras_treino']
            )
            
            # Sistema de persistência
            self.sistemas['persistencia'] = PersistenciaBancoRelacional(config_banco)
            
            # Sistema ML
            self.sistemas['ml'] = SistemaMLCompleto(config_banco, config_ml)
            
            # Sistema integrado
            self.sistemas['integrado'] = IntegracaoMLPipeline(config_banco, config_mqtt, config_ml)
            
            logger.info("Sistemas inicializados com sucesso")
            
        except Exception as e:
            logger.error(f"Erro ao inicializar sistemas: {e}")
            raise
    
    def iniciar(self, modo: str = "integrado"):
        """Inicia o sistema ML"""
        try:
            logger.info(f"Iniciando sistema ML em modo: {modo}")
            
            # Inicializa sistemas
            self.inicializar_sistemas()
            
            if modo == "integrado":
                # Inicia sistema integrado completo
                self.sistemas['integrado'].iniciar()
                self.executando = True
                self._iniciar_monitoramento()
                
            elif modo == "ml_apenas":
                # Inicia apenas sistema ML
                self.sistemas['ml'].iniciar()
                self.executando = True
                self._iniciar_monitoramento()
                
            elif modo == "treino_apenas":
                # Executa apenas treinamento
                self._executar_treino_apenas()
                
            else:
                raise ValueError(f"Modo inválido: {modo}")
            
            logger.info("Sistema ML iniciado")
            
        except Exception as e:
            logger.error(f"Erro ao iniciar sistema ML: {e}")
            raise
    
    def parar(self):
        """Para o sistema ML"""
        try:
            logger.info("Parando sistema ML")
            
            self.executando = False
            
            # Para sistemas
            if 'integrado' in self.sistemas:
                self.sistemas['integrado'].parar()
            
            if 'ml' in self.sistemas:
                self.sistemas['ml'].parar()
            
            logger.info("Sistema ML parado")
            
        except Exception as e:
            logger.error(f"Erro ao parar sistema ML: {e}")
    
    def _iniciar_monitoramento(self):
        """Inicia thread de monitoramento"""
        thread_monitoramento = threading.Thread(target=self._monitorar_sistema, daemon=True)
        thread_monitoramento.start()
    
    def _monitorar_sistema(self):
        """Thread de monitoramento do sistema"""
        logger.info("Thread de monitoramento iniciada")
        
        intervalo_estatisticas = self.config['monitoramento']['intervalo_estatisticas_segundos']
        
        while self.executando:
            try:
                # Mostra estatísticas
                self._mostrar_estatisticas()
                
                # Aguarda próximo ciclo
                time.sleep(intervalo_estatisticas)
                
            except Exception as e:
                logger.error(f"Erro no monitoramento: {e}")
                time.sleep(5)
        
        logger.info("Thread de monitoramento finalizada")
    
    def _mostrar_estatisticas(self):
        """Mostra estatísticas do sistema"""
        try:
            if 'integrado' in self.sistemas:
                stats = self.sistemas['integrado'].obter_estatisticas_completas()
                
                logger.info("=== ESTATÍSTICAS DO SISTEMA INTEGRADO ===")
                
                # Sistema integrado
                sistema = stats.get('sistema_integrado', {})
                logger.info(f"Dados recebidos: {sistema.get('dados_recebidos', 0)}")
                logger.info(f"Dados processados: {sistema.get('dados_processados', 0)}")
                logger.info(f"Anomalias detectadas: {sistema.get('anomalias_detectadas', 0)}")
                logger.info(f"Alertas criados: {sistema.get('alertas_criados', 0)}")
                
                # Pipeline ESP32
                esp32 = stats.get('pipeline_esp32', {})
                logger.info(f"Leituras ESP32: {esp32.get('leituras_recebidas', 0)}")
                logger.info(f"Taxa processamento: {esp32.get('taxa_processamento_por_segundo', 0):.2f}/s")
                
                # Sistema ML
                ml = stats.get('sistema_ml', {})
                logger.info(f"Modelo treinado: {ml.get('modelo_treinado', False)}")
                logger.info(f"Inferências ML: {ml.get('inferencias_realizadas', 0)}")
                logger.info(f"Taxa anomalias: {ml.get('taxa_anomalias', 0):.2%}")
                
                # Banco de dados
                banco = stats.get('banco_dados', {})
                logger.info(f"Dispositivos ativos: {banco.get('total_dispositivos', 0)}")
                logger.info(f"Alertas ativos: {banco.get('alertas_ativos', 0)}")
                
                logger.info("=" * 50)
                
            elif 'ml' in self.sistemas:
                stats = self.sistemas['ml'].obter_estatisticas()
                
                logger.info("=== ESTATÍSTICAS DO SISTEMA ML ===")
                logger.info(f"Modelo treinado: {stats.get('modelo_treinado', False)}")
                logger.info(f"Inferências realizadas: {stats.get('inferencias_realizadas', 0)}")
                logger.info(f"Anomalias detectadas: {stats.get('anomalias_detectadas', 0)}")
                logger.info(f"Taxa de anomalias: {stats.get('taxa_anomalias', 0):.2%}")
                logger.info(f"Fila de inferência: {stats.get('tamanho_fila', 0)}")
                
                # Estatísticas do modelo
                modelo_stats = stats.get('estatisticas_modelo', {})
                if modelo_stats:
                    logger.info("=== MÉTRICAS DO MODELO ===")
                    logger.info(f"Accuracy: {modelo_stats.get('accuracy', 0):.4f}")
                    logger.info(f"Precision: {modelo_stats.get('precision', 0):.4f}")
                    logger.info(f"Recall: {modelo_stats.get('recall', 0):.4f}")
                    logger.info(f"F1-Score: {modelo_stats.get('f1', 0):.4f}")
                    logger.info(f"AUC: {modelo_stats.get('auc', 0):.4f}")
                
                logger.info("=" * 50)
                
        except Exception as e:
            logger.error(f"Erro ao mostrar estatísticas: {e}")
    
    def _executar_treino_apenas(self):
        """Executa apenas treinamento do modelo"""
        try:
            logger.info("Executando treinamento do modelo")
            
            # Inicia sistema ML
            self.sistemas['ml'].iniciar()
            
            # Força retreinamento
            self.sistemas['ml'].forcar_retreinamento()
            
            # Mostra estatísticas do modelo
            stats = self.sistemas['ml'].obter_estatisticas()
            logger.info("Treinamento concluído!")
            logger.info(f"Estatísticas: {json.dumps(stats, indent=2, default=str)}")
            
            # Para sistema
            self.sistemas['ml'].parar()
            
        except Exception as e:
            logger.error(f"Erro no treinamento: {e}")
            raise
    
    def executar_teste_ml(self) -> bool:
        """Executa teste do sistema ML"""
        try:
            logger.info("Executando teste do sistema ML")
            
            # Inicializa sistemas
            self.inicializar_sistemas()
            
            # Testa sistema ML
            if 'integrado' in self.sistemas:
                sucesso = self.sistemas['integrado'].testar_sistema_completo()
            elif 'ml' in self.sistemas:
                # Testa apenas ML
                dados_teste = {
                    'temperature': 25.5,
                    'humidity': 60.0,
                    'pressure': 1.013,
                    'vibration': 0.1,
                    'level': 100.0,
                    'luminosity': 500.0,
                    'movement': 0
                }
                
                resultado = self.sistemas['ml'].inferir_anomalia(dados_teste)
                sucesso = resultado is not None and 'anomalia_detectada' in resultado
            else:
                sucesso = False
            
            if sucesso:
                logger.info("Teste do sistema ML: SUCESSO")
            else:
                logger.error("Teste do sistema ML: FALHA")
            
            return sucesso
            
        except Exception as e:
            logger.error(f"Erro no teste ML: {e}")
            return False
    
    def executar_demonstracao_ml(self):
        """Executa demonstração do sistema ML"""
        try:
            logger.info("Executando demonstração do sistema ML")
            
            # Inicializa sistemas
            self.inicializar_sistemas()
            
            # Inicia sistema ML
            self.sistemas['ml'].iniciar()
            
            # Dados de demonstração
            dados_demo = [
                {
                    'temperature': 25.5,
                    'humidity': 60.0,
                    'pressure': 1.013,
                    'vibration': 0.1,
                    'level': 100.0,
                    'luminosity': 500.0,
                    'movement': 0,
                    'descricao': 'Dados normais'
                },
                {
                    'temperature': 35.0,
                    'humidity': 85.0,
                    'pressure': 1.030,
                    'vibration': 1.2,
                    'level': 150.0,
                    'luminosity': 800.0,
                    'movement': 1,
                    'descricao': 'Dados de anomalia'
                },
                {
                    'temperature': 15.0,
                    'humidity': 30.0,
                    'pressure': 0.990,
                    'vibration': 0.05,
                    'level': 50.0,
                    'luminosity': 200.0,
                    'movement': 0,
                    'descricao': 'Dados extremos normais'
                }
            ]
            
            # Testa cada conjunto de dados
            for i, dados in enumerate(dados_demo, 1):
                logger.info(f"Teste {i}: {dados['descricao']}")
                
                resultado = self.sistemas['ml'].inferir_anomalia(dados)
                
                if resultado:
                    logger.info(f"  Resultado: {resultado['anomalia_detectada']}")
                    logger.info(f"  Probabilidade: {resultado['probabilidade']:.4f}")
                    logger.info(f"  Confiança: {resultado['confianca']}")
                else:
                    logger.error(f"  Erro na inferência")
                
                logger.info("")
            
            # Para sistema
            self.sistemas['ml'].parar()
            
            logger.info("Demonstração concluída")
            
        except Exception as e:
            logger.error(f"Erro na demonstração: {e}")

def main():
    """Função principal"""
    parser = argparse.ArgumentParser(description='Executador do Sistema ML Completo')
    parser.add_argument('--config', default='config_pipeline.json', help='Arquivo de configuração')
    parser.add_argument('--modo', choices=['integrado', 'ml_apenas', 'treino_apenas', 'teste', 'demo'], 
                       default='integrado', help='Modo de execução')
    parser.add_argument('--log-level', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'], 
                       default='INFO', help='Nível de log')
    
    args = parser.parse_args()
    
    # Configura nível de log
    logging.getLogger().setLevel(getattr(logging, args.log_level))
    
    # Inicializa executador
    executador = ExecutadorMLCompleto(args.config)
    
    try:
        if args.modo == 'teste':
            # Executa apenas teste
            sucesso = executador.executar_teste_ml()
            sys.exit(0 if sucesso else 1)
            
        elif args.modo == 'demo':
            # Executa demonstração
            executador.executar_demonstracao_ml()
            
        else:
            # Executa sistema completo
            executador.iniciar(args.modo)
            
            # Mantém execução
            while executador.executando:
                time.sleep(1)
    
    except KeyboardInterrupt:
        logger.info("Interrupção pelo usuário")
    except Exception as e:
        logger.error(f"Erro na execução: {e}")
        sys.exit(1)
    finally:
        executador.parar()

if __name__ == "__main__":
    main()

