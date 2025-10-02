-- =====================================================
-- Sistema IoT Monitoring - Evidências das Tabelas Principais
-- Enterprise Challenge Sprint 3 - Reply
-- =====================================================

USE iot_monitoring_db;

-- =====================================================
-- 1. ESTRUTURA DO BANCO
-- =====================================================

-- Mostrar todas as tabelas
SHOW TABLES;

-- Contar tabelas
SELECT 
    COUNT(*) as total_tabelas,
    'Tabelas criadas no banco iot_monitoring_db' as descricao
FROM information_schema.tables 
WHERE table_schema = 'iot_monitoring_db';

-- =====================================================
-- 2. TABELA: tipos_sensor
-- =====================================================

-- Estrutura da tabela
DESCRIBE tipos_sensor;

-- Dados da tabela
SELECT 
    id_tipo_sensor,
    nome,
    unidade_medida,
    range_min,
    range_max,
    ativo,
    created_at
FROM tipos_sensor
ORDER BY nome;

-- Contar tipos de sensor
SELECT 
    COUNT(*) as total_tipos,
    COUNT(CASE WHEN ativo = TRUE THEN 1 END) as tipos_ativos
FROM tipos_sensor;

-- =====================================================
-- 3. TABELA: dispositivos
-- =====================================================

-- Estrutura da tabela
DESCRIBE dispositivos;

-- Dados da tabela
SELECT 
    id_dispositivo,
    nome,
    localizacao,
    ip_address,
    status,
    ultima_comunicacao,
    created_at
FROM dispositivos
ORDER BY nome;

-- Contar dispositivos por status
SELECT 
    status,
    COUNT(*) as total_dispositivos
FROM dispositivos
GROUP BY status
ORDER BY total_dispositivos DESC;

-- =====================================================
-- 4. TABELA: sensores
-- =====================================================

-- Estrutura da tabela
DESCRIBE sensores;

-- Dados da tabela com informações do dispositivo e tipo
SELECT 
    s.id_sensor,
    s.nome as sensor_nome,
    d.nome as dispositivo_nome,
    d.localizacao,
    ts.nome as tipo_sensor,
    ts.unidade_medida,
    s.pino,
    s.ativo,
    s.created_at
FROM sensores s
JOIN dispositivos d ON s.id_dispositivo = d.id_dispositivo
JOIN tipos_sensor ts ON s.id_tipo_sensor = ts.id_tipo_sensor
ORDER BY d.nome, s.nome;

-- Contar sensores por dispositivo
SELECT 
    d.nome as dispositivo,
    COUNT(s.id_sensor) as total_sensores,
    COUNT(CASE WHEN s.ativo = TRUE THEN 1 END) as sensores_ativos
FROM dispositivos d
LEFT JOIN sensores s ON d.id_dispositivo = s.id_dispositivo
GROUP BY d.id_dispositivo, d.nome
ORDER BY total_sensores DESC;

-- Contar sensores por tipo
SELECT 
    ts.nome as tipo_sensor,
    ts.unidade_medida,
    COUNT(s.id_sensor) as total_sensores,
    COUNT(CASE WHEN s.ativo = TRUE THEN 1 END) as sensores_ativos
FROM tipos_sensor ts
LEFT JOIN sensores s ON ts.id_tipo_sensor = s.id_tipo_sensor
GROUP BY ts.id_tipo_sensor, ts.nome, ts.unidade_medida
ORDER BY total_sensores DESC;

-- =====================================================
-- 5. TABELA: leituras_sensores (TABELA PRINCIPAL)
-- =====================================================

-- Estrutura da tabela
DESCRIBE leituras_sensores;

-- Contar total de leituras
SELECT 
    COUNT(*) as total_leituras,
    MIN(timestamp_datetime) as primeira_leitura,
    MAX(timestamp_datetime) as ultima_leitura,
    COUNT(DISTINCT id_sensor) as sensores_com_dados
FROM leituras_sensores;

