# Documentação do Banco de Dados - Sistema IoT Monitoring Sprint 3

## 📋 Visão Geral

Este documento descreve o banco de dados completo para o sistema de monitoramento IoT com ESP32 e sensores. O banco foi projetado para suportar coleta de dados em tempo real, análise de anomalias, sistema de alertas e visualização de dados.

## 🎯 Objetivos do Banco de Dados

- **Coleta de Dados**: Armazenar leituras de sensores em tempo real
- **Monitoramento**: Rastrear status de dispositivos e sensores
- **Alertas**: Sistema configurável de notificações
- **Auditoria**: Log completo de atividades do sistema
- **Escalabilidade**: Suporte a múltiplos dispositivos e sensores
- **Performance**: Otimizado para consultas frequentes

## 🏗️ Arquitetura do Banco

### Tecnologias Utilizadas
- **SGBD**: MySQL 8.0+
- **Charset**: UTF8MB4 (suporte completo a Unicode)
- **Engine**: InnoDB (transações ACID)
- **Particionamento**: Por ano para tabela de leituras

### Características Principais
- **11 Tabelas** principais
- **Particionamento** por ano na tabela de leituras
- **Índices otimizados** para consultas frequentes
- **Stored Procedures** para operações complexas
- **Triggers** para atualizações automáticas
- **Views** para facilitar consultas

## 📊 Estrutura das Tabelas

### 1. DISPOSITIVOS
**Propósito**: Gerencia dispositivos ESP32 conectados

| Campo | Tipo | Descrição | Justificativa |
|-------|------|-----------|---------------|
| `id_dispositivo` | INT PK | Identificador único | Chave primária |
| `nome` | VARCHAR(100) | Nome do dispositivo | Identificação amigável |
| `mac_address` | VARCHAR(17) UK | Endereço MAC | Identificação única de hardware |
| `ip_address` | VARCHAR(15) | IP atual | Rastreamento de conectividade |
| `localizacao` | VARCHAR(200) | Local físico | Contexto geográfico |
| `status` | ENUM | Estado operacional | Monitoramento de saúde |
| `ultima_conexao` | TIMESTAMP | Última comunicação | Detecção de falhas |
| `versao_firmware` | VARCHAR(20) | Versão do firmware | Controle de versões |

### 2. TIPOS_SENSOR
**Propósito**: Catálogo de tipos de sensores

| Campo | Tipo | Descrição | Justificativa |
|-------|------|-----------|---------------|
| `id_tipo_sensor` | INT PK | Identificador único | Chave primária |
| `nome` | VARCHAR(50) UK | Nome do tipo | Padronização |
| `unidade_medida` | VARCHAR(20) | Unidade de medida | Consistência de dados |
| `faixa_min/max` | DECIMAL | Faixa operacional | Validação de dados |
| `precisao` | DECIMAL | Precisão do sensor | Qualidade dos dados |

### 3. SENSORES
**Propósito**: Sensores físicos instalados

| Campo | Tipo | Descrição | Justificativa |
|-------|------|-----------|---------------|
| `id_sensor` | INT PK | Identificador único | Chave primária |
| `id_dispositivo` | INT FK | Dispositivo pai | Relacionamento |
| `id_tipo_sensor` | INT FK | Tipo do sensor | Classificação |
| `pino_analogico/digital` | INT | Configuração de hardware | Mapeamento físico |
| `calibracao_min/max` | DECIMAL | Valores de calibração | Precisão individual |

### 4. LEITURAS_SENSORES
**Propósito**: Dados coletados (tabela principal)

| Campo | Tipo | Descrição | Justificativa |
|-------|------|-----------|---------------|
| `id_leitura` | BIGINT PK | Identificador único | Chave primária |
| `id_sensor` | INT FK | Sensor origem | Relacionamento |
| `timestamp_unix` | DECIMAL(15,3) | Timestamp Unix | Precisão temporal |
| `timestamp_datetime` | TIMESTAMP | Data/hora legível | Consultas humanas |
| `valor_numerico/booleano/string` | Vários | Valores lidos | Flexibilidade de tipos |
| `qualidade_dados` | ENUM | Classificação | Controle de qualidade |
| `anomalia_detectada` | BOOLEAN | Flag de anomalia | Detecção automática |

