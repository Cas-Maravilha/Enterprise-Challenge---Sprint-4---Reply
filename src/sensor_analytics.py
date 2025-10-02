#!/usr/bin/env python3
"""
Script para análise e visualização de dados de sensores industriais.
Inclui múltiplos tipos de gráficos, análise estatística básica e detecção de anomalias.
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import argparse
import os
import json
from datetime import datetime

def load_data(file_path):
    """Carrega dados do arquivo CSV ou JSON"""
    if file_path.endswith('.csv'):
        df = pd.read_csv(file_path)
    elif file_path.endswith('.json'):
        with open(file_path, 'r') as f:
            data = json.load(f)
        df = pd.DataFrame(data)
    else:
        raise ValueError("Formato de arquivo não suportado. Use CSV ou JSON.")
    
    # Converte timestamp para datetime se existir
    if 'timestamp' in df.columns:
        df['datetime'] = pd.to_datetime(df['timestamp'], unit='s')
    
    return df

def basic_statistics(df, sensors):
    """Calcula estatísticas básicas para os sensores"""
    stats_dict = {}
    for sensor in sensors:
        if sensor in df.columns:
            stats_dict[sensor] = {
                'mean': df[sensor].mean(),
                'median': df[sensor].median(),
                'std': df[sensor].std(),
                'min': df[sensor].min(),
                'max': df[sensor].max(),
                'q1': df[sensor].quantile(0.25),
                'q3': df[sensor].quantile(0.75),
                'iqr': df[sensor].quantile(0.75) - df[sensor].quantile(0.25),
                'skewness': stats.skew(df[sensor].dropna()),
                'kurtosis': stats.kurtosis(df[sensor].dropna())
            }
    return stats_dict

def detect_anomalies(df, sensors, method='zscore', threshold=3.0):
    """Detecta anomalias nos dados dos sensores"""
    anomalies = {}
    
    for sensor in sensors:
        if sensor not in df.columns:
            continue
            
        sensor_data = df[sensor].dropna()
        
        if method == 'zscore':
            # Método Z-Score
            z_scores = np.abs(stats.zscore(sensor_data))
            anomalies[sensor] = df.loc[z_scores > threshold].index.tolist()
            
        elif method == 'iqr':
            # Método IQR (Intervalo Interquartil)
            q1 = sensor_data.quantile(0.25)
            q3 = sensor_data.quantile(0.75)
            iqr = q3 - q1
            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr
            anomalies[sensor] = df.loc[(sensor_data < lower_bound) | (sensor_data > upper_bound)].index.tolist()
            
        elif method == 'isolation_forest':
            # Método Isolation Forest (requer scikit-learn)
            from sklearn.ensemble import IsolationForest
            model = IsolationForest(contamination=0.05, random_state=42)
            sensor_data_2d = sensor_data.values.reshape(-1, 1)
            preds = model.fit_predict(sensor_data_2d)
            anomalies[sensor] = df.loc[preds == -1].index.tolist()
    
    return anomalies

def plot_time_series(df, sensors, output_dir=None):
    """Gera gráficos de linha (série temporal) para os sensores"""
    if 'datetime' not in df.columns:
        if 'timestamp' in df.columns:
            df['datetime'] = pd.to_datetime(df['timestamp'], unit='s')
        else:
            df['datetime'] = pd.to_datetime(df.index, unit='s')
    
    plt.figure(figsize=(12, 6))
    for sensor in sensors:
        if sensor in df.columns:
            plt.plot(df['datetime'], df[sensor], label=sensor)
    
    plt.title('Série Temporal dos Sensores')
    plt.xlabel('Tempo')
    plt.ylabel('Valor')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        plt.savefig(os.path.join(output_dir, 'time_series.png'))
    else:
        plt.show()
    
    plt.close()

def plot_scatter(df, x_sensor, y_sensor, output_dir=None):
    """Gera gráfico de dispersão entre dois sensores"""
    if x_sensor in df.columns and y_sensor in df.columns:
        plt.figure(figsize=(10, 6))
        plt.scatter(df[x_sensor], df[y_sensor], alpha=0.6)
        
        # Adiciona linha de tendência
        z = np.polyfit(df[x_sensor].dropna(), df[y_sensor].dropna(), 1)
        p = np.poly1d(z)
        plt.plot(df[x_sensor], p(df[x_sensor]), "r--", alpha=0.8)
        
        plt.title(f'Dispersão: {x_sensor} vs {y_sensor}')
        plt.xlabel(x_sensor)
        plt.ylabel(y_sensor)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
            plt.savefig(os.path.join(output_dir, f'scatter_{x_sensor}_{y_sensor}.png'))
        else:
            plt.show()
        
        plt.close()

def plot_histograms(df, sensors, output_dir=None):
    """Gera histogramas para os sensores"""
    for sensor in sensors:
        if sensor in df.columns:
            plt.figure(figsize=(10, 6))
            sns.histplot(df[sensor].dropna(), kde=True)
            plt.title(f'Distribuição de {sensor}')
            plt.xlabel(sensor)
            plt.ylabel('Frequência')
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            
            if output_dir:
                os.makedirs(output_dir, exist_ok=True)
                plt.savefig(os.path.join(output_dir, f'histogram_{sensor}.png'))
            else:
                plt.show()
            
            plt.close()

def plot_boxplots(df, sensors, output_dir=None):
    """Gera boxplots para os sensores"""
    plt.figure(figsize=(12, 6))
    
    # Prepara os dados para o boxplot
    data_to_plot = []
    labels = []
    
    for sensor in sensors:
        if sensor in df.columns:
            data_to_plot.append(df[sensor].dropna())
            labels.append(sensor)
    
    plt.boxplot(data_to_plot, labels=labels)
    plt.title('Boxplots dos Sensores')
    plt.ylabel('Valor')
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        plt.savefig(os.path.join(output_dir, 'boxplots.png'))
    else:
        plt.show()
    
    plt.close()

def plot_correlation_heatmap(df, sensors, output_dir=None):
    """Gera mapa de calor de correlação entre os sensores"""
    # Filtra apenas as colunas dos sensores
    sensor_data = df[sensors].copy()
    
    # Calcula a matriz de correlação
    corr_matrix = sensor_data.corr()
    
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1, center=0)
    plt.title('Matriz de Correlação entre Sensores')
    plt.tight_layout()
    
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        plt.savefig(os.path.join(output_dir, 'correlation_heatmap.png'))
    else:
        plt.show()
    
    plt.close()

def plot_anomalies(df, sensors, anomalies, output_dir=None):
    """Plota os dados com anomalias destacadas"""
    if 'datetime' not in df.columns:
        if 'timestamp' in df.columns:
            df['datetime'] = pd.to_datetime(df['timestamp'], unit='s')
        else:
            df['datetime'] = pd.to_datetime(df.index, unit='s')
    
    for sensor in sensors:
        if sensor in df.columns and sensor in anomalies:
            plt.figure(figsize=(12, 6))
            
            # Plota todos os pontos
            plt.plot(df['datetime'], df[sensor], 'b-', label=sensor)
            
            # Destaca as anomalias
            if anomalies[sensor]:
                anomaly_dates = df.loc[anomalies[sensor], 'datetime']
                anomaly_values = df.loc[anomalies[sensor], sensor]
                plt.scatter(anomaly_dates, anomaly_values, color='red', s=50, label='Anomalias')
            
            plt.title(f'Detecção de Anomalias: {sensor}')
            plt.xlabel('Tempo')
            plt.ylabel('Valor')
            plt.legend()
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            
            if output_dir:
                os.makedirs(output_dir, exist_ok=True)
                plt.savefig(os.path.join(output_dir, f'anomalies_{sensor}.png'))
            else:
                plt.show()
            
            plt.close()

def generate_report(stats_dict, anomalies, output_file):
    """Gera um relatório de texto com estatísticas e anomalias"""
    with open(output_file, 'w') as f:
        f.write("# Relatório de Análise de Sensores\n\n")
        f.write(f"Gerado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        # Estatísticas básicas
        f.write("## Estatísticas Básicas\n\n")
        for sensor, stats in stats_dict.items():
            f.write(f"### {sensor}\n\n")
            f.write(f"- Média: {stats['mean']:.4f}\n")
            f.write(f"- Mediana: {stats['median']:.4f}\n")
            f.write(f"- Desvio Padrão: {stats['std']:.4f}\n")
            f.write(f"- Mínimo: {stats['min']:.4f}\n")
            f.write(f"- Máximo: {stats['max']:.4f}\n")
            f.write(f"- Q1 (25%): {stats['q1']:.4f}\n")
            f.write(f"- Q3 (75%): {stats['q3']:.4f}\n")
            f.write(f"- IQR: {stats['iqr']:.4f}\n")
            f.write(f"- Assimetria: {stats['skewness']:.4f}\n")
            f.write(f"- Curtose: {stats['kurtosis']:.4f}\n\n")
        
        # Anomalias
        f.write("## Detecção de Anomalias\n\n")
        for sensor, indices in anomalies.items():
            f.write(f"### {sensor}\n\n")
            f.write(f"- Total de anomalias detectadas: {len(indices)}\n")
            if indices:
                f.write(f"- Índices das anomalias: {', '.join(map(str, indices[:20]))}")
                if len(indices) > 20:
                    f.write(f" e mais {len(indices) - 20} índices")
                f.write("\n\n")
            else:
                f.write("- Nenhuma anomalia detectada\n\n")

def export_to_excel(df, output_file):
    df.to_excel(output_file, index=False)

def export_to_pdf(fig, output_file):
    fig.savefig(output_file, format='pdf')

def main():
    parser = argparse.ArgumentParser(description='Análise e visualização de dados de sensores industriais')
    parser.add_argument('--input', '-i', required=True, help='Arquivo CSV ou JSON com os dados')
    parser.add_argument('--output-dir', '-o', default='sensor_analysis', help='Diretório para salvar os resultados')
    parser.add_argument('--anomaly-method', '-a', choices=['zscore', 'iqr', 'isolation_forest'], 
                        default='zscore', help='Método de detecção de anomalias')
    parser.add_argument('--threshold', '-t', type=float, default=3.0, 
                        help='Limiar para detecção de anomalias (para z-score)')
    
    args = parser.parse_args()
    
    # Cria o diretório de saída
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Carrega os dados
    print(f"Carregando dados de {args.input}...")
    df = load_data(args.input)
    print(f"Dados carregados: {len(df)} registros, {len(df.columns)} colunas")
    
    # Identifica as colunas de sensores (exclui timestamp, datetime, etc.)
    non_sensor_cols = ['timestamp', 'datetime', 'mode', 'status']
    sensors = [col for col in df.columns if col not in non_sensor_cols]
    print(f"Sensores identificados: {', '.join(sensors)}")
    
    # Calcula estatísticas básicas
    print("Calculando estatísticas básicas...")
    stats_dict = basic_statistics(df, sensors)
    
    # Detecta anomalias
    print(f"Detectando anomalias usando método {args.anomaly_method}...")
    anomalies = detect_anomalies(df, sensors, method=args.anomaly_method, threshold=args.threshold)
    
    # Gera gráficos
    print("Gerando gráficos...")
    plot_time_series(df, sensors, args.output_dir)
    
    # Gera gráficos de dispersão para pares de sensores
    for i, sensor1 in enumerate(sensors):
        for sensor2 in sensors[i+1:]:
            plot_scatter(df, sensor1, sensor2, args.output_dir)
    
    plot_histograms(df, sensors, args.output_dir)
    plot_boxplots(df, sensors, args.output_dir)
    plot_correlation_heatmap(df, sensors, args.output_dir)
    plot_anomalies(df, sensors, anomalies, args.output_dir)
    
    # Gera relatório
    report_file = os.path.join(args.output_dir, 'analysis_report.md')
    print(f"Gerando relatório em {report_file}...")
    generate_report(stats_dict, anomalies, report_file)
    
    print(f"Análise concluída! Resultados salvos em {args.output_dir}")

if __name__ == "__main__":
    main()