# ML Básico Integrado - Sistema IoT Monitoring
## Enterprise Challenge Sprint 3 - Reply

## 🎯 Visão Geral

Este módulo implementa um **sistema completo de Machine Learning básico integrado** que opera sobre os dados do banco de dados, incluindo treino, inferência, métricas e visualizações pertinentes.

## 📋 Componentes do Sistema

### **1. ML Básico Integrado**
- **Arquivo**: `ml_basico_integrado.py`
- **Função**: Treino e inferência de modelos ML
- **Modelos**: Detecção de anomalias, Previsão de temperatura
- **Métricas**: Acurácia, MAE, R², Matriz de confusão

### **2. Analisador de Dataset**
- **Arquivo**: `dataset_ml_analisador.py`
- **Função**: Análise detalhada do dataset utilizado
- **Inclui**: Estrutura, distribuição, qualidade dos dados

### **3. Scripts de Execução**
- **Windows**: `executar_ml_basico.bat`
- **Linux/Mac**: `executar_ml_basico.sh`
- **Função**: Automação da execução

## 🤖 Modelos Implementados

### **1. Detecção de Anomalias**
- **Algoritmo**: Random Forest Classifier
- **Features**: valor atual, valor anterior, média móvel, desvio padrão, tendência
- **Target**: anomalia_detectada (0/1)
- **Métricas**: Acurácia, Matriz de confusão, Curva ROC

### **2. Previsão de Temperatura**
- **Algoritmo**: Random Forest Regressor
- **Features**: hora, dia da semana, dia do mês, valor anterior, média móvel
- **Target**: valor_numerico (temperatura)
- **Métricas**: MAE, RMSE, R², Análise de resíduos

## 📊 Dataset Utilizado

### **Fonte dos Dados**
- **Banco**: `iot_monitoring_db`
- **Tabela Principal**: `leituras_sensores`
- **Período**: Últimos 7 dias
- **Filtros**: Apenas sensores numéricos ativos

### **Estrutura do Dataset**
```sql
SELECT 
    l.id_leitura,
    l.id_sensor,
    l.timestamp_datetime,
    l.valor_numerico,
    l.valor_booleano,
    l.qualidade_dados,
    l.anomalia_detectada,
    s.nome as sensor_nome,
    s.id_tipo_sensor,
    d.nome as dispositivo_nome,
    d.localizacao,
    ts.nome as tipo_sensor_nome,
    ts.unidade_medida
FROM leituras_sensores l
JOIN sensores s ON l.id_sensor = s.id_sensor
JOIN dispositivos d ON s.id_dispositivo = d.id_dispositivo
JOIN tipos_sensor ts ON s.id_tipo_sensor = ts.id_tipo_sensor
WHERE l.timestamp_datetime >= DATE_SUB(NOW(), INTERVAL 7 DAY)
```

### **Características do Dataset**
- **Registros**: 50.000+ leituras
- **Sensores**: 70 sensores únicos
- **Dispositivos**: 7 dispositivos ESP32
- **Tipos**: DHT22, LDR, PIR, Pressão, Vibração, Nível
- **Período**: 7 dias de dados
- **Frequência**: 1 leitura por minuto

## 🔄 Passo a Passo da Execução

### **1. Conexão com Banco de Dados**
```python
# Conectar ao MySQL
connection = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    database=database
)
```

### **2. Carregamento de Dados**
```python
# Query para leituras com metadados
query_leituras = """
SELECT l.*, s.nome as sensor_nome, d.nome as dispositivo_nome, 
       ts.nome as tipo_sensor_nome
FROM leituras_sensores l
JOIN sensores s ON l.id_sensor = s.id_sensor
JOIN dispositivos d ON s.id_dispositivo = d.id_dispositivo
JOIN tipos_sensor ts ON s.id_tipo_sensor = ts.id_tipo_sensor
WHERE l.timestamp_datetime >= DATE_SUB(NOW(), INTERVAL 7 DAY)
"""
```

### **3. Preparação dos Dados**

#### **Para Detecção de Anomalias:**
```python
# Features: valor atual, valor anterior, média móvel, desvio padrão, tendência
df_sensor['valor_anterior'] = df_sensor['valor_numerico'].shift(1)
df_sensor['media_movel'] = df_sensor['valor_numerico'].rolling(window=5).mean()
df_sensor['std_movel'] = df_sensor['valor_numerico'].rolling(window=5).std()
df_sensor['tendencia'] = df_sensor['valor_numerico'].diff()
```

#### **Para Previsão de Temperatura:**
```python
# Features temporais
df_temp['hora'] = df_temp['timestamp_datetime'].dt.hour
df_temp['dia_semana'] = df_temp['timestamp_datetime'].dt.dayofweek
df_temp['dia_mes'] = df_temp['timestamp_datetime'].dt.day
df_temp['valor_anterior'] = df_temp.groupby('id_sensor')['valor_numerico'].shift(1)
df_temp['media_movel'] = df_temp.groupby('id_sensor')['valor_numerico'].rolling(window=3).mean()
```

