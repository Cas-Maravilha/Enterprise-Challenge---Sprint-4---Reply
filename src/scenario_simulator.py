#!/usr/bin/env python3
"""
Script para simular diferentes cenários de dados de sensores industriais.
Gera dados sintéticos para cenários normal, alerta e falha.
"""
import argparse
import csv
import random
import time
from datetime import datetime, timedelta
import os
import math
import json

# Parâmetros de simulação para cada sensor
SENSOR_PARAMS = {
    'temperature': {
        'normal': {'mean': 25.0, 'std': 2.0, 'min': 20.0, 'max': 30.0},
        'alert': {'mean': 35.0, 'std': 3.0, 'min': 30.0, 'max': 40.0},
        'failure': {'mean': 50.0, 'std': 10.0, 'min': -10.0, 'max': 120.0, 'null_prob': 0.3}
    },
    'pressure': {
        'normal': {'mean': 5.0, 'std': 0.5, 'min': 4.0, 'max': 6.0},
        'alert': {'mean': 7.0, 'std': 0.8, 'min': 6.0, 'max': 8.0},
        'failure': {'mean': 10.0, 'std': 3.0, 'min': 0.0, 'max': 15.0, 'null_prob': 0.3}
    },
    'vibration_mag': {
        'normal': {'mean': 0.5, 'std': 0.1, 'min': 0.3, 'max': 0.7},
        'alert': {'mean': 1.2, 'std': 0.2, 'min': 0.8, 'max': 1.5},
        'failure': {'mean': 2.5, 'std': 0.5, 'min': 1.5, 'max': 5.0, 'null_prob': 0.3}
    },
    'level': {
        'normal': {'mean': 100.0, 'std': 10.0, 'min': 80.0, 'max': 120.0},
        'alert': {'mean': 150.0, 'std': 15.0, 'min': 130.0, 'max': 170.0},
        'failure': {'mean': 200.0, 'std': 50.0, 'min': 0.0, 'max': 300.0, 'null_prob': 0.3}
    }
}

def generate_random_value(params):
    """
    Gera um valor aleatório com base nos parâmetros.
    
    Args:
        params: Dicionário com parâmetros (mean, std, min, max, null_prob)
        
    Returns:
        Valor aleatório ou None (se null_prob for atingida)
    """
    # Verifica se deve gerar um valor nulo
    if 'null_prob' in params and random.random() < params['null_prob']:
        return None
    
    # Gera um valor com distribuição normal
    value = random.normalvariate(params['mean'], params['std']) + random.gauss(0, params['std']*0.1)
    
    # Limita ao intervalo [min, max]
    value = max(params['min'], min(params['max'], value))
    
    return value

def generate_vibration_components(magnitude):
    """
    Gera componentes X, Y, Z para uma magnitude de vibração.
    
    Args:
        magnitude: Magnitude da vibração
        
    Returns:
        Tupla (x, y, z) com componentes da vibração
    """
    if magnitude is None:
        return None, None, None
    
    # Gera ângulos aleatórios em coordenadas esféricas
    theta = random.uniform(0, 2 * math.pi)  # Ângulo horizontal
    phi = random.uniform(0, math.pi)        # Ângulo vertical
    
    # Converte para coordenadas cartesianas
    x = magnitude * math.sin(phi) * math.cos(theta)
    y = magnitude * math.sin(phi) * math.sin(theta)
    z = magnitude * math.cos(phi)
    
    return x, y, z

def generate_sample(scenario, timestamp=None):
    """
    Gera uma amostra de dados para um cenário específico.
    
    Args:
        scenario: Nome do cenário ('normal', 'alert', 'failure')
        timestamp: Timestamp opcional (se None, usa o tempo atual)
        
    Returns:
        Dicionário com os dados da amostra
    """
    if timestamp is None:
        timestamp = time.time()
    
    # Mapeia o nome do cenário para o valor do modo
    mode = {'normal': 0, 'alert': 1, 'failure': 2}.get(scenario, 0)
    
    # Gera valores para cada sensor
    temperature = generate_random_value(SENSOR_PARAMS['temperature'][scenario])
    pressure = generate_random_value(SENSOR_PARAMS['pressure'][scenario])
    vibration_mag = generate_random_value(SENSOR_PARAMS['vibration_mag'][scenario])
    level = generate_random_value(SENSOR_PARAMS['level'][scenario])
    
    # Gera componentes de vibração
    vibration_x, vibration_y, vibration_z = generate_vibration_components(vibration_mag)
    
    # Cria a amostra
    sample = {
        'timestamp': timestamp,
        'mode': mode,
        'temperature': temperature,
        'pressure': pressure,
        'vibration_x': vibration_x,
        'vibration_y': vibration_y,
        'vibration_z': vibration_z,
        'vibration_mag': vibration_mag,
        'level': level,
        'status': scenario.upper()
    }
    
    return sample

