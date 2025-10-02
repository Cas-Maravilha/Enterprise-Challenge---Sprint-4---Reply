# Machine Learning - Sistema IoT Monitoring
## Enterprise Challenge Sprint 3 - Reply

## 📋 Visão Geral

Esta pasta contém todo o código de Machine Learning do Sistema IoT Monitoring, incluindo notebooks Jupyter, scripts Python para treino/inferência, métricas de avaliação e visualizações.

## 📁 Estrutura de Arquivos

```
ml/
├── README.md                           # Este arquivo
├── notebooks/                          # Notebooks Jupyter
│   ├── ML_Anomaly_Detection_IoT.ipynb  # Notebook principal
│   ├── ML_Model_Training.ipynb         # Notebook de treino
│   └── ML_Model_Evaluation.ipynb       # Notebook de avaliação
├── scripts/                            # Scripts Python
│   ├── treinar_modelo_ml.py            # Script de treino
│   ├── inferencia_tempo_real.py        # Script de inferência
│   ├── avaliar_modelo.py               # Script de avaliação
│   └── pipeline_ml_completo.py         # Pipeline completo
├── modelos/                            # Modelos treinados
│   ├── random_forest_anomaly.pkl       # Modelo Random Forest
│   ├── isolation_forest.pkl            # Modelo Isolation Forest
│   ├── scaler.pkl                      # Scaler para normalização
│   └── modelo_ensemble.pkl             # Modelo Ensemble
├── metricas/                           # Métricas de avaliação
│   ├── accuracy_score.json             # Acurácia
│   ├── confusion_matrix.json           # Matriz de confusão
│   ├── roc_auc_score.json              # ROC AUC
│   └── precision_recall.json           # Precision/Recall
├── visualizacoes/                      # Gráficos e visualizações
│   ├── confusion_matrix.png            # Matriz de confusão
│   ├── roc_curve.png                   # Curva ROC
│   ├── precision_recall_curve.png      # Curva Precision-Recall
│   ├── feature_importance.png          # Importância das features
│   └── anomaly_detection_plot.png      # Plot de detecção de anomalias
└── executar_ml_completo.bat            # Script de execução Windows
```

## 🤖 Algoritmos de Machine Learning

### **1. Detecção de Anomalias**
- **Random Forest Classifier**: Classificação de anomalias
- **Isolation Forest**: Detecção de outliers
- **One-Class SVM**: Detecção de anomalias não supervisionada
- **Local Outlier Factor (LOF)**: Detecção de outliers locais

### **2. Previsão de Valores**
- **Random Forest Regressor**: Previsão de temperatura/umidade
- **Linear Regression**: Regressão linear simples
- **Gradient Boosting**: Boosting para melhor performance
- **XGBoost**: Gradient boosting otimizado

### **3. Ensemble Methods**
- **Voting Classifier**: Combinação de múltiplos classificadores
- **Stacking**: Meta-learning com stacking
- **Bagging**: Bootstrap aggregating
- **AdaBoost**: Adaptive boosting

## 📊 Métricas de Avaliação

### **1. Métricas de Classificação**
- **Accuracy**: Acurácia geral do modelo
- **Precision**: Precisão por classe
- **Recall**: Sensibilidade por classe
- **F1-Score**: Média harmônica de precision e recall
- **ROC AUC**: Área sob a curva ROC
- **Confusion Matrix**: Matriz de confusão detalhada

### **2. Métricas de Regressão**
- **MAE**: Erro absoluto médio
- **MSE**: Erro quadrático médio
- **RMSE**: Raiz do erro quadrático médio
- **R²**: Coeficiente de determinação
- **MAPE**: Erro percentual absoluto médio

### **3. Métricas de Detecção de Anomalias**
- **Anomaly Detection Rate**: Taxa de detecção de anomalias
- **False Positive Rate**: Taxa de falsos positivos
- **True Positive Rate**: Taxa de verdadeiros positivos
- **F1-Score Anomaly**: F1-Score para anomalias

## 📈 Visualizações

### **1. Gráficos de Performance**
- **Confusion Matrix**: Matriz de confusão com heatmap
- **ROC Curve**: Curva ROC com AUC
- **Precision-Recall Curve**: Curva Precision-Recall
- **Learning Curve**: Curva de aprendizado
- **Validation Curve**: Curva de validação

### **2. Gráficos de Análise**
- **Feature Importance**: Importância das features
- **Anomaly Detection Plot**: Plot de detecção de anomalias
- **Residual Plot**: Plot de resíduos
- **Distribution Plot**: Distribuição dos dados
- **Correlation Heatmap**: Heatmap de correlação

### **3. Gráficos de Monitoramento**
- **Model Performance Over Time**: Performance ao longo do tempo
- **Drift Detection**: Detecção de drift nos dados
- **Prediction Confidence**: Confiança das previsões
- **Error Analysis**: Análise de erros

## 🔧 Scripts de Execução

### **1. Treino do Modelo (`treinar_modelo_ml.py`)**
```python
# Carregar dados do banco
# Preparar features
# Treinar modelos
# Avaliar performance
# Salvar modelos
```

### **2. Inferência em Tempo Real (`inferencia_tempo_real.py`)**
```python
# Carregar modelo treinado
# Receber dados em tempo real
# Fazer previsões
# Detectar anomalias
# Retornar resultados
```

