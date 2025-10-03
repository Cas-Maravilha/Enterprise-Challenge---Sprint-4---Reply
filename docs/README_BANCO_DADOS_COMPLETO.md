# Sistema de Banco de Dados - IoT Monitoring
## Enterprise Challenge Sprint 3 - Reply

## 🎯 Visão Geral

Este módulo implementa o **sistema completo de banco de dados** para o IoT Monitoring, utilizando o DER e tabelas definidos anteriormente, com scripts SQL de criação, carga e explicação detalhada das chaves e restrições de integridade.

## 📋 Componentes do Sistema

### **1. Script de Criação**
- **Arquivo**: `criar_tabelas_iot.sql`
- **Função**: Criação do banco e todas as tabelas
- **Inclui**: Chaves, índices, triggers, dados iniciais

### **2. Script de Carga**
- **Arquivo**: `carga_dados_iot.sql`
- **Função**: Carga de dados de exemplo e teste
- **Inclui**: Dados simulados, configurações, alertas

### **3. Explicação de Chaves**
- **Arquivo**: `explicacao_chaves_restricoes.md`
- **Função**: Documentação detalhada das restrições
- **Inclui**: Chaves primárias, estrangeiras, índices

### **4. Testes de Integridade**
- **Arquivo**: `testes_integridade_banco.py`
- **Função**: Validação automática da integridade
- **Inclui**: 7 tipos de testes diferentes

### **5. Scripts de Execução**
- **Windows**: `executar_banco_completo.bat`
- **Linux/Mac**: `executar_banco_completo.sh`
- **Função**: Automação da execução

## 🗄️ Estrutura do Banco de Dados

### **Tabelas Principais (11 tabelas)**

#### **1. `dispositivos`**
- **Função**: Armazena informações dos dispositivos ESP32
- **Chave Primária**: `id_dispositivo` (AUTO_INCREMENT)
- **Chave Única**: `mac_address` (único)
- **Campos**: nome, mac_address, ip_address, localizacao, status, etc.

#### **2. `tipos_sensor`**
- **Função**: Catálogo dos tipos de sensores
- **Chave Primária**: `id_tipo_sensor` (AUTO_INCREMENT)
- **Chave Única**: `nome` (único)
- **Campos**: nome, descricao, unidade_medida, faixa_min, faixa_max, etc.

#### **3. `sensores`**
- **Função**: Sensores instalados nos dispositivos
- **Chave Primária**: `id_sensor` (AUTO_INCREMENT)
- **Chaves Estrangeiras**: `id_dispositivo`, `id_tipo_sensor`
- **Campos**: nome, pino_analogico, pino_digital, calibracao_min, etc.

#### **4. `leituras_sensores`**
- **Função**: Dados coletados pelos sensores (tabela principal)
- **Chave Primária**: `id_leitura` (BIGINT AUTO_INCREMENT)
- **Chave Estrangeira**: `id_sensor`
- **Particionamento**: Por ano (2024, 2025, 2026, futuro)
- **Campos**: timestamp_unix, timestamp_datetime, valor_numerico, etc.

#### **5. `modos_operacao`**
- **Função**: Estados de operação do sistema
- **Chave Primária**: `id_modo` (AUTO_INCREMENT)
- **Chave Única**: `nome` (único)
- **Campos**: nome, descricao, cor_indicador, ativo, etc.

#### **6. `alertas`**
- **Função**: Sistema de alertas e notificações
- **Chave Primária**: `id_alerta` (BIGINT AUTO_INCREMENT)
- **Chaves Estrangeiras**: `id_dispositivo`, `id_sensor`, `id_modo`
- **Campos**: tipo_alerta, severidade, titulo, descricao, etc.

#### **7. `configuracoes_limites`**
- **Função**: Configurações de limites para alertas
- **Chave Primária**: `id_configuracao` (AUTO_INCREMENT)
- **Chave Estrangeira**: `id_sensor`
- **Campos**: tipo_limite, valor_limite, severidade, ativo, etc.

#### **8. `usuarios`**
- **Função**: Usuários do sistema
- **Chave Primária**: `id_usuario` (AUTO_INCREMENT)
- **Chave Única**: `email` (único)
- **Campos**: nome, email, senha_hash, perfil, ativo, etc.

#### **9. `logs_sistema`**
- **Função**: Log de atividades do sistema
- **Chave Primária**: `id_log` (BIGINT AUTO_INCREMENT)
- **Chave Estrangeira**: `id_usuario` (opcional)
- **Campos**: acao, tabela_afetada, dados_anteriores, dados_novos, etc.

