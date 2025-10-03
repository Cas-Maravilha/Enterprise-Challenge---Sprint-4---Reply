#!/usr/bin/env python3
"""
Script para detecção de anomalias em dados de sensores industriais.
Implementa múltiplos métodos de detecção de anomalias.
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import argparse
import os
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
import tensorflow as tf
from tensorflow import keras

def load_data(file_path):
    """Carrega dados do arquivo CSV"""
    df = pd.read_csv(file_path)
    
    # Converte timestamp para datetime se existir
    if 'timestamp' in df.columns:
        df['datetime'] = pd.to_datetime(df['timestamp'], unit='s')
    
    return df

def detect_zscore_anomalies(df, sensor_col, threshold=3.0):
    """
    Detecta anomalias usando o método Z-Score.
    
    Args:
        df: DataFrame com os dados
        sensor_col: Nome da coluna do sensor
        threshold: Limiar para considerar um ponto como anomalia
        
    Returns:
        DataFrame com os dados e uma coluna adicional indicando anomalias
    """
    # Cria uma cópia do DataFrame
    result_df = df.copy()
    
    # Calcula o Z-Score
    z_scores = np.abs(stats.zscore(result_df[sensor_col].dropna()))
    
    # Adiciona coluna de anomalias
    result_df['anomaly'] = False
    result_df.loc[z_scores > threshold, 'anomaly'] = True
    
    return result_df

def detect_iqr_anomalies(df, sensor_col):
    """
    Detecta anomalias usando o método IQR (Intervalo Interquartil).
    
    Args:
        df: DataFrame com os dados
        sensor_col: Nome da coluna do sensor
        
    Returns:
        DataFrame com os dados e uma coluna adicional indicando anomalias
    """
    # Cria uma cópia do DataFrame
    result_df = df.copy()
    
    # Calcula Q1, Q3 e IQR
    q1 = result_df[sensor_col].quantile(0.25)
    q3 = result_df[sensor_col].quantile(0.75)
    iqr = q3 - q1
    
    # Define os limites
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    
    # Adiciona coluna de anomalias
    result_df['anomaly'] = False
    result_df.loc[(result_df[sensor_col] < lower_bound) | (result_df[sensor_col] > upper_bound), 'anomaly'] = True
    
    return result_df

def detect_isolation_forest_anomalies(df, sensor_col, contamination=0.05):
    """
    Detecta anomalias usando o algoritmo Isolation Forest.
    
    Args:
        df: DataFrame com os dados
        sensor_col: Nome da coluna do sensor
        contamination: Proporção esperada de anomalias
        
    Returns:
        DataFrame com os dados e uma coluna adicional indicando anomalias
    """
    # Cria uma cópia do DataFrame
    result_df = df.copy()
    
    # Prepara os dados
    X = result_df[sensor_col].values.reshape(-1, 1)
    
    # Aplica o algoritmo
    model = IsolationForest(contamination=contamination, random_state=42)
    result_df['anomaly'] = model.fit_predict(X) == -1
    
    return result_df

def detect_lof_anomalies(df, sensor_col, n_neighbors=20, contamination=0.05):
    """
    Detecta anomalias usando o algoritmo Local Outlier Factor.
    
    Args:
        df: DataFrame com os dados
        sensor_col: Nome da coluna do sensor
        n_neighbors: Número de vizinhos a considerar
        contamination: Proporção esperada de anomalias
        
    Returns:
        DataFrame com os dados e uma coluna adicional indicando anomalias
    """
    # Cria uma cópia do DataFrame
    result_df = df.copy()
    
    # Prepara os dados
    X = result_df[sensor_col].values.reshape(-1, 1)
    
    # Aplica o algoritmo
    model = LocalOutlierFactor(n_neighbors=n_neighbors, contamination=contamination)
    result_df['anomaly'] = model.fit_predict(X) == -1
    
    return result_df

def detect_dbscan_anomalies(df, sensor_col, eps=0.5, min_samples=5):
    """
    Detecta anomalias usando o algoritmo DBSCAN.
    
    Args:
        df: DataFrame com os dados
        sensor_col: Nome da coluna do sensor
        eps: Distância máxima entre dois pontos para serem considerados vizinhos
        min_samples: Número mínimo de pontos para formar um cluster
        
    Returns:
        DataFrame com os dados e uma coluna adicional indicando anomalias
    """
    # Cria uma cópia do DataFrame
    result_df = df.copy()
    
    # Prepara os dados
    X = result_df[sensor_col].values.reshape(-1, 1)
    X = StandardScaler().fit_transform(X)
    
    # Aplica o algoritmo
    model = DBSCAN(eps=eps, min_samples=min_samples)
    labels = model.fit_predict(X)
    
    # Pontos com label -1 são considerados anomalias
    result_df['anomaly'] = labels == -1
    
    return result_df

def detect_multivariate_anomalies(df, sensor_cols, method='isolation_forest', **kwargs):
    """
    Detecta anomalias multivariadas usando vários sensores.
    
    Args:
        df: DataFrame com os dados
        sensor_cols: Lista de colunas de sensores
        method: Método de detecção ('isolation_forest', 'lof', 'dbscan')
        **kwargs: Parâmetros adicionais para o método escolhido
        
    Returns:
        DataFrame com os dados e uma coluna adicional indicando anomalias
    """
    # Cria uma cópia do DataFrame
    result_df = df.copy()
    
    # Prepara os dados
    X = result_df[sensor_cols].values
    
    # Normaliza os dados
    X = StandardScaler().fit_transform(X)
    
    # Aplica o algoritmo escolhido
    if method == 'isolation_forest':
        contamination = kwargs.get('contamination', 0.05)
        model = IsolationForest(contamination=contamination, random_state=42)
        result_df['anomaly'] = model.fit_predict(X) == -1
    
    elif method == 'lof':
        n_neighbors = kwargs.get('n_neighbors', 20)
        contamination = kwargs.get('contamination', 0.05)
        model = LocalOutlierFactor(n_neighbors=n_neighbors, contamination=contamination)
        result_df['anomaly'] = model.fit_predict(X) == -1
    
    elif method == 'dbscan':
        eps = kwargs.get('eps', 0.5)
        min_samples = kwargs.get('min_samples', 5)
        model = DBSCAN(eps=eps, min_samples=min_samples)
        labels = model.fit_predict(X)
        result_df['anomaly'] = labels == -1
    
    else:
        raise ValueError(f"Método desconhecido: {method}")
    
    return result_df

def detect_autoencoder_anomalies(df, sensor_col, threshold=None):
    # Exemplo simplificado de autoencoder para detecção de anomalias
    data = df[sensor_col].dropna().values.reshape(-1, 1)
    model = keras.Sequential([
        keras.layers.Input(shape=(1,)),
        keras.layers.Dense(8, activation='relu'),
        keras.layers.Dense(1)
    ])
    model.compile(optimizer='adam', loss='mse')
    model.fit(data, data, epochs=20, verbose=0)
    preds = model.predict(data)
    mse = np.mean(np.square(data - preds), axis=1)
    if threshold is None:
        threshold = np.percentile(mse, 95)
    anomalies = mse > threshold
    result_df = df.copy()
    result_df['anomaly'] = False
    result_df.loc[df[sensor_col].dropna().index, 'anomaly'] = anomalies
    return result_df

def plot_anomalies(df, sensor_col, title=None, output_file=None):
    """
    Plota os dados com anomalias destacadas.
    
    Args:
        df: DataFrame com os dados e coluna 'anomaly'
        sensor_col: Nome da coluna do sensor
        title: Título do gráfico (opcional)
        output_file: Caminho para salvar o gráfico (opcional)
    """
    plt.figure(figsize=(12, 6))
    
    # Verifica se há coluna datetime
    if 'datetime' in df.columns:
        x = df['datetime']
        xlabel = 'Tempo'
    else:
        x = df.index
        xlabel = 'Índice'
    
    # Plota os pontos normais
    plt.plot(x, df[sensor_col], 'b.', label='Normal')
    
    # Plota as anomalias
    anomalies = df[df['anomaly']]
    if len(anomalies) > 0:
        if 'datetime' in df.columns:
            plt.plot(anomalies['datetime'], anomalies[sensor_col], 'ro', label='Anomalia')
        else:
            plt.plot(anomalies.index, anomalies[sensor_col], 'ro', label='Anomalia')
    
    # Configura o gráfico
    if title:
        plt.title(title)
    else:
        plt.title(f'Detecção de Anomalias: {sensor_col}')
    
    plt.xlabel(xlabel)
    plt.ylabel(sensor_col)
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Salva ou mostra o gráfico
    if output_file:
        plt.savefig(output_file)
    else:
        plt.show()
    
    plt.close()

def plot_multivariate_anomalies(df, sensor_cols, output_file=None):
    """
    Plota matriz de dispersão com anomalias destacadas.
    
    Args:
        df: DataFrame com os dados e coluna 'anomaly'
        sensor_cols: Lista de colunas de sensores
        output_file: Caminho para salvar o gráfico (opcional)
    """
    # Cria uma cópia com uma coluna categórica para as anomalias
    plot_df = df.copy()
    plot_df['anomaly_cat'] = plot_df['anomaly'].map({True: 'Anomalia', False: 'Normal'})
    
    # Plota a matriz de dispersão
    plt.figure(figsize=(12, 10))
    sns.pairplot(plot_df, vars=sensor_cols, hue='anomaly_cat', 
                 palette={'Normal': 'blue', 'Anomalia': 'red'},
                 plot_kws={'alpha': 0.6})
    
    plt.suptitle('Detecção de Anomalias Multivariadas', y=1.02)
    
    # Salva ou mostra o gráfico
    if output_file:
        plt.savefig(output_file)
    else:
        plt.show()
    
    plt.close()

def main():
    parser = argparse.ArgumentParser(description='Detecção de anomalias em dados de sensores industriais')
    parser.add_argument('--input', '-i', required=True, help='Arquivo CSV com os dados')
    parser.add_argument('--output-dir', '-o', default='anomaly_detection', help='Diretório para salvar os resultados')
    parser.add_argument('--sensor', '-s', help='Coluna do sensor para análise univariada')
    parser.add_argument('--method', '-m', choices=['zscore', 'iqr', 'isolation_forest', 'lof', 'dbscan', 'multivariate', 'autoencoder'],
                        default='zscore', help='Método de detecção de anomalias')
    parser.add_argument('--threshold', '-t', type=float, default=3.0, help='Limiar para Z-Score')
    parser.add_argument('--contamination', '-c', type=float, default=0.05, 
                        help='Proporção esperada de anomalias (para Isolation Forest e LOF)')
    parser.add_argument('--eps', '-e', type=float, default=0.5, help='Parâmetro eps para DBSCAN')
    parser.add_argument('--min-samples', type=int, default=5, help='Parâmetro min_samples para DBSCAN')
    parser.add_argument('--n-neighbors', '-n', type=int, default=20, help='Número de vizinhos para LOF')
    
    args = parser.parse_args()
    
    # Cria o diretório de saída
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Carrega os dados
    print(f"Carregando dados de {args.input}...")
    df = load_data(args.input)
    print(f"Dados carregados: {len(df)} registros")
    
    # Identifica as colunas de sensores
    non_sensor_cols = ['timestamp', 'datetime', 'mode', 'status', 'anomaly', 'anomaly_cat']
    sensor_cols = [col for col in df.columns if col not in non_sensor_cols]
    print(f"Sensores identificados: {', '.join(sensor_cols)}")
    
    # Se não foi especificado um sensor, usa o primeiro
    if args.sensor is None and args.method != 'multivariate':
        args.sensor = sensor_cols[0]
        print(f"Nenhum sensor especificado, usando {args.sensor}")
    
    # Detecta anomalias
    if args.method == 'zscore':
        print(f"Detectando anomalias usando Z-Score (threshold={args.threshold})...")
        result_df = detect_zscore_anomalies(df, args.sensor, args.threshold)
        method_name = f"zscore_t{args.threshold}"
    
    elif args.method == 'iqr':
        print("Detectando anomalias usando IQR...")
        result_df = detect_iqr_anomalies(df, args.sensor)
        method_name = "iqr"
    
    elif args.method == 'isolation_forest':
        print(f"Detectando anomalias usando Isolation Forest (contamination={args.contamination})...")
        result_df = detect_isolation_forest_anomalies(df, args.sensor, args.contamination)
        method_name = f"isoforest_c{args.contamination}"
    
    elif args.method == 'lof':
        print(f"Detectando anomalias usando LOF (n_neighbors={args.n_neighbors}, contamination={args.contamination})...")
        result_df = detect_lof_anomalies(df, args.sensor, args.n_neighbors, args.contamination)
        method_name = f"lof_n{args.n_neighbors}_c{args.contamination}"
    
    elif args.method == 'dbscan':
        print(f"Detectando anomalias usando DBSCAN (eps={args.eps}, min_samples={args.min_samples})...")
        result_df = detect_dbscan_anomalies(df, args.sensor, args.eps, args.min_samples)
        method_name = f"dbscan_e{args.eps}_m{args.min_samples}"
    
    elif args.method == 'multivariate':
        print(f"Detectando anomalias multivariadas usando {len(sensor_cols)} sensores...")
        result_df = detect_multivariate_anomalies(
            df, sensor_cols, 'isolation_forest', contamination=args.contamination
        )
        method_name = f"multivariate_c{args.contamination}"
    
    elif args.method == 'autoencoder':
        print(f"Detectando anomalias usando Autoencoder...")
        result_df = detect_autoencoder_anomalies(df, args.sensor)
        method_name = "autoencoder"
    
    # Conta as anomalias
    anomaly_count = result_df['anomaly'].sum()
    print(f"Anomalias detectadas: {anomaly_count} ({anomaly_count/len(result_df):.2%})")
    
    # Salva os resultados
    output_csv = os.path.join(args.output_dir, f"anomalies_{method_name}.csv")
    result_df.to_csv(output_csv, index=False)
    print(f"Resultados salvos em {output_csv}")
    
    # Plota os resultados
    if args.method == 'multivariate':
        output_plot = os.path.join(args.output_dir, f"anomalies_{method_name}.png")
        plot_multivariate_anomalies(result_df, sensor_cols, output_plot)
        print(f"Gráfico salvo em {output_plot}")
    else:
        output_plot = os.path.join(args.output_dir, f"anomalies_{method_name}_{args.sensor}.png")
        plot_anomalies(result_df, args.sensor, 
                      f"Detecção de Anomalias: {args.sensor} ({args.method})",
                      output_plot)
        print(f"Gráfico salvo em {output_plot}")

if __name__ == "__main__":
    main()