### **4. Treinamento dos Modelos**

#### **Modelo de Anomalias:**
```python
# Random Forest Classifier
modelo_anomalia = RandomForestClassifier(
    n_estimators=100,
    max_depth=10,
    random_state=42,
    class_weight='balanced'
)
modelo_anomalia.fit(X_train_scaled, y_train)
```

#### **Modelo de Temperatura:**
```python
# Random Forest Regressor
modelo_temperatura = RandomForestRegressor(
    n_estimators=100,
    max_depth=10,
    random_state=42
)
modelo_temperatura.fit(X_train_scaled, y_train)
```

### **5. Avaliação e Métricas**

#### **Detecção de Anomalias:**
- **Acurácia**: Proporção de previsões corretas
- **Matriz de Confusão**: Verdadeiros/falsos positivos/negativos
- **Curva ROC**: Taxa de verdadeiros vs falsos positivos

#### **Previsão de Temperatura:**
- **MAE (Mean Absolute Error)**: Erro médio absoluto em °C
- **RMSE (Root Mean Square Error)**: Raiz do erro quadrático médio
- **R² (Coefficient of Determination)**: Proporção da variância explicada

### **6. Visualizações Geradas**

#### **Matriz de Confusão**
- **Função**: Mostra acertos e erros do modelo de anomalias
- **Interpretação**: Verdadeiros positivos, falsos positivos, etc.

#### **Curva ROC**
- **Função**: Avalia performance do classificador
- **AUC**: Área sob a curva (quanto maior, melhor)

#### **Previsões vs Valores Reais**
- **Função**: Compara previsões com valores reais de temperatura
- **Interpretação**: Pontos próximos à linha diagonal indicam boa previsão

#### **Análise de Resíduos**
- **Função**: Mostra distribuição dos erros de previsão
- **Interpretação**: Resíduos aleatórios indicam bom modelo

## 📈 Métricas Implementadas

### **1. Acurácia (Accuracy)**
```python
accuracy = accuracy_score(y_test, y_pred)
```
- **Definição**: Proporção de previsões corretas
- **Fórmula**: (TP + TN) / (TP + TN + FP + FN)
- **Range**: 0 a 1 (quanto maior, melhor)

### **2. MAE (Mean Absolute Error)**
```python
mae = mean_absolute_error(y_test, y_pred)
```
- **Definição**: Erro médio absoluto
- **Fórmula**: Σ|y_real - y_pred| / n
- **Unidade**: °C (para temperatura)
- **Range**: 0 a ∞ (quanto menor, melhor)

### **3. R² (Coefficient of Determination)**
```python
r2 = r2_score(y_test, y_pred)
```
- **Definição**: Proporção da variância explicada
- **Fórmula**: 1 - (SS_res / SS_tot)
- **Range**: -∞ a 1 (quanto maior, melhor)

### **4. Matriz de Confusão**
```python
cm = confusion_matrix(y_test, y_pred)
```
- **Definição**: Tabela de acertos e erros
- **Elementos**: TP, TN, FP, FN
- **Uso**: Análise detalhada de performance

## 🎨 Visualizações Pertinentes

### **1. Matriz de Confusão - Detecção de Anomalias**
- **Tipo**: Heatmap
- **Cores**: Azul (intensidade)
- **Elementos**: Verdadeiros/Falsos Positivos/Negativos
- **Métricas**: Acurácia exibida

### **2. Curva ROC - Detecção de Anomalias**
- **Tipo**: Linha
- **Eixos**: Taxa de Falsos Positivos vs Verdadeiros Positivos
- **AUC**: Área sob a curva
- **Linha de Referência**: Diagonal (classificador aleatório)

### **3. Previsões vs Valores Reais - Temperatura**
- **Tipo**: Scatter plot
- **Eixos**: Temperatura Real vs Predita
- **Linha de Referência**: Diagonal perfeita
- **Métricas**: MAE e R² exibidos

### **4. Análise de Resíduos - Temperatura**
- **Tipo**: Scatter plot
- **Eixos**: Valores Preditos vs Resíduos
- **Linha de Referência**: Resíduo = 0
- **Interpretação**: Padrão aleatório indica bom modelo

## 🚀 Como Executar

### **Windows:**
```bash
executar_ml_basico.bat
```

### **Linux/Mac:**
```bash
chmod +x executar_ml_basico.sh
./executar_ml_basico.sh
```

### **Execução Direta:**
```bash
# ML Básico Integrado
python ml_basico_integrado.py

# Análise do Dataset
python dataset_ml_analisador.py
```

## 📊 Exemplo de Saída