**Particionamento**: Por ano para otimizar consultas históricas

### 5. ALERTAS
**Propósito**: Sistema de notificações

| Campo | Tipo | Descrição | Justificativa |
|-------|------|-----------|---------------|
| `id_alerta` | BIGINT PK | Identificador único | Chave primária |
| `tipo_alerta` | ENUM | Categoria | Classificação |
| `severidade` | ENUM | Nível de criticidade | Priorização |
| `valor_atual/limite` | DECIMAL | Valores que geraram alerta | Contexto |
| `status` | ENUM | Estado do alerta | Rastreamento |

### 6. CONFIGURACOES_LIMITES
**Propósito**: Limites para alertas

| Campo | Tipo | Descrição | Justificativa |
|-------|------|-----------|---------------|
| `id_configuracao` | INT PK | Identificador único | Chave primária |
| `id_sensor` | INT FK | Sensor configurado | Relacionamento |
| `tipo_limite` | ENUM | Tipo (min/max/variação) | Flexibilidade |
| `valor_limite` | DECIMAL | Valor limite | Configuração |
| `severidade` | ENUM | Nível de alerta | Escalonamento |

### 7. USUARIOS
**Propósito**: Gestão de usuários

| Campo | Tipo | Descrição | Justificativa |
|-------|------|-----------|---------------|
| `id_usuario` | INT PK | Identificador único | Chave primária |
| `email` | VARCHAR(255) UK | Login único | Autenticação |
| `perfil` | ENUM | Nível de acesso | Controle de permissões |
| `senha_hash` | VARCHAR(255) | Hash da senha | Segurança |
| `token_reset_senha` | VARCHAR(255) | Token de recuperação | Funcionalidade |

### 8. LOGS_SISTEMA
**Propósito**: Auditoria de atividades

| Campo | Tipo | Descrição | Justificativa |
|-------|------|-----------|---------------|
| `id_log` | BIGINT PK | Identificador único | Chave primária |
| `id_usuario` | INT FK | Usuário responsável | Rastreabilidade |
| `acao` | VARCHAR(100) | Tipo de ação | Classificação |
| `dados_anteriores/novos` | JSON | Mudanças realizadas | Auditoria completa |
| `ip_origem` | VARCHAR(45) | IP de origem | Segurança |

### 9. DASHBOARDS
**Propósito**: Configurações de interface

| Campo | Tipo | Descrição | Justificativa |
|-------|------|-----------|---------------|
| `id_dashboard` | INT PK | Identificador único | Chave primária |
| `id_usuario` | INT FK | Proprietário | Personalização |
| `configuracoes` | JSON | Layout e widgets | Flexibilidade |
| `publico` | BOOLEAN | Compartilhamento | Colaboração |

### 10. RELATORIOS
**Propósito**: Relatórios automáticos

| Campo | Tipo | Descrição | Justificativa |
|-------|------|-----------|---------------|
| `id_relatorio` | INT PK | Identificador único | Chave primária |
| `tipo_relatorio` | ENUM | Frequência | Classificação |
| `frequencia` | VARCHAR(50) | Expressão cron | Agendamento |
| `proxima_execucao` | TIMESTAMP | Próxima execução | Controle temporal |

## 🔗 Relacionamentos

### Relacionamentos Principais
1. **DISPOSITIVOS (1) → SENSORES (N)**: Um dispositivo possui múltiplos sensores
2. **TIPOS_SENSOR (1) → SENSORES (N)**: Um tipo pode ser usado em múltiplos sensores
3. **SENSORES (1) → LEITURAS_SENSORES (N)**: Um sensor gera múltiplas leituras
4. **SENSORES (1) → CONFIGURACOES_LIMITES (N)**: Um sensor pode ter múltiplas configurações
5. **DISPOSITIVOS/SENSORES (1) → ALERTAS (N)**: Alertas podem ser gerados por dispositivos ou sensores

