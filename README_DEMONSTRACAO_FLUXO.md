# Demonstração do Fluxo Completo - Sistema IoT Monitoring

## 🎯 Objetivo

Este script demonstra o **fluxo completo de dados** no sistema IoT Monitoring, desde a coleta pelos sensores ESP32 até a visualização de resultados (gráficos, métricas e alertas).

## 🚀 Como Executar

### **Windows:**
```bash
executar_demonstracao.bat
```

### **Linux/Mac:**
```bash
chmod +x executar_demonstracao.sh
./executar_demonstracao.sh
```

### **Execução Direta:**
```bash
python demonstracao_fluxo_completo.py
```

## 📊 Fluxo Demonstrado

### **ETAPA 1: Coleta de Dados ESP32**
- Simulação de sensores ESP32 (DHT22, LDR, PIR, Pressão, Vibração, Nível)
- Geração de dados sintéticos realísticos
- Validação de qualidade dos dados

### **ETAPA 2: Transmissão MQTT**
- Simulação do protocolo MQTT
- Envio para tópico `industrial/sensors/{device_id}/data`
- Simulação de latência de rede

### **ETAPA 3: Processamento no Pipeline**
- Validação de dados de entrada
- Enriquecimento com metadados
- Cálculo de features derivadas
- Detecção básica de anomalias

### **ETAPA 4: Persistência no Banco**
- Criação de tabelas SQLite (simulação)
- Inserção de dispositivos e leituras
- Geração de alertas automáticos
- Cálculo de métricas do sistema

### **ETAPA 5: Inferência Machine Learning**
- Preparação de dados para ML
- Simulação de modelo treinado
- Cálculo de métricas de performance
- Predição de anomalias

### **ETAPA 6: Visualização de Resultados**
- Gráfico de temperatura ao longo do tempo
- Gráfico de detecção de anomalias
- Dashboard com KPIs do sistema
- Matriz de correlação entre variáveis

### **ETAPA 7: Sistema de Alertas**
- Análise de dados para alertas
- Geração de notificações
- Classificação por severidade

## 📈 Resultados Visíveis

### **Gráficos Gerados:**
1. **`grafico_temperatura_demo.png`**
   - Temperatura ao longo do tempo por dispositivo
   - Linhas coloridas para cada ESP32
   - Marcadores para cada leitura

2. **`grafico_anomalias_demo.png`**
   - Detecção visual de anomalias
   - Pontos azuis = dados normais
   - Pontos vermelhos com X = anomalias

3. **`dashboard_kpis_demo.png`**
   - Total de leituras coletadas
   - Taxa de anomalias (pizza chart)
   - Acurácia do modelo ML
   - Distribuição por dispositivo

4. **`grafico_correlacao_demo.png`**
   - Matriz de correlação entre variáveis
   - Heatmap colorido
   - Valores de correlação numéricos

### **Métricas Calculadas:**
- **Total de Leituras**: Quantidade de dados coletados
- **Taxa de Anomalias**: Percentual de anomalias detectadas
- **Acurácia ML**: Performance do modelo de ML
- **Precisão ML**: Precisão das predições
- **Recall ML**: Sensibilidade do modelo
- **F1-Score**: Métrica balanceada

### **Alertas Gerados:**
- **Temperatura Alta**: Valores > 30°C
- **Umidade Baixa**: Valores < 40%
- **Luminosidade Alta**: Valores > 800lx
- **Vibração Excessiva**: Magnitude > 1.5

## 🔧 Dependências

```bash
pip install pandas numpy matplotlib seaborn scikit-learn
```

## 📋 Estrutura do Código

### **Classe Principal:**
- `DemonstracaoFluxoCompleto`: Classe principal que orquestra toda a demonstração

### **Métodos Principais:**
- `etapa_1_coleta_dados_esp32()`: Simulação da coleta
- `etapa_2_transmissao_mqtt()`: Simulação MQTT
- `etapa_3_processamento_pipeline()`: Processamento de dados
- `etapa_4_persistencia_banco()`: Persistência no banco
- `etapa_5_inferencia_ml()`: Inferência de ML
- `etapa_6_visualizacao_resultados()`: Geração de gráficos
- `etapa_7_alertas_notificacoes()`: Sistema de alertas

### **Métodos Auxiliares:**
- `_validar_dados()`: Validação de dados
- `_enriquecer_dados()`: Enriquecimento com metadados
- `_calcular_features_derivadas()`: Features para ML
- `_detectar_anomalia_basica()`: Detecção de anomalias
- `_criar_grafico_*()`: Geração de gráficos específicos

## 🎯 Exemplo de Saída

