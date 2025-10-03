#!/usr/bin/env python3
"""
Script para análise dos dados coletados do ESP32.
Processa os arquivos CSV e gera gráficos e estatísticas.
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import argparse
import os
from datetime import datetime

def load_data(file_path):
    """
    Carrega os dados do arquivo CSV.
    
    Args:
        file_path: Caminho para o arquivo CSV
        
    Returns:
        DataFrame com os dados carregados
    """
    try:
        # Ignora linhas de comentário (começando com #)
        df = pd.read_csv(file_path, comment='#')
        
        # Converte a coluna timestamp para datetime
        df['datetime'] = pd.to_datetime(df['timestamp'], unit='s')
        
        # Substitui "NULL" por NaN
        df = df.replace("NULL", np.nan)
        
        # Converte colunas numéricas
        numeric_cols = ['temperature', 'pressure', 'vibration_x', 'vibration_y', 
                       'vibration_z', 'vibration_mag', 'level']
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        print(f"Dados carregados: {len(df)} linhas, {len(df.columns)} colunas")
        return df
    
    except Exception as e:
        print(f"Erro ao carregar o arquivo {file_path}: {e}")
        return None

def analyze_data(df):
    """
    Analisa os dados e retorna estatísticas básicas.
    
    Args:
        df: DataFrame com os dados
        
    Returns:
        dict com estatísticas
    """
    if df is None or len(df) == 0:
        return None
    
    # Estatísticas básicas
    stats = {}
    
    # Contagem por modo
    mode_counts = df['mode'].value_counts()
    stats['mode_counts'] = mode_counts.to_dict()
    
    # Estatísticas por sensor
    sensor_cols = ['temperature', 'pressure', 'vibration_mag', 'level']
    stats['sensors'] = {}
    
    for col in sensor_cols:
        if col in df.columns:
            stats['sensors'][col] = {
                'mean': df[col].mean(),
                'std': df[col].std(),
                'min': df[col].min(),
                'max': df[col].max(),
                'null_count': df[col].isna().sum(),
                'null_percent': (df[col].isna().sum() / len(df)) * 100
            }
    
    # Estatísticas por modo
    stats['by_mode'] = {}
    for mode in df['mode'].unique():
        mode_df = df[df['mode'] == mode]
        stats['by_mode'][mode] = {}
        
        for col in sensor_cols:
            if col in df.columns:
                stats['by_mode'][mode][col] = {
                    'mean': mode_df[col].mean(),
                    'std': mode_df[col].std(),
                    'min': mode_df[col].min(),
                    'max': mode_df[col].max(),
                    'null_count': mode_df[col].isna().sum(),
                    'null_percent': (mode_df[col].isna().sum() / len(mode_df)) * 100
                }
    
    return stats

def plot_time_series(df, output_dir):
    """
    Gera gráficos de séries temporais para cada sensor.
    
    Args:
        df: DataFrame com os dados
        output_dir: Diretório para salvar os gráficos
    """
    if df is None or len(df) == 0:
        return
    
    # Cria o diretório de saída se não existir
    os.makedirs(output_dir, exist_ok=True)
    
    # Define o estilo dos gráficos
    sns.set(style="darkgrid")
    
    # Lista de sensores para plotar
    sensors = [
        ('temperature', 'Temperatura (°C)'),
        ('pressure', 'Pressão (bar)'),
        ('vibration_mag', 'Vibração (g)'),
        ('level', 'Nível (cm)')
    ]
    
    # Plota cada sensor
    for sensor_col, sensor_label in sensors:
        if sensor_col not in df.columns:
            continue
        
        plt.figure(figsize=(12, 6))
        
        # Plota os dados por modo
        for mode, mode_name in [(0, 'Normal'), (1, 'Alerta'), (2, 'Falha')]:
            mode_df = df[df['mode'] == mode]
            if len(mode_df) > 0:
                plt.plot(mode_df['datetime'], mode_df[sensor_col], 
                         label=mode_name, alpha=0.7, 
                         marker='o' if len(mode_df) < 50 else None)
        
        plt.title(f'Série Temporal - {sensor_label}')
        plt.xlabel('Tempo')
        plt.ylabel(sensor_label)
        plt.legend()
        plt.tight_layout()
        
        # Salva o gráfico
        output_file = os.path.join(output_dir, f'timeseries_{sensor_col}.png')
        plt.savefig(output_file)
        plt.close()
        print(f"Gráfico salvo: {output_file}")
    
    # Plota todos os sensores em um único gráfico
    plt.figure(figsize=(14, 10))
    
    # Cria subplots para cada sensor
    for i, (sensor_col, sensor_label) in enumerate(sensors, 1):
        if sensor_col not in df.columns:
            continue
        
        plt.subplot(len(sensors), 1, i)
        
        # Plota os dados por modo
        for mode, mode_name, color in [(0, 'Normal', 'green'), (1, 'Alerta', 'orange'), (2, 'Falha', 'red')]:
            mode_df = df[df['mode'] == mode]
            if len(mode_df) > 0:
                plt.plot(mode_df['datetime'], mode_df[sensor_col], 
                         label=mode_name, color=color, alpha=0.7)
        
        plt.ylabel(sensor_label)
        if i == 1:
            plt.title('Séries Temporais - Todos os Sensores')
            plt.legend()
        if i == len(sensors):
            plt.xlabel('Tempo')
    
    plt.tight_layout()
    
    # Salva o gráfico
    output_file = os.path.join(output_dir, 'timeseries_all_sensors.png')
    plt.savefig(output_file)
    plt.close()
    print(f"Gráfico salvo: {output_file}")

def plot_distributions(df, output_dir):
    """
    Gera gráficos de distribuição para cada sensor.
    
    Args:
        df: DataFrame com os dados
        output_dir: Diretório para salvar os gráficos
    """
    if df is None or len(df) == 0:
        return
    
    # Cria o diretório de saída se não existir
    os.makedirs(output_dir, exist_ok=True)
    
    # Define o estilo dos gráficos
    sns.set(style="whitegrid")
    
    # Lista de sensores para plotar
    sensors = [
        ('temperature', 'Temperatura (°C)'),
        ('pressure', 'Pressão (bar)'),
        ('vibration_mag', 'Vibração (g)'),
        ('level', 'Nível (cm)')
    ]
    
    # Plota histogramas para cada sensor
    for sensor_col, sensor_label in sensors:
        if sensor_col not in df.columns:
            continue
        
        plt.figure(figsize=(12, 6))
        
        # Plota histograma por modo
        for mode, mode_name, color in [(0, 'Normal', 'green'), (1, 'Alerta', 'orange'), (2, 'Falha', 'red')]:
            mode_df = df[df['mode'] == mode]
            if len(mode_df) > 0:
                sns.histplot(mode_df[sensor_col].dropna(), 
                            label=mode_name, color=color, alpha=0.5, kde=True)
        
        plt.title(f'Distribuição - {sensor_label}')
        plt.xlabel(sensor_label)
        plt.ylabel('Frequência')
        plt.legend()
        plt.tight_layout()
        
        # Salva o gráfico
        output_file = os.path.join(output_dir, f'distribution_{sensor_col}.png')
        plt.savefig(output_file)
        plt.close()
        print(f"Gráfico salvo: {output_file}")
    
    # Plota boxplots para cada sensor
    plt.figure(figsize=(14, 10))
    
    # Cria subplots para cada sensor
    for i, (sensor_col, sensor_label) in enumerate(sensors, 1):
        if sensor_col not in df.columns:
            continue
        
        plt.subplot(2, 2, i)
        
        # Cria uma coluna de modo como texto para o boxplot
        df['mode_name'] = df['mode'].map({0: 'Normal', 1: 'Alerta', 2: 'Falha'})
        
        # Plota boxplot
        sns.boxplot(x='mode_name', y=sensor_col, data=df, 
                   palette={'Normal': 'green', 'Alerta': 'orange', 'Falha': 'red'})
        
        plt.title(f'Boxplot - {sensor_label}')
        plt.xlabel('Modo')
        plt.ylabel(sensor_label)
    
    plt.tight_layout()
    
    # Salva o gráfico
    output_file = os.path.join(output_dir, 'boxplots_all_sensors.png')
    plt.savefig(output_file)
    plt.close()
    print(f"Gráfico salvo: {output_file}")

def generate_report(stats, output_file):
    """
    Gera um relatório de texto com as estatísticas.
    
    Args:
        stats: Dicionário com estatísticas
        output_file: Arquivo de saída para o relatório
    """
    if stats is None:
        return
    
    with open(output_file, 'w') as f:
        f.write("# Relatório de Análise de Dados\n")
        f.write(f"Gerado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        # Contagem por modo
        f.write("## Contagem por Modo\n")
        for mode, count in stats['mode_counts'].items():
            mode_name = {0: 'Normal', 1: 'Alerta', 2: 'Falha'}.get(mode, mode)
            f.write(f"- {mode_name}: {count} amostras\n")
        f.write("\n")
        
        # Estatísticas por sensor
        f.write("## Estatísticas por Sensor\n")
        for sensor, sensor_stats in stats['sensors'].items():
            sensor_label = {
                'temperature': 'Temperatura (°C)',
                'pressure': 'Pressão (bar)',
                'vibration_mag': 'Vibração (g)',
                'level': 'Nível (cm)'
            }.get(sensor, sensor)
            
            f.write(f"### {sensor_label}\n")
            f.write(f"- Média: {sensor_stats['mean']:.2f}\n")
            f.write(f"- Desvio Padrão: {sensor_stats['std']:.2f}\n")
            f.write(f"- Mínimo: {sensor_stats['min']:.2f}\n")
            f.write(f"- Máximo: {sensor_stats['max']:.2f}\n")
            f.write(f"- Valores Nulos: {sensor_stats['null_count']} ({sensor_stats['null_percent']:.1f}%)\n")
            f.write("\n")
        
        # Estatísticas por modo
        f.write("## Estatísticas por Modo\n")
        for mode, mode_stats in stats['by_mode'].items():
            mode_name = {0: 'Normal', 1: 'Alerta', 2: 'Falha'}.get(mode, mode)
            f.write(f"### Modo: {mode_name}\n")
            
            for sensor, sensor_stats in mode_stats.items():
                sensor_label = {
                    'temperature': 'Temperatura (°C)',
                    'pressure': 'Pressão (bar)',
                    'vibration_mag': 'Vibração (g)',
                    'level': 'Nível (cm)'
                }.get(sensor, sensor)
                
                f.write(f"#### {sensor_label}\n")
                f.write(f"- Média: {sensor_stats['mean']:.2f}\n")
                f.write(f"- Desvio Padrão: {sensor_stats['std']:.2f}\n")
                f.write(f"- Mínimo: {sensor_stats['min']:.2f}\n")
                f.write(f"- Máximo: {sensor_stats['max']:.2f}\n")
                f.write(f"- Valores Nulos: {sensor_stats['null_count']} ({sensor_stats['null_percent']:.1f}%)\n")
                f.write("\n")
    
    print(f"Relatório gerado: {output_file}")

def main():
    """Função principal"""
    # Configura o parser de argumentos
    parser = argparse.ArgumentParser(description='Analisa dados coletados do ESP32.')
    parser.add_argument('--input', '-i', required=True, help='Arquivo CSV de entrada ou diretório com arquivos CSV')
    parser.add_argument('--output-dir', '-o', default='analysis', help='Diretório para salvar os resultados (padrão: analysis)')
    
    args = parser.parse_args()
    
    # Cria o diretório de saída se não existir
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Verifica se o input é um arquivo ou diretório
    if os.path.isdir(args.input):
        # Processa todos os arquivos CSV no diretório
        csv_files = [f for f in os.listdir(args.input) if f.endswith('.csv')]
        
        if not csv_files:
            print(f"Nenhum arquivo CSV encontrado no diretório {args.input}")
            return
        
        print(f"Encontrados {len(csv_files)} arquivos CSV para análise")
        
        # Processa cada arquivo
        for csv_file in csv_files:
            file_path = os.path.join(args.input, csv_file)
            file_name = os.path.splitext(csv_file)[0]
            
            print(f"\nProcessando arquivo: {csv_file}")
            
            # Carrega os dados
            df = load_data(file_path)
            
            if df is not None and len(df) > 0:
                # Cria subdiretório para os resultados deste arquivo
                file_output_dir = os.path.join(args.output_dir, file_name)
                os.makedirs(file_output_dir, exist_ok=True)
                
                # Analisa os dados
                stats = analyze_data(df)
                
                # Gera gráficos
                plot_time_series(df, file_output_dir)
                plot_distributions(df, file_output_dir)
                
                # Gera relatório
                report_file = os.path.join(file_output_dir, 'report.md')
                generate_report(stats, report_file)
    else:
        # Processa um único arquivo
        print(f"Processando arquivo: {args.input}")
        
        # Carrega os dados
        df = load_data(args.input)
        
        if df is not None and len(df) > 0:
            # Analisa os dados
            stats = analyze_data(df)
            
            # Gera gráficos
            plot_time_series(df, args.output_dir)
            plot_distributions(df, args.output_dir)
            
            # Gera relatório
            report_file = os.path.join(args.output_dir, 'report.md')
            generate_report(stats, report_file)

if __name__ == "__main__":
    main()