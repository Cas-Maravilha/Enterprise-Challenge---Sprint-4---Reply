#!/usr/bin/env python3
"""
Geração de Dataset CSV para Treinamento do Modelo ML
Sistema de Detecção de Anomalias IoT
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

def gerar_dataset_completo(n_samples=5000, salvar_csv=True):
    """
    Gera dataset completo baseado nos dados reais do projeto IoT
    """
    print("🔄 GERANDO DATASET COMPLETO PARA ML")
    print("=" * 50)
    
    np.random.seed(42)
    data = []
    
    # Data base para timestamps
    data_base = datetime(2024, 1, 1)
    
    print(f"Gerando {n_samples} amostras sintéticas...")
    print("Baseado nos dados reais coletados pelos sensores ESP32")
    
    for i in range(n_samples):
        # Simular diferentes modos de operação
        mode = np.random.choice([0, 1, 2], p=[0.7, 0.2, 0.1])  # Normal, Alerta, Falha
        
        # Timestamp realista (a cada 30 segundos)
        timestamp = data_base + timedelta(seconds=i * 30)
        timestamp_unix = timestamp.timestamp()
        
        if mode == 0:  # Normal
            temperature = np.random.normal(25.0, 2.0)
            humidity = np.random.normal(60.0, 5.0)
            pressure = np.random.normal(5.0, 0.5)
            vibration_x = np.random.normal(0.0, 0.3)
            vibration_y = np.random.normal(0.0, 0.1)
            vibration_z = np.random.normal(0.0, 0.1)
            level = np.random.normal(100.0, 10.0)
            luminosity = np.random.normal(500.0, 100.0)
            movement = np.random.choice([0, 1], p=[0.9, 0.1])
            
        elif mode == 1:  # Alerta
            temperature = np.random.normal(28.0, 3.0)
            humidity = np.random.normal(70.0, 8.0)
            pressure = np.random.normal(6.5, 0.8)
            vibration_x = np.random.normal(0.5, 0.4)
            vibration_y = np.random.normal(0.2, 0.2)
            vibration_z = np.random.normal(0.1, 0.2)
            level = np.random.normal(120.0, 15.0)
            luminosity = np.random.normal(600.0, 150.0)
            movement = np.random.choice([0, 1], p=[0.7, 0.3])
            
        else:  # Falha
            temperature = np.random.normal(35.0, 5.0)
            humidity = np.random.normal(85.0, 10.0)
            pressure = np.random.normal(8.0, 1.5)
            vibration_x = np.random.normal(1.5, 0.8)
            vibration_y = np.random.normal(0.8, 0.5)
            vibration_z = np.random.normal(0.6, 0.4)
            level = np.random.normal(150.0, 25.0)
            luminosity = np.random.normal(800.0, 200.0)
            movement = np.random.choice([0, 1], p=[0.5, 0.5])
        
        # Adicionar anomalias ocasionais (5% de chance)
        if np.random.random() < 0.05:
            temperature += np.random.normal(0, 10)
            humidity += np.random.normal(0, 20)
            pressure += np.random.normal(0, 2)
            vibration_x += np.random.normal(0, 1)
            vibration_y += np.random.normal(0, 0.5)
            vibration_z += np.random.normal(0, 0.5)
            level += np.random.normal(0, 30)
            luminosity += np.random.normal(0, 300)
            movement = np.random.choice([0, 1], p=[0.3, 0.7])
            mode = 2  # Marcar como falha
        
        # Calcular magnitude da vibração
        vibration_mag = np.sqrt(vibration_x**2 + vibration_y**2 + vibration_z**2)
        
        # Calcular correlações entre variáveis
        if temperature > 30:
            humidity = min(100, humidity + (temperature - 30) * 2)
        
        # Adicionar variação temporal (tendências)
        if i > 100:  # Após as primeiras 100 amostras
            # Simular variação diária
            hora = timestamp.hour
            if 6 <= hora <= 18:  # Dia
                temperature += 2
                luminosity += 100
            else:  # Noite
                temperature -= 1
                luminosity -= 50
        
        # Simular sazonalidade semanal
        dia_semana = timestamp.weekday()
        if dia_semana < 5:  # Dias úteis
            movement += np.random.choice([0, 1], p=[0.8, 0.2])
        else:  # Fim de semana
            movement += np.random.choice([0, 1], p=[0.9, 0.1])
        
        data.append({
            'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'timestamp_unix': timestamp_unix,
            'mode': mode,
            'temperature': max(-40, min(80, round(temperature, 2))),
            'humidity': max(0, min(100, round(humidity, 2))),
            'pressure': max(0, min(10, round(pressure, 2))),
            'vibration_x': round(vibration_x, 3),
            'vibration_y': round(vibration_y, 3),
            'vibration_z': round(vibration_z, 3),
            'vibration_mag': round(vibration_mag, 3),
            'level': max(0, min(200, round(level, 1))),
            'luminosity': max(0, min(1023, round(luminosity, 0))),
            'movement': int(movement),
            'anomaly': 1 if mode == 2 else 0,
            'device_id': f"ESP32_{i % 3 + 1:02d}",  # 3 dispositivos
            'location': ['Sala_01', 'Garagem_01', 'Cozinha_01'][i % 3]
        })
    
    df = pd.DataFrame(data)
    
    # Adicionar features derivadas
    df['temp_humidity_ratio'] = round(df['temperature'] / (df['humidity'] + 1), 4)
    df['pressure_vibration'] = round(df['pressure'] * df['vibration_mag'], 4)
    df['level_luminosity'] = round(df['level'] * df['luminosity'] / 1000, 2)
    df['temp_pressure_ratio'] = round(df['temperature'] / (df['pressure'] + 0.1), 2)
    df['humidity_level_ratio'] = round(df['humidity'] / (df['level'] + 1), 4)
    
    # Adicionar indicadores de qualidade dos dados
    df['data_quality'] = np.random.choice(['excelente', 'bom', 'regular', 'ruim'], 
                                        p=[0.6, 0.25, 0.12, 0.03], size=len(df))
    
    # Adicionar status do dispositivo
    df['device_status'] = np.where(df['anomaly'] == 1, 'falha', 
                                  np.where(df['mode'] == 1, 'alerta', 'normal'))
    
    print(f"✅ Dataset gerado com sucesso!")
    print(f"   • Total de amostras: {len(df)}")
    print(f"   • Total de features: {len(df.columns)}")
    print(f"   • Período: {df['timestamp'].min()} a {df['timestamp'].max()}")
    print(f"   • Dispositivos: {df['device_id'].nunique()}")
    print(f"   • Localizações: {df['location'].nunique()}")
    
    # Estatísticas por classe
    print(f"\n📊 Distribuição por classe:")
    print(f"   • Normal (0): {len(df[df['anomaly'] == 0])} amostras ({len(df[df['anomaly'] == 0])/len(df):.1%})")
    print(f"   • Anomalia (1): {len(df[df['anomaly'] == 1])} amostras ({len(df[df['anomaly'] == 1])/len(df):.1%})")
    
    print(f"\n📊 Distribuição por modo:")
    print(f"   • Normal (0): {len(df[df['mode'] == 0])} amostras ({len(df[df['mode'] == 0])/len(df):.1%})")
    print(f"   • Alerta (1): {len(df[df['mode'] == 1])} amostras ({len(df[df['mode'] == 1])/len(df):.1%})")
    print(f"   • Falha (2): {len(df[df['mode'] == 2])} amostras ({len(df[df['mode'] == 2])/len(df):.1%})")
    
    # Salvar CSV se solicitado
    if salvar_csv:
        nome_arquivo = f"dataset_iot_ml_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        df.to_csv(nome_arquivo, index=False)
        print(f"\n💾 Dataset salvo como: {nome_arquivo}")
        
        # Salvar também versão simplificada para ML
        features_ml = [
            'timestamp', 'temperature', 'humidity', 'pressure', 'vibration_mag',
            'level', 'luminosity', 'movement', 'temp_humidity_ratio',
            'pressure_vibration', 'level_luminosity', 'anomaly'
        ]
        
        df_ml = df[features_ml].copy()
        nome_arquivo_ml = f"dataset_iot_ml_features_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        df_ml.to_csv(nome_arquivo_ml, index=False)
        print(f"💾 Dataset para ML salvo como: {nome_arquivo_ml}")
        
        return df, nome_arquivo, nome_arquivo_ml
    
    return df

def analisar_dataset(df):
    """
    Análise detalhada do dataset gerado
    """
    print("\n🔍 ANÁLISE DETALHADA DO DATASET")
    print("=" * 50)
    
    print("📊 Informações básicas:")
    print(f"   • Shape: {df.shape}")
    print(f"   • Memória utilizada: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
    print(f"   • Tipos de dados:")
    print(df.dtypes.value_counts())
    
    print(f"\n📈 Estatísticas descritivas das features numéricas:")
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    print(df[numeric_cols].describe().round(2))
    
    print(f"\n📊 Distribuição por dispositivo:")
    print(df['device_id'].value_counts())
    
    print(f"\n📊 Distribuição por localização:")
    print(df['location'].value_counts())
    
    print(f"\n📊 Distribuição por qualidade dos dados:")
    print(df['data_quality'].value_counts())
    
    print(f"\n📊 Distribuição por status do dispositivo:")
    print(df['device_status'].value_counts())
    
    # Análise temporal
    print(f"\n📅 Análise temporal:")
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    print(f"   • Período: {df['timestamp'].min()} a {df['timestamp'].max()}")
    print(f"   • Duração: {df['timestamp'].max() - df['timestamp'].min()}")
    print(f"   • Frequência média: {len(df) / ((df['timestamp'].max() - df['timestamp'].min()).total_seconds() / 3600):.1f} amostras/hora")
    
    return df

def criar_amostras_pequenas():
    """
    Cria amostras menores para demonstração
    """
    print("\n📦 CRIANDO AMOSTRAS PEQUENAS PARA DEMONSTRAÇÃO")
    print("=" * 50)
    
    # Dataset pequeno (100 amostras)
    df_small = gerar_dataset_completo(100, salvar_csv=False)
    df_small.to_csv('dataset_iot_pequeno.csv', index=False)
    print("💾 Dataset pequeno salvo como: dataset_iot_pequeno.csv")
    
    # Dataset médio (1000 amostras)
    df_medium = gerar_dataset_completo(1000, salvar_csv=False)
    df_medium.to_csv('dataset_iot_medio.csv', index=False)
    print("💾 Dataset médio salvo como: dataset_iot_medio.csv")
    
    return df_small, df_medium

def demonstrar_uso_dataset():
    """
    Demonstra como usar o dataset CSV no treinamento
    """
    print("\n🚀 DEMONSTRAÇÃO DE USO DO DATASET CSV")
    print("=" * 50)
    
    # Carregar dataset
    try:
        df = pd.read_csv('dataset_iot_ml_features_20250111_120000.csv')
        print("✅ Dataset carregado com sucesso!")
        print(f"   • Shape: {df.shape}")
        print(f"   • Colunas: {list(df.columns)}")
        
        # Preparar dados para ML
        feature_columns = [
            'temperature', 'humidity', 'pressure', 'vibration_mag',
            'level', 'luminosity', 'movement', 'temp_humidity_ratio',
            'pressure_vibration', 'level_luminosity'
        ]
        
        X = df[feature_columns]
        y = df['anomaly']
        
        print(f"\n📊 Dados preparados para ML:")
        print(f"   • Features: {X.shape[1]}")
        print(f"   • Amostras: {X.shape[0]}")
        print(f"   • Distribuição do target: {y.value_counts().to_dict()}")
        
        # Estatísticas básicas
        print(f"\n📈 Estatísticas das features:")
        print(X.describe().round(2))
        
        return True
        
    except FileNotFoundError:
        print("❌ Arquivo CSV não encontrado. Execute primeiro a geração do dataset.")
        return False

def main():
    """
    Função principal
    """
    print("🚀 GERADOR DE DATASET CSV PARA ML - SISTEMA IoT")
    print("=" * 60)
    
    # Gerar dataset completo
    df, arquivo_completo, arquivo_ml = gerar_dataset_completo(5000, salvar_csv=True)
    
    # Analisar dataset
    df = analisar_dataset(df)
    
    # Criar amostras pequenas
    df_small, df_medium = criar_amostras_pequenas()
    
    # Demonstrar uso
    demonstrar_uso_dataset()
    
    print("\n" + "=" * 60)
    print("🎯 RESUMO FINAL")
    print("=" * 60)
    print("✅ Datasets gerados com sucesso!")
    print(f"📁 Arquivos CSV criados:")
    print(f"   • {arquivo_completo} - Dataset completo (5000 amostras)")
    print(f"   • {arquivo_ml} - Dataset para ML (features selecionadas)")
    print(f"   • dataset_iot_pequeno.csv - Amostra pequena (100 amostras)")
    print(f"   • dataset_iot_medio.csv - Amostra média (1000 amostras)")
    
    print(f"\n📊 Características dos datasets:")
    print(f"   • Baseado em dados reais do projeto ESP32")
    print(f"   • Features: temperatura, umidade, pressão, vibração, nível, luminosidade")
    print(f"   • Features derivadas: correlações e relações entre variáveis")
    print(f"   • Distribuição realista: 70% Normal, 20% Alerta, 10% Falha")
    print(f"   • Timestamps reais para análise temporal")
    print(f"   • Múltiplos dispositivos e localizações")
    
    print(f"\n🚀 Pronto para uso em treinamento de modelos ML!")
    
    return df

if __name__ == "__main__":
    df = main()
