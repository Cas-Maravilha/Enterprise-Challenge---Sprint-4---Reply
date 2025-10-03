#!/usr/bin/env python3
"""
Coletor de Dados ESP32 - Simulação Wokwi
Coleta dados do ESP32 simulado no Wokwi e envia para o pipeline integrado

Autor: Enterprise Challenge - Sprint 3 - Reply
Data: 2024
"""

import time
import json
import logging
import paho.mqtt.client as mqtt
import random
import math
from datetime import datetime
from typing import Dict, List

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger("Coletor Wokwi")

class ColetorDadosWokwi:
    """
    Simulador de coleta de dados do ESP32 para Wokwi
    """
    
    def __init__(self, broker="broker.hivemq.com", port=1883, topic="industrial/sensors/data"):
        self.broker = broker
        self.port = port
        self.topic = topic
        self.client = None
        self.executando = False
        
        # Configurações de simulação
        self.config_sensores = {
            'temperature': {'min': -10, 'max': 120, 'normal': 25, 'std': 5},
            'pressure': {'min': 0, 'max': 10, 'normal': 5, 'std': 1},
            'vibration': {'min': 0, 'max': 5, 'normal': 0.5, 'std': 0.3},
            'level': {'min': 0, 'max': 400, 'normal': 100, 'std': 20},
            'accel_x': {'min': -2, 'max': 2, 'normal': 0, 'std': 0.2},
            'accel_y': {'min': -2, 'max': 2, 'normal': 0, 'std': 0.2},
            'accel_z': {'min': -2, 'max': 2, 'normal': 1, 'std': 0.1}
        }
        
        # Estados de simulação
        self.modo_operacao = 'normal'  # normal, alerta, falha
        self.tempo_inicio = time.time()
        self.contador_leituras = 0
        
        logger.info("Coletor de dados Wokwi inicializado")
    
    def conectar_mqtt(self):
        """Conecta ao broker MQTT"""
        try:
            self.client = mqtt.Client("coletor_wokwi_esp32")
            self.client.on_connect = self._on_connect
            self.client.on_disconnect = self._on_disconnect
            
            self.client.connect(self.broker, self.port, 60)
            self.client.loop_start()
            
            logger.info(f"Conectado ao broker MQTT: {self.broker}:{self.port}")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao conectar MQTT: {e}")
            return False
    
    def _on_connect(self, client, userdata, flags, rc):
        """Callback de conexão MQTT"""
        if rc == 0:
            logger.info("MQTT conectado com sucesso")
        else:
            logger.error(f"Falha na conexão MQTT. Código: {rc}")
    
    def _on_disconnect(self, client, userdata, rc):
        """Callback de desconexão MQTT"""
        logger.warning("MQTT desconectado")
    
    def simular_leituras_sensores(self) -> Dict:
        """
        Simula leituras dos sensores do ESP32
        
        Returns:
            dict: Dados dos sensores simulados
        """
        timestamp = time.time()
        self.contador_leituras += 1
        
        # Determinar modo de operação baseado no tempo
        tempo_decorrido = timestamp - self.tempo_inicio
        
        if tempo_decorrido < 60:  # Primeiro minuto: normal
            self.modo_operacao = 'normal'
        elif tempo_decorrido < 120:  # Segundo minuto: alerta
            self.modo_operacao = 'alerta'
        elif tempo_decorrido < 180:  # Terceiro minuto: falha
            self.modo_operacao = 'falha'
        else:  # Reiniciar ciclo
            self.tempo_inicio = timestamp
            self.modo_operacao = 'normal'
        
        # Gerar dados baseados no modo de operação
        dados = self._gerar_dados_modo(self.modo_operacao)
        
        # Adicionar metadados
        dados.update({
            'timestamp': timestamp,
            'modo_operacao': self.modo_operacao,
            'contador_leituras': self.contador_leituras,
            'device_id': 'esp32_wokwi_001',
            'firmware_version': '1.0.0',
            'wifi_signal': random.randint(-80, -30),
            'free_heap': random.randint(100000, 200000)
        })
        
        return dados
    
    def _gerar_dados_modo(self, modo: str) -> Dict:
        """Gera dados baseados no modo de operação"""
        dados = {}
        
        for sensor, config in self.config_sensores.items():
            if modo == 'normal':
                # Valores normais com pequena variação
                valor = random.gauss(config['normal'], config['std'])
                valor = max(config['min'], min(config['max'], valor))
                
            elif modo == 'alerta':
                # Valores próximos aos limites
                if random.random() < 0.7:  # 70% chance de valor normal
                    valor = random.gauss(config['normal'], config['std'])
                else:  # 30% chance de valor de alerta
                    if random.random() < 0.5:
                        valor = config['max'] * 0.8 + random.uniform(0, config['max'] * 0.2)
                    else:
                        valor = config['min'] + random.uniform(0, config['min'] * 0.2)
                
                valor = max(config['min'], min(config['max'], valor))
                
            elif modo == 'falha':
                # Valores extremos ou nulos
                if random.random() < 0.3:  # 30% chance de valor nulo (falha de sensor)
                    valor = None
                elif random.random() < 0.5:  # 50% chance de valor extremo
                    valor = random.choice([config['min'], config['max']])
                else:  # 20% chance de valor normal (para simular falha intermitente)
                    valor = random.gauss(config['normal'], config['std'])
                    valor = max(config['min'], min(config['max'], valor))
            
            dados[sensor] = valor
        
        # Calcular magnitude da vibração
        if all(dados.get(f'accel_{axis}') is not None for axis in ['x', 'y', 'z']):
            vib_mag = math.sqrt(
                dados['accel_x']**2 + 
                dados['accel_y']**2 + 
                dados['accel_z']**2
            )
            dados['vibration'] = vib_mag
        else:
            dados['vibration'] = None
        
        return dados
    
    def enviar_dados(self, dados: Dict) -> bool:
        """Envia dados para o broker MQTT"""
        try:
            if self.client and self.client.is_connected():
                # Converter para JSON
                json_data = json.dumps(dados, indent=2)
                
                # Publicar
                result = self.client.publish(self.topic, json_data)
                
                if result.rc == mqtt.MQTT_ERR_SUCCESS:
                    logger.debug(f"Dados enviados: {dados['modo_operacao']} - {dados['contador_leituras']}")
                    return True
                else:
                    logger.error(f"Erro ao publicar dados: {result.rc}")
                    return False
            else:
                logger.warning("Cliente MQTT não conectado")
                return False
                
        except Exception as e:
            logger.error(f"Erro ao enviar dados: {e}")
            return False
    
    def executar_simulacao(self, duracao_minutos: int = 10, intervalo_segundos: float = 2.0):
        """
        Executa simulação de coleta de dados
        
        Args:
            duracao_minutos: Duração da simulação em minutos
            intervalo_segundos: Intervalo entre leituras em segundos
        """
        logger.info(f"Iniciando simulação por {duracao_minutos} minutos...")
        logger.info(f"Intervalo entre leituras: {intervalo_segundos} segundos")
        
        self.executando = True
        inicio = time.time()
        fim = inicio + (duracao_minutos * 60)
        
        leituras_enviadas = 0
        leituras_falharam = 0
        
        try:
            while self.executando and time.time() < fim:
                # Gerar dados
                dados = self.simular_leituras_sensores()
                
                # Enviar dados
                if self.enviar_dados(dados):
                    leituras_enviadas += 1
                else:
                    leituras_falharam += 1
                
                # Log periódico
                if self.contador_leituras % 10 == 0:
                    logger.info(f"Leituras: {self.contador_leituras}, "
                              f"Modo: {self.modo_operacao}, "
                              f"Enviadas: {leituras_enviadas}, "
                              f"Falharam: {leituras_falharam}")
                
                # Aguardar próximo ciclo
                time.sleep(intervalo_segundos)
        
        except KeyboardInterrupt:
            logger.info("Simulação interrompida pelo usuário")
        
        finally:
            self.executando = False
            
            # Relatório final
            duracao_real = time.time() - inicio
            logger.info("=" * 50)
            logger.info("RELATÓRIO FINAL DA SIMULAÇÃO")
            logger.info("=" * 50)
            logger.info(f"Duração: {duracao_real:.1f} segundos")
            logger.info(f"Total de leituras: {self.contador_leituras}")
            logger.info(f"Leituras enviadas: {leituras_enviadas}")
            logger.info(f"Leituras falharam: {leituras_falharam}")
            logger.info(f"Taxa de sucesso: {(leituras_enviadas/self.contador_leituras)*100:.1f}%")
            logger.info("=" * 50)
    
    def parar_simulacao(self):
        """Para a simulação"""
        self.executando = False
        logger.info("Simulação parada")
    
    def desconectar(self):
        """Desconecta do broker MQTT"""
        if self.client:
            self.client.loop_stop()
            self.client.disconnect()
            logger.info("Desconectado do broker MQTT")


def main():
    """Função principal"""
    print("🔌 COLETOR DE DADOS ESP32 - SIMULAÇÃO WOKWI")
    print("=" * 50)
    
    # Criar coletor
    coletor = ColetorDadosWokwi()
    
    try:
        # Conectar MQTT
        if coletor.conectar_mqtt():
            print("✅ Conectado ao broker MQTT")
            
            # Executar simulação
            print("🚀 Iniciando simulação...")
            print("📊 Modos de operação:")
            print("   - 0-1min: Normal")
            print("   - 1-2min: Alerta") 
            print("   - 2-3min: Falha")
            print("   - 3min+: Reinicia ciclo")
            print("\nPressione Ctrl+C para parar...")
            
            coletor.executar_simulacao(
                duracao_minutos=10,  # 10 minutos de simulação
                intervalo_segundos=2.0  # Leitura a cada 2 segundos
            )
        
        else:
            print("❌ Falha ao conectar MQTT")
            return 1
    
    except KeyboardInterrupt:
        print("\n🛑 Parando simulação...")
        coletor.parar_simulacao()
    
    finally:
        coletor.desconectar()
        print("✅ Simulação finalizada!")
        return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
