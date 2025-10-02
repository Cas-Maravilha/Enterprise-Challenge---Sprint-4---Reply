#!/usr/bin/env python3
"""
Script para gerar dataset CSV para treino/teste do modelo ML
Sistema de Detecção de Anomalias IoT
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

def gerar_dados_sinteticos_detalhados(n_samples=5000, random_state=42):
    """
    Gera dados sintéticos detalhados baseados em parâmetros reais de sensores IoT
    """
    print("🔄 Gerando dataset sintético detalhado...")
    
    np.random.seed(random_state)
    data = []
    
    # Simular diferentes dispositivos e localizações
    dispositivos = [
        {'id': 'ESP32-Sala-01', 'localizacao': 'Sala de Controle Principal'},
        {'id': 'ESP32-Garagem-01', 'localizacao': 'Garagem - Portão Principal'},
        {'id': 'ESP32-Cozinha-01', 'localizacao': 'Cozinha - Monitoramento'},
        {'id': 'ESP32-Quarto-01', 'localizacao': 'Quarto Principal'},
        {'id': 'ESP32-Lavanderia-01', 'localizacao': 'Lavanderia'},
        {'id': 'ESP32-Externo-01', 'localizacao': 'Área Externa'}
    ]
    
    # Simular diferentes períodos do dia
    periodos_dia = ['madrugada', 'manha', 'tarde', 'noite']
    periodos_pesos = [0.1, 0.3, 0.4, 0.2]
    
    # Simular diferentes dias da semana
    dias_semana = ['segunda', 'terca', 'quarta', 'quinta', 'sexta', 'sabado', 'domingo']
    dias_pesos = [0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.10]
    
    # Data base para simulação
    data_base = datetime(2025, 1, 1, 0, 0, 0)
    
    for i in range(n_samples):
        # Selecionar dispositivo e período
        dispositivo = np.random.choice(dispositivos)
        periodo = np.random.choice(periodos_dia, p=periodos_pesos)
        dia_semana = np.random.choice(dias_semana, p=dias_pesos)
        
        # Simular timestamp
        dias_offset = np.random.randint(0, 30)  # Últimos 30 dias
        horas_offset = np.random.randint(0, 24)
        minutos_offset = np.random.randint(0, 60)
        segundos_offset = np.random.randint(0, 60)
        
        timestamp = data_base + timedelta(
            days=dias_offset, 
            hours=horas_offset, 
            minutes=minutos_offset, 
            seconds=segundos_offset
        )
        
        # Simular diferentes modos de operação
        mode = np.random.choice([0, 1, 2], p=[0.7, 0.2, 0.1])  # Normal, Alerta, Falha
        
        # Ajustar parâmetros baseado no período do dia
        if periodo == 'madrugada':
            temp_base = 20.0
            umidade_base = 70.0
            luminosidade_base = 50.0
        elif periodo == 'manha':
            temp_base = 22.0
            umidade_base = 60.0
            luminosidade_base = 400.0
        elif periodo == 'tarde':
            temp_base = 28.0
            umidade_base = 50.0
            luminosidade_base = 800.0
        else:  # noite
            temp_base = 24.0
            umidade_base = 65.0
            luminosidade_base = 200.0
        
        # Ajustar baseado no dia da semana
        if dia_semana in ['sabado', 'domingo']:
            movimento_prob = 0.3  # Menos movimento nos fins de semana
        else:
            movimento_prob = 0.1
        
        if mode == 0:  # Normal
            temperature = np.random.normal(temp_base, 2.0)
            humidity = np.random.normal(umidade_base, 5.0)
            pressure = np.random.normal(1.013, 0.01)
            vibration_x = np.random.normal(0.0, 0.1)
            vibration_y = np.random.normal(0.0, 0.1)
            vibration_z = np.random.normal(0.0, 0.1)
            level = np.random.normal(100.0, 10.0)
            luminosity = np.random.normal(luminosidade_base, 100.0)
            movement = np.random.choice([0, 1], p=[1-movimento_prob, movimento_prob])
            co2 = np.random.normal(400.0, 50.0)
            noise = np.random.normal(45.0, 5.0)
            
        elif mode == 1:  # Alerta
            temperature = np.random.normal(temp_base + 3.0, 3.0)
            humidity = np.random.normal(umidade_base + 10.0, 8.0)
            pressure = np.random.normal(1.020, 0.02)
            vibration_x = np.random.normal(0.3, 0.2)
            vibration_y = np.random.normal(0.2, 0.15)
            vibration_z = np.random.normal(0.1, 0.1)
            level = np.random.normal(120.0, 15.0)
            luminosity = np.random.normal(luminosidade_base + 200.0, 150.0)
            movement = np.random.choice([0, 1], p=[0.7, 0.3])
            co2 = np.random.normal(800.0, 100.0)
            noise = np.random.normal(55.0, 8.0)
            
        else:  # Falha
            temperature = np.random.normal(temp_base + 10.0, 5.0)
            humidity = np.random.normal(umidade_base + 20.0, 10.0)
            pressure = np.random.normal(1.030, 0.05)
            vibration_x = np.random.normal(1.0, 0.5)
            vibration_y = np.random.normal(0.8, 0.4)
            vibration_z = np.random.normal(0.6, 0.3)
            level = np.random.normal(150.0, 25.0)
            luminosity = np.random.normal(luminosidade_base + 400.0, 200.0)
            movement = np.random.choice([0, 1], p=[0.5, 0.5])
            co2 = np.random.normal(1500.0, 300.0)
            noise = np.random.normal(75.0, 15.0)
        
        # Adicionar anomalias ocasionais (5% de chance)
        if np.random.random() < 0.05:
            temperature += np.random.normal(0, 10)
            humidity += np.random.normal(0, 20)
            pressure += np.random.normal(0, 0.1)
            vibration_x += np.random.normal(0, 0.5)
            vibration_y += np.random.normal(0, 0.5)
            vibration_z += np.random.normal(0, 0.5)
            level += np.random.normal(0, 30)
            luminosity += np.random.normal(0, 300)
            co2 += np.random.normal(0, 500)
            noise += np.random.normal(0, 20)
            mode = 2  # Marcar como falha
        
        # Calcular magnitude da vibração
        vibration_mag = np.sqrt(vibration_x**2 + vibration_y**2 + vibration_z**2)
        
        # Features derivadas
        temp_humidity_ratio = temperature / (humidity + 1)
        pressure_vibration = pressure * vibration_mag
        level_luminosity = level * luminosity / 1000
        temp_pressure_ratio = temperature / (pressure + 0.1)
        humidity_level_ratio = humidity / (level + 1)
        co2_noise_ratio = co2 / (noise + 1)
        
        # Calcular qualidade dos dados baseada na variabilidade
        variabilidade = np.std([temperature, humidity, pressure, vibration_mag, level, luminosity])
        if variabilidade < 5:
            qualidade_dados = 'excelente'
        elif variabilidade < 15:
            qualidade_dados = 'bom'
        elif variabilidade < 30:
            qualidade_dados = 'regular'
        else:
            qualidade_dados = 'ruim'
        
        data.append({
            'timestamp': timestamp.isoformat(),
            'device_id': dispositivo['id'],
            'localizacao': dispositivo['localizacao'],
            'periodo_dia': periodo,
            'dia_semana': dia_semana,
            'temperature': max(-40, min(80, round(temperature, 2))),
            'humidity': max(0, min(100, round(humidity, 2))),
            'pressure': max(0, min(2, round(pressure, 3))),
            'vibration_x': round(vibration_x, 3),
            'vibration_y': round(vibration_y, 3),
            'vibration_z': round(vibration_z, 3),
            'vibration_mag': round(vibration_mag, 3),
            'level': max(0, min(200, round(level, 1))),
            'luminosity': max(0, min(1023, round(luminosity, 0))),
            'movement': int(movement),
            'co2': max(0, min(5000, round(co2, 0))),
            'noise': max(30, min(120, round(noise, 1))),
            'temp_humidity_ratio': round(temp_humidity_ratio, 4),
            'pressure_vibration': round(pressure_vibration, 4),
            'level_luminosity': round(level_luminosity, 2),
            'temp_pressure_ratio': round(temp_pressure_ratio, 2),
            'humidity_level_ratio': round(humidity_level_ratio, 4),
            'co2_noise_ratio': round(co2_noise_ratio, 2),
            'qualidade_dados': qualidade_dados,
            'anomaly': 1 if mode == 2 else 0,
            'mode': mode,
            'mode_label': ['Normal', 'Alerta', 'Falha'][mode]
        })
    
    df = pd.DataFrame(data)
    print(f"✅ Dataset sintético gerado: {len(df)} amostras")
    print(f"   • Normal: {len(df[df['anomaly'] == 0])} amostras")
    print(f"   • Anomalia: {len(df[df['anomaly'] == 1])} amostras")
    print(f"   • Dispositivos: {df['device_id'].nunique()}")
    print(f"   • Períodos: {df['periodo_dia'].nunique()}")
    
    return df

def salvar_datasets(df, base_filename='iot_sensor_data'):
    """
    Salva os datasets em diferentes formatos e divisões
    """
    print("💾 Salvando datasets...")
    
    # Criar diretório para datasets
    os.makedirs('datasets', exist_ok=True)
    
    # 1. Dataset completo
    df.to_csv(f'datasets/{base_filename}_completo.csv', index=False)
    print(f"   ✅ Dataset completo: datasets/{base_filename}_completo.csv")
    
    # 2. Dividir em treino e teste
    from sklearn.model_selection import train_test_split
    
    # Preparar dados para divisão
    feature_columns = [
        'temperature', 'humidity', 'pressure', 'vibration_mag',
        'level', 'luminosity', 'movement', 'co2', 'noise',
        'temp_humidity_ratio', 'pressure_vibration', 'level_luminosity',
        'temp_pressure_ratio', 'humidity_level_ratio', 'co2_noise_ratio'
    ]
    
    X = df[feature_columns]
    y = df['anomaly']
    
    # Divisão estratificada
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Adicionar colunas de contexto para treino
    train_indices = X_train.index
    test_indices = X_test.index
    
    df_train = df.loc[train_indices].copy()
    df_test = df.loc[test_indices].copy()
    
    # Salvar datasets de treino e teste
    df_train.to_csv(f'datasets/{base_filename}_treino.csv', index=False)
    df_test.to_csv(f'datasets/{base_filename}_teste.csv', index=False)
    
    print(f"   ✅ Dataset treino: datasets/{base_filename}_treino.csv ({len(df_train)} amostras)")
    print(f"   ✅ Dataset teste: datasets/{base_filename}_teste.csv ({len(df_test)} amostras)")
    
    # 3. Dataset apenas com features numéricas para ML
    features_ml = feature_columns + ['anomaly', 'mode']
    df_ml = df[features_ml].copy()
    df_ml.to_csv(f'datasets/{base_filename}_ml.csv', index=False)
    print(f"   ✅ Dataset ML: datasets/{base_filename}_ml.csv")
    
    # 4. Dataset por dispositivo
    for device in df['device_id'].unique():
        df_device = df[df['device_id'] == device].copy()
        device_name = device.replace('ESP32-', '').replace('-', '_').lower()
        df_device.to_csv(f'datasets/{base_filename}_{device_name}.csv', index=False)
        print(f"   ✅ Dataset {device}: datasets/{base_filename}_{device_name}.csv")
    
    # 5. Dataset por modo de operação
    for mode in df['mode'].unique():
        df_mode = df[df['mode'] == mode].copy()
        mode_name = ['normal', 'alerta', 'falha'][mode]
        df_mode.to_csv(f'datasets/{base_filename}_{mode_name}.csv', index=False)
        print(f"   ✅ Dataset {mode_name}: datasets/{base_filename}_{mode_name}.csv")
    
    # 6. Dataset de anomalias apenas
    df_anomalias = df[df['anomaly'] == 1].copy()
    df_anomalias.to_csv(f'datasets/{base_filename}_anomalias.csv', index=False)
    print(f"   ✅ Dataset anomalias: datasets/{base_filename}_anomalias.csv")
    
    # 7. Dataset de dados normais apenas
    df_normais = df[df['anomaly'] == 0].copy()
    df_normais.to_csv(f'datasets/{base_filename}_normais.csv', index=False)
    print(f"   ✅ Dataset normais: datasets/{base_filename}_normais.csv")
    
    return df_train, df_test

def gerar_relatorio_dataset(df):
    """
    Gera relatório detalhado do dataset
    """
    print("📊 Gerando relatório do dataset...")
    
    relatorio = f"""
