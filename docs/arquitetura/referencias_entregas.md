# Referências às Entregas - Sistema IoT Monitoring
## Enterprise Challenge Sprint 3 - Reply

## 📋 Visão Geral

Este documento mapeia as referências explícitas entre as diferentes entregas do projeto, mostrando como cada componente evoluiu e se integrou ao sistema final.

## 🏗️ Mapeamento de Entregas

### **Entrega 1: Arquitetura e Design**
**Período**: Semana 1-2  
**Foco**: Definição da arquitetura geral e componentes

#### **Componentes Entregues**
- **Arquitetura Geral**: Definição das 4 camadas
- **Diagramas de Alto Nível**: Fluxo de dados e componentes
- **Especificações Técnicas**: Protocolos, formatos, frequências
- **Decisões Arquiteturais**: Justificativas e alternativas

#### **Arquivos Principais**
- `arquitetura_integrada_completa.xml` - Diagrama principal
- `README_ARQUITETURA_INTEGRADA.md` - Documentação detalhada
- `decisoes_tecnicas.md` - Decisões arquiteturais

#### **Integração com Entregas Posteriores**
- **Base para Entrega 2**: Definição de protocolos e formatos
- **Base para Entrega 3**: Estrutura de dados e persistência
- **Base para Entrega 4**: Interface e visualizações

### **Entrega 2: Simulação e Coleta**
**Período**: Semana 3-4  
**Foco**: Implementação da coleta de dados

#### **Componentes Entregues**
- **ESP32 Hardware**: Código Arduino para sensores
- **Wokwi Simulação**: Simulação online dos sensores
- **Coletor Python**: Scripts para coleta via Serial/MQTT
- **Simulador Dados**: Geração de dados sintéticos

#### **Arquivos Principais**
- `coleta_ingestao_esp32.ino` - Código Arduino
- `wokwi_simulacao_esp32.json` - Configuração Wokwi
- `coletor_dados_serial.py` - Coletor Serial
- `simulador_dados_esp32.py` - Simulador Python

#### **Integração com Entregas Anteriores**
- **Implementa Entrega 1**: Protocolos MQTT e Serial definidos
- **Base para Entrega 3**: Dados estruturados para persistência
- **Base para Entrega 4**: Dados em tempo real para visualização

### **Entrega 3: Modelagem e ML**
**Período**: Semana 5-6  
**Foco**: Banco de dados e machine learning

#### **Componentes Entregues**
- **Banco de Dados**: 11 tabelas normalizadas em MySQL
- **Machine Learning**: Modelos de anomalia e predição
- **Análise de Dados**: Scripts de análise e visualização
- **Métricas**: Acurácia, MAE, R², confusion matrix

#### **Arquivos Principais**
- `criar_tabelas_iot.sql` - Estrutura do banco
- `ml_basico_integrado.py` - Sistema ML completo
- `dataset_ml_analisador.py` - Análise de dados
- `persistencia_banco_relacional.py` - Camada de persistência

#### **Integração com Entregas Anteriores**
- **Implementa Entrega 1**: Estrutura de dados definida
- **Usa Entrega 2**: Dados coletados para treinamento
- **Base para Entrega 4**: Modelos treinados para inferência

### **Entrega 4: Visualização e Alertas**
**Período**: Semana 7-8  
**Foco**: Interface e sistema de alertas

#### **Componentes Entregues**
- **Dashboard Streamlit**: Interface web interativa
- **Sistema de Alertas**: Thresholds e notificações
- **KPIs**: Métricas de negócio em tempo real
- **Relatórios**: Geração automática de relatórios

#### **Arquivos Principais**
- `dashboard_visualizacao_alertas.py` - Dashboard principal
- `sistema_alertas_avancado.py` - Sistema de alertas
- `kpis_negocio.py` - Cálculo de KPIs
- `sistema_relatorios_automaticos.py` - Relatórios

#### **Integração com Entregas Anteriores**
- **Usa Entrega 1**: Interface definida na arquitetura
- **Usa Entrega 2**: Dados em tempo real da coleta
- **Usa Entrega 3**: Modelos ML e dados do banco

## 🔄 Fluxo de Integração

### **Evolução dos Componentes**

