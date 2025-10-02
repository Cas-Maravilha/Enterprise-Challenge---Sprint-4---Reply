#!/usr/bin/env python3
"""
Executador da Persistência Completa - Sistema IoT Monitoring Sprint 3
Executa o sistema completo de persistência no banco relacional

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
from integracao_persistencia_esp32 import (
    IntegracaoPersistenciaESP32,
    ConfiguracaoMQTT
)

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger("ExecutadorPersistencia")

class ExecutadorPersistenciaCompleta:
    """
    Executador do sistema completo de persistência
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
                "client_id": "persistencia_esp32"
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
            logger.info("Inicializando sistemas de persistência")
            
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
            
            # Sistema de persistência
            self.sistemas['persistencia'] = PersistenciaBancoRelacional(config_banco)
            
            # Sistema de integração ESP32
            self.sistemas['integracao'] = IntegracaoPersistenciaESP32(config_banco, config_mqtt)
            
            logger.info("Sistemas inicializados com sucesso")
            
        except Exception as e:
            logger.error(f"Erro ao inicializar sistemas: {e}")
            raise
    
    def iniciar(self):
        """Inicia o sistema completo"""
        try:
            logger.info("Iniciando sistema completo de persistência")
            
            # Inicializa sistemas
            self.inicializar_sistemas()
            
            # Inicia integração ESP32
            self.sistemas['integracao'].iniciar()
            
            # Inicia monitoramento
            self.executando = True
            self._iniciar_monitoramento()
            
            logger.info("Sistema completo iniciado")
            
        except Exception as e:
            logger.error(f"Erro ao iniciar sistema: {e}")
            raise
    
    def parar(self):
        """Para o sistema completo"""
        try:
            logger.info("Parando sistema completo")
            
            self.executando = False
            
            # Para integração ESP32
            if 'integracao' in self.sistemas:
                self.sistemas['integracao'].parar()
            
            logger.info("Sistema completo parado")
            
        except Exception as e:
            logger.error(f"Erro ao parar sistema: {e}")
    
    def _iniciar_monitoramento(self):
        """Inicia thread de monitoramento"""
        thread_monitoramento = threading.Thread(target=self._monitorar_sistema, daemon=True)
        thread_monitoramento.start()
    
    def _monitorar_sistema(self):
        """Thread de monitoramento do sistema"""
        logger.info("Thread de monitoramento iniciada")
        
        ultima_limpeza = datetime.now()
        intervalo_estatisticas = self.config['monitoramento']['intervalo_estatisticas_segundos']
        intervalo_limpeza = self.config['monitoramento']['intervalo_limpeza_horas']
        dias_manter = self.config['monitoramento']['dias_manter_dados']
        
        while self.executando:
            try:
                # Mostra estatísticas
                self._mostrar_estatisticas()
                
                # Verifica se precisa fazer limpeza
                agora = datetime.now()
                if (agora - ultima_limpeza).total_seconds() > (intervalo_limpeza * 3600):
                    self._executar_limpeza(dias_manter)
                    ultima_limpeza = agora
                
                # Aguarda próximo ciclo
                time.sleep(intervalo_estatisticas)
                
            except Exception as e:
                logger.error(f"Erro no monitoramento: {e}")
                time.sleep(5)
        
        logger.info("Thread de monitoramento finalizada")
    
    def _mostrar_estatisticas(self):
        """Mostra estatísticas do sistema"""
        try:
            if 'integracao' in self.sistemas:
                stats = self.sistemas['integracao'].obter_estatisticas()
                
                logger.info("=== ESTATÍSTICAS DO SISTEMA ===")
                logger.info(f"Tempo de execução: {stats.get('tempo_execucao_segundos', 0):.1f}s")
                logger.info(f"Leituras recebidas: {stats.get('leituras_recebidas', 0)}")
                logger.info(f"Leituras processadas: {stats.get('leituras_processadas', 0)}")
                logger.info(f"Leituras com erro: {stats.get('leituras_erro', 0)}")
                logger.info(f"Alertas criados: {stats.get('alertas_criados', 0)}")
                logger.info(f"Taxa de processamento: {stats.get('taxa_processamento_por_segundo', 0):.2f}/s")
                logger.info(f"Tamanho da fila: {stats.get('tamanho_fila', 0)}")
                
                # KPIs do banco
                kpis = stats.get('kpis_banco', {})
                if kpis:
                    logger.info("=== KPIs DO BANCO ===")
                    logger.info(f"Dispositivos ativos: {kpis.get('total_dispositivos', 0)}")
                    logger.info(f"Sensores ativos: {kpis.get('total_sensores', 0)}")
                    logger.info(f"Leituras (24h): {kpis.get('leituras_24h', 0)}")
                    logger.info(f"Alertas ativos: {kpis.get('alertas_ativos', 0)}")
                    logger.info(f"Dispositivos offline: {kpis.get('dispositivos_offline', 0)}")
                
                logger.info("=" * 40)
                
        except Exception as e:
            logger.error(f"Erro ao mostrar estatísticas: {e}")
    
    def _executar_limpeza(self, dias_manter: int):
        """Executa limpeza de dados antigos"""
        try:
            logger.info(f"Iniciando limpeza de dados antigos (manter {dias_manter} dias)")
            
            if 'persistencia' in self.sistemas:
                registros_removidos = self.sistemas['persistencia'].limpar_dados_antigos(dias_manter)
                logger.info(f"Limpeza concluída: {registros_removidos} registros removidos")
                
                # Otimiza banco após limpeza
                self.sistemas['persistencia'].otimizar_banco()
                logger.info("Banco de dados otimizado")
            
        except Exception as e:
            logger.error(f"Erro na limpeza: {e}")
    
    def executar_teste_persistencia(self):
        """Executa teste de persistência"""
        try:
            logger.info("Executando teste de persistência")
            
            if 'persistencia' not in self.sistemas:
                logger.error("Sistema de persistência não inicializado")
                return False
            
            persistencia = self.sistemas['persistencia']
            
            # Teste 1: Inserir dispositivo
            dispositivo = {
                'nome': 'ESP32-Teste-Persistencia',
                'mac_address': 'AA:BB:CC:DD:EE:99',
                'ip_address': '192.168.1.199',
                'localizacao': 'Teste de Persistência',
                'versao_firmware': 'v1.0.0'
            }
            
            id_dispositivo = persistencia.inserir_dispositivo(dispositivo)
            logger.info(f"Dispositivo de teste inserido: {id_dispositivo}")
            
            # Teste 2: Inserir sensor
            sensor = {
                'id_dispositivo': id_dispositivo,
                'id_tipo_sensor': 1,  # DHT22
                'nome': 'DHT22-Teste',
                'pino_digital': 2
            }
            
            id_sensor = persistencia.inserir_sensor(sensor)
            logger.info(f"Sensor de teste inserido: {id_sensor}")
            
            # Teste 3: Inserir leituras
            leituras_teste = []
            for i in range(10):
                leitura = {
                    'id_sensor': id_sensor,
                    'timestamp_unix': time.time() + i,
                    'valor_numerico': 20.0 + (i * 0.5),
                    'qualidade_dados': 'bom'
                }
                leituras_teste.append(leitura)
            
            ids_leituras = persistencia.inserir_multiplas_leituras(leituras_teste)
            logger.info(f"Leituras de teste inseridas: {len(ids_leituras)}")
            
            # Teste 4: Obter estatísticas
            stats = persistencia.obter_estatisticas_sensor(
                id_sensor, 
                datetime.now() - timedelta(hours=1),
                datetime.now()
            )
            logger.info(f"Estatísticas do sensor: {stats}")
            
            # Teste 5: Obter KPIs
            kpis = persistencia.obter_kpis_sistema()
            logger.info(f"KPIs do sistema: {kpis}")
            
            logger.info("Teste de persistência concluído com sucesso")
            return True
            
        except Exception as e:
            logger.error(f"Erro no teste de persistência: {e}")
            return False

def main():
    """Função principal"""
    parser = argparse.ArgumentParser(description='Executador da Persistência Completa')
    parser.add_argument('--config', default='config_pipeline.json', help='Arquivo de configuração')
    parser.add_argument('--teste', action='store_true', help='Executa apenas teste de persistência')
    parser.add_argument('--modo', choices=['producao', 'desenvolvimento'], default='desenvolvimento', help='Modo de execução')
    
    args = parser.parse_args()
    
    # Configura nível de log baseado no modo
    if args.modo == 'producao':
        logging.getLogger().setLevel(logging.WARNING)
    else:
        logging.getLogger().setLevel(logging.INFO)
    
    # Inicializa executador
    executador = ExecutadorPersistenciaCompleta(args.config)
    
    try:
        if args.teste:
            # Executa apenas teste
            executador.inicializar_sistemas()
            sucesso = executador.executar_teste_persistencia()
            sys.exit(0 if sucesso else 1)
        else:
            # Executa sistema completo
            executador.iniciar()
            
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

