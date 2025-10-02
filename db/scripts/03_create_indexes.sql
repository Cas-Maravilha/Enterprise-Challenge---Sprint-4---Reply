-- =====================================================
-- Sistema IoT Monitoring - Criação de Índices
-- Enterprise Challenge Sprint 3 - Reply
-- =====================================================

USE iot_monitoring_db;

-- =====================================================
-- ÍNDICES PARA TABELA: tipos_sensor
-- =====================================================

-- Índice para busca por nome
CREATE INDEX IF NOT EXISTS idx_tipos_sensor_nome ON tipos_sensor(nome);

-- Índice para filtro por status ativo
CREATE INDEX IF NOT EXISTS idx_tipos_sensor_ativo ON tipos_sensor(ativo);

-- Índice composto para consultas frequentes
CREATE INDEX IF NOT EXISTS idx_tipos_sensor_ativo_nome ON tipos_sensor(ativo, nome);

-- =====================================================
-- ÍNDICES PARA TABELA: modos_operacao
-- =====================================================

-- Índice para busca por nome
CREATE INDEX IF NOT EXISTS idx_modos_operacao_nome ON modos_operacao(nome);

-- Índice para filtro por status ativo
CREATE INDEX IF NOT EXISTS idx_modos_operacao_ativo ON modos_operacao(ativo);

-- Índice para ordenação por frequência
CREATE INDEX IF NOT EXISTS idx_modos_operacao_frequencia ON modos_operacao(frequencia_coleta);

-- =====================================================
-- ÍNDICES PARA TABELA: dispositivos
-- =====================================================

-- Índice para busca por nome
CREATE INDEX IF NOT EXISTS idx_dispositivos_nome ON dispositivos(nome);

-- Índice para filtro por status
CREATE INDEX IF NOT EXISTS idx_dispositivos_status ON dispositivos(status);

-- Índice para busca por IP
CREATE INDEX IF NOT EXISTS idx_dispositivos_ip ON dispositivos(ip_address);

-- Índice para busca por MAC
CREATE INDEX IF NOT EXISTS idx_dispositivos_mac ON dispositivos(mac_address);

-- Índice para ordenação por última comunicação
CREATE INDEX IF NOT EXISTS idx_dispositivos_ultima_comunicacao ON dispositivos(ultima_comunicacao);

-- Índice composto para consultas de monitoramento
CREATE INDEX IF NOT EXISTS idx_dispositivos_status_ultima_comunicacao ON dispositivos(status, ultima_comunicacao);

-- Índice para foreign key
CREATE INDEX IF NOT EXISTS idx_dispositivos_modo_operacao ON dispositivos(id_modo_operacao);

-- =====================================================
-- ÍNDICES PARA TABELA: sensores
-- =====================================================

-- Índice para foreign key dispositivo
CREATE INDEX IF NOT EXISTS idx_sensores_dispositivo ON sensores(id_dispositivo);

-- Índice para foreign key tipo sensor
CREATE INDEX IF NOT EXISTS idx_sensores_tipo ON sensores(id_tipo_sensor);

-- Índice para filtro por status ativo
CREATE INDEX IF NOT EXISTS idx_sensores_ativo ON sensores(ativo);

-- Índice para busca por nome
CREATE INDEX IF NOT EXISTS idx_sensores_nome ON sensores(nome);

-- Índice composto para consultas por dispositivo e status
CREATE INDEX IF NOT EXISTS idx_sensores_dispositivo_ativo ON sensores(id_dispositivo, ativo);

-- Índice composto para consultas por tipo e status
CREATE INDEX IF NOT EXISTS idx_sensores_tipo_ativo ON sensores(id_tipo_sensor, ativo);

-- =====================================================
-- ÍNDICES PARA TABELA: leituras_sensores (TABELA PRINCIPAL)
-- =====================================================

-- Índice para foreign key sensor
CREATE INDEX IF NOT EXISTS idx_leituras_sensor ON leituras_sensores(id_sensor);

-- Índice para ordenação por timestamp
CREATE INDEX IF NOT EXISTS idx_leituras_timestamp ON leituras_sensores(timestamp_datetime);

-- Índice para filtro por qualidade
CREATE INDEX IF NOT EXISTS idx_leituras_qualidade ON leituras_sensores(qualidade_dados);

-- Índice para filtro por anomalia
CREATE INDEX IF NOT EXISTS idx_leituras_anomalia ON leituras_sensores(anomalia_detectada);

-- Índice composto para consultas por sensor e timestamp (MUITO IMPORTANTE)
CREATE INDEX IF NOT EXISTS idx_leituras_sensor_timestamp ON leituras_sensores(id_sensor, timestamp_datetime);

