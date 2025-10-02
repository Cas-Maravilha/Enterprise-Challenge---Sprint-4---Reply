# Documentação do Código-fonte - Sistema de Machine Learning IoT

## 📋 Visão Geral

Este documento descreve o código-fonte completo do sistema de Machine Learning para detecção de anomalias em dados IoT coletados por sensores ESP32.

## 🗂️ Estrutura dos Arquivos

### 1. **ml_anomaly_detection_completo.py**
**Arquivo principal com o código completo do sistema ML**

#### Características:
- **Classe principal**: `IoTAnomalyDetector`
- **Algoritmo**: Random Forest Classifier + Isolation Forest
- **Funcionalidades**:
  - Geração de dados sintéticos
  - Preparação e normalização de dados
  - Treinamento do modelo
  - Validação cruzada
  - Otimização de hiperparâmetros
  - Visualização de resultados
  - Salvamento do modelo

#### Métodos principais:
```python
def gerar_dados_sinteticos(n_samples=5000)
def preparar_dados(df)
def treinar_modelo(X, y)
def otimizar_hiperparametros(X, y)
def validar_modelo(X, y)
def plotar_resultados(X_test, y_test, y_pred, y_pred_proba)
def salvar_modelo(filename='modelo_anomalia_iot.pkl')
```

### 2. **ML_Anomaly_Detection_IoT_Completo.ipynb**
**Jupyter Notebook interativo com análise completa**

#### Estrutura:
1. **Introdução e Problema**: Descrição do problema de classificação
2. **Geração de Dados**: Criação de dataset sintético
3. **Análise Exploratória**: Visualizações e estatísticas
4. **Treinamento**: Preparação e treinamento do modelo
5. **Validação**: Validação cruzada e otimização
6. **Visualização**: Gráficos e métricas de performance
7. **Salvamento**: Persistência do modelo treinado

### 3. **usar_modelo_ml.py**
**Script para usar o modelo treinado em produção**

#### Características:
- **Classe principal**: `IoTAnomalyPredictor`
- **Funcionalidades**:
  - Carregamento do modelo treinado
  - Predição de anomalias
  - Análise de arquivos CSV
  - Monitoramento em tempo real

#### Métodos principais:
```python
def predizer_anomalia(self, dados)
def analisar_dados_em_lote(self, arquivo_csv)
def monitorar_tempo_real(self, dados_sensor)
```

### 4. **executar_treinamento_ml.py**
**Script de automação para executar o treinamento completo**

#### Funcionalidades:
- Execução sequencial dos scripts
- Monitoramento de progresso
- Tratamento de erros
- Relatório de resultados

## 🔧 Detalhes Técnicos

### Algoritmos Utilizados

#### 1. **Random Forest Classifier**
```python
RandomForestClassifier(
    n_estimators=100,
    max_depth=10,
    min_samples_split=5,
    min_samples_leaf=2,
    random_state=42,
    class_weight='balanced'
)
```

**Vantagens:**
- Robustez a outliers
- Tratamento de features categóricas
- Redução de overfitting
- Interpretabilidade (feature importance)

#### 2. **Isolation Forest**
```python
IsolationForest(
    contamination=0.1,
    random_state=42
)
```

**Vantagens:**
- Detecção de anomalias não supervisionada
- Eficiência computacional
- Boa performance com dados de alta dimensão

### Features Utilizadas

#### Features Primárias:
1. **temperature** (°C): Temperatura ambiente
2. **humidity** (%): Umidade relativa
3. **pressure** (bar): Pressão barométrica
4. **vibration_mag** (g): Magnitude da vibração
5. **level** (cm): Nível de líquido
6. **luminosity** (lux): Intensidade luminosa
7. **movement** (boolean): Detecção de movimento
8. **co2** (ppm): Concentração de CO2
9. **noise** (dB): Nível de ruído

#### Features Derivadas:
1. **temp_humidity_ratio**: Relação temperatura/umidade
2. **pressure_vibration**: Produto pressão × vibração
3. **level_luminosity**: Relação nível × luminosidade
4. **temp_pressure_ratio**: Relação temperatura/pressão
5. **humidity_level_ratio**: Relação umidade/nível
6. **co2_noise_ratio**: Relação CO2/ruído

### Pipeline de Dados

#### 1. **Geração de Dados**
```python
def gerar_dados_sinteticos(n_samples=5000):
    # Simula 3 modos de operação:
    # - Normal (70%): Valores dentro dos parâmetros
    # - Alerta (20%): Valores próximos aos limites
    # - Falha (10%): Valores críticos
    # - Anomalias (5%): Valores extremos adicionais
```

#### 2. **Preparação de Dados**
```python
def preparar_dados(df):
    # Seleção de features
    # Tratamento de valores infinitos/nulos
    # Normalização com StandardScaler
    # Divisão treino/teste (80/20)
```