#### **1. Coleta de Dados**
```
Entrega 1: Definição de protocolos e formatos
    ↓
Entrega 2: Implementação ESP32 + Wokwi + Python
    ↓
Entrega 3: Integração com banco de dados
    ↓
Entrega 4: Dados em tempo real para dashboard
```

#### **2. Processamento de Dados**
```
Entrega 1: Definição de ETL e validação
    ↓
Entrega 2: Parsing e validação básica
    ↓
Entrega 3: Pipeline completo + persistência
    ↓
Entrega 4: Cache inteligente + otimizações
```

#### **3. Machine Learning**
```
Entrega 1: Definição de algoritmos e métricas
    ↓
Entrega 2: Dados sintéticos para desenvolvimento
    ↓
Entrega 3: Modelos treinados + avaliação
    ↓
Entrega 4: Inferência em tempo real + monitoramento
```

#### **4. Visualização**
```
Entrega 1: Definição de KPIs e interface
    ↓
Entrega 2: Gráficos básicos de dados coletados
    ↓
Entrega 3: Visualizações de análise ML
    ↓
Entrega 4: Dashboard completo + alertas
```

## 📊 Matriz de Dependências

| Componente | Entrega 1 | Entrega 2 | Entrega 3 | Entrega 4 |
|------------|-----------|-----------|-----------|-----------|
| **Arquitetura** | ✅ Definição | ✅ Implementação | ✅ Refinamento | ✅ Otimização |
| **Coleta** | ✅ Especificação | ✅ Implementação | ✅ Integração | ✅ Monitoramento |
| **Processamento** | ✅ Design | ✅ Básico | ✅ Completo | ✅ Otimizado |
| **Persistência** | ✅ Modelo | ✅ Estrutura | ✅ Implementação | ✅ Performance |
| **ML** | ✅ Algoritmos | ✅ Dados | ✅ Modelos | ✅ Inferência |
| **Visualização** | ✅ Interface | ✅ Básica | ✅ Análise | ✅ Completa |
| **Alertas** | ✅ Conceito | ✅ Básico | ✅ Integração | ✅ Avançado |

## 🔗 Referências Explícitas

### **Entrega 1 → Entrega 2**
- **Protocolos**: MQTT e Serial definidos na arquitetura
- **Formatos**: JSON e CSV especificados
- **Frequência**: 1Hz definida para coleta
- **Sensores**: DHT22, LDR, PIR, BME280 especificados

### **Entrega 2 → Entrega 3**
- **Dados**: Estrutura JSON implementada na coleta
- **Validação**: Range checks implementados
- **Qualidade**: Scoring de qualidade dos dados
- **Timestamp**: Formato ISO 8601 padronizado

### **Entrega 3 → Entrega 4**
- **Modelos**: Modelos treinados salvos como .pkl
- **Métricas**: Acurácia, MAE, R² calculados
- **Features**: Feature engineering implementado
- **Banco**: 11 tabelas com dados históricos

### **Entrega 4 → Sistema Completo**
- **Dashboard**: Interface web com dados reais
- **Alertas**: Sistema baseado em thresholds
- **KPIs**: Métricas calculadas em tempo real
- **Relatórios**: Geração automática de relatórios

## 📁 Estrutura de Arquivos por Entrega

### **Entrega 1: Arquitetura**
```
docs/arquitetura/
├── fluxo_integrado_completo.drawio
├── componentes_detalhados.drawio
├── fluxo_dados.drawio
├── decisoes_tecnicas.md
└── referencias_entregas.md
```

### **Entrega 2: Simulação e Coleta**
```
coleta_ingestao_esp32.ino
wokwi_simulacao_esp32.json
coletor_dados_serial.py
simulador_dados_esp32.py
README_COLETA_INGESTAO.md
```

### **Entrega 3: Modelagem e ML**
```
criar_tabelas_iot.sql
ml_basico_integrado.py
dataset_ml_analisador.py
persistencia_banco_relacional.py
README_ML_BASICO_INTEGRADO.md
```

### **Entrega 4: Visualização e Alertas**
```
dashboard_visualizacao_alertas.py
sistema_alertas_avancado.py
kpis_negocio.py
sistema_relatorios_automaticos.py
README_VISUALIZACAO_ALERTAS.md
```

