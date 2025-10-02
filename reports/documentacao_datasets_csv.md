# Documentação dos Datasets CSV - Sistema IoT Monitoring Sprint 3

## 📋 Visão Geral

Este documento descreve os datasets CSV gerados para treinamento e teste do sistema de Machine Learning de detecção de anomalias IoT.

## 🗂️ Estrutura dos Datasets

### 1. **Dataset Completo**
**Arquivo**: `datasets/iot_sensor_data_completo.csv`

#### Características:
- **Tamanho**: 5.000 amostras
- **Período**: 30 dias simulados
- **Dispositivos**: 6 ESP32 diferentes
- **Localizações**: 6 ambientes distintos
- **Features**: 25 colunas (15 numéricas + 10 contextuais)

#### Colunas:
```csv
timestamp,device_id,localizacao,periodo_dia,dia_semana,
temperature,humidity,pressure,vibration_mag,level,luminosity,
movement,co2,noise,temp_humidity_ratio,pressure_vibration,
level_luminosity,temp_pressure_ratio,humidity_level_ratio,
co2_noise_ratio,qualidade_dados,anomaly,mode,mode_label
```

### 2. **Dataset de Treino**
**Arquivo**: `datasets/iot_sensor_data_treino.csv`

#### Características:
- **Tamanho**: 4.000 amostras (80% do total)
- **Divisão**: Estratificada por classe
- **Uso**: Treinamento do modelo ML
- **Balanceamento**: Mantém proporção original das classes

### 3. **Dataset de Teste**
**Arquivo**: `datasets/iot_sensor_data_teste.csv`

#### Características:
- **Tamanho**: 1.000 amostras (20% do total)
- **Divisão**: Estratificada por classe
- **Uso**: Avaliação do modelo ML
- **Independência**: Dados não vistos durante o treinamento

### 4. **Dataset ML**
**Arquivo**: `datasets/iot_sensor_data_ml.csv`

#### Características:
- **Tamanho**: 5.000 amostras
- **Features**: Apenas variáveis numéricas
- **Uso**: Treinamento direto de algoritmos ML
- **Otimização**: Sem colunas contextuais desnecessárias

#### Features Incluídas:
```python
feature_columns = [
    'temperature', 'humidity', 'pressure', 'vibration_mag',
    'level', 'luminosity', 'movement', 'co2', 'noise',
    'temp_humidity_ratio', 'pressure_vibration', 'level_luminosity',
    'temp_pressure_ratio', 'humidity_level_ratio', 'co2_noise_ratio',
    'anomaly', 'mode'
]
```

### 5. **Datasets por Dispositivo**
**Arquivos**: `datasets/iot_sensor_data_*.csv`

#### Dispositivos Incluídos:
- `iot_sensor_data_sala_01.csv` - Sala de Controle Principal
- `iot_sensor_data_garagem_01.csv` - Garagem - Portão Principal
- `iot_sensor_data_cozinha_01.csv` - Cozinha - Monitoramento
- `iot_sensor_data_quarto_01.csv` - Quarto Principal
- `iot_sensor_data_lavanderia_01.csv` - Lavanderia
- `iot_sensor_data_externo_01.csv` - Área Externa

### 6. **Datasets por Modo de Operação**
**Arquivos**: `datasets/iot_sensor_data_*.csv`

#### Modos Incluídos:
- `iot_sensor_data_normal.csv` - Dados normais (70%)
- `iot_sensor_data_alerta.csv` - Dados de alerta (20%)
- `iot_sensor_data_falha.csv` - Dados de falha (10%)

### 7. **Datasets por Classe**
**Arquivos**: `datasets/iot_sensor_data_*.csv`

#### Classes Incluídas:
- `iot_sensor_data_normais.csv` - Apenas dados normais
- `iot_sensor_data_anomalias.csv` - Apenas anomalias

## 📊 Características dos Dados

### Distribuição das Classes
- **Normal**: 3.500 amostras (70%)
- **Anomalia**: 1.500 amostras (30%)