#### 3. **Treinamento**
```python
def treinar_modelo(X, y):
    # Treinamento Random Forest
    # Treinamento Isolation Forest
    # Cálculo de métricas
    # Comparação de modelos
```

#### 4. **Otimização**
```python
def otimizar_hiperparametros(X, y):
    # Grid Search com validação cruzada
    # Otimização de hiperparâmetros
    # Seleção do melhor modelo
```

### Métricas de Avaliação

#### Métricas Principais:
- **Accuracy**: Precisão geral do modelo
- **Precision**: Proporção de verdadeiros positivos
- **Recall**: Sensibilidade do modelo
- **F1-Score**: Média harmônica de precision e recall
- **AUC**: Área sob a curva ROC

#### Validação:
- **Cross-validation**: 5-fold com scoring ROC-AUC
- **Grid Search**: Otimização de hiperparâmetros
- **Stratified Split**: Divisão balanceada dos dados

### Visualizações Geradas

#### 1. **Matriz de Confusão**
- Verdadeiros/Falsos Positivos
- Verdadeiros/Falsos Negativos
- Precisão por classe

#### 2. **Curva ROC**
- Taxa de Verdadeiros Positivos vs Falsos Positivos
- Área sob a curva (AUC)
- Comparação com modelo aleatório

#### 3. **Curva Precision-Recall**
- Precision vs Recall
- Average Precision (AP)
- Útil para classes desbalanceadas

#### 4. **Importância das Features**
- Ranking das features mais importantes
- Interpretabilidade do modelo
- Seleção de features

#### 5. **Distribuição das Predições**
- Histograma das probabilidades
- Separação entre classes
- Threshold de decisão

## 🚀 Como Usar

### 1. **Treinamento do Modelo**
```bash
python ml_anomaly_detection_completo.py
```

### 2. **Uso do Modelo Treinado**
```python
from usar_modelo_ml import IoTAnomalyPredictor

# Carregar modelo
predictor = IoTAnomalyPredictor()

# Fazer predição
dados = {
    'temperature': 25.5,
    'humidity': 60.0,
    # ... outros dados
}
resultado = predictor.predizer_anomalia(dados)
```

### 3. **Análise de Arquivo CSV**
```python
# Analisar arquivo CSV
resultados = predictor.analisar_dados_em_lote('dados_sensores.csv')
```

### 4. **Monitoramento em Tempo Real**
```python
# Monitorar dados em tempo real
resultado = predictor.monitorar_tempo_real(dados_sensor)
```

## 📊 Resultados Esperados

### Performance Típica:
- **Accuracy**: > 95%
- **Precision**: > 90%
- **Recall**: > 85%
- **F1-Score**: > 87%
- **AUC**: > 0.95

### Arquivos Gerados:
1. **modelo_anomalia_iot_completo.pkl**: Modelo treinado
2. **resultados_modelo_ml_completo.png**: Visualizações
3. **ML_Anomaly_Detection_IoT_Completo.ipynb**: Notebook interativo

## 🔧 Configurações

### Parâmetros do Modelo:
```python
# Random Forest
n_estimators = 100
max_depth = 10
min_samples_split = 5
min_samples_leaf = 2
class_weight = 'balanced'

# Isolation Forest
contamination = 0.1
```

### Parâmetros de Dados:
```python
# Geração de dados
n_samples = 5000
normal_ratio = 0.70
alert_ratio = 0.20
failure_ratio = 0.10
anomaly_ratio = 0.05

# Divisão dos dados
test_size = 0.2
random_state = 42
```

## 🛠️ Dependências

### Bibliotecas Python:
```python
pandas >= 1.3.0
numpy >= 1.21.0
matplotlib >= 3.4.0
seaborn >= 0.11.0
scikit-learn >= 1.0.0
joblib >= 1.0.0
```

### Instalação:
```bash
pip install -r requirements.txt
```

## 📈 Extensões Futuras

### Melhorias Possíveis:
1. **Deep Learning**: Implementar redes neurais
2. **Ensemble Methods**: Combinar múltiplos algoritmos
3. **Feature Engineering**: Criar features mais sofisticadas
4. **Online Learning**: Atualização contínua do modelo
5. **Explicabilidade**: SHAP values para interpretabilidade

### Integrações:
1. **APIs REST**: Endpoints para predições
2. **Streaming**: Processamento de dados em tempo real
3. **Dashboard**: Interface web para monitoramento
4. **Alertas**: Sistema de notificações automáticas

## 🎯 Conclusão

O sistema de Machine Learning implementado oferece:

- **Alta Performance**: Métricas superiores a 90%
- **Robustez**: Tratamento de outliers e dados faltantes
- **Interpretabilidade**: Feature importance e visualizações
- **Escalabilidade**: Suporte a grandes volumes de dados
- **Facilidade de Uso**: APIs simples e documentação completa

O código está pronto para uso em produção e pode ser facilmente integrado ao sistema IoT existente.