### Chaves Estrangeiras
- `sensores.id_dispositivo` → `dispositivos.id_dispositivo`
- `sensores.id_tipo_sensor` → `tipos_sensor.id_tipo_sensor`
- `leituras_sensores.id_sensor` → `sensores.id_sensor`
- `alertas.id_dispositivo` → `dispositivos.id_dispositivo`
- `alertas.id_sensor` → `sensores.id_sensor`
- `configuracoes_limites.id_sensor` → `sensores.id_sensor`

## 📈 Otimizações de Performance

### Índices Criados
```sql
-- Índices principais
CREATE INDEX idx_sensor_timestamp ON leituras_sensores(id_sensor, timestamp_datetime);
CREATE INDEX idx_timestamp ON leituras_sensores(timestamp_datetime);
CREATE INDEX idx_qualidade ON leituras_sensores(qualidade_dados);
CREATE INDEX idx_anomalia ON leituras_sensores(anomalia_detectada);

-- Índices compostos
CREATE INDEX idx_leituras_sensor_data ON leituras_sensores(id_sensor, timestamp_datetime, qualidade_dados);
CREATE INDEX idx_alertas_status_data ON alertas(status, timestamp_alerta, severidade);
CREATE INDEX idx_dispositivos_status_local ON dispositivos(status, localizacao);
```

### Particionamento
A tabela `leituras_sensores` é particionada por ano:
- **p2024**: Dados de 2024
- **p2025**: Dados de 2025
- **p2026**: Dados de 2026
- **p_future**: Dados futuros

**Benefícios**:
- Consultas mais rápidas em dados históricos
- Manutenção facilitada (drop de partições antigas)
- Paralelização de operações

## 🔧 Stored Procedures

### sp_inserir_leitura
**Propósito**: Inserir leitura de sensor com validação
**Parâmetros**:
- `p_id_sensor`: ID do sensor
- `p_timestamp_unix`: Timestamp Unix
- `p_valor_numerico`: Valor numérico lido
- `p_qualidade_dados`: Qualidade dos dados

**Funcionalidades**:
- Converte timestamp Unix para datetime
- Detecta anomalias automaticamente
- Retorna ID da leitura inserida

### sp_verificar_limites
**Propósito**: Verificar limites e criar alertas
**Parâmetros**:
- `p_id_sensor`: ID do sensor
- `p_valor`: Valor a verificar

**Funcionalidades**:
- Consulta limites configurados
- Cria alertas quando limites são excedidos
- Suporta limites mínimos e máximos

## 🎯 Views Criadas

### vw_leituras_completas
**Propósito**: Consulta unificada de leituras com informações contextuais
**Campos**: dispositivo, localização, tipo_sensor, valores, qualidade, modo_operacao

### vw_alertas_ativos
**Propósito**: Lista de alertas ativos com contexto
**Campos**: dispositivo, sensor, tipo, severidade, valores, timestamp

## 🔄 Triggers

### tr_atualizar_ultima_conexao
**Evento**: AFTER INSERT ON leituras_sensores
**Ação**: Atualiza `ultima_conexao` do dispositivo relacionado
**Justificativa**: Manter status de conectividade atualizado automaticamente

## 📊 Dados de Exemplo

### Tipos de Sensores Inseridos
- **DHT22**: Temperatura e umidade (-40°C a 80°C)
- **LDR**: Luminosidade (0-1023 lux)
- **PIR**: Movimento (boolean)
- **Pressão**: Barométrica (0-10 bar)
- **Vibração**: Triaxial (-2g a +2g)
- **Nível**: Ultrassônico (0-200 cm)