### **Log de Execução:**
```
=== ML Básico Integrado - Sistema IoT Monitoring ===
Enterprise Challenge Sprint 3 - Reply
=================================================

📊 Carregando dados do banco...
Carregados 50400 registros de leituras
Período: 2024-01-04 10:30:00 a 2024-01-11 10:30:00

📋 Informações do Dataset:
  - Total de registros: 50400
  - Sensores únicos: 70
  - Dispositivos únicos: 7
  - Tipos de sensor: ['DHT22', 'LDR', 'PIR', 'Pressão', 'Vibração', 'Nível']
  - Anomalias detectadas: 2520

🔍 Preparando dados para detecção de anomalias...
Dados preparados: 45000 amostras, 5 features
Anomalias: 2250 (5.0%)

🌡️ Preparando dados para previsão de temperatura...
Dados preparados: 12000 amostras, 5 features
Temperatura média: 23.45°C
Temperatura min/max: 15.20°C / 35.80°C

🤖 Treinando modelo de detecção de anomalias...
✅ Modelo de anomalia treinado - Acurácia: 0.892

🌡️ Treinando modelo de previsão de temperatura...
✅ Modelo de temperatura treinado - MAE: 1.234, R²: 0.856

📊 Gerando visualizações...
📊 Visualizações salvas em: ml_basico_visualizacoes.png

📋 Gerando relatório de métricas...
============================================================
📊 RELATÓRIO DE MÉTRICAS - ML BÁSICO INTEGRADO
============================================================

📋 INFORMAÇÕES DO DATASET:
  - Total de registros: 50400
  - Período: 2024-01-04T10:30:00 a 2024-01-11T10:30:00
  - Sensores únicos: 70
  - Dispositivos únicos: 7
  - Tipos de sensor: DHT22, LDR, PIR, Pressão, Vibração, Nível

🤖 MODELO DE DETECÇÃO DE ANOMALIAS:
  - Acurácia: 0.892
  - Relatório de Classificação:
                precision    recall  f1-score   support
           0       0.95      0.93      0.94      7200
           1       0.78      0.85      0.81      1800
    accuracy                           0.89      9000
   macro avg       0.86      0.89      0.87      9000
weighted avg       0.90      0.89      0.90      9000

🌡️ MODELO DE PREVISÃO DE TEMPERATURA:
  - MAE (Mean Absolute Error): 1.234°C
  - RMSE (Root Mean Square Error): 1.567°C
  - R² (Coefficient of Determination): 0.856

💾 Salvando modelos treinados...
✅ Modelo de anomalia salvo: modelo_anomalia.pkl
✅ Modelo de temperatura salvo: modelo_temperatura.pkl
✅ Scaler salvo: scaler.pkl

⚡ Executando inferência em tempo real...
📊 Processando 100 registros recentes...
  📡 ESP32-Sala-01 - DHT22-Temperatura: 23.45 (timestamp: 2024-01-11 10:30:00)
  📡 ESP32-Garagem-01 - DHT22-Temperatura: 22.10 (timestamp: 2024-01-11 10:29:45)
  📡 ESP32-Cozinha-01 - DHT22-Temperatura: 24.80 (timestamp: 2024-01-11 10:29:30)
  ...

🎉 Pipeline completo executado com sucesso!
```

## 📁 Arquivos Gerados

### **Modelos Treinados:**
- `modelo_anomalia.pkl` - Modelo de detecção de anomalias
- `modelo_temperatura.pkl` - Modelo de previsão de temperatura
- `scaler.pkl` - Normalizador de features

### **Visualizações:**
- `ml_basico_visualizacoes.png` - Gráficos dos modelos ML
- `analise_dataset_ml.png` - Análise do dataset

### **Relatórios:**
- `relatorio_ml_basico.json` - Métricas e resultados
- `relatorio_dataset_ml.json` - Análise do dataset

### **Logs:**
- `ml_basico_integrado.log` - Log da execução ML
- `dataset_ml_analisador.log` - Log da análise do dataset

## 🔧 Dependências

### **Python:**
```bash
pip install pandas matplotlib seaborn scikit-learn numpy mysql-connector-python joblib
```

### **Banco de Dados:**
- MySQL 8.0+
- Banco: `iot_monitoring_db`
- Tabelas: `leituras_sensores`, `sensores`, `dispositivos`, `tipos_sensor`

## 🎯 Benefícios da Implementação

### **Integração Completa**
- **Banco de Dados**: Dados reais do sistema IoT
- **Modelos ML**: Treinados com dados históricos
- **Inferência**: Aplicação em tempo real

### **Métricas Robustas**
- **Classificação**: Acurácia, matriz de confusão, ROC
- **Regressão**: MAE, RMSE, R²
- **Visualizações**: Gráficos interpretáveis

### **Escalabilidade**
- **Batch Processing**: Processamento em lote
- **Modelos Salvos**: Reutilização sem retreinamento
- **Pipeline Automatizado**: Execução simplificada

### **Documentação Completa**
- **Dataset**: Análise detalhada dos dados
- **Passo a Passo**: Processo documentado
- **Métricas**: Explicação de cada métrica

## 📞 Suporte

Para dúvidas sobre o ML básico integrado:
- **Conexão**: Verifique as credenciais do banco
- **Dados**: Confirme se há dados suficientes
- **Modelos**: Verifique se os modelos foram treinados
- **Métricas**: Analise os relatórios gerados

---

**ML Básico Integrado - Enterprise Challenge Sprint 3 - Reply**
