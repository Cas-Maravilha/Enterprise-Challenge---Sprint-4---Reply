# Documentação de Decisões Técnicas - Sistema IoT Monitoring
## Enterprise Challenge Sprint 3 - Reply

## 🎯 Visão Geral

Este documento detalha as **decisões técnicas** tomadas ao longo do desenvolvimento do sistema IoT Monitoring e como as **peças se integram** entre as diferentes entregas do projeto, demonstrando a evolução e consolidação da solução.

## 📋 Estrutura do Documento

1. [Ligação com Entregas Anteriores](#ligação-com-entregas-anteriores)
2. [Decisões de Arquitetura](#decisões-de-arquitetura)
3. [Decisões de Tecnologia](#decisões-de-tecnologia)
4. [Integração entre Componentes](#integração-entre-componentes)
5. [Decisões de Implementação](#decisões-de-implementação)
6. [Evolução e Consolidação](#evolução-e-consolidação)

---

## 🔗 Ligação com Entregas Anteriores

### **ENTREGA 1: Arquitetura e Visão Técnica**

#### **Decisões Consolidadas:**
- **Arquitetura de Microserviços**: Mantida e expandida
- **Comunicação Assíncrona**: MQTT como protocolo principal
- **Banco Relacional**: MySQL como persistência principal
- **Escalabilidade Horizontal**: Implementada com load balancing

#### **Evolução na Entrega 3:**
```python
# ENTREGA 1: Conceito de arquitetura
# ENTREGA 3: Implementação real com pipeline_integrado_esp32.py

class PipelineIntegradoESP32:
    def __init__(self):
        # Decisão: Pool de conexões para performance
        self.connection_pool = self._create_connection_pool()
        
        # Decisão: Cache inteligente para dispositivos
        self.device_cache = {}
        
        # Decisão: Thread pool para processamento assíncrono
        self.thread_pool = ThreadPoolExecutor(max_workers=10)
```

#### **Ligação Explícita:**
- **Arquitetura Original** → **Implementação Funcional**
- **Conceitos Abstratos** → **Código Executável**
- **Visão de Alto Nível** → **Detalhes de Implementação**

### **ENTREGA 2: Simulação e Coleta de Dados**

#### **Decisões Consolidadas:**
- **Simulação Wokwi**: Mantida como ambiente de desenvolvimento
- **Protocolo MQTT**: Implementado com QoS 1
- **Validação de Dados**: Expandida com regras de negócio
- **Qualidade de Dados**: Implementada com métricas

#### **Evolução na Entrega 3:**
```python
# ENTREGA 2: Simulação básica
# ENTREGA 3: Integração completa com pipeline

def processar_dados_mqtt(self, mensagem):
    # Decisão: Validação robusta de dados
    if not self._validar_dados(mensagem):
        self._log_erro("Dados inválidos recebidos")
        return
    
    # Decisão: Enriquecimento automático
    dados_enriquecidos = self._enriquecer_dados(mensagem)
    
    # Decisão: Processamento assíncrono
    self.thread_pool.submit(self._processar_async, dados_enriquecidos)
```

#### **Ligação Explícita:**
- **Simulação Básica** → **Integração Real**
- **Dados Sintéticos** → **Dados Validados e Enriquecidos**
- **Testes Isolados** → **Pipeline Integrado**

### **ENTREGA 3: Modelagem + ML**

#### **Decisões Consolidadas:**
- **Banco Relacional**: 11 tabelas normalizadas
- **Modelos ML**: Random Forest + Isolation Forest
- **Detecção de Anomalias**: Tempo real com thresholds
- **Persistência**: Robusta com auditoria

#### **Evolução na Entrega 3:**
```python
# ENTREGA 3: Implementação completa do ML
class SistemaMLCompleto:
    def __init__(self):
        # Decisão: Ensemble de modelos
        self.modelos = {
            'random_forest': RandomForestClassifier(),
            'isolation_forest': IsolationForest()
        }
        
        # Decisão: Features derivadas
        self.features_derivadas = [
            'temp_umidade_ratio',
            'luminosidade_normalizada',
            'vibracao_magnitude'
        ]
```

#### **Ligação Explícita:**
- **Modelagem Conceitual** → **Implementação Funcional**
- **Algoritmos Teóricos** → **Código Executável**
- **Métricas de Avaliação** → **Monitoramento Contínuo**

---

## 🏗️ Decisões de Arquitetura

### **1. Arquitetura de Microserviços**

#### **Decisão:**
Implementar arquitetura de microserviços para permitir escalabilidade e manutenibilidade.

#### **Justificativa:**
- **Escalabilidade**: Cada serviço pode ser escalado independentemente
- **Manutenibilidade**: Mudanças em um serviço não afetam outros
- **Tecnologia**: Diferentes serviços podem usar tecnologias diferentes
- **Falhas**: Isolamento de falhas entre serviços

#### **Implementação:**
```python
# Serviços identificados:
# 1. Coletor de Dados (ESP32/Wokwi)
# 2. Pipeline de Processamento
# 3. Serviço de Persistência
# 4. Serviço de ML
# 5. Serviço de Dashboard
# 6. Serviço de Alertas
```

### **2. Comunicação Assíncrona com MQTT**

#### **Decisão:**
Usar MQTT como protocolo principal para comunicação entre sensores e sistema.

#### **Justificativa:**
- **IoT Nativo**: Protocolo otimizado para IoT
- **Confiabilidade**: QoS 1 garante entrega
- **Escalabilidade**: Suporta milhares de dispositivos
- **Padrão**: Protocolo amplamente adotado

#### **Implementação:**
```python
# Configuração MQTT
MQTT_CONFIG = {
    'broker': 'broker.hivemq.com',
    'port': 1883,
    'topic': 'industrial/sensors/{device_id}/data',
    'qos': 1,  # At least once
    'retain': False
}
```

### **3. Banco de Dados Relacional**

#### **Decisão:**
Usar MySQL como banco de dados principal com 11 tabelas normalizadas.

#### **Justificativa:**
- **ACID**: Garantia de consistência
- **Relacionamentos**: Integridade referencial
- **Performance**: Índices otimizados
- **Escalabilidade**: Particionamento por ano

#### **Implementação:**
```sql
-- Estrutura das 11 tabelas
CREATE TABLE dispositivos (
    id VARCHAR(50) PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    tipo VARCHAR(50),
    localizacao VARCHAR(100),
    status ENUM('ativo', 'inativo', 'manutencao'),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Índices para performance
CREATE INDEX idx_dispositivos_status ON dispositivos(status);
CREATE INDEX idx_leituras_timestamp ON leituras_sensores(timestamp);
```

---

## 🔧 Decisões de Tecnologia

### **1. Stack Tecnológico**

#### **Backend: Python**
- **Justificativa**: Bibliotecas ricas para ML e IoT
- **Bibliotecas**: Pandas, NumPy, Scikit-learn, Flask
- **Performance**: Adequada para o volume de dados

#### **Banco de Dados: MySQL**
- **Justificativa**: Relacional, ACID, escalável
- **Recursos**: Índices, particionamento, stored procedures
- **Integração**: Fácil integração com Python

#### **ML: Scikit-learn**
- **Justificativa**: Biblioteca madura e confiável
- **Algoritmos**: Random Forest, Isolation Forest
- **Performance**: Otimizada para produção

#### **Visualização: Plotly + Bootstrap**
- **Justificativa**: Gráficos interativos e responsivos
- **Integração**: Fácil integração com Flask
- **UX**: Interface moderna e intuitiva

### **2. Padrões de Desenvolvimento**

#### **Padrão Repository**
```python
class DispositivoRepository:
    def __init__(self, connection_pool):
        self.connection_pool = connection_pool
    
    def criar(self, dispositivo):
        # Implementação do padrão Repository
        pass
    
    def buscar_por_id(self, id):
        # Implementação do padrão Repository
        pass
```

#### **Padrão Factory**
```python
class ModeloMLFactory:
    @staticmethod
    def criar_modelo(tipo):
        if tipo == 'random_forest':
            return RandomForestClassifier()
        elif tipo == 'isolation_forest':
            return IsolationForest()
        else:
            raise ValueError(f"Tipo de modelo não suportado: {tipo}")
```

#### **Padrão Observer**
```python
class SistemaAlertas:
    def __init__(self):
        self.observers = []
    
    def adicionar_observer(self, observer):
        self.observers.append(observer)
    
    def notificar_anomalia(self, anomalia):
        for observer in self.observers:
            observer.atualizar(anomalia)
```

---

## 🔗 Integração entre Componentes

### **1. Fluxo de Dados Completo**

#### **Coleta → Processamento → Persistência → ML → Visualização**

```mermaid
graph LR
    A[ESP32/Wokwi] --> B[MQTT Broker]
    B --> C[Pipeline Integrado]
    C --> D[Validação + Enriquecimento]
    D --> E[MySQL Database]
    E --> F[Modelos ML]
    F --> G[Detecção Anomalias]
    G --> H[Dashboard + Alertas]
```

#### **Implementação:**
```python
# Fluxo integrado no pipeline_integrado_esp32.py
def processar_mensagem_mqtt(self, mensagem):
    # 1. Receber dados MQTT
    dados = self._parse_mqtt_message(mensagem)
    
    # 2. Validar dados
    if not self._validar_dados(dados):
        return
    
    # 3. Enriquecer dados
    dados_enriquecidos = self._enriquecer_dados(dados)
    
    # 4. Persistir no banco
    self._persistir_dados(dados_enriquecidos)
    
    # 5. Inferência ML
    anomalia = self._detectar_anomalia_ml(dados_enriquecidos)
    
    # 6. Gerar alertas
    if anomalia:
        self._gerar_alerta(dados_enriquecidos, anomalia)
    
    # 7. Atualizar dashboard
    self._atualizar_dashboard(dados_enriquecidos)
```

### **2. Integração de Serviços**

#### **Serviço de Persistência**
```python
class ServicoPersistencia:
    def __init__(self, connection_pool):
        self.connection_pool = connection_pool
        self.dispositivo_repo = DispositivoRepository(connection_pool)
        self.leitura_repo = LeituraRepository(connection_pool)
        self.alerta_repo = AlertaRepository(connection_pool)
    
    def processar_leitura(self, dados):
        # Integração entre repositórios
        dispositivo = self.dispositivo_repo.buscar_ou_criar(dados['dispositivo_id'])
        leitura = self.leitura_repo.criar(dados)
        
        # Integração com ML
        anomalia = self._detectar_anomalia(dados)
        if anomalia:
            self.alerta_repo.criar(dispositivo.id, anomalia)
```

#### **Serviço de ML**
```python
class ServicoML:
    def __init__(self):
        self.modelos = self._carregar_modelos()
        self.scaler = self._carregar_scaler()
    
    def detectar_anomalia(self, dados):
        # Preparar features
        features = self._preparar_features(dados)
        
        # Normalizar dados
        features_scaled = self.scaler.transform([features])
        
        # Predição com ensemble
        predicao_rf = self.modelos['random_forest'].predict(features_scaled)
        predicao_if = self.modelos['isolation_forest'].predict(features_scaled)
        
        # Decisão final
        return predicao_rf[0] == 1 or predicao_if[0] == -1
```

### **3. Integração de APIs**

#### **API REST Unificada**
```python
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/api/kpis', methods=['GET'])
def obter_kpis():
    # Integração com serviço de persistência
    kpis = servico_persistencia.calcular_kpis()
    return jsonify(kpis)

@app.route('/api/alertas', methods=['GET'])
def obter_alertas():
    # Integração com serviço de alertas
    alertas = servico_alertas.listar_alertas()
    return jsonify(alertas)

@app.route('/api/graficos/temperatura', methods=['GET'])
def obter_grafico_temperatura():
    # Integração com serviço de visualização
    grafico = servico_visualizacao.gerar_grafico_temperatura()
    return jsonify(grafico)
```

---

## ⚙️ Decisões de Implementação

### **1. Gerenciamento de Conexões**

#### **Decisão:**
Usar pool de conexões para otimizar performance do banco de dados.

#### **Implementação:**
```python
class ConnectionPool:
    def __init__(self, max_connections=10):
        self.max_connections = max_connections
        self.connections = queue.Queue(maxsize=max_connections)
        self._initialize_connections()
    
    def get_connection(self):
        return self.connections.get()
    
    def return_connection(self, conn):
        self.connections.put(conn)
```

### **2. Cache Inteligente**

#### **Decisão:**
Implementar cache para dispositivos e sensores para reduzir consultas ao banco.

#### **Implementação:**
```python
class DeviceCache:
    def __init__(self, ttl=300):  # 5 minutos
        self.cache = {}
        self.ttl = ttl
    
    def get_device(self, device_id):
        if device_id in self.cache:
            device, timestamp = self.cache[device_id]
            if time.time() - timestamp < self.ttl:
                return device
        return None
    
    def set_device(self, device_id, device):
        self.cache[device_id] = (device, time.time())
```

### **3. Processamento Assíncrono**

#### **Decisão:**
Usar thread pool para processamento assíncrono de dados.

#### **Implementação:**
```python
from concurrent.futures import ThreadPoolExecutor

class PipelineIntegradoESP32:
    def __init__(self):
        self.thread_pool = ThreadPoolExecutor(max_workers=10)
    
    def processar_dados_async(self, dados):
        future = self.thread_pool.submit(self._processar_dados, dados)
        return future
```

### **4. Validação Robusta**

#### **Decisão:**
Implementar validação em múltiplas camadas para garantir qualidade dos dados.

#### **Implementação:**
```python
def validar_dados(self, dados):
    # Validação de estrutura
    if not self._validar_estrutura(dados):
        return False
    
    # Validação de tipos
    if not self._validar_tipos(dados):
        return False
    
    # Validação de ranges
    if not self._validar_ranges(dados):
        return False
    
    # Validação de qualidade
    if not self._validar_qualidade(dados):
        return False
    
    return True
```

---

## 📈 Evolução e Consolidação

### **1. Evolução das Entregas**

#### **Entrega 1 → Entrega 3:**
- **Conceito** → **Implementação**
- **Arquitetura** → **Código Executável**
- **Visão** → **Realidade**

#### **Entrega 2 → Entrega 3:**
- **Simulação** → **Integração Real**
- **Dados Sintéticos** → **Dados Validados**
- **Testes Isolados** → **Pipeline Integrado**

#### **Entrega 3 → Consolidação:**
- **Componentes Separados** → **Sistema Integrado**
- **Funcionalidades Básicas** → **Sistema Completo**
- **Prototipagem** → **Solução de Produção**

### **2. Consolidação Técnica**

#### **Arquitetura Unificada:**
```python
# Sistema consolidado
class SistemaIoTMonitoring:
    def __init__(self):
        # Integração de todos os componentes
        self.pipeline = PipelineIntegradoESP32()
        self.persistencia = ServicoPersistencia()
        self.ml = ServicoML()
        self.dashboard = ServicoDashboard()
        self.alertas = ServicoAlertas()
    
    def iniciar_sistema(self):
        # Orquestração completa
        self.pipeline.iniciar()
        self.persistencia.iniciar()
        self.ml.iniciar()
        self.dashboard.iniciar()
        self.alertas.iniciar()
```

#### **Fluxo de Dados Unificado:**
```python
# Fluxo completo integrado
def processar_dados_completos(self, dados_mqtt):
    # 1. Pipeline de processamento
    dados_processados = self.pipeline.processar(dados_mqtt)
    
    # 2. Persistência
    self.persistencia.salvar(dados_processados)
    
    # 3. ML e detecção
    anomalia = self.ml.detectar_anomalia(dados_processados)
    
    # 4. Alertas
    if anomalia:
        self.alertas.gerar_alerta(dados_processados, anomalia)
    
    # 5. Dashboard
    self.dashboard.atualizar(dados_processados)
```

### **3. Benefícios da Consolidação**

#### **Técnicos:**
- **Integração**: Todos os componentes trabalhando juntos
- **Performance**: Otimizações em todo o pipeline
- **Manutenibilidade**: Código bem estruturado e documentado
- **Escalabilidade**: Arquitetura preparada para crescimento

#### **Negócio:**
- **Valor**: Solução completa e funcional
- **ROI**: Retorno sobre investimento demonstrado
- **Competitividade**: Diferencial tecnológico
- **Futuro**: Base sólida para evolução

---

## 🎯 Conclusões

### **Decisões Técnicas Consolidadas:**
1. **Arquitetura de Microserviços** com comunicação assíncrona
2. **MQTT** como protocolo principal para IoT
3. **MySQL** como banco de dados relacional
4. **Python** como linguagem principal
5. **Scikit-learn** para Machine Learning
6. **Flask** para APIs REST
7. **Plotly + Bootstrap** para visualização

### **Integração Bem-Sucedida:**
- **Entrega 1**: Arquitetura implementada
- **Entrega 2**: Simulação integrada
- **Entrega 3**: ML e persistência funcionais
- **Consolidação**: Sistema completo e integrado

### **Resultado Final:**
Sistema IoT Monitoring **completo, funcional e integrado**, demonstrando o fluxo completo de dados desde a coleta até a visualização, com todas as peças trabalhando em conjunto de forma coesa e eficiente.

---

**Documentação de Decisões Técnicas - Enterprise Challenge Sprint 3 - Reply**
