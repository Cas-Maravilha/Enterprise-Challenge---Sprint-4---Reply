#!/usr/bin/env python3
"""
Simulador de sensores para ESP32
Simula DHT22 (temperatura/umidade), LDR (luz) e PIR (movimento)
"""
import random
import time
from datetime import datetime
import json
import os

# Parâmetros dos sensores
SENSOR_PARAMS = {
    'dht22': {
        'temperature': {'mean': 25.0, 'std': 2.0, 'min': 20.0, 'max': 30.0},
        'humidity': {'mean': 60.0, 'std': 5.0, 'min': 40.0, 'max': 80.0}
    },
    'ldr': {
        'normal': {'mean': 500, 'std': 100, 'min': 0, 'max': 1023}
    },
    'pir': {
        'detection_prob': 0.1  # 10% de chance de detectar movimento
    }
}

def generate_dht22_data():
    """Gera dados simulados do DHT22"""
    temp = random.normalvariate(
        SENSOR_PARAMS['dht22']['temperature']['mean'],
        SENSOR_PARAMS['dht22']['temperature']['std']
    )
    temp = max(SENSOR_PARAMS['dht22']['temperature']['min'],
              min(SENSOR_PARAMS['dht22']['temperature']['max'], temp))
    
    hum = random.normalvariate(
        SENSOR_PARAMS['dht22']['humidity']['mean'],
        SENSOR_PARAMS['dht22']['humidity']['std']
    )
    hum = max(SENSOR_PARAMS['dht22']['humidity']['min'],
             min(SENSOR_PARAMS['dht22']['humidity']['max'], hum))
    
    return round(temp, 1), round(hum, 1)

def generate_ldr_data():
    """Gera dados simulados do LDR"""
    value = random.normalvariate(
        SENSOR_PARAMS['ldr']['normal']['mean'],
        SENSOR_PARAMS['ldr']['normal']['std']
    )
    value = max(SENSOR_PARAMS['ldr']['normal']['min'],
               min(SENSOR_PARAMS['ldr']['normal']['max'], value))
    return round(value)

def generate_pir_data():
    """Gera dados simulados do PIR"""
    return 1 if random.random() < SENSOR_PARAMS['pir']['detection_prob'] else 0

def save_to_json(data, filename):
    """Salva os dados em formato JSON"""
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

def main():
    # Cria diretório para dados se não existir
    os.makedirs('data', exist_ok=True)
    
    print("Iniciando simulação de sensores ESP32...")
    print("Pressione Ctrl+C para encerrar")
    
    try:
        while True:
            # Gera dados dos sensores
            temperatura, umidade = generate_dht22_data()
            luminosidade = generate_ldr_data()
            movimento = generate_pir_data()
            
            # Cria timestamp
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Prepara dados
            dados = {
                'timestamp': timestamp,
                'sensores': {
                    'dht22': {
                        'temperatura': temperatura,
                        'umidade': umidade
                    },
                    'ldr': {
                        'luminosidade': luminosidade
                    },
                    'pir': {
                        'movimento': movimento
                    }
                }
            }
            
            # Salva dados
            save_to_json(dados, 'data/ultima_leitura.json')
            
            # Mostra dados no console
            print("\n=== Leituras dos Sensores ===")
            print(f"Timestamp: {timestamp}")
            print(f"Temperatura: {temperatura}°C")
            print(f"Umidade: {umidade}%")
            print(f"Luminosidade: {luminosidade} (0-1023)")
            print(f"Movimento: {'Detectado' if movimento else 'Nenhum'}")
            
            # Aguarda 2 segundos
            time.sleep(2)
            
    except KeyboardInterrupt:
        print("\nSimulação encerrada pelo usuário")

if __name__ == '__main__':
    main() 