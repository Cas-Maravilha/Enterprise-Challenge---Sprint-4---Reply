-- =====================================================
-- Sistema IoT Monitoring - Criação das Tabelas
-- Enterprise Challenge Sprint 3 - Reply
-- =====================================================

USE iot_monitoring_db;

-- =====================================================
-- 1. TABELA: tipos_sensor
-- =====================================================
CREATE TABLE IF NOT EXISTS tipos_sensor (
    id_tipo_sensor INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(50) NOT NULL UNIQUE,
    unidade_medida VARCHAR(20) NOT NULL,
    range_min DECIMAL(10,2) NOT NULL,
    range_max DECIMAL(10,2) NOT NULL,
    descricao TEXT,
    ativo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_tipos_sensor_nome (nome),
    INDEX idx_tipos_sensor_ativo (ativo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- 2. TABELA: modos_operacao
-- =====================================================
CREATE TABLE IF NOT EXISTS modos_operacao (
    id_modo_operacao INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(50) NOT NULL UNIQUE,
    descricao TEXT,
    frequencia_coleta INT DEFAULT 1,
    ativo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_modos_operacao_nome (nome),
    INDEX idx_modos_operacao_ativo (ativo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- 3. TABELA: dispositivos
-- =====================================================
CREATE TABLE IF NOT EXISTS dispositivos (
    id_dispositivo INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    localizacao VARCHAR(200),
    ip_address VARCHAR(45),
    mac_address VARCHAR(17),
    status ENUM('ativo', 'inativo', 'manutencao', 'erro') DEFAULT 'ativo',
    id_modo_operacao INT,
    ultima_comunicacao TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (id_modo_operacao) REFERENCES modos_operacao(id_modo_operacao),
    INDEX idx_dispositivos_nome (nome),
    INDEX idx_dispositivos_status (status),
    INDEX idx_dispositivos_ip (ip_address),
    INDEX idx_dispositivos_ultima_comunicacao (ultima_comunicacao)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- 4. TABELA: sensores
-- =====================================================
CREATE TABLE IF NOT EXISTS sensores (
    id_sensor INT AUTO_INCREMENT PRIMARY KEY,
    id_dispositivo INT NOT NULL,
    id_tipo_sensor INT NOT NULL,
    nome VARCHAR(100) NOT NULL,
    pino VARCHAR(10),
    ativo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (id_dispositivo) REFERENCES dispositivos(id_dispositivo) ON DELETE CASCADE,
    FOREIGN KEY (id_tipo_sensor) REFERENCES tipos_sensor(id_tipo_sensor),
    UNIQUE KEY uk_sensores_dispositivo_nome (id_dispositivo, nome),
    INDEX idx_sensores_dispositivo (id_dispositivo),
    INDEX idx_sensores_tipo (id_tipo_sensor),
    INDEX idx_sensores_ativo (ativo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- 5. TABELA: leituras_sensores (TABELA PRINCIPAL)
-- =====================================================
CREATE TABLE IF NOT EXISTS leituras_sensores (
    id_leitura BIGINT AUTO_INCREMENT PRIMARY KEY,
    id_sensor INT NOT NULL,
    timestamp_datetime TIMESTAMP NOT NULL,
    valor_numerico DECIMAL(10,3) NULL,
    valor_booleano BOOLEAN NULL,
    qualidade_dados ENUM('excelente', 'boa', 'regular', 'ruim') DEFAULT 'boa',
    anomalia_detectada BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (id_sensor) REFERENCES sensores(id_sensor) ON DELETE CASCADE,
    INDEX idx_leituras_sensor (id_sensor),
    INDEX idx_leituras_timestamp (timestamp_datetime),
    INDEX idx_leituras_qualidade (qualidade_dados),
    INDEX idx_leituras_anomalia (anomalia_detectada),
    INDEX idx_leituras_sensor_timestamp (id_sensor, timestamp_datetime),
    INDEX idx_leituras_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
PARTITION BY RANGE (YEAR(timestamp_datetime) * 100 + MONTH(timestamp_datetime)) (
    PARTITION p202401 VALUES LESS THAN (202402),
    PARTITION p202402 VALUES LESS THAN (202403),
    PARTITION p202403 VALUES LESS THAN (202404),
    PARTITION p202404 VALUES LESS THAN (202405),
    PARTITION p202405 VALUES LESS THAN (202406),
    PARTITION p202406 VALUES LESS THAN (202407),
    PARTITION p202407 VALUES LESS THAN (202408),
    PARTITION p202408 VALUES LESS THAN (202409),
    PARTITION p202409 VALUES LESS THAN (202410),
    PARTITION p202410 VALUES LESS THAN (202411),
    PARTITION p202411 VALUES LESS THAN (202412),
    PARTITION p202412 VALUES LESS THAN (202501),
    PARTITION p_future VALUES LESS THAN MAXVALUE
);

-- =====================================================
-- 6. TABELA: alertas
-- =====================================================
CREATE TABLE IF NOT EXISTS alertas (
    id_alerta BIGINT AUTO_INCREMENT PRIMARY KEY,
    id_dispositivo INT,
    id_sensor INT,
    tipo_alerta ENUM('temperatura_alta', 'temperatura_baixa', 'umidade_alta', 'umidade_baixa', 
                     'luminosidade_alta', 'luminosidade_baixa', 'movimento_detectado', 
                     'pressao_alta', 'pressao_baixa', 'sensor_offline', 'qualidade_ruim') NOT NULL,
    severidade ENUM('critica', 'alta', 'media', 'baixa') DEFAULT 'media',
    titulo VARCHAR(200) NOT NULL,
    descricao TEXT,
    valor_atual DECIMAL(10,3),
    valor_limite DECIMAL(10,3),
    timestamp_alerta TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status ENUM('ativo', 'resolvido', 'ignorado') DEFAULT 'ativo',
    resolved_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (id_dispositivo) REFERENCES dispositivos(id_dispositivo) ON DELETE SET NULL,
    FOREIGN KEY (id_sensor) REFERENCES sensores(id_sensor) ON DELETE SET NULL,
    INDEX idx_alertas_dispositivo (id_dispositivo),
    INDEX idx_alertas_sensor (id_sensor),
    INDEX idx_alertas_tipo (tipo_alerta),
    INDEX idx_alertas_severidade (severidade),
    INDEX idx_alertas_status (status),
    INDEX idx_alertas_timestamp (timestamp_alerta)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- 7. TABELA: configuracoes
-- =====================================================
CREATE TABLE IF NOT EXISTS configuracoes (
    id_configuracao INT AUTO_INCREMENT PRIMARY KEY,
    chave VARCHAR(100) NOT NULL UNIQUE,
    valor TEXT NOT NULL,
    tipo ENUM('string', 'integer', 'decimal', 'boolean', 'json') DEFAULT 'string',
    descricao TEXT,
    ativo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_configuracoes_chave (chave),
    INDEX idx_configuracoes_ativo (ativo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- 8. TABELA: usuarios
-- =====================================================
CREATE TABLE IF NOT EXISTS usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    senha_hash VARCHAR(255) NOT NULL,
    role ENUM('admin', 'operador', 'visualizador') DEFAULT 'visualizador',
    ativo BOOLEAN DEFAULT TRUE,
    ultimo_login TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_usuarios_email (email),
    INDEX idx_usuarios_role (role),
    INDEX idx_usuarios_ativo (ativo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- 9. TABELA: logs_sistema
-- =====================================================
CREATE TABLE IF NOT EXISTS logs_sistema (
    id_log BIGINT AUTO_INCREMENT PRIMARY KEY,
    nivel ENUM('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL') NOT NULL,
    componente VARCHAR(100) NOT NULL,
    mensagem TEXT NOT NULL,
    dados_extras JSON NULL,
    timestamp_log TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_logs_nivel (nivel),
    INDEX idx_logs_componente (componente),
    INDEX idx_logs_timestamp (timestamp_log),
    INDEX idx_logs_nivel_timestamp (nivel, timestamp_log)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- 10. TABELA: metricas_performance
-- =====================================================
CREATE TABLE IF NOT EXISTS metricas_performance (
    id_metrica BIGINT AUTO_INCREMENT PRIMARY KEY,
    componente VARCHAR(100) NOT NULL,
    metrica VARCHAR(100) NOT NULL,
    valor DECIMAL(15,6) NOT NULL,
    unidade VARCHAR(20),
    timestamp_metrica TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_metricas_componente (componente),
    INDEX idx_metricas_metrica (metrica),
    INDEX idx_metricas_timestamp (timestamp_metrica),
    INDEX idx_metricas_componente_metrica (componente, metrica)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- 11. TABELA: relatorios
-- =====================================================
CREATE TABLE IF NOT EXISTS relatorios (
    id_relatorio INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(200) NOT NULL,
    tipo ENUM('diario', 'semanal', 'mensal', 'personalizado') NOT NULL,
    configuracao JSON NOT NULL,
    ativo BOOLEAN DEFAULT TRUE,
    proxima_execucao TIMESTAMP NULL,
    ultima_execucao TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_relatorios_nome (nome),
    INDEX idx_relatorios_tipo (tipo),
    INDEX idx_relatorios_ativo (ativo),
    INDEX idx_relatorios_proxima_execucao (proxima_execucao)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- VERIFICAÇÃO DE CRIAÇÃO
-- =====================================================

-- Mostrar tabelas criadas
SHOW TABLES;

-- Contar tabelas
SELECT 
    COUNT(*) as total_tabelas,
    'Tabelas criadas com sucesso!' as status
FROM information_schema.tables 
WHERE table_schema = 'iot_monitoring_db';

-- Mostrar estrutura das tabelas principais
DESCRIBE tipos_sensor;
DESCRIBE dispositivos;
DESCRIBE sensores;
DESCRIBE leituras_sensores;
DESCRIBE alertas;

-- Verificar foreign keys
SELECT 
    TABLE_NAME,
    COLUMN_NAME,
    CONSTRAINT_NAME,
    REFERENCED_TABLE_NAME,
    REFERENCED_COLUMN_NAME
FROM information_schema.KEY_COLUMN_USAGE 
WHERE TABLE_SCHEMA = 'iot_monitoring_db' 
AND REFERENCED_TABLE_NAME IS NOT NULL;

-- Verificar particionamento da tabela principal
SELECT 
    TABLE_NAME,
    PARTITION_NAME,
    PARTITION_ORDINAL_POSITION,
    PARTITION_METHOD,
    PARTITION_EXPRESSION
FROM information_schema.PARTITIONS 
WHERE TABLE_SCHEMA = 'iot_monitoring_db' 
AND TABLE_NAME = 'leituras_sensores';

-- Mensagem de sucesso
SELECT 
    '===============================================' as separator,
    'Sistema IoT Monitoring - Tabelas Criadas' as title,
    'Enterprise Challenge Sprint 3 - Reply' as subtitle,
    '===============================================' as separator,
    'Total de tabelas: 11' as tabelas_info,
    'Engine: InnoDB' as engine_info,
    'Charset: utf8mb4' as charset_info,
    'Particionamento: Ativo' as particionamento_info,
    'Status: CRIADAS COM SUCESSO' as status,
    '===============================================' as separator;