```
🚀 Iniciando Demonstração do Fluxo Completo IoT Monitoring
============================================================

📡 ETAPA 1: Coleta de Dados ESP32
----------------------------------------
🔌 Simulando sensores ESP32...
  📊 ESP32_001: Temp=23.5°C, Umidade=65.2%, Luz=450lx
  📊 ESP32_002: Temp=25.1°C, Umidade=58.7%, Luz=320lx
  📊 ESP32_003: Temp=22.8°C, Umidade=71.3%, Luz=580lx
✅ Coletados 10 registros de sensores

📡 ETAPA 2: Transmissão MQTT
----------------------------------------
🌐 Simulando envio via MQTT...
  📤 Tópico: industrial/sensors/ESP32_001/data
  📤 Tópico: industrial/sensors/ESP32_002/data
✅ Dados transmitidos via MQTT com sucesso

⚙️ ETAPA 3: Processamento no Pipeline
----------------------------------------
🔄 Processando dados no pipeline...
  ✅ Normal ESP32_001: Temp=23.5°C, Anomalia=False
  🚨 ANOMALIA ESP32_002: Temp=32.1°C, Anomalia=True
  ✅ Normal ESP32_003: Temp=22.8°C, Anomalia=False
✅ Processados 10 registros

💾 ETAPA 4: Persistência no Banco
----------------------------------------
🗄️ Persistindo dados no banco...
✅ Dados persistidos com sucesso
📊 Métricas calculadas: 3

🤖 ETAPA 5: Inferência Machine Learning
----------------------------------------
🧠 Executando inferência ML...
✅ Inferência ML concluída
📈 Acurácia: 85.00%
🎯 Precisão: 80.00%

📊 ETAPA 6: Visualização de Resultados
----------------------------------------
📈 Gerando visualizações...
📊 Gráfico de temperatura salvo: grafico_temperatura_demo.png
🚨 Gráfico de anomalias salvo: grafico_anomalias_demo.png
📊 Dashboard KPIs salvo: dashboard_kpis_demo.png
🔗 Gráfico de correlação salvo: grafico_correlacao_demo.png
✅ Visualizações geradas com sucesso

🚨 ETAPA 7: Sistema de Alertas
----------------------------------------
🔍 Analisando dados para alertas...
  🚨 Temperatura Alta: 2 ocorrências
  🚨 Umidade Baixa: 1 ocorrências
📢 Gerando notificações...
  🔔 3 alertas gerados
  📧 Notificações enviadas para:
     - Email: admin@empresa.com
     - Slack: #iot-alerts
     - Teams: #monitoring

============================================================
🎯 RESUMO FINAL DA DEMONSTRAÇÃO
============================================================
📊 Dados Coletados: 10 leituras
⚙️ Dados Processados: 10 registros
🚨 Alertas Gerados: 3 alertas
💾 Leituras Persistidas: 10
🤖 Acurácia ML: 85.00%
📈 Taxa de Anomalias: 20.00%

📁 Arquivos Gerados:
  📊 grafico_temperatura_demo.png
  🚨 grafico_anomalias_demo.png
  📊 dashboard_kpis_demo.png
  🔗 grafico_correlacao_demo.png

✅ DEMONSTRAÇÃO CONCLUÍDA COM SUCESSO!
🎉 Fluxo completo de dados demonstrado desde ESP32 até visualização!
```

## 🔍 Detalhes Técnicos

### **Simulação de Dados:**
- **Sensores**: DHT22, LDR, PIR, Pressão, Vibração, Nível
- **Variação**: Dados realísticos com tendências temporais
- **Qualidade**: Simulação de qualidade de leitura (0.7-1.0)
- **Anomalias**: Detecção baseada em thresholds configuráveis

### **Processamento:**
- **Validação**: Verificação de campos obrigatórios e qualidade
- **Enriquecimento**: Adição de metadados e timestamps
- **Features**: Cálculo de features derivadas para ML
- **Anomalias**: Detecção baseada em regras de negócio

### **Machine Learning:**
- **Modelo**: Simulação de Random Forest + Isolation Forest
- **Features**: 10 variáveis (7 originais + 3 derivadas)
- **Métricas**: Acurácia, Precisão, Recall, F1-Score
- **Predições**: Classificação binária (Normal/Anomalia)

### **Visualizações:**
- **Temperatura**: Gráfico temporal por dispositivo
- **Anomalias**: Scatter plot com detecção visual
- **KPIs**: Dashboard com 4 métricas principais
- **Correlação**: Heatmap de correlação entre variáveis

## 🎯 Benefícios da Demonstração

### **Educacional:**
- **Fluxo Completo**: Mostra todo o pipeline de dados
- **Visualização**: Resultados tangíveis e compreensíveis
- **Métricas**: Demonstração de KPIs reais
- **Alertas**: Sistema de notificações funcionando

### **Técnico:**
- **Integração**: Todos os componentes trabalhando juntos
- **Performance**: Métricas de tempo e qualidade
- **Escalabilidade**: Demonstração de processamento em lote
- **Robustez**: Validação e tratamento de erros

### **Negócio:**
- **ROI**: Demonstração de valor do sistema
- **Insights**: Visualização de dados operacionais
- **Alertas**: Detecção proativa de problemas
- **Relatórios**: Geração automática de relatórios

## 🚀 Próximos Passos

1. **Executar Demonstração**: Use os scripts fornecidos
2. **Analisar Resultados**: Examine os gráficos gerados
3. **Personalizar**: Modifique parâmetros conforme necessário
4. **Integrar**: Use como base para implementação real
5. **Escalar**: Adapte para volumes maiores de dados

---

**Demonstração do Fluxo Completo - Enterprise Challenge Sprint 3 - Reply**