-- Amostra de leituras (últimas 10)
SELECT 
    l.id_leitura,
    s.nome as sensor_nome,
    d.nome as dispositivo_nome,
    l.timestamp_datetime,
    l.valor_numerico,
    l.valor_booleano,
    l.qualidade_dados,
    l.anomalia_detectada,
    l.created_at
FROM leituras_sensores l
JOIN sensores s ON l.id_sensor = s.id_sensor
JOIN dispositivos d ON s.id_dispositivo = d.id_dispositivo
ORDER BY l.timestamp_datetime DESC
LIMIT 10;

-- Leituras por qualidade
SELECT 
    qualidade_dados,
    COUNT(*) as total_leituras,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM leituras_sensores), 2) as percentual
FROM leituras_sensores
GROUP BY qualidade_dados
ORDER BY 
    CASE qualidade_dados
        WHEN 'excelente' THEN 1
        WHEN 'boa' THEN 2
        WHEN 'regular' THEN 3
        WHEN 'ruim' THEN 4
    END;

-- Leituras com anomalias
SELECT 
    COUNT(*) as total_anomalias,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM leituras_sensores), 2) as percentual_anomalias
FROM leituras_sensores
WHERE anomalia_detectada = TRUE;

-- Top 10 sensores com mais leituras
SELECT 
    s.nome as sensor_nome,
    d.nome as dispositivo_nome,
    ts.nome as tipo_sensor,
    COUNT(l.id_leitura) as total_leituras,
    MAX(l.timestamp_datetime) as ultima_leitura
FROM leituras_sensores l
JOIN sensores s ON l.id_sensor = s.id_sensor
JOIN dispositivos d ON s.id_dispositivo = d.id_dispositivo
JOIN tipos_sensor ts ON s.id_tipo_sensor = ts.id_tipo_sensor
GROUP BY s.id_sensor, s.nome, d.nome, ts.nome
ORDER BY total_leituras DESC
LIMIT 10;

-- =====================================================
-- 6. TABELA: alertas
-- =====================================================

-- Estrutura da tabela
DESCRIBE alertas;

-- Contar alertas
SELECT 
    COUNT(*) as total_alertas,
    COUNT(CASE WHEN status = 'ativo' THEN 1 END) as alertas_ativos,
    COUNT(CASE WHEN status = 'resolvido' THEN 1 END) as alertas_resolvidos,
    COUNT(CASE WHEN status = 'ignorado' THEN 1 END) as alertas_ignorados
FROM alertas;

-- Alertas por severidade
SELECT 
    severidade,
    COUNT(*) as total_alertas,
    COUNT(CASE WHEN status = 'ativo' THEN 1 END) as alertas_ativos
FROM alertas
GROUP BY severidade
ORDER BY 
    CASE severidade
        WHEN 'critica' THEN 1
        WHEN 'alta' THEN 2
        WHEN 'media' THEN 3
        WHEN 'baixa' THEN 4
    END;

-- Alertas por tipo
SELECT 
    tipo_alerta,
    COUNT(*) as total_alertas,
    COUNT(CASE WHEN status = 'ativo' THEN 1 END) as alertas_ativos
FROM alertas
GROUP BY tipo_alerta
ORDER BY total_alertas DESC;

-- Últimos 10 alertas
SELECT 
    a.id_alerta,
    a.tipo_alerta,
    a.severidade,
    a.titulo,
    d.nome as dispositivo_nome,
    s.nome as sensor_nome,
    a.valor_atual,
    a.valor_limite,
    a.timestamp_alerta,
    a.status
FROM alertas a
LEFT JOIN dispositivos d ON a.id_dispositivo = d.id_dispositivo
LEFT JOIN sensores s ON a.id_sensor = s.id_sensor
ORDER BY a.timestamp_alerta DESC
LIMIT 10;

-- =====================================================
-- 7. TABELA: configuracoes
-- =====================================================

-- Estrutura da tabela
DESCRIBE configuracoes;

-- Configurações ativas
SELECT 
    chave,
    valor,
    tipo,
    descricao
