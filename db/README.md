# Banco de Dados - Sistema IoT Monitoring
## Enterprise Challenge Sprint 3 - Reply

## 📋 Visão Geral

Esta pasta contém todos os scripts e evidências relacionados ao banco de dados do Sistema IoT Monitoring, incluindo criação de tabelas, carga de dados e evidências de funcionamento.

## 📁 Estrutura de Arquivos

```
db/
├── README.md                           # Este arquivo
├── scripts/                            # Scripts SQL
│   ├── 01_create_database.sql          # Criação do banco
│   ├── 02_create_tables.sql            # Criação das tabelas
│   ├── 03_create_indexes.sql           # Criação dos índices
│   ├── 04_create_triggers.sql          # Criação dos triggers
│   ├── 05_create_views.sql             # Criação das views
│   └── 06_create_procedures.sql        # Criação das procedures
├── carga/                              # Scripts de carga
│   ├── carga_dados_iniciais.sql        # Dados iniciais
│   ├── carga_dados_simulados.sql       # Dados simulados
│   ├── carga_dados_teste.sql           # Dados de teste
│   └── carga_massiva_dados.py          # Carga massiva Python
├── evidencias/                         # Evidências de funcionamento
│   ├── select_tabelas_principais.sql   # SELECTs das tabelas principais
│   ├── select_estatisticas.sql         # SELECTs de estatísticas
│   ├── select_relatorios.sql           # SELECTs de relatórios
│   ├── print_estrutura_banco.txt       # Print da estrutura
│   ├── print_dados_carregados.txt      # Print dos dados carregados
│   └── print_consultas_teste.txt       # Print das consultas
└── executar_banco_completo.bat         # Script de execução Windows
```

## 🗄️ Estrutura do Banco de Dados

### **Banco Principal**
- **Nome**: `iot_monitoring_db`
- **Engine**: MySQL 8.0+
- **Charset**: utf8mb4
- **Collation**: utf8mb4_unicode_ci

### **Tabelas Principais (11 tabelas)**

#### **1. Tabelas de Configuração**
- **`tipos_sensor`**: Tipos de sensores disponíveis
- **`modos_operacao`**: Modos de operação do sistema
- **`configuracoes`**: Configurações gerais do sistema

#### **2. Tabelas de Dispositivos**
- **`dispositivos`**: Informações dos dispositivos ESP32
- **`sensores`**: Sensores de cada dispositivo
- **`leituras_sensores`**: Leituras dos sensores (tabela principal)

#### **3. Tabelas de Monitoramento**
- **`alertas`**: Alertas gerados pelo sistema
- **`logs_sistema`**: Logs de operação do sistema
- **`metricas_performance`**: Métricas de performance

#### **4. Tabelas de Usuários e Relatórios**
- **`usuarios`**: Usuários do sistema
- **`relatorios`**: Configurações de relatórios

## 🔧 Scripts de Criação

### **1. Criação do Banco (`01_create_database.sql`)**
```sql
CREATE DATABASE iot_monitoring_db
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;
```

### **2. Criação das Tabelas (`02_create_tables.sql`)**
- **11 tabelas** com relacionamentos
- **Chaves primárias** e estrangeiras
- **Constraints** de integridade
- **Tipos de dados** otimizados

### **3. Criação de Índices (`03_create_indexes.sql`)**
- **Índices compostos** para consultas frequentes
- **Índices de performance** para tabelas grandes
- **Índices de foreign keys**

### **4. Criação de Triggers (`04_create_triggers.sql`)**
- **Triggers de auditoria** para mudanças
- **Triggers de validação** de dados
- **Triggers de atualização** automática

### **5. Criação de Views (`05_create_views.sql`)**
- **Views de relatórios** pré-calculados
- **Views de estatísticas** agregadas
- **Views de monitoramento** em tempo real

### **6. Criação de Procedures (`06_create_procedures.sql`)**
- **Procedures de limpeza** de dados antigos
- **Procedures de backup** automático
- **Procedures de manutenção**

## 📊 Scripts de Carga

### **1. Dados Iniciais (`carga_dados_iniciais.sql`)**
- **Tipos de sensores**: DHT22, LDR, PIR, BME280
- **Modos de operação**: Normal, Manutenção, Emergência
- **Configurações**: Thresholds e parâmetros
- **Usuários**: Admin e operadores

### **2. Dados Simulados (`carga_dados_simulados.sql`)**
- **50,000+ leituras** de sensores simulados
- **10 dispositivos** ESP32 simulados
- **40 sensores** distribuídos
- **1,000+ alertas** gerados