-- Índice composto para consultas por sensor e qualidade
CREATE INDEX IF NOT EXISTS idx_leituras_sensor_qualidade ON leituras_sensores(id_sensor, qualidade_dados);

-- Índice composto para consultas por sensor e anomalia
CREATE INDEX IF NOT EXISTS idx_leituras_sensor_anomalia ON leituras_sensores(id_sensor, anomalia_detectada);

-- Índice para ordenação por created_at
CREATE INDEX IF NOT EXISTS idx_leituras_created_at ON leituras_sensores(created_at);

-- Índice composto para consultas de relatórios
CREATE INDEX IF NOT EXISTS idx_leituras_timestamp_qualidade ON leituras_sensores(timestamp_datetime, qualidade_dados);

-- Índice composto para consultas de anomalias
CREATE INDEX IF NOT EXISTS idx_leituras_timestamp_anomalia ON leituras_sensores(timestamp_datetime, anomalia_detectada);

-- =====================================================
-- ÍNDICES PARA TABELA: alertas
-- =====================================================

-- Índice para foreign key dispositivo
CREATE INDEX IF NOT EXISTS idx_alertas_dispositivo ON alertas(id_dispositivo);

-- Índice para foreign key sensor
CREATE INDEX IF NOT EXISTS idx_alertas_sensor ON alertas(id_sensor);

-- Índice para filtro por tipo de alerta
CREATE INDEX IF NOT EXISTS idx_alertas_tipo ON alertas(tipo_alerta);

-- Índice para filtro por severidade
CREATE INDEX IF NOT EXISTS idx_alertas_severidade ON alertas(severidade);

-- Índice para filtro por status
CREATE INDEX IF NOT EXISTS idx_alertas_status ON alertas(status);

-- Índice para ordenação por timestamp
CREATE INDEX IF NOT EXISTS idx_alertas_timestamp ON alertas(timestamp_alerta);

-- Índice composto para consultas de alertas ativos
CREATE INDEX IF NOT EXISTS idx_alertas_status_timestamp ON alertas(status, timestamp_alerta);

-- Índice composto para consultas por dispositivo e status
CREATE INDEX IF NOT EXISTS idx_alertas_dispositivo_status ON alertas(id_dispositivo, status);

-- Índice composto para consultas por sensor e status
CREATE INDEX IF NOT EXISTS idx_alertas_sensor_status ON alertas(id_sensor, status);

-- Índice composto para consultas por severidade e status
CREATE INDEX IF NOT EXISTS idx_alertas_severidade_status ON alertas(severidade, status);

-- =====================================================
-- ÍNDICES PARA TABELA: configuracoes
-- =====================================================

-- Índice para busca por chave
CREATE INDEX IF NOT EXISTS idx_configuracoes_chave ON configuracoes(chave);

-- Índice para filtro por status ativo
CREATE INDEX IF NOT EXISTS idx_configuracoes_ativo ON configuracoes(ativo);

-- Índice composto para consultas ativas
CREATE INDEX IF NOT EXISTS idx_configuracoes_ativo_chave ON configuracoes(ativo, chave);

-- =====================================================
-- ÍNDICES PARA TABELA: usuarios
-- =====================================================

-- Índice para busca por email (UNIQUE já existe)
CREATE INDEX IF NOT EXISTS idx_usuarios_email ON usuarios(email);

-- Índice para filtro por role
CREATE INDEX IF NOT EXISTS idx_usuarios_role ON usuarios(role);

-- Índice para filtro por status ativo
CREATE INDEX IF NOT EXISTS idx_usuarios_ativo ON usuarios(ativo);

-- Índice para ordenação por último login
CREATE INDEX IF NOT EXISTS idx_usuarios_ultimo_login ON usuarios(ultimo_login);

-- Índice composto para consultas por role e status
CREATE INDEX IF NOT EXISTS idx_usuarios_role_ativo ON usuarios(role, ativo);

-- =====================================================
-- ÍNDICES PARA TABELA: logs_sistema
-- =====================================================

-- Índice para filtro por nível
CREATE INDEX IF NOT EXISTS idx_logs_nivel ON logs_sistema(nivel);

-- Índice para filtro por componente
CREATE INDEX IF NOT EXISTS idx_logs_componente ON logs_sistema(componente);

-- Índice para ordenação por timestamp
CREATE INDEX IF NOT EXISTS idx_logs_timestamp ON logs_sistema(timestamp_log);

-- Índice composto para consultas por nível e timestamp
CREATE INDEX IF NOT EXISTS idx_logs_nivel_timestamp ON logs_sistema(nivel, timestamp_log);