FROM configuracoes
WHERE ativo = TRUE
ORDER BY chave;

-- Contar configurações por tipo
SELECT 
    tipo,
    COUNT(*) as total_configuracoes,
    COUNT(CASE WHEN ativo = TRUE THEN 1 END) as configuracoes_ativas
FROM configuracoes
GROUP BY tipo
ORDER BY total_configuracoes DESC;

-- =====================================================
-- 8. TABELA: usuarios
-- =====================================================

-- Estrutura da tabela
DESCRIBE usuarios;

-- Usuários (sem senha)
SELECT 
    id_usuario,
    nome,
    email,
    role,
    ativo,
    ultimo_login,
    created_at
FROM usuarios
ORDER BY nome;

-- Usuários por role
SELECT 
    role,
    COUNT(*) as total_usuarios,
    COUNT(CASE WHEN ativo = TRUE THEN 1 END) as usuarios_ativos
FROM usuarios
GROUP BY role
ORDER BY total_usuarios DESC;

-- =====================================================
-- 9. TABELA: logs_sistema
-- =====================================================

-- Estrutura da tabela
DESCRIBE logs_sistema;

-- Contar logs por nível
SELECT 
    nivel,
    COUNT(*) as total_logs
FROM logs_sistema
GROUP BY nivel
ORDER BY 
    CASE nivel
        WHEN 'DEBUG' THEN 1
        WHEN 'INFO' THEN 2
        WHEN 'WARNING' THEN 3
        WHEN 'ERROR' THEN 4
        WHEN 'CRITICAL' THEN 5
    END;

-- Últimos 10 logs
SELECT 
    id_log,
    nivel,
    componente,
    mensagem,
    timestamp_log
FROM logs_sistema
ORDER BY timestamp_log DESC
LIMIT 10;

-- =====================================================
-- 10. TABELA: metricas_performance
-- =====================================================

-- Estrutura da tabela
DESCRIBE metricas_performance;

-- Métricas atuais
SELECT 
    componente,
    metrica,
    valor,
    unidade,
    timestamp_metrica
FROM metricas_performance
ORDER BY timestamp_metrica DESC;

-- =====================================================
-- 11. TABELA: relatorios
-- =====================================================

-- Estrutura da tabela
DESCRIBE relatorios;

-- Relatórios configurados
SELECT 
    id_relatorio,
    nome,
    tipo,
    ativo,
    proxima_execucao,
    ultima_execucao,
    created_at
FROM relatorios
ORDER BY nome;

-- =====================================================
-- RESUMO GERAL
-- =====================================================

-- Resumo de todas as tabelas
SELECT 
    'tipos_sensor' as tabela,
    COUNT(*) as total_registros
FROM tipos_sensor
UNION ALL
SELECT 
    'modos_operacao' as tabela,
    COUNT(*) as total_registros
FROM modos_operacao
UNION ALL
SELECT 
    'dispositivos' as tabela,
    COUNT(*) as total_registros
FROM dispositivos
UNION ALL
SELECT 
    'sensores' as tabela,
    COUNT(*) as total_registros
FROM sensores
UNION ALL
SELECT 
    'leituras_sensores' as tabela,
    COUNT(*) as total_registros
FROM leituras_sensores
UNION ALL
SELECT 
    'alertas' as tabela,
    COUNT(*) as total_registros
FROM alertas
UNION ALL
SELECT 
    'configuracoes' as tabela,
    COUNT(*) as total_registros
FROM configuracoes
UNION ALL
SELECT 
    'usuarios' as tabela,
    COUNT(*) as total_registros
FROM usuarios
UNION ALL
SELECT 
    'logs_sistema' as tabela,
    COUNT(*) as total_registros
FROM logs_sistema
UNION ALL
SELECT 
    'metricas_performance' as tabela,
    COUNT(*) as total_registros
FROM metricas_performance
UNION ALL
SELECT 
    'relatorios' as tabela,
    COUNT(*) as total_registros
FROM relatorios
ORDER BY total_registros DESC;