# RELATÓRIO DO DATASET - SISTEMA IoT MONITORING
## Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}

## 📊 INFORMAÇÕES GERAIS
- **Total de amostras**: {len(df):,}
- **Período**: {df['timestamp'].min()} a {df['timestamp'].max()}
- **Dispositivos**: {df['device_id'].nunique()}
- **Localizações**: {df['localizacao'].nunique()}

## 🔍 DISTRIBUIÇÃO DAS CLASSES
- **Normal**: {len(df[df['anomaly'] == 0]):,} amostras ({len(df[df['anomaly'] == 0])/len(df):.1%})
- **Anomalia**: {len(df[df['anomaly'] == 1]):,} amostras ({len(df[df['anomaly'] == 1])/len(df):.1%})

## 📱 DISPOSITIVOS
"""
    
    for device in df['device_id'].unique():
        count = len(df[df['device_id'] == device])
        relatorio += f"- **{device}**: {count:,} amostras ({count/len(df):.1%})\n"
    
    relatorio += f"""
## 🏠 LOCALIZAÇÕES
"""
    
    for loc in df['localizacao'].unique():
        count = len(df[df['localizacao'] == loc])
        relatorio += f"- **{loc}**: {count:,} amostras ({count/len(df):.1%})\n"
    
    relatorio += f"""