## 🔄 Evolução dos Diagramas

### **Diagrama de Arquitetura**
- **Entrega 1**: Diagrama conceitual de alto nível
- **Entrega 2**: Adição de detalhes de implementação
- **Entrega 3**: Inclusão de componentes de ML
- **Entrega 4**: Diagrama completo com alertas

### **Diagrama de Fluxo de Dados**
- **Entrega 1**: Fluxo conceitual
- **Entrega 2**: Fluxo com formatos específicos
- **Entrega 3**: Fluxo com persistência e ML
- **Entrega 4**: Fluxo completo com visualização

### **Diagrama de Componentes**
- **Entrega 1**: Componentes principais
- **Entrega 2**: Detalhamento de coleta
- **Entrega 3**: Detalhamento de ML
- **Entrega 4**: Detalhamento completo

## 📈 Métricas de Evolução

### **Complexidade do Código**
- **Entrega 1**: 0 linhas (apenas especificação)
- **Entrega 2**: ~500 linhas (coleta básica)
- **Entrega 3**: ~2000 linhas (ML + persistência)
- **Entrega 4**: ~3000 linhas (sistema completo)

### **Arquivos Gerados**
- **Entrega 1**: 5 arquivos (documentação)
- **Entrega 2**: 8 arquivos (coleta + simulação)
- **Entrega 3**: 15 arquivos (ML + banco)
- **Entrega 4**: 25 arquivos (sistema completo)

### **Funcionalidades**
- **Entrega 1**: 0 funcionalidades (especificação)
- **Entrega 2**: 4 funcionalidades (coleta)
- **Entrega 3**: 8 funcionalidades (ML + persistência)
- **Entrega 4**: 12 funcionalidades (sistema completo)

## 🎯 Lições Aprendidas

### **Entrega 1 → Entrega 2**
- **Especificação Clara**: Definições detalhadas facilitaram implementação
- **Protocolos Padrão**: MQTT e Serial foram escolhas acertadas
- **Formato JSON**: Flexibilidade para evolução futura

### **Entrega 2 → Entrega 3**
- **Dados Estruturados**: JSON facilitou parsing e validação
- **Validação Precoce**: Range checks evitaram problemas
- **Timestamp Padronizado**: ISO 8601 facilitou ordenação

### **Entrega 3 → Entrega 4**
- **Modelos Salvos**: .pkl facilitou carregamento
- **Métricas Calculadas**: Acurácia e MAE prontos
- **Banco Estruturado**: Consultas otimizadas

### **Entrega 4 → Sistema Completo**
- **Interface Responsiva**: Streamlit facilitou desenvolvimento
- **Alertas Configuráveis**: Thresholds flexíveis
- **KPIs Automáticos**: Cálculo em tempo real

## 🔮 Próximos Passos

### **Evolução Contínua**
- **Monitoramento**: Drift detection e performance
- **Escalabilidade**: Microserviços e containerização
- **Segurança**: Autenticação e autorização avançadas
- **ML Avançado**: Deep learning e autoML

### **Integração com Outros Sistemas**
- **APIs**: REST e GraphQL para integração
- **Webhooks**: Notificações para sistemas externos
- **Exportação**: Dados para sistemas de BI
- **Sincronização**: Múltiplos ambientes

## 📚 Referências

### **Documentação Técnica**
- [Arquitetura Integrada](../README_ARQUITETURA_INTEGRADA.md)
- [Coleta e Ingestão](../README_COLETA_INGESTAO.md)
- [ML Básico Integrado](../README_ML_BASICO_INTEGRADO.md)
- [Visualização e Alertas](../README_VISUALIZACAO_ALERTAS.md)

### **Scripts de Execução**
- [Setup Completo](../setup_sistema_completo.sh)
- [Fluxo Completo](../executar_fluxo_completo.sh)
- [Geração de Evidências](../gerar_evidencias.py)

### **Configurações**
- [Database](../configs/database.json)
- [MQTT](../configs/mqtt.json)
- [Sensores](../configs/sensores.json)
- [Thresholds](../configs/thresholds.json)
- [ML](../configs/ml.json)

---

**Referências às Entregas - Sistema IoT Monitoring - Enterprise Challenge Sprint 3 - Reply**