-- Índice composto para consultas por componente e timestamp
CREATE INDEX IF NOT EXISTS idx_logs_componente_timestamp ON logs_sistema(componente, timestamp_log);

-- =====================================================
-- ÍNDICES PARA TABELA: metricas_performance
-- =====================================================

-- Índice para filtro por componente
CREATE INDEX IF NOT EXISTS idx_metricas_componente ON metricas_performance(componente);

-- Índice para filtro por métrica
CREATE INDEX IF NOT EXISTS idx_metricas_metrica ON metricas_performance(metrica);

-- Índice para ordenação por timestamp
CREATE INDEX IF NOT EXISTS idx_metricas_timestamp ON metricas_performance(timestamp_metrica);

-- Índice composto para consultas por componente e métrica
CREATE INDEX IF NOT EXISTS idx_metricas_componente_metrica ON metricas_performance(componente, metrica);

-- Índice composto para consultas por componente e timestamp
CREATE INDEX IF NOT EXISTS idx_metricas_componente_timestamp ON metricas_performance(componente, timestamp_metrica);

-- =====================================================
-- ÍNDICES PARA TABELA: relatorios
-- =====================================================

-- Índice para busca por nome
CREATE INDEX IF NOT EXISTS idx_relatorios_nome ON relatorios(nome);

-- Índice para filtro por tipo
CREATE INDEX IF NOT EXISTS idx_relatorios_tipo ON relatorios(tipo);

-- Índice para filtro por status ativo
CREATE INDEX IF NOT EXISTS idx_relatorios_ativo ON relatorios(ativo);

-- Índice para ordenação por próxima execução
CREATE INDEX IF NOT EXISTS idx_relatorios_proxima_execucao ON relatorios(proxima_execucao);

-- Índice composto para consultas ativas
CREATE INDEX IF NOT EXISTS idx_relatorios_ativo_tipo ON relatorios(ativo, tipo);

-- =====================================================
-- VERIFICAÇÃO DE ÍNDICES
-- =====================================================

-- Mostrar todos os índices criados
SELECT 
    TABLE_NAME,
    INDEX_NAME,
    COLUMN_NAME,
    SEQ_IN_INDEX,
    NON_UNIQUE,
    INDEX_TYPE
FROM information_schema.STATISTICS 
WHERE TABLE_SCHEMA = 'iot_monitoring_db'
ORDER BY TABLE_NAME, INDEX_NAME, SEQ_IN_INDEX;

-- Contar índices por tabela
SELECT 
    TABLE_NAME,
    COUNT(DISTINCT INDEX_NAME) as total_indices,
    COUNT(COLUMN_NAME) as total_colunas_indexadas
FROM information_schema.STATISTICS 
WHERE TABLE_SCHEMA = 'iot_monitoring_db'
GROUP BY TABLE_NAME
ORDER BY TABLE_NAME;

-- Verificar índices compostos
SELECT 
    TABLE_NAME,
    INDEX_NAME,
    GROUP_CONCAT(COLUMN_NAME ORDER BY SEQ_IN_INDEX) as colunas
FROM information_schema.STATISTICS 
WHERE TABLE_SCHEMA = 'iot_monitoring_db'
AND INDEX_NAME NOT IN ('PRIMARY')
GROUP BY TABLE_NAME, INDEX_NAME
HAVING COUNT(COLUMN_NAME) > 1
ORDER BY TABLE_NAME, INDEX_NAME;

-- Verificar tamanho dos índices
SELECT 
    TABLE_NAME,
    ROUND(SUM(INDEX_LENGTH) / 1024 / 1024, 2) as tamanho_indices_mb,
    ROUND(SUM(DATA_LENGTH) / 1024 / 1024, 2) as tamanho_dados_mb,
    ROUND(SUM(INDEX_LENGTH) / SUM(DATA_LENGTH) * 100, 2) as percentual_indices
FROM information_schema.TABLES 
WHERE TABLE_SCHEMA = 'iot_monitoring_db'
GROUP BY TABLE_NAME
ORDER BY tamanho_indices_mb DESC;

-- Mensagem de sucesso
SELECT 
    '===============================================' as separator,
    'Sistema IoT Monitoring - Índices Criados' as title,
    'Enterprise Challenge Sprint 3 - Reply' as subtitle,
    '===============================================' as separator,
    'Total de índices: 50+' as indices_info,
    'Índices compostos: 15+' as compostos_info,
    'Cobertura: 100%' as cobertura_info,
    'Status: CRIADOS COM SUCESSO' as status,
    '===============================================' as separator;