#### **10. `dashboards`**
- **Função**: Configurações de dashboards personalizados
- **Chave Primária**: `id_dashboard` (AUTO_INCREMENT)
- **Chave Estrangeira**: `id_usuario`
- **Campos**: nome, descricao, configuracoes (JSON), publico, etc.

#### **11. `relatorios`**
- **Função**: Configurações de relatórios automáticos
- **Chave Primária**: `id_relatorio` (AUTO_INCREMENT)
- **Chave Estrangeira**: `id_usuario`
- **Campos**: nome, tipo_relatorio, configuracoes (JSON), frequencia, etc.

## 🔑 Chaves e Restrições

### **Chaves Primárias (11)**
- **Função**: Identificadores únicos para cada tabela
- **Tipo**: AUTO_INCREMENT (INT ou BIGINT)
- **Performance**: Índices clusterizados (InnoDB)

### **Chaves Estrangeiras (10)**
- **Função**: Garantem integridade referencial
- **Cascata**: DELETE CASCADE, UPDATE CASCADE
- **NULL Controlado**: Campos opcionais bem definidos

### **Restrições UNIQUE (4)**
- **MAC Address**: Único por dispositivo
- **Email**: Único por usuário
- **Nome Tipo Sensor**: Único por tipo
- **Nome Modo Operação**: Único por modo

### **Restrições ENUM (5)**
- **Status Dispositivo**: ativo, inativo, manutencao
- **Severidade Alertas**: baixa, media, alta, critica
- **Perfil Usuário**: admin, operador, visualizador
- **Qualidade Dados**: excelente, bom, regular, ruim
- **Status Alertas**: ativo, resolvido, ignorado

### **Restrições NOT NULL**
- **Campos Obrigatórios**: nome, mac_address, email, timestamps
- **Integridade**: Evita registros incompletos
- **Validação**: Dados críticos protegidos

## 📊 Índices para Performance

### **Índices Simples (15+)**
- **Status**: Filtros por estado operacional
- **Timestamp**: Consultas temporais eficientes
- **Qualidade**: Filtros por qualidade dos dados
- **Severidade**: Classificação de alertas

### **Índices Compostos (5)**
- **Sensor + Timestamp + Qualidade**: Consultas complexas
- **Status + Data + Severidade**: Alertas filtrados
- **Dispositivo + Status + Local**: Consultas geográficas
- **Sensor + Dispositivo + Tipo**: Relacionamentos

### **Índices de Cobertura**
- **Evitam Lookups**: Consultas mais eficientes
- **Performance**: Menos I/O de disco
- **Escalabilidade**: Suporte a grandes volumes

## ⚡ Triggers e Procedimentos

### **Trigger de Atualização de Conexão**
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
- **Performance**: Mantém dados atualizados
- **Uso**: Monitoramento de dispositivos online

### **Procedimento de Geração de Leituras**
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

## 📈 Particionamento

### **Particionamento por Ano**
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

## 🚀 Como Executar

### **Windows:**
```bash
executar_banco_completo.bat
```

### **Linux/Mac:**
```bash
chmod +x executar_banco_completo.sh
./executar_banco_completo.sh
```

### **Execução Manual:**
```bash
# 1. Criar banco e tabelas
mysql -u root -p < criar_tabelas_iot.sql

# 2. Carregar dados
mysql -u root -p < carga_dados_iot.sql

# 3. Executar testes
python testes_integridade_banco.py
```

## 🧪 Testes de Integridade

### **Teste 1: Chaves Primárias**
- **Função**: Verifica se todas as tabelas têm registros
- **Validação**: Contagem de registros por tabela
- **Resultado**: OK se todas as tabelas têm dados

### **Teste 2: Chaves Estrangeiras**
- **Função**: Verifica integridade referencial
- **Validação**: Contagem de registros órfãos
- **Resultado**: OK se não há órfãos

### **Teste 3: Restrições UNIQUE**
- **Função**: Verifica unicidade de campos
- **Validação**: Contagem de duplicatas
- **Resultado**: OK se não há duplicatas

### **Teste 4: Restrições ENUM**
- **Função**: Verifica valores válidos
- **Validação**: Valores dentro dos ENUMs
- **Resultado**: OK se todos os valores são válidos

### **Teste 5: Restrições NOT NULL**
- **Função**: Verifica campos obrigatórios
- **Validação**: Contagem de valores nulos
- **Resultado**: OK se não há nulos em campos obrigatórios

### **Teste 6: Consistência dos Dados**
- **Função**: Verifica consistência geral
- **Validação**: Dados mínimos esperados
- **Resultado**: OK se dados são consistentes