### **3. Avaliação do Modelo (`avaliar_modelo.py`)**
```python
# Carregar modelo e dados de teste
# Calcular métricas
# Gerar visualizações
# Salvar resultados
```

### **4. Pipeline Completo (`pipeline_ml_completo.py`)**
```python
# Treino → Avaliação → Inferência
# Monitoramento contínuo
# Atualização de modelos
# Relatórios automáticos
```

## 📓 Notebooks Jupyter

### **1. Notebook Principal (`ML_Anomaly_Detection_IoT.ipynb`)**
- **Análise exploratória** dos dados
- **Preparação** de features
- **Treino** de múltiplos modelos
- **Avaliação** comparativa
- **Visualizações** interativas

### **2. Notebook de Treino (`ML_Model_Training.ipynb`)**
- **Carregamento** de dados do banco
- **Feature engineering** avançado
- **Hyperparameter tuning** com GridSearch
- **Cross-validation** estratificada
- **Salvamento** de modelos

### **3. Notebook de Avaliação (`ML_Model_Evaluation.ipynb`)**
- **Métricas** detalhadas de avaliação
- **Visualizações** de performance
- **Análise** de erros
- **Comparação** de modelos
- **Relatórios** de resultados

## 🚀 Como Executar

### **1. Execução Completa**
```bash
# Windows
ml\executar_ml_completo.bat

# Linux/Mac
chmod +x ml/executar_ml_completo.sh
./ml/executar_ml_completo.sh
```

### **2. Execução Individual**
```bash
# Treinar modelo
python ml\scripts\treinar_modelo_ml.py

# Inferência em tempo real
python ml\scripts\inferencia_tempo_real.py

# Avaliar modelo
python ml\scripts\avaliar_modelo.py
```

### **3. Notebooks Jupyter**
```bash
# Iniciar Jupyter
jupyter notebook ml/notebooks/

# Ou usar JupyterLab
jupyter lab ml/notebooks/
```

## 📊 Dataset

### **Fonte dos Dados**
- **Banco de dados**: `iot_monitoring_db.leituras_sensores`
- **Período**: 30 dias de dados simulados
- **Frequência**: 1 leitura por minuto
- **Sensores**: 40 sensores distribuídos
- **Total**: 1.7M+ leituras

### **Features Utilizadas**
- **Temperatura**: Valores numéricos
- **Umidade**: Valores numéricos
- **Luminosidade**: Valores numéricos
- **Pressão**: Valores numéricos
- **Movimento**: Valores booleanos
- **Timestamp**: Features temporais
- **Qualidade**: Features categóricas

### **Target Variables**
- **Anomalia**: Boolean (0 = normal, 1 = anomalia)
- **Qualidade**: Categorical (excelente, boa, regular, ruim)
- **Temperatura**: Continuous (previsão)
- **Umidade**: Continuous (previsão)

## 🔧 Configurações

### **Parâmetros do Modelo**
```python
# Random Forest
n_estimators = 100
max_depth = 10
min_samples_split = 5
min_samples_leaf = 2

# Isolation Forest
contamination = 0.1
n_estimators = 100
max_samples = 256

# XGBoost
n_estimators = 100
max_depth = 6
learning_rate = 0.1
subsample = 0.8
```

### **Configurações de Treino**
```python
# Split dos dados
test_size = 0.2
validation_size = 0.1
random_state = 42

# Cross-validation
cv_folds = 5
scoring = 'f1_weighted'

# Feature scaling
scaler = StandardScaler()
normalize = True
```

## 📈 Performance Esperada

### **Detecção de Anomalias**
- **Accuracy**: > 95%
- **Precision**: > 90%
- **Recall**: > 85%
- **F1-Score**: > 87%
- **ROC AUC**: > 0.95

### **Previsão de Valores**
- **MAE**: < 1.0°C (temperatura)
- **RMSE**: < 1.5°C (temperatura)
- **R²**: > 0.90
- **MAPE**: < 5%

### **Tempo de Execução**
- **Treino**: < 5 minutos
- **Inferência**: < 100ms
- **Avaliação**: < 2 minutos
- **Pipeline completo**: < 10 minutos

## 🔍 Troubleshooting

### **Problemas Comuns**

#### **1. Erro de Memória**
- Reduzir tamanho do dataset
- Usar amostragem estratificada
- Ajustar parâmetros do modelo

#### **2. Erro de Dados**
- Verificar conexão com banco
- Validar formato dos dados
- Verificar missing values

#### **3. Erro de Modelo**
- Verificar se o modelo foi treinado
- Validar arquivo .pkl
- Retreinar o modelo

## 📚 Referências

### **Documentação Técnica**
- [Arquitetura](../docs/arquitetura/README.md)
- [Banco de Dados](../db/README.md)
- [Ingestão](../ingest/README.md)

### **Scripts Relacionados**
- [ML Básico Integrado](../ml_basico_integrado.py)
- [Sistema ML Completo](../sistema_ml_completo.py)
- [Integração ML Pipeline](../integracao_ml_pipeline.py)

---

**Machine Learning - Sistema IoT Monitoring - Enterprise Challenge Sprint 3 - Reply**
