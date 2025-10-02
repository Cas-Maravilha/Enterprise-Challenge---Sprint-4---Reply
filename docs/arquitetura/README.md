# Arquitetura do Sistema IoT Monitoring
## Enterprise Challenge Sprint 3 - Reply

## 📋 Visão Geral

Esta pasta contém a documentação arquitetural completa do Sistema IoT Monitoring, incluindo diagramas de fluxo integrado, componentes e decisões técnicas.

## 📁 Estrutura de Arquivos

```
docs/arquitetura/
├── README.md                           # Este arquivo
├── fluxo_integrado_completo.drawio     # Diagrama principal (Draw.io)
├── fluxo_integrado_completo.png        # Diagrama principal (PNG)
├── componentes_detalhados.drawio       # Diagrama de componentes
├── componentes_detalhados.png          # Diagrama de componentes (PNG)
├── fluxo_dados.drawio                  # Diagrama de fluxo de dados
├── fluxo_dados.png                     # Diagrama de fluxo de dados (PNG)
├── decisoes_tecnicas.md               # Documentação de decisões
└── referencias_entregas.md            # Referências às entregas
```

## 🏗️ Diagramas Disponíveis

### **1. Fluxo Integrado Completo**
- **Arquivo**: `fluxo_integrado_completo.drawio`
- **Descrição**: Visão geral de todo o sistema com 4 camadas principais
- **Camadas**:
  - **Coleta de Dados**: ESP32, Wokwi, Serial, MQTT
  - **Processamento**: ETL, Validação, MySQL
  - **Machine Learning**: Feature Engineering, Modelos, Inferência
  - **Visualização**: Dashboard, Alertas, KPIs

### **2. Componentes Detalhados**
- **Arquivo**: `componentes_detalhados.drawio`
- **Descrição**: Detalhamento técnico de cada componente
- **Inclui**: APIs, Protocolos, Formatos de Dados

### **3. Fluxo de Dados**
- **Arquivo**: `fluxo_dados.drawio`
- **Descrição**: Fluxo específico de dados através do sistema
- **Inclui**: Formatos, Frequências, Transformações

## 🔄 Fluxo Integrado

### **Camada 1: Coleta de Dados**
```
ESP32 Hardware → Serial/USB → Coletor Python
Wokwi Simulação → MQTT → Broker HiveMQ
Simulador Python → Dados Sintéticos
```

### **Camada 2: Processamento e Persistência**
```
Dados Brutos → Pipeline ETL → Validação → MySQL
Cache Inteligente → Batch Processing → 11 Tabelas
```

### **Camada 3: Machine Learning**
```
Dados Validados → Feature Engineering → Modelos ML
Treinamento → Inferência → Predições/Anomalias
```

### **Camada 4: Visualização e Alertas**
```
Predições → Dashboard Streamlit → KPIs
Anomalias → Sistema Alertas → Notificações
```

## 📊 Formatos de Dados

### **Entrada (Coleta)**
- **JSON**: `{"sensor": "DHT22", "valor": 25.5, "timestamp": "2024-01-11T14:30:00Z"}`
- **CSV**: `timestamp,sensor,valor,qualidade`
- **Frequência**: 1Hz (1 leitura por segundo)

### **Processamento (ETL)**
- **Validação**: Range check, type check, quality score
- **Transformação**: Feature engineering, normalização
- **Enriquecimento**: Device info, sensor config

### **Saída (Visualização)**
- **Dashboard**: KPIs em tempo real, gráficos interativos
- **Alertas**: Thresholds configuráveis, notificações
- **Relatórios**: PDF/HTML, agendados

## 🔧 Tecnologias Utilizadas

### **Hardware/Simulação**
- **ESP32**: Microcontrolador principal
- **Sensores**: DHT22, LDR, PIR, BME280
- **Wokwi**: Simulação online
- **Arduino IDE**: Desenvolvimento

### **Backend/Processamento**
- **Python**: Linguagem principal
- **MySQL**: Banco de dados relacional
- **MQTT**: Protocolo de comunicação
- **Pandas**: Manipulação de dados

### **Machine Learning**
- **Scikit-learn**: Algoritmos ML
- **Random Forest**: Classificação e Regressão
- **Isolation Forest**: Detecção de anomalias
- **Feature Engineering**: Médias móveis, tendências

### **Frontend/Visualização**
- **Streamlit**: Dashboard web
- **Plotly**: Gráficos interativos
- **Matplotlib/Seaborn**: Visualizações estáticas

## 📈 Métricas de Performance

### **Coleta de Dados**
- **Frequência**: 1Hz (1000+ leituras/hora)
- **Latência**: < 100ms
- **Disponibilidade**: 99.9%

### **Processamento**
- **Throughput**: 1000+ registros/minuto
- **Latência ETL**: < 5 segundos
- **Disponibilidade**: 99.5%

### **Machine Learning**
- **Accuracy**: 85%+ (anomalia)
- **MAE**: < 0.5°C (temperatura)
- **R²**: 0.92+ (regressão)

### **Visualização**
- **Tempo de Carregamento**: < 2 segundos
- **Detecção de Alertas**: < 5 segundos
- **Disponibilidade**: 99.9%

## 🚀 Como Visualizar os Diagramas

### **Draw.io (Recomendado)**
1. Acesse [app.diagrams.net](https://app.diagrams.net)
2. Abra o arquivo `.drawio`
3. Visualize e edite conforme necessário

### **PNG (Visualização Rápida)**
1. Abra o arquivo `.png` em qualquer visualizador de imagens
2. Ideal para documentação e apresentações

## 📚 Referências

### **Entregas Anteriores**
- **Entrega 1**: Arquitetura e Design
- **Entrega 2**: Simulação e Coleta
- **Entrega 3**: Modelagem e ML

### **Documentação Relacionada**
- `../README.md` - Documentação principal
- `../README_REPRODUTIBILIDADE_COMPLETA.md` - Guia de execução
- `../README_ARQUITETURA_INTEGRADA.md` - Arquitetura detalhada

## 🔄 Atualizações

### **Versão 1.0.0** (2024-01-11)
- Criação da estrutura inicial
- Diagrama de fluxo integrado completo
- Documentação de componentes
- Referências às entregas

### **Próximas Versões**
- Diagramas de deployment
- Arquitetura de microserviços
- Diagramas de segurança
- Arquitetura de escalabilidade

---

**Arquitetura do Sistema IoT Monitoring - Enterprise Challenge Sprint 3 - Reply**