### **Teste 7: Performance dos Índices**
- **Função**: Verifica performance das consultas
- **Validação**: Tempo de execução das consultas
- **Resultado**: OK se consultas são rápidas

## 📊 Dados de Exemplo

### **Dispositivos (7 dispositivos)**
- **Sala de Controle**: ESP32-Sala-01
- **Garagem**: ESP32-Garagem-01
- **Cozinha**: ESP32-Cozinha-01
- **Quarto**: ESP32-Quarto-01
- **Lavanderia**: ESP32-Lavanderia-01
- **Externo**: ESP32-Externo-01
- **Estufa**: ESP32-Estufa-01

### **Sensores (70 sensores)**
- **10 sensores por dispositivo**
- **Tipos**: DHT22, LDR, PIR, Pressão, Vibração, Nível
- **Configurações**: Pinos, calibração, status

### **Leituras (50.000+ leituras)**
- **Período**: Últimas 24 horas
- **Frequência**: 1 leitura por minuto
- **Dados**: Temperatura, umidade, luminosidade, pressão, vibração
- **Qualidade**: Classificação automática
- **Anomalias**: 5% de chance de anomalia

### **Alertas (50+ alertas)**
- **Baseados**: Em anomalias detectadas
- **Tipos**: Temperatura, umidade, pressão, vibração
- **Severidade**: Baixa, média, alta, crítica
- **Status**: Ativo, resolvido, ignorado

### **Usuários (4 usuários)**
- **Administrador**: admin@iot.com
- **Operador**: operador@iot.com
- **Visualizador**: visualizador@iot.com
- **Técnico**: tecnico@iot.com

### **Configurações**
- **Limites**: Para cada tipo de sensor
- **Dashboards**: Configurações personalizadas
- **Relatórios**: Agendamentos automáticos
- **Logs**: Rastreabilidade completa

## 📁 Arquivos Gerados

### **Scripts SQL**
- `criar_tabelas_iot.sql` - Criação do banco
- `carga_dados_iot.sql` - Carga de dados

### **Documentação**
- `explicacao_chaves_restricoes.md` - Explicação detalhada
- `README_BANCO_DADOS_COMPLETO.md` - Este arquivo

### **Testes**
- `testes_integridade_banco.py` - Script de testes
- `relatorio_testes_integridade.json` - Relatório dos testes

### **Logs**
- `testes_integridade.log` - Log dos testes
- `relatorio_testes_integridade.json` - Resultados

## 🔍 Consultas de Exemplo

### **Leituras Recentes**
```sql
SELECT l.*, s.nome as sensor_nome, d.nome as dispositivo_nome
FROM leituras_sensores l
JOIN sensores s ON l.id_sensor = s.id_sensor
JOIN dispositivos d ON s.id_dispositivo = d.id_dispositivo
WHERE l.timestamp_datetime >= DATE_SUB(NOW(), INTERVAL 1 HOUR)
ORDER BY l.timestamp_datetime DESC;
```

### **Alertas Ativos**
```sql
SELECT a.*, d.nome as dispositivo_nome, s.nome as sensor_nome
FROM alertas a
JOIN dispositivos d ON a.id_dispositivo = d.id_dispositivo
LEFT JOIN sensores s ON a.id_sensor = s.id_sensor
WHERE a.status = 'ativo'
ORDER BY a.timestamp_alerta DESC;
```

### **Estatísticas por Dispositivo**
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

## 🎯 Benefícios da Implementação

### **Integridade Referencial**
- **10 Chaves Estrangeiras**: Relacionamentos válidos
- **Cascata**: Consistência automática
- **NULL Controlado**: Campos opcionais bem definidos

### **Performance Otimizada**
- **15+ Índices**: Consultas rápidas
- **Particionamento**: Escalabilidade temporal
- **Índices Compostos**: Consultas complexas eficientes

### **Auditoria Completa**
- **Logs**: Rastreabilidade de operações
- **Triggers**: Atualizações automáticas
- **Timestamps**: Controle temporal

### **Flexibilidade**
- **JSON**: Configurações flexíveis
- **ENUMs**: Valores padronizados
- **Particionamento**: Manutenção facilitada

## 📞 Suporte

Para dúvidas sobre o banco de dados:
- **Criação**: Verifique as permissões do MySQL
- **Carga**: Confirme se o banco existe
- **Testes**: Verifique a conexão e credenciais
- **Performance**: Analise os logs de consulta

---

**Sistema de Banco de Dados - Enterprise Challenge Sprint 3 - Reply**