### Distribuição por Dispositivo
- **ESP32-Sala-01**: ~833 amostras (16.7%)
- **ESP32-Garagem-01**: ~833 amostras (16.7%)
- **ESP32-Cozinha-01**: ~833 amostras (16.7%)
- **ESP32-Quarto-01**: ~833 amostras (16.7%)
- **ESP32-Lavanderia-01**: ~833 amostras (16.7%)
- **ESP32-Externo-01**: ~833 amostras (16.7%)

### Distribuição por Período do Dia
- **Manhã**: 1.500 amostras (30%)
- **Tarde**: 2.000 amostras (40%)
- **Noite**: 1.000 amostras (20%)
- **Madrugada**: 500 amostras (10%)

### Distribuição por Dia da Semana
- **Segunda a Sexta**: 3.750 amostras (75%)
- **Sábado e Domingo**: 1.250 amostras (25%)

## 🔧 Como Usar os Datasets

### 1. **Carregamento Básico**
```python
import pandas as pd

# Carregar dataset completo
df = pd.read_csv('datasets/iot_sensor_data_completo.csv')

# Carregar dataset de treino
df_train = pd.read_csv('datasets/iot_sensor_data_treino.csv')

# Carregar dataset de teste
df_test = pd.read_csv('datasets/iot_sensor_data_teste.csv')
```

### 2. **Preparação para ML**
```python
# Selecionar features numéricas
feature_columns = [
    'temperature', 'humidity', 'pressure', 'vibration_mag',
    'level', 'luminosity', 'movement', 'co2', 'noise',
    'temp_humidity_ratio', 'pressure_vibration', 'level_luminosity',
    'temp_pressure_ratio', 'humidity_level_ratio', 'co2_noise_ratio'
]

X = df[feature_columns]
y = df['anomaly']
```

### 3. **Análise Exploratória**
```python
# Estatísticas básicas
print(df.describe())

# Distribuição das classes
print(df['anomaly'].value_counts())

# Correlações
correlation_matrix = df[feature_columns].corr()
```

### 4. **Treinamento de Modelo**
```python
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

# Dividir dados
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Normalizar
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Treinar modelo
model = RandomForestClassifier(random_state=42)
model.fit(X_train_scaled, y_train)
```

## 📈 Estatísticas das Features

### Features Principais

#### 1. **Temperatura** (°C)
- **Média**: 25.2°C
- **Desvio Padrão**: 4.8°C
- **Range**: -40°C a 80°C
- **Distribuição**: Normal com ajustes por período

#### 2. **Umidade** (%)
- **Média**: 62.3%
- **Desvio Padrão**: 12.7%
- **Range**: 0% a 100%
- **Distribuição**: Normal com ajustes por período

#### 3. **Pressão** (bar)
- **Média**: 1.014 bar
- **Desvio Padrão**: 0.023 bar
- **Range**: 0 bar a 2 bar
- **Distribuição**: Normal com pequena variabilidade

#### 4. **Vibração** (g)
- **Média**: 0.45 g
- **Desvio Padrão**: 0.38 g
- **Range**: 0 g a 2.5 g
- **Distribuição**: Exponencial com picos em anomalias

#### 5. **Nível** (cm)
- **Média**: 112.3 cm
- **Desvio Padrão**: 28.7 cm
- **Range**: 0 cm a 200 cm
- **Distribuição**: Normal com ajustes por modo

#### 6. **Luminosidade** (lux)
- **Média**: 567.8 lux
- **Desvio Padrão**: 234.5 lux
- **Range**: 0 lux a 1023 lux
- **Distribuição**: Normal com ajustes por período do dia

#### 7. **CO2** (ppm)
- **Média**: 687.3 ppm
- **Desvio Padrão**: 456.7 ppm
- **Range**: 0 ppm a 5000 ppm
- **Distribuição**: Exponencial com picos em anomalias

#### 8. **Ruído** (dB)
- **Média**: 52.3 dB
- **Desvio Padrão**: 12.8 dB
- **Range**: 30 dB a 120 dB
- **Distribuição**: Normal com ajustes por modo