## ⏰ PERÍODOS DO DIA
"""
    
    for periodo in df['periodo_dia'].unique():
        count = len(df[df['periodo_dia'] == periodo])
        relatorio += f"- **{periodo}**: {count:,} amostras ({count/len(df):.1%})\n"
    
    relatorio += f"""
## 📅 DIAS DA SEMANA
"""
    
    for dia in df['dia_semana'].unique():
        count = len(df[df['dia_semana'] == dia])
        relatorio += f"- **{dia}**: {count:,} amostras ({count/len(df):.1%})\n"
    
    relatorio += f"""
## 📈 ESTATÍSTICAS DAS FEATURES PRINCIPAIS
"""
    
    features_principais = ['temperature', 'humidity', 'pressure', 'vibration_mag', 'level', 'luminosity', 'co2', 'noise']
    
    for feature in features_principais:
        stats = df[feature].describe()
        relatorio += f"""
### {feature.upper()}
- **Média**: {stats['mean']:.2f}
- **Mediana**: {stats['50%']:.2f}
- **Desvio Padrão**: {stats['std']:.2f}
- **Mínimo**: {stats['min']:.2f}
- **Máximo**: {stats['max']:.2f}
"""
    
    relatorio += f"""
## 🎯 QUALIDADE DOS DADOS
"""
    
    for qualidade in df['qualidade_dados'].unique():
        count = len(df[df['qualidade_dados'] == qualidade])
        relatorio += f"- **{qualidade}**: {count:,} amostras ({count/len(df):.1%})\n"
    
    relatorio += f"""
