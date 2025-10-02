# Decisões Técnicas - Sistema IoT Monitoring
## Enterprise Challenge Sprint 3 - Reply

## 📋 Visão Geral

Este documento detalha as decisões técnicas tomadas durante o desenvolvimento do Sistema IoT Monitoring, incluindo justificativas, alternativas consideradas e impactos.

## 🏗️ Decisões Arquiteturais

### **1. Arquitetura em Camadas**

#### **Decisão**
Implementar arquitetura em 4 camadas principais:
- **Coleta de Dados**: Hardware e simulação
- **Processamento**: ETL e persistência
- **Machine Learning**: Treinamento e inferência
- **Visualização**: Dashboard e alertas

#### **Justificativa**
- **Separação de Responsabilidades**: Cada camada tem responsabilidade específica
- **Escalabilidade**: Facilita expansão de componentes individuais
- **Manutenibilidade**: Mudanças em uma camada não afetam outras
- **Testabilidade**: Permite testes isolados por camada

#### **Alternativas Consideradas**
- **Microserviços**: Mais complexo para o escopo atual
- **Monolito**: Menos flexível para futuras expansões
- **Event-Driven**: Desnecessário para o volume de dados atual

### **2. Protocolo de Comunicação**

#### **Decisão**
Usar **MQTT** como protocolo principal de comunicação.

#### **Justificativa**
- **IoT Nativo**: Protocolo padrão para IoT
- **Baixo Overhead**: Eficiente para sensores
- **QoS**: Garantia de entrega configurável
- **Broker Público**: HiveMQ Cloud disponível gratuitamente

#### **Alternativas Consideradas**
- **HTTP REST**: Mais overhead, menos eficiente
- **WebSocket**: Mais complexo para múltiplos sensores
- **CoAP**: Menos suporte de bibliotecas

### **3. Banco de Dados**

#### **Decisão**
Usar **MySQL** como banco de dados principal.

#### **Justificativa**
- **Relacional**: Adequado para dados estruturados
- **ACID**: Garantia de consistência
- **Índices**: Performance otimizada
- **Familiaridade**: Equipe conhece a tecnologia

#### **Alternativas Consideradas**
- **PostgreSQL**: Mais recursos, mas maior complexidade
- **MongoDB**: Menos adequado para dados estruturados
- **InfluxDB**: Específico para time-series, mas limitado

## 🔧 Decisões de Implementação

### **1. Linguagem de Programação**

#### **Decisão**
Usar **Python** como linguagem principal.

#### **Justificativa**
- **Ecosystem ML**: Scikit-learn, Pandas, NumPy
- **IoT Libraries**: Paho MQTT, PySerial
- **Visualização**: Streamlit, Plotly, Matplotlib
- **Rapid Prototyping**: Desenvolvimento ágil

#### **Alternativas Consideradas**
- **Java**: Mais verboso, menos adequado para ML
- **C++**: Mais performático, mas menos produtivo
- **Node.js**: Bom para IoT, mas limitado para ML

### **2. Framework de Visualização**

#### **Decisão**
Usar **Streamlit** para dashboard.

#### **Justificativa**
- **Rapid Development**: Interface web rápida
- **Python Native**: Integração natural
- **Interactive**: Widgets interativos
- **Deployment**: Fácil deploy

#### **Alternativas Consideradas**
- **Dash**: Mais complexo, curva de aprendizado
- **Flask/FastAPI**: Mais controle, mas mais código
- **Grafana**: Específico para métricas, menos flexível

### **3. Algoritmos de Machine Learning**

#### **Decisão**
Usar **Random Forest** para classificação e regressão.

#### **Justificativa**
- **Robustez**: Funciona bem com dados ruidosos
- **Interpretabilidade**: Feature importance
- **Performance**: Boa acurácia sem tuning extensivo
- **Overfitting**: Menos propenso ao overfitting

#### **Alternativas Consideradas**
- **Neural Networks**: Mais complexo, requer mais dados
- **SVM**: Bom para classificação, limitado para regressão
- **XGBoost**: Mais performático, mas mais complexo

## 📊 Decisões de Dados

### **1. Estrutura do Banco de Dados**

#### **Decisão**
Implementar **11 tabelas normalizadas** em 3NF.

#### **Justificativa**
- **Integridade**: Chaves estrangeiras garantem consistência
- **Flexibilidade**: Fácil adição de novos sensores/dispositivos
- **Performance**: Índices otimizados para consultas
- **Manutenibilidade**: Estrutura clara e documentada

#### **Tabelas Principais**
```sql
leituras_sensores (id_leitura, id_sensor, timestamp_datetime, valor_numerico, valor_booleano, qualidade_dados, anomalia_detectada)
dispositivos (id_dispositivo, nome, localizacao, ip_address, status)
sensores (id_sensor, id_dispositivo, id_tipo_sensor, nome, pino, ativo)
tipos_sensor (id_tipo_sensor, nome, unidade_medida, range_min, range_max)
alertas (id_alerta, id_dispositivo, id_sensor, tipo_alerta, severidade, titulo, descricao, valor_atual, valor_limite, timestamp_alerta, status)
```