def format_csv_line(sample):
    """
    Formata uma amostra como linha CSV.
    
    Args:
        sample: Dicionário com os dados da amostra
        
    Returns:
        String formatada como linha CSV
    """
    # Formata cada valor, substituindo None por "NULL"
    values = []
    for key in ['timestamp', 'mode', 'temperature', 'pressure', 'vibration_x', 
               'vibration_y', 'vibration_z', 'vibration_mag', 'level', 'status']:
        value = sample.get(key)
        
        if value is None:
            values.append("NULL")
        elif isinstance(value, float):
            if key in ['vibration_x', 'vibration_y', 'vibration_z', 'vibration_mag']:
                values.append(f"{value:.3f}")
            elif key == 'level':
                values.append(f"{value:.1f}")
            else:
                values.append(f"{value:.2f}")
        else:
            values.append(str(value))
    
    return ','.join(values)

def generate_scenario_data(scenario, num_samples, interval_sec, start_time=None, add_anomalies=False):
    """
    Gera dados para um cenário específico.
    
    Args:
        scenario: Nome do cenário ('normal', 'alert', 'failure')
        num_samples: Número de amostras a gerar
        interval_sec: Intervalo entre amostras em segundos
        start_time: Timestamp inicial (se None, usa o tempo atual)
        add_anomalies: Se True, adiciona anomalias aleatórias
        
    Returns:
        Lista de amostras
    """
    samples = []
    
    # Define o timestamp inicial
    if start_time is None:
        start_time = time.time()
    
    # Gera as amostras
    for i in range(num_samples):
        timestamp = start_time + i * interval_sec
        
        # Decide se esta amostra será uma anomalia
        current_scenario = scenario
        if add_anomalies and random.random() < 0.05:  # 5% de chance de anomalia
            # Escolhe um cenário diferente para a anomalia
            if scenario == 'normal':
                current_scenario = random.choice(['alert', 'failure'])
            elif scenario == 'alert':
                current_scenario = random.choice(['normal', 'failure'])
            else:  # failure
                current_scenario = random.choice(['normal', 'alert'])
        
        # Gera a amostra
        sample = generate_sample(current_scenario, timestamp)
        samples.append(sample)
    
    return samples

def save_csv(samples, output_file, write_header=True):
    """
    Salva amostras em um arquivo CSV.
    
    Args:
        samples: Lista de amostras
        output_file: Caminho do arquivo de saída
        write_header: Se True, escreve o cabeçalho
    """
    # Define o modo de abertura do arquivo
    mode = 'w' if write_header else 'a'
    
    with open(output_file, mode, newline='') as f:
        # Escreve o cabeçalho se necessário
        if write_header:
            f.write("timestamp,mode,temperature,pressure,vibration_x,vibration_y,vibration_z,vibration_mag,level,status\n")
        
        # Escreve as amostras
        for sample in samples:
            f.write(format_csv_line(sample) + '\n')

def load_simulation_params(config_file=None):
    if config_file and os.path.exists(config_file):
        with open(config_file, 'r') as f:
            return json.load(f)
    return SENSOR_PARAMS

def main():
    """Função principal"""
    # Configura o parser de argumentos
    parser = argparse.ArgumentParser(description='Simulador de cenários de sensores industriais.')
    parser.add_argument('--scenario', '-s', choices=['normal', 'alert', 'failure', 'all'], 
                        default='all', help='Cenário a simular (padrão: all)')
    parser.add_argument('--samples', '-n', type=int, default=100, 
                        help='Número de amostras por cenário (padrão: 100)')
    parser.add_argument('--interval', '-i', type=float, default=1.0, 
                        help='Intervalo entre amostras em segundos (padrão: 1.0)')
    parser.add_argument('--output-dir', '-o', default='simulated_data', 
                        help='Diretório para salvar os arquivos de saída (padrão: simulated_data)')
    parser.add_argument('--anomalies', '-a', action='store_true', 
                        help='Adicionar anomalias aleatórias')
    parser.add_argument('--print', '-p', action='store_true', 
                        help='Imprimir amostras no console')
    parser.add_argument('--config', type=str, help='Arquivo JSON com parâmetros de simulação')
    
    args = parser.parse_args()
    
    # Cria o diretório de saída se não existir
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Define os cenários a simular
    scenarios = ['normal', 'alert', 'failure'] if args.scenario == 'all' else [args.scenario]
    
    # Define o timestamp inicial (1 hora atrás)
    start_time = time.time() - 3600
    
    # Simula cada cenário
    for scenario in scenarios:
        print(f"Simulando cenário: {scenario}")
        
        # Gera os dados
        samples = generate_scenario_data(
            scenario, 
            args.samples, 
            args.interval, 
            start_time, 
            args.anomalies
        )
        
        # Define o nome do arquivo de saída
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(args.output_dir, f"{scenario}_{timestamp}.csv")
        
        # Salva os dados
        save_csv(samples, output_file)
        print(f"Dados salvos em: {output_file}")
        
        # Imprime amostras se solicitado
        if args.print:
            print("\nPrimeiras 5 amostras:")
            for i, sample in enumerate(samples[:5]):
                print(format_csv_line(sample))
            print("...")
        
        # Incrementa o timestamp inicial para o próximo cenário
        start_time += args.samples * args.interval

if __name__ == "__main__":
    main()