## 📁 ARQUIVOS GERADOS
- `datasets/iot_sensor_data_completo.csv` - Dataset completo
- `datasets/iot_sensor_data_treino.csv` - Dataset de treino
- `datasets/iot_sensor_data_teste.csv` - Dataset de teste
- `datasets/iot_sensor_data_ml.csv` - Dataset para ML (apenas features numéricas)
- `datasets/iot_sensor_data_anomalias.csv` - Apenas anomalias
- `datasets/iot_sensor_data_normais.csv` - Apenas dados normais
- `datasets/iot_sensor_data_*.csv` - Datasets por dispositivo e modo

## 🔧 COMO USAR
```python
import pandas as pd

# Carregar dataset completo
df = pd.read_csv('datasets/iot_sensor_data_completo.csv')

# Carregar dataset de treino
df_train = pd.read_csv('datasets/iot_sensor_data_treino.csv')

# Carregar dataset de teste
df_test = pd.read_csv('datasets/iot_sensor_data_teste.csv')
```

## 📊 PRÓXIMOS PASSOS
1. Usar os datasets para treinar modelos de ML
2. Implementar validação cruzada
3. Testar diferentes algoritmos
4. Implementar monitoramento em tempo real
"""
    
    # Salvar relatório
    with open('datasets/relatorio_dataset.md', 'w', encoding='utf-8') as f:
        f.write(relatorio)
    
    print("   ✅ Relatório salvo: datasets/relatorio_dataset.md")

def main():
    """
    Função principal para gerar os datasets
    """
    print("🚀 GERADOR DE DATASETS - SISTEMA IoT MONITORING")
    print("=" * 60)
    
    # Gerar dados sintéticos
    df = gerar_dados_sinteticos_detalhados(n_samples=5000)
    
    # Salvar datasets
    df_train, df_test = salvar_datasets(df)
    
    # Gerar relatório
    gerar_relatorio_dataset(df)
    
    print(f"\n✅ DATASETS GERADOS COM SUCESSO!")
    print("=" * 60)
    print("📁 Arquivos criados na pasta 'datasets/':")
    print("   • Dataset completo com 5.000 amostras")
    print("   • Datasets de treino e teste (80/20)")
    print("   • Datasets por dispositivo e modo")
    print("   • Datasets de anomalias e normais")
    print("   • Relatório detalhado")
    
    print(f"\n🎯 PRÓXIMOS PASSOS:")
    print("   1. Usar os datasets para treinar modelos ML")
    print("   2. Implementar validação cruzada")
    print("   3. Testar diferentes algoritmos")
    print("   4. Implementar monitoramento em tempo real")
    
    return df, df_train, df_test

if __name__ == "__main__":
    df, df_train, df_test = main()