### **2. Frequência de Coleta**

#### **Decisão**
Coletar dados a **1Hz** (1 leitura por segundo).

#### **Justificativa**
- **Tempo Real**: Suficiente para monitoramento industrial
- **Recursos**: Não sobrecarrega o ESP32
- **Storage**: Volume de dados gerenciável
- **Latência**: Resposta rápida para alertas

#### **Alternativas Consideradas**
- **10Hz**: Muito frequente, sobrecarga desnecessária
- **0.1Hz**: Muito lento para monitoramento industrial
- **Variável**: Complexidade adicional desnecessária

### **3. Formato de Dados**

#### **Decisão**
Usar **JSON** como formato principal de dados.

#### **Justificativa**
- **Estrutura**: Dados hierárquicos organizados
- **Legibilidade**: Fácil debug e manutenção
- **Flexibilidade**: Fácil adição de campos
- **Padrão**: Formato padrão para APIs

#### **Exemplo**
```json
{
  "device": "ESP32-01",
  "sensor": "DHT22",
  "data": {
    "temperature": 25.5,
    "humidity": 60.0
  },
  "timestamp": "2024-01-11T14:30:00Z",
  "quality": "good"
}
```

## 🚀 Decisões de Performance

### **1. Cache Inteligente**

#### **Decisão**
Implementar **cache em memória** para informações de dispositivos e sensores.

#### **Justificativa**
- **Performance**: Reduz consultas ao banco
- **Latência**: Resposta mais rápida
- **Recursos**: Uso eficiente de memória
- **TTL**: Atualização automática

#### **Implementação**
```python
cache = {
    'devices': {},  # TTL: 300s
    'sensors': {},  # TTL: 300s
    'thresholds': {}  # TTL: 600s
}
```

### **2. Processamento em Lote**

#### **Decisão**
Processar dados em **lotes de 1 minuto**.

#### **Justificativa**
- **Eficiência**: Menos operações de I/O
- **Consistência**: Dados agrupados por período
- **Recursos**: Uso otimizado de CPU/memória
- **Latência**: Aceitável para monitoramento

### **3. Índices de Banco**

#### **Decisão**
Criar **índices compostos** para consultas frequentes.

#### **Justificativa**
- **Performance**: Consultas mais rápidas
- **Escalabilidade**: Suporte a mais dados
- **Manutenibilidade**: Consultas otimizadas

#### **Índices Implementados**
```sql
-- Índice para consultas por sensor e tempo
CREATE INDEX idx_leituras_sensor_tempo ON leituras_sensores(id_sensor, timestamp_datetime);

-- Índice para consultas por dispositivo
CREATE INDEX idx_leituras_dispositivo ON leituras_sensores(id_sensor) 
USING HASH;

-- Índice para consultas de anomalias
CREATE INDEX idx_leituras_anomalia ON leituras_sensores(anomalia_detectada, timestamp_datetime);
```

## 🔒 Decisões de Segurança

### **1. Autenticação**

#### **Decisão**
Implementar **autenticação básica** para APIs.

#### **Justificativa**
- **Simplicidade**: Fácil implementação
- **Segurança**: Suficiente para ambiente controlado
- **Manutenibilidade**: Menos complexidade

#### **Alternativas Consideradas**
- **JWT**: Mais seguro, mas mais complexo
- **OAuth2**: Overkill para o escopo atual
- **Sem autenticação**: Inseguro para produção

### **2. Criptografia**

#### **Decisão**
Usar **TLS 1.3** para comunicação segura.

#### **Justificativa**
- **Padrão**: Protocolo mais seguro disponível
- **Performance**: Otimizado para performance
- **Compatibilidade**: Suporte amplo

## 📈 Decisões de Escalabilidade

### **1. Particionamento**

#### **Decisão**
Implementar **particionamento por data** na tabela de leituras.

#### **Justificativa**
- **Performance**: Consultas mais rápidas
- **Manutenção**: Limpeza de dados antigos
- **Escalabilidade**: Suporte a mais dados históricos

#### **Implementação**
```sql
-- Particionamento por mês
ALTER TABLE leituras_sensores
PARTITION BY RANGE (YEAR(timestamp_datetime) * 100 + MONTH(timestamp_datetime)) (
    PARTITION p202401 VALUES LESS THAN (202402),
    PARTITION p202402 VALUES LESS THAN (202403),
    -- ... mais partições
);
```

### **2. Microserviços**

#### **Decisão**
Manter **arquitetura monolítica** por enquanto.

#### **Justificativa**
- **Simplicidade**: Menos complexidade operacional
- **Desenvolvimento**: Mais rápido para MVP
- **Debugging**: Mais fácil de debugar
- **Futuro**: Pode ser refatorado para microserviços

## 🔄 Decisões de Monitoramento

### **1. Logging**

#### **Decisão**
Implementar **logging estruturado** em JSON.