### Modos de Operação
- **Normal**: Sistema operando normalmente (#28a745)
- **Alerta**: Valores próximos aos limites (#ffc107)
- **Falha**: Valores críticos ou falhas (#dc3545)

### Usuário Padrão
- **Email**: admin@iot.com
- **Perfil**: Administrador
- **Senha**: Hash bcrypt (deve ser alterada)

## 🚀 Scripts de Criação

### Execução do Script Principal
```bash
mysql -u root -p < database_schema.sql
```

### Verificação da Criação
```sql
-- Verificar tabelas criadas
SHOW TABLES;

-- Verificar estrutura de uma tabela
DESCRIBE leituras_sensores;

-- Verificar particionamento
SELECT 
    TABLE_NAME,
    PARTITION_NAME,
    PARTITION_DESCRIPTION
FROM INFORMATION_SCHEMA.PARTITIONS 
WHERE TABLE_NAME = 'leituras_sensores';
```

## 🔍 Consultas Úteis

### Leituras Recentes
```sql
SELECT 
    d.nome as dispositivo,
    s.nome as sensor,
    ls.timestamp_datetime,
    ls.valor_numerico,
    ls.qualidade_dados
FROM leituras_sensores ls
JOIN sensores s ON ls.id_sensor = s.id_sensor
JOIN dispositivos d ON s.id_dispositivo = d.id_dispositivo
WHERE ls.timestamp_datetime >= DATE_SUB(NOW(), INTERVAL 1 HOUR)
ORDER BY ls.timestamp_datetime DESC;
```

### Alertas Ativos
```sql
SELECT 
    a.titulo,
    d.nome as dispositivo,
    a.severidade,
    a.timestamp_alerta
FROM alertas a
JOIN dispositivos d ON a.id_dispositivo = d.id_dispositivo
WHERE a.status = 'ativo'
ORDER BY a.severidade DESC, a.timestamp_alerta DESC;
```

### Estatísticas por Sensor
```sql
SELECT 
    s.nome as sensor,
    COUNT(*) as total_leituras,
    AVG(ls.valor_numerico) as media_valor,
    MAX(ls.valor_numerico) as max_valor,
    MIN(ls.valor_numerico) as min_valor
FROM leituras_sensores ls
JOIN sensores s ON ls.id_sensor = s.id_sensor
WHERE ls.timestamp_datetime >= DATE_SUB(NOW(), INTERVAL 24 HOUR)
GROUP BY s.id_sensor, s.nome;
```

## 🔧 Manutenção

### Limpeza de Dados Antigos
```sql
-- Remover leituras com mais de 1 ano
DELETE FROM leituras_sensores 
WHERE timestamp_datetime < DATE_SUB(NOW(), INTERVAL 1 YEAR);

-- Remover logs com mais de 6 meses
DELETE FROM logs_sistema 
WHERE timestamp_log < DATE_SUB(NOW(), INTERVAL 6 MONTH);
```

### Backup
```bash
# Backup completo
mysqldump -u root -p iot_monitoring_db > backup_iot_$(date +%Y%m%d).sql

# Backup apenas estrutura
mysqldump -u root -p --no-data iot_monitoring_db > estrutura_iot.sql
```

## 📈 Integração com Ferramentas de Visualização

### Grafana
**Conexão**: MySQL Data Source
**Dashboards Sugeridos**:
- Monitoramento em tempo real
- Análise de tendências
- Alertas e notificações
- Status de dispositivos

### Power BI
**Conexão**: MySQL Connector
**Relatórios Sugeridos**:
- Análise de performance
- Relatórios executivos
- Análise de anomalias
- KPIs operacionais

### Tableau
**Conexão**: MySQL via ODBC
**Visualizações Sugeridas**:
- Mapas de calor por localização
- Gráficos de correlação
- Análise temporal avançada
- Dashboards interativos

## 🔒 Considerações de Segurança

### Controle de Acesso
- Usuários com perfis específicos
- Senhas com hash bcrypt
- Tokens de recuperação com expiração
- Logs de auditoria completos

### Dados Sensíveis
- Senhas sempre hasheadas
- Tokens com expiração
- Logs de IP para rastreamento
- Backup criptografado recomendado

## 📋 Próximos Passos

1. **Implementar** scripts de migração
2. **Configurar** backup automático
3. **Criar** dashboards no Grafana
4. **Implementar** API REST para inserção de dados
5. **Configurar** monitoramento de performance
6. **Implementar** limpeza automática de dados antigos

## 📞 Suporte

Para dúvidas sobre o banco de dados:
- Consulte a documentação técnica
- Verifique os logs do sistema
- Execute consultas de diagnóstico
- Contate a equipe de desenvolvimento

---

**Versão**: 1.0  
**Data**: 2025-01-11  
**Autor**: Sistema IoT Monitoring - Sprint 3  
**Status**: Produção