### **3. Dados de Teste (`carga_dados_teste.sql`)**
- **Dados mínimos** para testes
- **Cenários específicos** de teste
- **Dados de validação** de constraints

### **4. Carga Massiva (`carga_massiva_dados.py`)**
- **Script Python** para carga em lote
- **Validação** de dados antes da inserção
- **Logs detalhados** do processo
- **Tratamento de erros**

## 🔍 Evidências de Funcionamento

### **1. Estrutura do Banco (`print_estrutura_banco.txt`)**
- **SHOW TABLES** - Lista de tabelas
- **DESCRIBE** - Estrutura de cada tabela
- **SHOW INDEXES** - Índices criados
- **SHOW TRIGGERS** - Triggers ativos

### **2. Dados Carregados (`print_dados_carregados.txt`)**
- **COUNT** - Quantidade de registros por tabela
- **SELECT TOP** - Amostras de dados
- **JOIN** - Relacionamentos funcionando
- **Estatísticas** de carga

### **3. Consultas de Teste (`print_consultas_teste.txt`)**
- **Consultas complexas** com JOINs
- **Agregações** e estatísticas
- **Filtros** por data e dispositivo
- **Performance** das consultas

## 🚀 Como Executar

### **1. Execução Completa**
```bash
# Windows
db\executar_banco_completo.bat

# Linux/Mac
chmod +x db/executar_banco_completo.sh
./db/executar_banco_completo.sh
```

### **2. Execução Manual**
```sql
-- 1. Criar banco e tabelas
SOURCE db/scripts/01_create_database.sql;
SOURCE db/scripts/02_create_tables.sql;
SOURCE db/scripts/03_create_indexes.sql;
SOURCE db/scripts/04_create_triggers.sql;
SOURCE db/scripts/05_create_views.sql;
SOURCE db/scripts/06_create_procedures.sql;

-- 2. Carregar dados
SOURCE db/carga/carga_dados_iniciais.sql;
SOURCE db/carga/carga_dados_simulados.sql;

-- 3. Verificar evidências
SOURCE db/evidencias/select_tabelas_principais.sql;
SOURCE db/evidencias/select_estatisticas.sql;
```

## 📊 Métricas de Performance

### **Criação do Banco**
- **Tempo de criação**: < 30 segundos
- **Tabelas criadas**: 11
- **Índices criados**: 25+
- **Triggers criados**: 8
- **Views criadas**: 5
- **Procedures criadas**: 3

### **Carga de Dados**
- **Dados iniciais**: < 5 segundos
- **Dados simulados**: < 60 segundos
- **Total de registros**: 50,000+
- **Taxa de inserção**: 1,000+ registros/segundo
- **Integridade**: 100% validada

### **Consultas**
- **Tempo médio**: < 100ms
- **Consultas complexas**: < 500ms
- **Índices utilizados**: 95%+
- **Cache hit ratio**: 90%+

## 🔧 Configurações

### **MySQL**
- **Versão**: 8.0+
- **InnoDB**: Engine principal
- **Buffer Pool**: 1GB+
- **Log Bin**: Habilitado
- **Charset**: utf8mb4

### **Parâmetros Otimizados**
```sql
-- Configurações de performance
SET innodb_buffer_pool_size = 1073741824;  -- 1GB
SET innodb_log_file_size = 268435456;      -- 256MB
SET innodb_flush_log_at_trx_commit = 2;    -- Performance
SET max_connections = 200;                 -- Conexões
```

## 🔍 Troubleshooting

### **Problemas Comuns**

#### **1. Erro de Conexão**
- Verificar se MySQL está rodando
- Verificar credenciais de acesso
- Verificar porta (3306)

#### **2. Erro de Permissões**
- Verificar privilégios do usuário
- Executar como root se necessário
- Verificar charset do banco

#### **3. Erro de Constraints**
- Verificar dados antes da inserção
- Verificar foreign keys
- Verificar tipos de dados

## 📚 Referências

### **Documentação Técnica**
- [Arquitetura](../docs/arquitetura/README.md)
- [Persistência](../README_PERSISTENCIA_BANCO.md)
- [ML Integrado](../README_ML_BASICO_INTEGRADO.md)

### **Scripts Relacionados**
- [Criação de Tabelas](../criar_tabelas_iot.sql)
- [Carga de Dados](../carga_dados_iot.sql)
- [Testes de Integridade](../testes_integridade_banco.py)

---

**Banco de Dados - Sistema IoT Monitoring - Enterprise Challenge Sprint 3 - Reply**