#### **Justificativa**
- **Análise**: Fácil parsing e análise
- **Agregação**: Compatível com ferramentas de log
- **Debugging**: Informações detalhadas
- **Auditoria**: Rastreamento de ações

#### **Exemplo**
```json
{
  "timestamp": "2024-01-11T14:30:00Z",
  "level": "INFO",
  "component": "data_collector",
  "message": "Data collected successfully",
  "sensor_id": "DHT22-01",
  "value": 25.5,
  "quality": "good"
}
```

### **2. Métricas**

#### **Decisão**
Implementar **métricas customizadas** para KPIs.

#### **Justificativa**
- **Visibilidade**: Monitoramento de performance
- **Alertas**: Detecção de problemas
- **Otimização**: Identificação de gargalos
- **Relatórios**: Dados para relatórios

#### **Métricas Implementadas**
- **Throughput**: Leituras por minuto
- **Latência**: Tempo de processamento
- **Erros**: Taxa de erro por componente
- **Recursos**: Uso de CPU/memória

## 🎯 Decisões de UX/UI

### **1. Dashboard Responsivo**

#### **Decisão**
Usar **Streamlit** com layout responsivo.

#### **Justificativa**
- **Acessibilidade**: Funciona em diferentes dispositivos
- **Usabilidade**: Interface intuitiva
- **Manutenibilidade**: Menos código customizado
- **Performance**: Carregamento rápido

### **2. Alertas Visuais**

#### **Decisão**
Implementar **alertas com cores** e **banners visuais**.

#### **Justificativa**
- **Visibilidade**: Fácil identificação de problemas
- **Severidade**: Cores indicam nível de urgência
- **Ação**: Incentiva ação imediata
- **Padrão**: Segue convenções de UI

## 📚 Decisões de Documentação

### **1. Documentação Técnica**

#### **Decisão**
Manter **documentação em Markdown** no repositório.

#### **Justificativa**
- **Versionamento**: Controle de versão com código
- **Colaboração**: Fácil edição colaborativa
- **Renderização**: Fácil visualização no GitHub
- **Manutenibilidade**: Atualização simples

### **2. Diagramas**

#### **Decisão**
Usar **Draw.io** para diagramas arquiteturais.

#### **Justificativa**
- **Padrão**: Formato amplamente aceito
- **Colaboração**: Edição colaborativa
- **Integração**: Fácil integração com GitHub
- **Flexibilidade**: Suporte a diferentes tipos de diagramas

## 🔮 Decisões Futuras

### **1. Migração para Microserviços**

#### **Planejamento**
Quando o sistema crescer, migrar para microserviços:
- **API Gateway**: Kong ou Istio
- **Service Mesh**: Istio para comunicação
- **Containerização**: Docker + Kubernetes
- **Observabilidade**: Prometheus + Grafana

### **2. Machine Learning Avançado**

#### **Planejamento**
Implementar ML mais avançado:
- **Deep Learning**: TensorFlow/PyTorch
- **Time Series**: Prophet ou LSTM
- **AutoML**: H2O ou Auto-sklearn
- **MLOps**: MLflow para versionamento

### **3. Edge Computing**

#### **Planejamento**
Implementar processamento na borda:
- **Edge ML**: Modelos no ESP32
- **Filtros**: Processamento local
- **Sincronização**: Sync com cloud
- **Offline**: Funcionamento sem internet

## 📊 Resumo de Decisões

| Categoria | Decisão | Justificativa | Alternativas |
|-----------|---------|---------------|--------------|
| Arquitetura | 4 Camadas | Separação de responsabilidades | Microserviços, Monolito |
| Protocolo | MQTT | IoT nativo, baixo overhead | HTTP, WebSocket |
| Banco | MySQL | Relacional, ACID | PostgreSQL, MongoDB |
| Linguagem | Python | Ecosystem ML, IoT | Java, C++, Node.js |
| Dashboard | Streamlit | Rapid development | Dash, Flask |
| ML | Random Forest | Robustez, interpretabilidade | Neural Networks, SVM |
| Dados | JSON | Estrutura, flexibilidade | XML, CSV |
| Cache | Memória | Performance, latência | Redis, Database |
| Segurança | TLS 1.3 | Padrão, performance | TLS 1.2, Sem criptografia |
| Escalabilidade | Particionamento | Performance, manutenção | Sharding, Replicação |

## 🎯 Conclusão

As decisões técnicas tomadas foram baseadas em:

1. **Simplicidade**: Escolhas que facilitam desenvolvimento e manutenção
2. **Performance**: Otimizações para o volume de dados atual
3. **Escalabilidade**: Preparação para crescimento futuro
4. **Padrões**: Uso de tecnologias estabelecidas e documentadas
5. **Custo**: Soluções que minimizam custos operacionais

Essas decisões formam a base sólida para o Sistema IoT Monitoring, permitindo evolução e adaptação conforme as necessidades do negócio.

---

**Decisões Técnicas - Sistema IoT Monitoring - Enterprise Challenge Sprint 3 - Reply**
