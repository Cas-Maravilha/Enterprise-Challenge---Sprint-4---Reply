# Explicação de Chaves e Restrições - Sistema IoT Monitoring
## Enterprise Challenge Sprint 3 - Reply

## 🎯 Visão Geral

Este documento explica detalhadamente as **chaves primárias**, **chaves estrangeiras** e **restrições de integridade** implementadas no banco de dados do sistema IoT Monitoring, garantindo a consistência e performance das consultas.

## 📋 Estrutura do Documento

1. [Chaves Primárias](#chaves-primárias)
2. [Chaves Estrangeiras](#chaves-estrangeiras)
3. [Restrições de Integridade](#restrições-de-integridade)
4. [Índices para Performance](#índices-para-performance)
5. [Triggers e Procedimentos](#triggers-e-procedimentos)
6. [Particionamento](#particionamento)

---

## 🔑 Chaves Primárias

### **1. Tabela `dispositivos`**
```sql
PRIMARY KEY (`id_dispositivo`)
```
- **Tipo**: AUTO_INCREMENT INT
- **Função**: Identificador único de cada dispositivo ESP32
- **Justificativa**: Garante unicidade e facilita relacionamentos
- **Performance**: Índice clusterizado (InnoDB)

### **2. Tabela `tipos_sensor`**
```sql
PRIMARY KEY (`id_tipo_sensor`)
```
- **Tipo**: AUTO_INCREMENT INT
- **Função**: Identificador único de cada tipo de sensor
- **Justificativa**: Normalização para evitar redundância
- **Exemplos**: DHT22, LDR, PIR, BME280

### **3. Tabela `sensores`**
```sql
PRIMARY KEY (`id_sensor`)
```
- **Tipo**: AUTO_INCREMENT INT
- **Função**: Identificador único de cada sensor físico
- **Justificativa**: Cada sensor tem configurações específicas
- **Relacionamento**: Muitos sensores por dispositivo

### **4. Tabela `leituras_sensores`**
```sql
PRIMARY KEY (`id_leitura`)
```
- **Tipo**: BIGINT AUTO_INCREMENT
- **Função**: Identificador único de cada leitura
- **Justificativa**: Alto volume de dados (milhões de registros)
- **Performance**: BIGINT para suportar grande escala

### **5. Tabela `alertas`**
```sql
PRIMARY KEY (`id_alerta`)
```
- **Tipo**: BIGINT AUTO_INCREMENT
- **Função**: Identificador único de cada alerta
- **Justificativa**: Alto volume de alertas gerados
- **Relacionamento**: Muitos alertas por dispositivo

### **6. Tabela `usuarios`**
```sql
PRIMARY KEY (`id_usuario`)
```
- **Tipo**: AUTO_INCREMENT INT
- **Função**: Identificador único de cada usuário
- **Justificativa**: Controle de acesso e auditoria
- **Segurança**: Base para autenticação

### **7. Tabela `logs_sistema`**
```sql
PRIMARY KEY (`id_log`)
```
- **Tipo**: BIGINT AUTO_INCREMENT
- **Função**: Identificador único de cada log
- **Justificativa**: Alto volume de logs de auditoria
- **Compliance**: Rastreabilidade de operações

---

## 🔗 Chaves Estrangeiras

### **1. Relacionamento `sensores` → `dispositivos`**
```sql
CONSTRAINT `fk_sensores_dispositivos`
    FOREIGN KEY (`id_dispositivo`)
    REFERENCES `dispositivos` (`id_dispositivo`)
    ON DELETE CASCADE
    ON UPDATE CASCADE
```
- **Função**: Cada sensor pertence a um dispositivo
- **Integridade**: Não permite sensores órfãos
- **Cascata**: Se dispositivo for deletado, sensores também são
- **Atualização**: Se ID do dispositivo mudar, sensores são atualizados

### **2. Relacionamento `sensores` → `tipos_sensor`**
```sql
CONSTRAINT `fk_sensores_tipos_sensor`
    FOREIGN KEY (`id_tipo_sensor`)
    REFERENCES `tipos_sensor` (`id_tipo_sensor`)
    ON DELETE CASCADE
    ON UPDATE CASCADE
```
- **Função**: Cada sensor tem um tipo específico
- **Integridade**: Garante que tipo existe antes de criar sensor
- **Normalização**: Evita duplicação de informações de tipos

### **3. Relacionamento `leituras_sensores` → `sensores`**
```sql
CONSTRAINT `fk_leituras_sensores`
    FOREIGN KEY (`id_sensor`)
    REFERENCES `sensores` (`id_sensor`)
    ON DELETE CASCADE
    ON UPDATE CASCADE
```
- **Função**: Cada leitura pertence a um sensor
- **Integridade**: Não permite leituras órfãs
- **Performance**: Índice para consultas por sensor
- **Cascata**: Se sensor for deletado, leituras também são

### **4. Relacionamento `alertas` → `dispositivos`**
```sql
CONSTRAINT `fk_alertas_dispositivos`
    FOREIGN KEY (`id_dispositivo`)
    REFERENCES `dispositivos` (`id_dispositivo`)
    ON DELETE CASCADE
    ON UPDATE CASCADE
```
- **Função**: Cada alerta está associado a um dispositivo
- **Integridade**: Garante que dispositivo existe
- **Cascata**: Se dispositivo for deletado, alertas também são

### **5. Relacionamento `alertas` → `sensores`**
```sql
CONSTRAINT `fk_alertas_sensores`
    FOREIGN KEY (`id_sensor`)
    REFERENCES `sensores` (`id_sensor`)
    ON DELETE SET NULL
    ON UPDATE CASCADE
```
- **Função**: Alertas podem estar associados a sensores específicos
- **Integridade**: Sensor pode ser NULL (alertas gerais)
- **Cascata**: Se sensor for deletado, alerta fica com sensor NULL

### **6. Relacionamento `alertas` → `modos_operacao`**
```sql
CONSTRAINT `fk_alertas_modos_operacao`
    FOREIGN KEY (`id_modo`)
    REFERENCES `modos_operacao` (`id_modo`)
    ON DELETE CASCADE
    ON UPDATE CASCADE
```
- **Função**: Cada alerta tem um modo de operação
- **Integridade**: Garante que modo existe
- **Classificação**: Normal, Alerta, Falha, etc.

### **7. Relacionamento `configuracoes_limites` → `sensores`**
```sql
CONSTRAINT `fk_configuracoes_limites_sensores`
    FOREIGN KEY (`id_sensor`)
    REFERENCES `sensores` (`id_sensor`)
    ON DELETE CASCADE
    ON UPDATE CASCADE
```
- **Função**: Cada configuração de limite pertence a um sensor
- **Integridade**: Garante que sensor existe
- **Cascata**: Se sensor for deletado, configurações também são

### **8. Relacionamento `logs_sistema` → `usuarios`**
```sql
CONSTRAINT `fk_logs_sistema_usuarios`
    FOREIGN KEY (`id_usuario`)
    REFERENCES `usuarios` (`id_usuario`)
    ON DELETE SET NULL
    ON UPDATE CASCADE
```
- **Função**: Logs podem estar associados a usuários
- **Integridade**: Usuário pode ser NULL (logs do sistema)
- **Auditoria**: Rastreabilidade de ações por usuário

### **9. Relacionamento `dashboards` → `usuarios`**
```sql
CONSTRAINT `fk_dashboards_usuarios`
    FOREIGN KEY (`id_usuario`)
    REFERENCES `usuarios` (`id_usuario`)
    ON DELETE CASCADE
    ON UPDATE CASCADE
```
- **Função**: Cada dashboard pertence a um usuário
- **Integridade**: Garante que usuário existe
- **Personalização**: Dashboards personalizados por usuário

### **10. Relacionamento `relatorios` → `usuarios`**
```sql
CONSTRAINT `fk_relatorios_usuarios`
    FOREIGN KEY (`id_usuario`)
    REFERENCES `usuarios` (`id_usuario`)
    ON DELETE CASCADE
    ON UPDATE CASCADE
```
- **Função**: Cada relatório pertence a um usuário
- **Integridade**: Garante que usuário existe
- **Personalização**: Relatórios personalizados por usuário

---

## 🛡️ Restrições de Integridade

### **1. Restrições UNIQUE**

#### **MAC Address Único**
```sql
UNIQUE INDEX `uk_dispositivos_mac_address` (`mac_address` ASC)
```
- **Função**: Garante que cada dispositivo tenha MAC único
- **Justificativa**: MAC é identificador único de hardware
- **Integridade**: Evita duplicação de dispositivos

#### **Email Único**
```sql
UNIQUE INDEX `uk_usuarios_email` (`email` ASC)
```
- **Função**: Garante que cada usuário tenha email único
- **Justificativa**: Email é usado para login
- **Segurança**: Evita contas duplicadas

#### **Nome de Tipo de Sensor Único**
```sql
UNIQUE INDEX `uk_tipos_sensor_nome` (`nome` ASC)
```
- **Função**: Garante que cada tipo tenha nome único
- **Justificativa**: Evita confusão entre tipos
- **Integridade**: Facilita identificação

#### **Nome de Modo de Operação Único**
```sql
UNIQUE INDEX `uk_modos_operacao_nome` (`nome` ASC)
```
- **Função**: Garante que cada modo tenha nome único
- **Justificativa**: Evita confusão entre modos
- **Integridade**: Facilita classificação

### **2. Restrições CHECK (Simuladas com ENUM)**

#### **Status de Dispositivo**
```sql
`status` ENUM('ativo', 'inativo', 'manutencao') NOT NULL DEFAULT 'ativo'
```
- **Função**: Limita valores válidos para status
- **Justificativa**: Controle de estado operacional
- **Integridade**: Evita valores inválidos

#### **Severidade de Alertas**
```sql
`severidade` ENUM('baixa', 'media', 'alta', 'critica') NOT NULL
```
- **Função**: Classifica nível de criticidade
- **Justificativa**: Priorização de alertas
- **Integridade**: Valores padronizados

#### **Perfil de Usuário**
```sql
`perfil` ENUM('admin', 'operador', 'visualizador') NOT NULL
```
- **Função**: Define nível de acesso
- **Justificativa**: Controle de permissões
- **Segurança**: RBAC (Role-Based Access Control)

#### **Qualidade de Dados**
```sql
`qualidade_dados` ENUM('excelente', 'bom', 'regular', 'ruim') NOT NULL DEFAULT 'bom'
```
- **Função**: Classifica qualidade das leituras
- **Justificativa**: Controle de qualidade
- **Integridade**: Valores padronizados

### **3. Restrições NOT NULL**

#### **Campos Obrigatórios**
```sql
`nome` VARCHAR(100) NOT NULL
`mac_address` VARCHAR(17) NOT NULL
`timestamp_datetime` TIMESTAMP NOT NULL
```
- **Função**: Garante que campos essenciais não sejam nulos
- **Justificativa**: Dados críticos para funcionamento
- **Integridade**: Evita registros incompletos

### **4. Restrições de Formato**

#### **MAC Address**
```sql
`mac_address` VARCHAR(17) NOT NULL
```
- **Formato**: XX:XX:XX:XX:XX:XX
- **Validação**: 17 caracteres com dois pontos
- **Exemplo**: AA:BB:CC:DD:EE:FF

#### **IP Address**
```sql
`ip_address` VARCHAR(15) NULL DEFAULT NULL
```
- **Formato**: XXX.XXX.XXX.XXX
- **Validação**: Máximo 15 caracteres
- **Exemplo**: 192.168.1.100

#### **Email**
```sql
`email` VARCHAR(255) NOT NULL
```
- **Formato**: user@domain.com
- **Validação**: Máximo 255 caracteres
- **Exemplo**: admin@iot.com

---

## 📊 Índices para Performance

### **1. Índices Simples**

#### **Status de Dispositivos**
```sql
INDEX `idx_dispositivos_status` (`status` ASC)
```
- **Função**: Consultas por status
- **Performance**: Filtros rápidos
- **Uso**: "Dispositivos ativos", "Em manutenção"

#### **Timestamp de Leituras**
```sql
INDEX `idx_leituras_timestamp` (`timestamp_datetime` ASC)
```
- **Função**: Consultas temporais
- **Performance**: Range scans eficientes
- **Uso**: "Leituras do último dia", "Tendências"

#### **Qualidade de Dados**
```sql
INDEX `idx_leituras_qualidade` (`qualidade_dados` ASC)
```
- **Função**: Filtros por qualidade
- **Performance**: Consultas de qualidade
- **Uso**: "Leituras excelentes", "Dados ruins"

### **2. Índices Compostos**

#### **Sensor + Timestamp + Qualidade**
```sql
INDEX `idx_leituras_sensor_data_qualidade` (`id_sensor`, `timestamp_datetime`, `qualidade_dados`)
```
- **Função**: Consultas complexas por sensor
- **Performance**: Cobertura de múltiplas colunas
- **Uso**: "Leituras de sensor X no período Y com qualidade Z"

#### **Status + Data + Severidade de Alertas**
```sql
INDEX `idx_alertas_status_data_severidade` (`status`, `timestamp_alerta`, `severidade`)
```
- **Função**: Consultas de alertas complexas
- **Performance**: Filtros múltiplos eficientes
- **Uso**: "Alertas ativos críticos do último dia"

#### **Dispositivo + Status + Localização**
```sql
INDEX `idx_dispositivos_status_local` (`status`, `localizacao`)
```
- **Função**: Consultas por local e status
- **Performance**: Filtros geográficos
- **Uso**: "Dispositivos ativos na sala X"

### **3. Índices de Cobertura**

#### **Sensor + Dispositivo + Tipo**
```sql
INDEX `idx_sensores_dispositivo_tipo` (`id_dispositivo`, `id_tipo_sensor`)
```
- **Função**: Consultas de sensores por dispositivo
- **Performance**: Evita lookups adicionais
- **Uso**: "Todos os sensores de temperatura do dispositivo X"

---

## ⚡ Triggers e Procedimentos

### **1. Trigger de Atualização de Conexão**
```sql
CREATE TRIGGER `tr_atualizar_ultima_conexao`
AFTER INSERT ON `leituras_sensores`
FOR EACH ROW
BEGIN
    UPDATE dispositivos 
    SET ultima_conexao = CURRENT_TIMESTAMP
    WHERE id_dispositivo = (
        SELECT id_dispositivo 
        FROM sensores 
        WHERE id_sensor = NEW.id_sensor
    );
END
```
- **Função**: Atualiza última conexão automaticamente
- **Trigger**: AFTER INSERT
- **Performance**: Mantém dados atualizados
- **Uso**: Monitoramento de dispositivos online

### **2. Procedimento de Geração de Leituras**
```sql
CREATE PROCEDURE GerarLeiturasSimuladas(
    IN p_id_sensor INT,
    IN p_num_leituras INT,
    IN p_data_inicio TIMESTAMP
)
```
- **Função**: Gera dados de teste realísticos
- **Parâmetros**: Sensor, quantidade, data inicial
- **Performance**: Inserção em lote
- **Uso**: Testes e demonstrações

---

## 📈 Particionamento

### **1. Particionamento por Ano**
```sql
PARTITION BY RANGE (UNIX_TIMESTAMP(timestamp_datetime)) (
    PARTITION p2024 VALUES LESS THAN (UNIX_TIMESTAMP('2025-01-01')),
    PARTITION p2025 VALUES LESS THAN (UNIX_TIMESTAMP('2026-01-01')),
    PARTITION p2026 VALUES LESS THAN (UNIX_TIMESTAMP('2027-01-01')),
    PARTITION p_future VALUES LESS THAN MAXVALUE
)
```
- **Função**: Divide dados por ano
- **Performance**: Consultas mais rápidas
- **Manutenção**: Fácil remoção de dados antigos
- **Escalabilidade**: Suporte a crescimento

### **2. Benefícios do Particionamento**
- **Performance**: Consultas em partições específicas
- **Manutenção**: Backup/restore por partição
- **Escalabilidade**: Distribuição de dados
- **Arquivo**: Dados antigos podem ser removidos

---

## 🔍 Consultas Otimizadas

### **1. Consulta de Leituras Recentes**
```sql
SELECT l.*, s.nome as sensor_nome, d.nome as dispositivo_nome
FROM leituras_sensores l
JOIN sensores s ON l.id_sensor = s.id_sensor
JOIN dispositivos d ON s.id_dispositivo = d.id_dispositivo
WHERE l.timestamp_datetime >= DATE_SUB(NOW(), INTERVAL 1 HOUR)
ORDER BY l.timestamp_datetime DESC;
```
- **Índices Usados**: `idx_leituras_timestamp`, `fk_leituras_sensores`
- **Performance**: Range scan eficiente
- **Uso**: Dashboard em tempo real

### **2. Consulta de Alertas Ativos**
```sql
SELECT a.*, d.nome as dispositivo_nome, s.nome as sensor_nome
FROM alertas a
JOIN dispositivos d ON a.id_dispositivo = d.id_dispositivo
LEFT JOIN sensores s ON a.id_sensor = s.id_sensor
WHERE a.status = 'ativo'
ORDER BY a.timestamp_alerta DESC;
```
- **Índices Usados**: `idx_alertas_status`, `fk_alertas_dispositivos`
- **Performance**: Filtro por status
- **Uso**: Sistema de notificações

### **3. Consulta de Estatísticas por Dispositivo**
```sql
SELECT 
    d.nome,
    COUNT(DISTINCT s.id_sensor) as total_sensores,
    COUNT(l.id_leitura) as total_leituras,
    AVG(l.valor_numerico) as media_valor
FROM dispositivos d
JOIN sensores s ON d.id_dispositivo = s.id_dispositivo
LEFT JOIN leituras_sensores l ON s.id_sensor = l.id_sensor
WHERE l.timestamp_datetime >= DATE_SUB(NOW(), INTERVAL 1 DAY)
GROUP BY d.id_dispositivo, d.nome;
```
- **Índices Usados**: `idx_leituras_timestamp`, `idx_sensores_dispositivo_tipo`
- **Performance**: Agregação eficiente
- **Uso**: Relatórios de performance

---

## 🎯 Resumo das Restrições

### **Integridade Referencial**
- **10 Chaves Estrangeiras**: Garantem relacionamentos válidos
- **Cascata**: Mantém consistência ao deletar/atualizar
- **NULL Controlado**: Campos opcionais bem definidos

### **Integridade de Dados**
- **4 Chaves Únicas**: Evitam duplicação
- **ENUMs**: Valores padronizados e válidos
- **NOT NULL**: Campos obrigatórios protegidos

### **Performance**
- **15+ Índices**: Consultas otimizadas
- **Índices Compostos**: Consultas complexas eficientes
- **Particionamento**: Escalabilidade temporal

### **Auditoria**
- **Triggers**: Atualizações automáticas
- **Logs**: Rastreabilidade completa
- **Timestamps**: Controle temporal

---

**Explicação de Chaves e Restrições - Enterprise Challenge Sprint 3 - Reply**
