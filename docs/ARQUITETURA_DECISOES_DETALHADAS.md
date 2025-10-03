# Arquitetura e Decisões Detalhadas - Sistema IoT Monitoring
## Enterprise Challenge Sprint 3 - Reply

## 🎯 Visão Geral

Este documento detalha as **decisões arquiteturais** tomadas ao longo do desenvolvimento do sistema IoT Monitoring, explicando o **porquê** de cada decisão e como ela se integra com o todo.

## 📋 Estrutura do Documento

1. [Decisões de Arquitetura de Alto Nível](#decisões-de-arquitetura-de-alto-nível)
2. [Decisões de Tecnologia](#decisões-de-tecnologia)
3. [Decisões de Integração](#decisões-de-integração)
4. [Decisões de Performance](#decisões-de-performance)
5. [Decisões de Segurança](#decisões-de-segurança)
6. [Decisões de Escalabilidade](#decisões-de-escalabilidade)

---

## 🏗️ Decisões de Arquitetura de Alto Nível

### **1. Arquitetura de Microserviços**

#### **Decisão:**
Implementar arquitetura de microserviços para o sistema IoT Monitoring.

#### **Justificativa:**
- **Escalabilidade Independente**: Cada serviço pode ser escalado conforme demanda
- **Manutenibilidade**: Mudanças em um serviço não afetam outros
- **Tecnologia**: Diferentes serviços podem usar tecnologias diferentes
- **Falhas**: Isolamento de falhas entre serviços
- **Desenvolvimento**: Equipes podem trabalhar independentemente

#### **Implementação:**
```python
# Serviços identificados e implementados:
class ServicosIoT:
    def __init__(self):
        self.coletor = ServicoColeta()           # Coleta de dados ESP32
        self.pipeline = ServicoPipeline()        # Processamento de dados
        self.persistencia = ServicoPersistencia() # Armazenamento
        self.ml = ServicoML()                    # Machine Learning
        self.dashboard = ServicoDashboard()      # Visualização
        self.alertas = ServicoAlertas()          # Notificações
        self.monitoramento = ServicoMonitoramento() # Observabilidade
```

#### **Benefícios Observados:**
- **Desenvolvimento Paralelo**: Equipes podem trabalhar em serviços diferentes
- **Deploy Independente**: Cada serviço pode ser atualizado separadamente
- **Escalabilidade Granular**: Apenas serviços com alta demanda são escalados
- **Resiliência**: Falha em um serviço não derruba o sistema todo

### **2. Comunicação Assíncrona**

#### **Decisão:**
Usar comunicação assíncrona entre microserviços, com MQTT como protocolo principal.

#### **Justificativa:**
- **Desacoplamento**: Serviços não precisam estar disponíveis simultaneamente
- **Resiliência**: Mensagens são persistidas até serem processadas
- **Escalabilidade**: Fácil adição de novos consumidores
- **IoT Nativo**: MQTT é otimizado para dispositivos IoT
- **Padrão**: Protocolo amplamente adotado na indústria

#### **Implementação:**
```python
# Configuração MQTT
MQTT_CONFIG = {
    'broker': 'broker.hivemq.com',
    'port': 1883,
    'topic_pattern': 'industrial/sensors/{device_id}/data',
    'qos': 1,  # At least once delivery
    'retain': False,
    'clean_session': True
}

# Tópicos definidos:
TOPICS = {
    'sensor_data': 'industrial/sensors/{device_id}/data',
    'alerts': 'industrial/alerts/{device_id}',
    'commands': 'industrial/commands/{device_id}',
    'status': 'industrial/status/{device_id}'
}
```

#### **Benefícios Observados:**
- **Desacoplamento**: Serviços podem ser desenvolvidos independentemente
- **Resiliência**: Mensagens não são perdidas em caso de falha
- **Escalabilidade**: Fácil adição de novos dispositivos
- **Padrão**: Uso de protocolo padrão da indústria

### **3. Camadas de Abstração**

#### **Decisão:**
Implementar camadas de abstração para separar responsabilidades.

#### **Justificativa:**
- **Separação de Responsabilidades**: Cada camada tem uma responsabilidade específica
- **Manutenibilidade**: Mudanças em uma camada não afetam outras
- **Testabilidade**: Cada camada pode ser testada independentemente
- **Reutilização**: Camadas podem ser reutilizadas em diferentes contextos

#### **Implementação:**
```python
# Camadas implementadas:
class CamadasSistema:
    def __init__(self):
        # Camada 1: Coleta
        self.coleta = CamadaColeta()
        
        # Camada 2: Processamento
        self.processamento = CamadaProcessamento()
        
        # Camada 3: Persistência
        self.persistencia = CamadaPersistencia()
        
        # Camada 4: Analytics
        self.analytics = CamadaAnalytics()
        
        # Camada 5: Apresentação
        self.apresentacao = CamadaApresentacao()

# Exemplo de implementação de camada:
class CamadaProcessamento:
    def __init__(self):
        self.validadores = [ValidadorEstrutura(), ValidadorTipos()]
        self.enriquecedor = EnriquecedorDados()
        self.transformador = TransformadorDados()
    
    def processar(self, dados):
        # Validação
        if not self._validar(dados):
            raise DadosInvalidosException()
        
        # Enriquecimento
        dados_enriquecidos = self.enriquecedor.enriquecer(dados)
        
        # Transformação
        dados_transformados = self.transformador.transformar(dados_enriquecidos)
        
        return dados_transformados
```

---

## 🔧 Decisões de Tecnologia

### **1. Linguagem de Programação: Python**

#### **Decisão:**
Usar Python como linguagem principal para o sistema.

#### **Justificativa:**
- **Bibliotecas Ricas**: Pandas, NumPy, Scikit-learn para ML e dados
- **IoT**: Bibliotecas para MQTT, serial, etc.
- **Rapidez de Desenvolvimento**: Sintaxe clara e expressiva
- **Comunidade**: Grande comunidade e suporte
- **Integração**: Fácil integração com diferentes sistemas

#### **Implementação:**
```python
# Stack tecnológico escolhido:
TECNOLOGIAS = {
    'linguagem': 'Python 3.8+',
    'framework_web': 'Flask',
    'banco_dados': 'MySQL',
    'mqtt': 'paho-mqtt',
    'ml': 'scikit-learn',
    'visualizacao': 'Plotly',
    'frontend': 'Bootstrap + HTML/CSS/JS'
}
```

### **2. Banco de Dados: MySQL**

#### **Decisão:**
Usar MySQL como banco de dados principal.

#### **Justificativa:**
- **ACID**: Garantia de consistência transacional
- **Relacional**: Suporte a relacionamentos complexos
- **Performance**: Índices otimizados para consultas
- **Escalabilidade**: Suporte a particionamento e replicação
- **Padrão**: Banco amplamente adotado na indústria

#### **Implementação:**
```sql
-- Estrutura do banco implementada:
CREATE DATABASE iot_monitoring;

-- Tabelas principais:
CREATE TABLE dispositivos (
    id VARCHAR(50) PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    tipo VARCHAR(50),
    localizacao VARCHAR(100),
    status ENUM('ativo', 'inativo', 'manutencao'),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Índices para performance:
CREATE INDEX idx_dispositivos_status ON dispositivos(status);
CREATE INDEX idx_dispositivos_tipo ON dispositivos(tipo);
CREATE INDEX idx_leituras_timestamp ON leituras_sensores(timestamp);
CREATE INDEX idx_leituras_dispositivo ON leituras_sensores(dispositivo_id);
```

### **3. Machine Learning: Scikit-learn**

#### **Decisão:**
Usar Scikit-learn para implementação de modelos de ML.

#### **Justificativa:**
- **Maturidade**: Biblioteca madura e estável
- **Algoritmos**: Amplo conjunto de algoritmos disponíveis
- **Performance**: Otimizada para produção
- **Documentação**: Excelente documentação e exemplos
- **Integração**: Fácil integração com Python

#### **Implementação:**
```python
# Modelos implementados:
class ModelosML:
    def __init__(self):
        self.random_forest = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
        
        self.isolation_forest = IsolationForest(
            contamination=0.1,
            random_state=42
        )
        
        self.scaler = StandardScaler()
    
    def treinar(self, X, y):
        # Treinamento dos modelos
        X_scaled = self.scaler.fit_transform(X)
        self.random_forest.fit(X_scaled, y)
        self.isolation_forest.fit(X_scaled)
    
    def predizer(self, X):
        # Predição com ensemble
        X_scaled = self.scaler.transform(X)
        pred_rf = self.random_forest.predict(X_scaled)
        pred_if = self.isolation_forest.predict(X_scaled)
        
        # Combinação dos resultados
        return self._combinar_predicoes(pred_rf, pred_if)
```

---

## 🔗 Decisões de Integração

### **1. Padrão Repository**

#### **Decisão:**
Implementar padrão Repository para abstração de acesso a dados.

#### **Justificativa:**
- **Abstração**: Separação entre lógica de negócio e acesso a dados
- **Testabilidade**: Fácil criação de mocks para testes
- **Flexibilidade**: Possibilidade de trocar implementação de banco
- **Manutenibilidade**: Centralização da lógica de acesso a dados

#### **Implementação:**
```python
# Interface do repositório:
class Repository(ABC):
    @abstractmethod
    def criar(self, entidade):
        pass
    
    @abstractmethod
    def buscar_por_id(self, id):
        pass
    
    @abstractmethod
    def listar(self, filtros=None):
        pass
    
    @abstractmethod
    def atualizar(self, entidade):
        pass
    
    @abstractmethod
    def deletar(self, id):
        pass

# Implementação concreta:
class DispositivoRepository(Repository):
    def __init__(self, connection_pool):
        self.connection_pool = connection_pool
    
    def criar(self, dispositivo):
        with self.connection_pool.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO dispositivos (id, nome, tipo, localizacao, status) VALUES (?, ?, ?, ?, ?)",
                (dispositivo.id, dispositivo.nome, dispositivo.tipo, 
                 dispositivo.localizacao, dispositivo.status)
            )
            conn.commit()
    
    def buscar_por_id(self, id):
        with self.connection_pool.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM dispositivos WHERE id = ?", (id,))
            row = cursor.fetchone()
            return Dispositivo.from_row(row) if row else None
```

### **2. Padrão Factory**

#### **Decisão:**
Usar padrão Factory para criação de objetos complexos.

#### **Justificativa:**
- **Encapsulamento**: Lógica de criação encapsulada
- **Flexibilidade**: Fácil adição de novos tipos
- **Consistência**: Criação padronizada de objetos
- **Testabilidade**: Fácil criação de mocks

#### **Implementação:**
```python
# Factory para modelos ML:
class ModeloMLFactory:
    @staticmethod
    def criar_modelo(tipo, parametros=None):
        if tipo == 'random_forest':
            return RandomForestClassifier(**parametros or {})
        elif tipo == 'isolation_forest':
            return IsolationForest(**parametros or {})
        elif tipo == 'svm':
            return SVC(**parametros or {})
        else:
            raise ValueError(f"Tipo de modelo não suportado: {tipo}")

# Factory para validadores:
class ValidadorFactory:
    @staticmethod
    def criar_validador(tipo):
        if tipo == 'estrutura':
            return ValidadorEstrutura()
        elif tipo == 'tipos':
            return ValidadorTipos()
        elif tipo == 'ranges':
            return ValidadorRanges()
        else:
            raise ValueError(f"Tipo de validador não suportado: {tipo}")
```

### **3. Padrão Observer**

#### **Decisão:**
Implementar padrão Observer para sistema de alertas.

#### **Justificativa:**
- **Desacoplamento**: Observadores não conhecem o sujeito
- **Extensibilidade**: Fácil adição de novos observadores
- **Flexibilidade**: Diferentes tipos de notificações
- **Manutenibilidade**: Mudanças em observadores não afetam o sujeito

#### **Implementação:**
```python
# Interface do observador:
class Observer(ABC):
    @abstractmethod
    def atualizar(self, dados):
        pass

# Sujeito observável:
class SistemaAlertas:
    def __init__(self):
        self.observers = []
    
    def adicionar_observer(self, observer):
        self.observers.append(observer)
    
    def remover_observer(self, observer):
        self.observers.remove(observer)
    
    def notificar_anomalia(self, anomalia):
        for observer in self.observers:
            observer.atualizar(anomalia)

# Implementações concretas:
class EmailObserver(Observer):
    def atualizar(self, anomalia):
        self.enviar_email(anomalia)

class SlackObserver(Observer):
    def atualizar(self, anomalia):
        self.enviar_slack(anomalia)

class TeamsObserver(Observer):
    def atualizar(self, anomalia):
        self.enviar_teams(anomalia)
```

---

## ⚡ Decisões de Performance

### **1. Pool de Conexões**

#### **Decisão:**
Implementar pool de conexões para o banco de dados.

#### **Justificativa:**
- **Performance**: Reutilização de conexões evita overhead
- **Escalabilidade**: Controle do número máximo de conexões
- **Recursos**: Uso eficiente de recursos do sistema
- **Confiabilidade**: Gerenciamento automático de conexões

#### **Implementação:**
```python
class ConnectionPool:
    def __init__(self, max_connections=10, min_connections=2):
        self.max_connections = max_connections
        self.min_connections = min_connections
        self.connections = queue.Queue(maxsize=max_connections)
        self.active_connections = 0
        self.lock = threading.Lock()
        self._initialize_connections()
    
    def _initialize_connections(self):
        for _ in range(self.min_connections):
            conn = self._create_connection()
            self.connections.put(conn)
            self.active_connections += 1
    
    def get_connection(self):
        try:
            return self.connections.get_nowait()
        except queue.Empty:
            with self.lock:
                if self.active_connections < self.max_connections:
                    conn = self._create_connection()
                    self.active_connections += 1
                    return conn
                else:
                    return self.connections.get(timeout=5)
    
    def return_connection(self, conn):
        if conn.is_connected():
            self.connections.put(conn)
        else:
            with self.lock:
                self.active_connections -= 1
```

### **2. Cache Inteligente**

#### **Decisão:**
Implementar cache para dados frequentemente acessados.

#### **Justificativa:**
- **Performance**: Redução de consultas ao banco
- **Latência**: Acesso mais rápido a dados
- **Recursos**: Redução de carga no banco
- **Escalabilidade**: Melhor performance com mais usuários

#### **Implementação:**
```python
class DeviceCache:
    def __init__(self, ttl=300):  # 5 minutos
        self.cache = {}
        self.ttl = ttl
        self.lock = threading.RLock()
    
    def get_device(self, device_id):
        with self.lock:
            if device_id in self.cache:
                device, timestamp = self.cache[device_id]
                if time.time() - timestamp < self.ttl:
                    return device
                else:
                    del self.cache[device_id]
            return None
    
    def set_device(self, device_id, device):
        with self.lock:
            self.cache[device_id] = (device, time.time())
    
    def invalidate(self, device_id):
        with self.lock:
            if device_id in self.cache:
                del self.cache[device_id]
```

### **3. Processamento Assíncrono**

#### **Decisão:**
Usar thread pool para processamento assíncrono.

#### **Justificativa:**
- **Throughput**: Processamento paralelo de dados
- **Responsividade**: Interface não bloqueia durante processamento
- **Escalabilidade**: Fácil ajuste do número de threads
- **Recursos**: Uso eficiente de CPU

#### **Implementação:**
```python
from concurrent.futures import ThreadPoolExecutor

class PipelineIntegradoESP32:
    def __init__(self, max_workers=10):
        self.thread_pool = ThreadPoolExecutor(max_workers=max_workers)
        self.futures = []
    
    def processar_dados_async(self, dados):
        future = self.thread_pool.submit(self._processar_dados, dados)
        self.futures.append(future)
        return future
    
    def _processar_dados(self, dados):
        # Processamento pesado em thread separada
        dados_validados = self._validar_dados(dados)
        dados_enriquecidos = self._enriquecer_dados(dados_validados)
        anomalia = self._detectar_anomalia(dados_enriquecidos)
        
        return {
            'dados': dados_enriquecidos,
            'anomalia': anomalia,
            'timestamp': datetime.now().isoformat()
        }
```

---

## 🔒 Decisões de Segurança

### **1. Autenticação JWT**

#### **Decisão:**
Usar JWT (JSON Web Tokens) para autenticação.

#### **Justificativa:**
- **Stateless**: Não requer armazenamento no servidor
- **Escalabilidade**: Fácil distribuição entre servidores
- **Padrão**: Protocolo amplamente adotado
- **Segurança**: Assinatura digital para verificação

#### **Implementação:**
```python
import jwt
from datetime import datetime, timedelta

class AutenticadorJWT:
    def __init__(self, secret_key):
        self.secret_key = secret_key
        self.algorithm = 'HS256'
    
    def gerar_token(self, usuario_id, roles):
        payload = {
            'usuario_id': usuario_id,
            'roles': roles,
            'exp': datetime.utcnow() + timedelta(hours=24),
            'iat': datetime.utcnow()
        }
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
    
    def verificar_token(self, token):
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            raise TokenExpiradoException()
        except jwt.InvalidTokenError:
            raise TokenInvalidoException()
```

### **2. Controle de Acesso Baseado em Roles (RBAC)**

#### **Decisão:**
Implementar RBAC para controle de acesso granular.

#### **Justificativa:**
- **Segurança**: Controle granular de acesso
- **Flexibilidade**: Fácil adição de novos roles
- **Manutenibilidade**: Centralização de permissões
- **Auditoria**: Rastreamento de acessos

#### **Implementação:**
```python
class RBAC:
    def __init__(self):
        self.roles = {
            'admin': ['read', 'write', 'delete', 'manage_users'],
            'operator': ['read', 'write'],
            'viewer': ['read'],
            'analyst': ['read', 'analyze']
        }
    
    def verificar_permissao(self, usuario, acao):
        roles = usuario.get('roles', [])
        for role in roles:
            if acao in self.roles.get(role, []):
                return True
        return False
    
    def autorizar(self, usuario, acao, recurso):
        if not self.verificar_permissao(usuario, acao):
            raise AcessoNegadoException(f"Usuário {usuario['id']} não tem permissão para {acao} em {recurso}")
        return True
```

### **3. Criptografia de Dados**

#### **Decisão:**
Implementar criptografia para dados sensíveis.

#### **Justificativa:**
- **Confidencialidade**: Proteção de dados sensíveis
- **Compliance**: Atendimento a regulamentações
- **Segurança**: Proteção contra vazamentos
- **Integridade**: Verificação de integridade dos dados

#### **Implementação:**
```python
from cryptography.fernet import Fernet

class Criptografia:
    def __init__(self, key):
        self.cipher = Fernet(key)
    
    def criptografar(self, dados):
        dados_bytes = json.dumps(dados).encode()
        dados_criptografados = self.cipher.encrypt(dados_bytes)
        return base64.b64encode(dados_criptografados).decode()
    
    def descriptografar(self, dados_criptografados):
        dados_bytes = base64.b64decode(dados_criptografados.encode())
        dados_descriptografados = self.cipher.decrypt(dados_bytes)
        return json.loads(dados_descriptografados.decode())
```

---

## 📈 Decisões de Escalabilidade

### **1. Particionamento de Dados**

#### **Decisão:**
Implementar particionamento por ano para tabelas de leituras.

#### **Justificativa:**
- **Performance**: Consultas mais rápidas em dados recentes
- **Manutenção**: Fácil remoção de dados antigos
- **Escalabilidade**: Distribuição de dados entre partições
- **Backup**: Backup incremental por partição

#### **Implementação:**
```sql
-- Particionamento por ano:
CREATE TABLE leituras_sensores (
    id INT AUTO_INCREMENT,
    dispositivo_id VARCHAR(50),
    timestamp TIMESTAMP,
    temperatura DECIMAL(5,2),
    umidade DECIMAL(5,2),
    -- outros campos...
    PRIMARY KEY (id, timestamp)
) PARTITION BY RANGE (YEAR(timestamp)) (
    PARTITION p2023 VALUES LESS THAN (2024),
    PARTITION p2024 VALUES LESS THAN (2025),
    PARTITION p2025 VALUES LESS THAN (2026),
    PARTITION p_future VALUES LESS THAN MAXVALUE
);
```

### **2. Load Balancing**

#### **Decisão:**
Implementar load balancing para distribuição de carga.

#### **Justificativa:**
- **Performance**: Distribuição de requisições
- **Disponibilidade**: Redundância de servidores
- **Escalabilidade**: Fácil adição de servidores
- **Resiliência**: Falha de um servidor não derruba o sistema

#### **Implementação:**
```python
# Configuração de load balancing:
LOAD_BALANCER_CONFIG = {
    'strategy': 'round_robin',  # ou 'least_connections', 'weighted'
    'servers': [
        {'host': 'server1.example.com', 'port': 5000, 'weight': 1},
        {'host': 'server2.example.com', 'port': 5000, 'weight': 1},
        {'host': 'server3.example.com', 'port': 5000, 'weight': 2}
    ],
    'health_check': {
        'interval': 30,  # segundos
        'timeout': 5,    # segundos
        'path': '/health'
    }
}
```

### **3. Cache Distribuído**

#### **Decisão:**
Implementar cache distribuído com Redis.

#### **Justificativa:**
- **Performance**: Cache compartilhado entre servidores
- **Escalabilidade**: Fácil distribuição de cache
- **Consistência**: Dados consistentes entre servidores
- **Persistência**: Cache persistente entre reinicializações

#### **Implementação:**
```python
import redis

class CacheDistribuido:
    def __init__(self, host='localhost', port=6379, db=0):
        self.redis = redis.Redis(host=host, port=port, db=db)
    
    def get(self, key):
        dados = self.redis.get(key)
        return json.loads(dados) if dados else None
    
    def set(self, key, value, ttl=300):
        dados = json.dumps(value)
        self.redis.setex(key, ttl, dados)
    
    def delete(self, key):
        self.redis.delete(key)
    
    def invalidate_pattern(self, pattern):
        keys = self.redis.keys(pattern)
        if keys:
            self.redis.delete(*keys)
```

---

## 🎯 Resumo das Decisões

### **Decisões Arquiteturais:**
1. **Microserviços** para escalabilidade e manutenibilidade
2. **Comunicação Assíncrona** com MQTT para desacoplamento
3. **Camadas de Abstração** para separação de responsabilidades

### **Decisões Tecnológicas:**
1. **Python** como linguagem principal
2. **MySQL** como banco de dados relacional
3. **Scikit-learn** para Machine Learning
4. **Flask** para APIs REST

### **Decisões de Integração:**
1. **Padrão Repository** para abstração de dados
2. **Padrão Factory** para criação de objetos
3. **Padrão Observer** para sistema de alertas

### **Decisões de Performance:**
1. **Pool de Conexões** para otimização de banco
2. **Cache Inteligente** para redução de consultas
3. **Processamento Assíncrono** para throughput

### **Decisões de Segurança:**
1. **JWT** para autenticação stateless
2. **RBAC** para controle de acesso granular
3. **Criptografia** para dados sensíveis

### **Decisões de Escalabilidade:**
1. **Particionamento** para performance de consultas
2. **Load Balancing** para distribuição de carga
3. **Cache Distribuído** para escalabilidade horizontal

---

**Arquitetura e Decisões Detalhadas - Enterprise Challenge Sprint 3 - Reply**