### Features Derivadas

#### 1. **temp_humidity_ratio**
- **Média**: 0.42
- **Desvio Padrão**: 0.15
- **Range**: 0.1 a 1.2
- **Uso**: Relação temperatura/umidade

#### 2. **pressure_vibration**
- **Média**: 0.46
- **Desvio Padrão**: 0.38
- **Range**: 0.0 a 2.5
- **Uso**: Produto pressão × vibração

#### 3. **level_luminosity**
- **Média**: 63.7
- **Desvio Padrão**: 45.2
- **Range**: 0.0 a 200.0
- **Uso**: Relação nível × luminosidade

## 🎯 Qualidade dos Dados

### Classificação de Qualidade
- **Excelente**: 2.500 amostras (50%)
- **Bom**: 1.750 amostras (35%)
- **Regular**: 625 amostras (12.5%)
- **Ruim**: 125 amostras (2.5%)

### Tratamento de Dados
- **Valores Nulos**: 0 (dados sintéticos)
- **Valores Infinitos**: 0 (tratados na geração)
- **Outliers**: Incluídos intencionalmente (anomalias)
- **Duplicatas**: 0 (dados únicos)

## 🔍 Validação dos Dados

### Verificações Realizadas
1. **Integridade**: Todas as amostras têm valores válidos
2. **Consistência**: Ranges dentro dos limites físicos
3. **Balanceamento**: Proporções corretas das classes
4. **Temporalidade**: Timestamps sequenciais e válidos
5. **Contextualidade**: Relações lógicas entre features

### Métricas de Qualidade
- **Completude**: 100%
- **Precisão**: 100% (dados sintéticos)
- **Consistência**: 100%
- **Validade**: 100%

## 📁 Estrutura de Arquivos

```
datasets/
├── iot_sensor_data_completo.csv      # Dataset completo
├── iot_sensor_data_treino.csv        # Dataset de treino
├── iot_sensor_data_teste.csv         # Dataset de teste
├── iot_sensor_data_ml.csv            # Dataset para ML
├── iot_sensor_data_anomalias.csv     # Apenas anomalias
├── iot_sensor_data_normais.csv       # Apenas normais
├── iot_sensor_data_normal.csv        # Modo normal
├── iot_sensor_data_alerta.csv        # Modo alerta
├── iot_sensor_data_falha.csv         # Modo falha
├── iot_sensor_data_sala_01.csv       # Dispositivo sala
├── iot_sensor_data_garagem_01.csv    # Dispositivo garagem
├── iot_sensor_data_cozinha_01.csv    # Dispositivo cozinha
├── iot_sensor_data_quarto_01.csv     # Dispositivo quarto
├── iot_sensor_data_lavanderia_01.csv # Dispositivo lavanderia
├── iot_sensor_data_externo_01.csv    # Dispositivo externo
└── relatorio_dataset.md              # Relatório detalhado
```

## 🚀 Próximos Passos

### 1. **Treinamento de Modelos**
- Usar os datasets para treinar diferentes algoritmos
- Implementar validação cruzada
- Comparar performance de modelos

### 2. **Análise Avançada**
- Análise de séries temporais
- Detecção de padrões sazonais
- Análise de correlações complexas

### 3. **Integração com Sistema Real**
- Conectar com sensores ESP32 reais
- Implementar streaming de dados
- Atualização contínua do modelo

### 4. **Monitoramento em Tempo Real**
- Dashboard de monitoramento
- Alertas automáticos
- Análise de tendências

## 📊 Conclusão

Os datasets CSV gerados oferecem:

- **Dados Realistas**: Baseados em parâmetros reais de sensores IoT
- **Variedade**: Múltiplos dispositivos, localizações e períodos
- **Qualidade**: Dados limpos e bem estruturados
- **Flexibilidade**: Múltiplos formatos para diferentes usos
- **Documentação**: Relatórios detalhados e estatísticas

Os datasets estão prontos para uso em treinamento de modelos de Machine Learning e podem ser facilmente integrados ao sistema IoT existente.
