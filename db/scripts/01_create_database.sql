-- =====================================================
-- Sistema IoT Monitoring - Criação do Banco de Dados
-- Enterprise Challenge Sprint 3 - Reply
-- =====================================================

-- Criar banco de dados principal
CREATE DATABASE IF NOT EXISTS iot_monitoring_db
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

-- Usar o banco criado
USE iot_monitoring_db;

-- Verificar criação do banco
SELECT 
    'Banco de dados criado com sucesso!' as status,
    DATABASE() as database_name,
    @@character_set_database as charset,
    @@collation_database as collation;

-- Mostrar informações do banco
SHOW CREATE DATABASE iot_monitoring_db;

-- Verificar espaço disponível
SELECT 
    table_schema as 'Database',
    ROUND(SUM(data_length + index_length) / 1024 / 1024, 2) as 'Size (MB)'
FROM information_schema.tables 
WHERE table_schema = 'iot_monitoring_db'
GROUP BY table_schema;

-- Configurações de performance para o banco
SET SESSION sql_mode = 'STRICT_TRANS_TABLES,NO_ZERO_DATE,NO_ZERO_IN_DATE,ERROR_FOR_DIVISION_BY_ZERO';

-- Configurações de charset para sessão
SET NAMES utf8mb4;

-- Verificar configurações
SELECT 
    'Configurações aplicadas:' as info,
    @@sql_mode as sql_mode,
    @@character_set_client as client_charset,
    @@character_set_connection as connection_charset,
    @@character_set_results as results_charset;

-- Log de criação
INSERT INTO mysql.general_log 
SET event_time = NOW(),
    user_host = CONCAT(USER(), '@', @@hostname),
    thread_id = CONNECTION_ID(),
    server_id = @@server_id,
    command_type = 'Query',
    argument = 'CREATE DATABASE iot_monitoring_db - Sistema IoT Monitoring';

-- Mensagem de sucesso
SELECT 
    '===============================================' as separator,
    'Sistema IoT Monitoring - Banco de Dados' as title,
    'Enterprise Challenge Sprint 3 - Reply' as subtitle,
    '===============================================' as separator,
    'Banco: iot_monitoring_db' as database_info,
    'Charset: utf8mb4' as charset_info,
    'Collation: utf8mb4_unicode_ci' as collation_info,
    'Status: CRIADO COM SUCESSO' as status,
    '===============================================' as separator;
