-- =====================================================
-- SCRIPT DE CRIAÇÃO DO BANCO DE DADOS - PROJETO IoT
-- Sistema de Monitoramento com ESP32 e Sensores
-- =====================================================

-- Criação do banco de dados
CREATE DATABASE IF NOT EXISTS iot_monitoring_db
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE iot_monitoring_db;

-- =====================================================
-- TABELA: dispositivos
-- Armazena informações dos dispositivos ESP32
-- =====================================================
CREATE TABLE dispositivos (
    id_dispositivo INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    mac_address VARCHAR(17) UNIQUE NOT NULL,
    ip_address VARCHAR(15),
    localizacao VARCHAR(200),
    status ENUM('ativo', 'inativo', 'manutencao') DEFAULT 'ativo',
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ultima_conexao TIMESTAMP NULL,
    versao_firmware VARCHAR(20),
    observacoes TEXT,
    INDEX idx_status (status),
    INDEX idx_localizacao (localizacao)
) ENGINE=InnoDB;

-- =====================================================
-- TABELA: tipos_sensor
-- Catálogo dos tipos de sensores disponíveis
-- =====================================================
CREATE TABLE tipos_sensor (
    id_tipo_sensor INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(50) NOT NULL UNIQUE,
    descricao TEXT,
    unidade_medida VARCHAR(20),
    faixa_min DECIMAL(10,3),
    faixa_max DECIMAL(10,3),
    precisao DECIMAL(8,3),
    ativo BOOLEAN DEFAULT TRUE,
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- =====================================================
-- TABELA: sensores
-- Sensores instalados nos dispositivos
-- =====================================================
CREATE TABLE sensores (
    id_sensor INT AUTO_INCREMENT PRIMARY KEY,
    id_dispositivo INT NOT NULL,
    id_tipo_sensor INT NOT NULL,
    nome VARCHAR(100) NOT NULL,
    pino_analogico INT,
    pino_digital INT,
    calibracao_min DECIMAL(10,3),
    calibracao_max DECIMAL(10,3),
    status ENUM('ativo', 'inativo', 'falha') DEFAULT 'ativo',
    data_instalacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ultima_calibracao TIMESTAMP NULL,
    observacoes TEXT,
    FOREIGN KEY (id_dispositivo) REFERENCES dispositivos(id_dispositivo) ON DELETE CASCADE,
    FOREIGN KEY (id_tipo_sensor) REFERENCES tipos_sensor(id_tipo_sensor),
    INDEX idx_dispositivo (id_dispositivo),
    INDEX idx_tipo_sensor (id_tipo_sensor),
    INDEX idx_status (status)
) ENGINE=InnoDB;

-- =====================================================
-- TABELA: leituras_sensores
-- Dados coletados pelos sensores (tabela principal)
-- =====================================================
CREATE TABLE leituras_sensores (
    id_leitura BIGINT AUTO_INCREMENT PRIMARY KEY,
    id_sensor INT NOT NULL,
    timestamp_unix DECIMAL(15,3) NOT NULL,
    timestamp_datetime TIMESTAMP NOT NULL,
    valor_numerico DECIMAL(12,6),
    valor_booleano BOOLEAN,
    valor_string VARCHAR(255),
    qualidade_dados ENUM('excelente', 'bom', 'regular', 'ruim') DEFAULT 'bom',
    anomalia_detectada BOOLEAN DEFAULT FALSE,
    data_coleta TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_sensor) REFERENCES sensores(id_sensor) ON DELETE CASCADE,
    INDEX idx_sensor_timestamp (id_sensor, timestamp_datetime),
    INDEX idx_timestamp (timestamp_datetime),
    INDEX idx_qualidade (qualidade_dados),
    INDEX idx_anomalia (anomalia_detectada)
) ENGINE=InnoDB
PARTITION BY RANGE (UNIX_TIMESTAMP(timestamp_datetime)) (
    PARTITION p2024 VALUES LESS THAN (UNIX_TIMESTAMP('2025-01-01')),
    PARTITION p2025 VALUES LESS THAN (UNIX_TIMESTAMP('2026-01-01')),
    PARTITION p2026 VALUES LESS THAN (UNIX_TIMESTAMP('2027-01-01')),
    PARTITION p_future VALUES LESS THAN MAXVALUE
);

-- =====================================================
-- TABELA: modos_operacao
-- Estados de operação do sistema
-- =====================================================
CREATE TABLE modos_operacao (
    id_modo INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(50) NOT NULL UNIQUE,
    descricao TEXT,
    cor_indicador VARCHAR(7), -- Código hexadecimal da cor
    ativo BOOLEAN DEFAULT TRUE,
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- =====================================================
-- TABELA: alertas
-- Sistema de alertas e notificações
-- =====================================================
CREATE TABLE alertas (
    id_alerta BIGINT AUTO_INCREMENT PRIMARY KEY,
    id_dispositivo INT NOT NULL,
    id_sensor INT,
    id_modo INT NOT NULL,
    tipo_alerta ENUM('temperatura', 'umidade', 'pressao', 'vibracao', 'nivel', 'conexao', 'geral') NOT NULL,
    severidade ENUM('baixa', 'media', 'alta', 'critica') NOT NULL,
    titulo VARCHAR(200) NOT NULL,
    descricao TEXT,
    valor_atual DECIMAL(12,6),
    valor_limite DECIMAL(12,6),
    timestamp_alerta TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status ENUM('ativo', 'resolvido', 'ignorado') DEFAULT 'ativo',
    data_resolucao TIMESTAMP NULL,
    usuario_resolucao VARCHAR(100),
    observacoes_resolucao TEXT,
    FOREIGN KEY (id_dispositivo) REFERENCES dispositivos(id_dispositivo) ON DELETE CASCADE,
    FOREIGN KEY (id_sensor) REFERENCES sensores(id_sensor) ON DELETE SET NULL,
    FOREIGN KEY (id_modo) REFERENCES modos_operacao(id_modo),
    INDEX idx_dispositivo (id_dispositivo),
    INDEX idx_timestamp (timestamp_alerta),
    INDEX idx_status (status),
    INDEX idx_severidade (severidade)
) ENGINE=InnoDB;

-- =====================================================
-- TABELA: configuracoes_limites
-- Configurações de limites para alertas
-- =====================================================
CREATE TABLE configuracoes_limites (
    id_configuracao INT AUTO_INCREMENT PRIMARY KEY,
    id_sensor INT NOT NULL,
    tipo_limite ENUM('minimo', 'maximo', 'variacao') NOT NULL,
    valor_limite DECIMAL(12,6) NOT NULL,
    severidade ENUM('baixa', 'media', 'alta', 'critica') NOT NULL,
    ativo BOOLEAN DEFAULT TRUE,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    usuario_criacao VARCHAR(100),
    observacoes TEXT,
    FOREIGN KEY (id_sensor) REFERENCES sensores(id_sensor) ON DELETE CASCADE,
    INDEX idx_sensor (id_sensor),
    INDEX idx_tipo_limite (tipo_limite),
    INDEX idx_ativo (ativo)
) ENGINE=InnoDB;

-- =====================================================
-- TABELA: usuarios
-- Usuários do sistema
-- =====================================================
CREATE TABLE usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    senha_hash VARCHAR(255) NOT NULL,
    perfil ENUM('admin', 'operador', 'visualizador') NOT NULL,
    ativo BOOLEAN DEFAULT TRUE,
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ultimo_login TIMESTAMP NULL,
    token_reset_senha VARCHAR(255),
    data_expiracao_token TIMESTAMP NULL,
    INDEX idx_email (email),
    INDEX idx_perfil (perfil),
    INDEX idx_ativo (ativo)
) ENGINE=InnoDB;

-- =====================================================
-- TABELA: logs_sistema
-- Log de atividades do sistema
-- =====================================================
CREATE TABLE logs_sistema (
    id_log BIGINT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT,
    acao VARCHAR(100) NOT NULL,
    tabela_afetada VARCHAR(50),
    id_registro_afetado BIGINT,
    dados_anteriores JSON,
    dados_novos JSON,
    ip_origem VARCHAR(45),
    user_agent TEXT,
    timestamp_log TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE SET NULL,
    INDEX idx_usuario (id_usuario),
    INDEX idx_acao (acao),
    INDEX idx_timestamp (timestamp_log),
    INDEX idx_tabela (tabela_afetada)
) ENGINE=InnoDB;

-- =====================================================
-- TABELA: dashboards
-- Configurações de dashboards personalizados
-- =====================================================
CREATE TABLE dashboards (
    id_dashboard INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    nome VARCHAR(100) NOT NULL,
    descricao TEXT,
    configuracoes JSON,
    publico BOOLEAN DEFAULT FALSE,
    ativo BOOLEAN DEFAULT TRUE,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE CASCADE,
    INDEX idx_usuario (id_usuario),
    INDEX idx_publico (publico),
    INDEX idx_ativo (ativo)
) ENGINE=InnoDB;

-- =====================================================
-- TABELA: relatorios
-- Configurações de relatórios automáticos
-- =====================================================
CREATE TABLE relatorios (
    id_relatorio INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    nome VARCHAR(100) NOT NULL,
    tipo_relatorio ENUM('diario', 'semanal', 'mensal', 'personalizado') NOT NULL,
    configuracoes JSON,
    frequencia VARCHAR(50), -- Cron expression
    ativo BOOLEAN DEFAULT TRUE,
    proxima_execucao TIMESTAMP,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE CASCADE,
    INDEX idx_usuario (id_usuario),
    INDEX idx_tipo (tipo_relatorio),
    INDEX idx_proxima_execucao (proxima_execucao)
) ENGINE=InnoDB;

-- =====================================================
-- INSERÇÃO DE DADOS INICIAIS
-- =====================================================

-- Inserir tipos de sensores
INSERT INTO tipos_sensor (nome, descricao, unidade_medida, faixa_min, faixa_max, precisao) VALUES
('DHT22', 'Sensor de temperatura e umidade digital', '°C/%', -40.0, 80.0, 0.5),
('LDR', 'Sensor de luminosidade (Light Dependent Resistor)', 'lux', 0.0, 1023.0, 1.0),
('PIR', 'Sensor de movimento passivo infravermelho', 'boolean', 0.0, 1.0, 1.0),
('Pressão', 'Sensor de pressão barométrica', 'bar', 0.0, 10.0, 0.01),
('Vibração', 'Sensor de vibração triaxial', 'g', -2.0, 2.0, 0.001),
('Nível', 'Sensor de nível ultrassônico', 'cm', 0.0, 200.0, 0.1);

-- Inserir modos de operação
INSERT INTO modos_operacao (nome, descricao, cor_indicador) VALUES
('Normal', 'Sistema operando dentro dos parâmetros normais', '#28a745'),
('Alerta', 'Sistema com valores próximos aos limites', '#ffc107'),
('Falha', 'Sistema com falha ou valores críticos', '#dc3545');

-- Inserir usuário administrador padrão
INSERT INTO usuarios (nome, email, senha_hash, perfil) VALUES
('Administrador', 'admin@iot.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/8Kz8KzK', 'admin');

-- Inserir dispositivo de exemplo
INSERT INTO dispositivos (nome, mac_address, ip_address, localizacao, versao_firmware) VALUES
('ESP32-Sala-01', 'AA:BB:CC:DD:EE:FF', '192.168.1.100', 'Sala de Controle Principal', 'v1.2.3'),
('ESP32-Garagem-01', '11:22:33:44:55:66', '192.168.1.101', 'Garagem - Portão Principal', 'v1.2.3');

-- Inserir sensores para o dispositivo
INSERT INTO sensores (id_dispositivo, id_tipo_sensor, nome, pino_analogico, pino_digital) VALUES
(1, 1, 'DHT22-Temperatura', NULL, 2),
(1, 1, 'DHT22-Umidade', NULL, 2),
(1, 2, 'LDR-Luminosidade', 34, NULL),
(1, 3, 'PIR-Movimento', NULL, 4),
(1, 4, 'Pressão-Barométrica', 36, NULL),
(1, 5, 'Vibração-X', 39, NULL),
(1, 5, 'Vibração-Y', 35, NULL),
(1, 5, 'Vibração-Z', 32, NULL),
(1, 6, 'Nível-Ultrassônico', 33, NULL);

-- =====================================================
-- VIEWS PARA FACILITAR CONSULTAS
-- =====================================================

-- View para leituras com informações completas
CREATE VIEW vw_leituras_completas AS
SELECT 
    ls.id_leitura,
    d.nome as dispositivo,
    d.localizacao,
    ts.nome as tipo_sensor,
    s.nome as sensor,
    ls.timestamp_datetime,
    ls.valor_numerico,
    ls.valor_booleano,
    ls.valor_string,
    ls.qualidade_dados,
    ls.anomalia_detectada,
    mo.nome as modo_operacao,
    mo.cor_indicador
FROM leituras_sensores ls
JOIN sensores s ON ls.id_sensor = s.id_sensor
JOIN dispositivos d ON s.id_dispositivo = d.id_dispositivo
JOIN tipos_sensor ts ON s.id_tipo_sensor = ts.id_tipo_sensor
LEFT JOIN modos_operacao mo ON ls.qualidade_dados = mo.nome;

-- View para alertas ativos
CREATE VIEW vw_alertas_ativos AS
SELECT 
    a.id_alerta,
    d.nome as dispositivo,
    d.localizacao,
    s.nome as sensor,
    a.tipo_alerta,
    a.severidade,
    a.titulo,
    a.descricao,
    a.valor_atual,
    a.valor_limite,
    a.timestamp_alerta,
    mo.cor_indicador
FROM alertas a
JOIN dispositivos d ON a.id_dispositivo = d.id_dispositivo
LEFT JOIN sensores s ON a.id_sensor = s.id_sensor
JOIN modos_operacao mo ON a.id_modo = mo.id_modo
WHERE a.status = 'ativo';

-- =====================================================
-- STORED PROCEDURES
-- =====================================================

DELIMITER //

-- Procedure para inserir leitura de sensor
CREATE PROCEDURE sp_inserir_leitura(
    IN p_id_sensor INT,
    IN p_timestamp_unix DECIMAL(15,3),
    IN p_valor_numerico DECIMAL(12,6),
    IN p_valor_booleano BOOLEAN,
    IN p_valor_string VARCHAR(255),
    IN p_qualidade_dados ENUM('excelente', 'bom', 'regular', 'ruim')
)
BEGIN
    DECLARE v_timestamp_datetime TIMESTAMP;
    DECLARE v_anomalia BOOLEAN DEFAULT FALSE;
    
    -- Converte timestamp unix para datetime
    SET v_timestamp_datetime = FROM_UNIXTIME(p_timestamp_unix);
    
    -- Verifica se há anomalia baseada na qualidade dos dados
    IF p_qualidade_dados IN ('regular', 'ruim') THEN
        SET v_anomalia = TRUE;
    END IF;
    
    -- Insere a leitura
    INSERT INTO leituras_sensores (
        id_sensor, timestamp_unix, timestamp_datetime, 
        valor_numerico, valor_booleano, valor_string, 
        qualidade_dados, anomalia_detectada
    ) VALUES (
        p_id_sensor, p_timestamp_unix, v_timestamp_datetime,
        p_valor_numerico, p_valor_booleano, p_valor_string,
        p_qualidade_dados, v_anomalia
    );
    
    -- Retorna o ID da leitura inserida
    SELECT LAST_INSERT_ID() as id_leitura;
END //

-- Procedure para verificar limites e criar alertas
CREATE PROCEDURE sp_verificar_limites(IN p_id_sensor INT, IN p_valor DECIMAL(12,6))
BEGIN
    DECLARE v_limite_max DECIMAL(12,6);
    DECLARE v_limite_min DECIMAL(12,6);
    DECLARE v_severidade_max VARCHAR(20);
    DECLARE v_severidade_min VARCHAR(20);
    DECLARE v_id_dispositivo INT;
    DECLARE v_tipo_sensor VARCHAR(50);
    
    -- Obtém informações do sensor
    SELECT s.id_dispositivo, ts.nome
    INTO v_id_dispositivo, v_tipo_sensor
    FROM sensores s
    JOIN tipos_sensor ts ON s.id_tipo_sensor = ts.id_tipo_sensor
    WHERE s.id_sensor = p_id_sensor;
    
    -- Verifica limite máximo
    SELECT valor_limite, severidade
    INTO v_limite_max, v_severidade_max
    FROM configuracoes_limites
    WHERE id_sensor = p_id_sensor 
    AND tipo_limite = 'maximo' 
    AND ativo = TRUE
    ORDER BY severidade DESC
    LIMIT 1;
    
    -- Verifica limite mínimo
    SELECT valor_limite, severidade
    INTO v_limite_min, v_severidade_min
    FROM configuracoes_limites
    WHERE id_sensor = p_id_sensor 
    AND tipo_limite = 'minimo' 
    AND ativo = TRUE
    ORDER BY severidade DESC
    LIMIT 1;
    
    -- Cria alerta se excedeu limite máximo
    IF v_limite_max IS NOT NULL AND p_valor > v_limite_max THEN
        INSERT INTO alertas (
            id_dispositivo, id_sensor, id_modo, tipo_alerta, severidade,
            titulo, descricao, valor_atual, valor_limite
        ) VALUES (
            v_id_dispositivo, p_id_sensor, 2, -- Modo de falha
            v_tipo_sensor, v_severidade_max,
            CONCAT('Valor excedeu limite máximo: ', v_tipo_sensor),
            CONCAT('Valor atual: ', p_valor, ' | Limite: ', v_limite_max),
            p_valor, v_limite_max
        );
    END IF;
    
    -- Cria alerta se excedeu limite mínimo
    IF v_limite_min IS NOT NULL AND p_valor < v_limite_min THEN
        INSERT INTO alertas (
            id_dispositivo, id_sensor, id_modo, tipo_alerta, severidade,
            titulo, descricao, valor_atual, valor_limite
        ) VALUES (
            v_id_dispositivo, p_id_sensor, 2, -- Modo de falha
            v_tipo_sensor, v_severidade_min,
            CONCAT('Valor abaixo do limite mínimo: ', v_tipo_sensor),
            CONCAT('Valor atual: ', p_valor, ' | Limite: ', v_limite_min),
            p_valor, v_limite_min
        );
    END IF;
END //

DELIMITER ;

-- =====================================================
-- TRIGGERS
-- =====================================================

-- Trigger para atualizar última conexão do dispositivo
DELIMITER //
CREATE TRIGGER tr_atualizar_ultima_conexao
AFTER INSERT ON leituras_sensores
FOR EACH ROW
BEGIN
    UPDATE dispositivos 
    SET ultima_conexao = CURRENT_TIMESTAMP
    WHERE id_dispositivo = (
        SELECT id_dispositivo 
        FROM sensores 
        WHERE id_sensor = NEW.id_sensor
    );
END //
DELIMITER ;

-- =====================================================
-- ÍNDICES ADICIONAIS PARA PERFORMANCE
-- =====================================================

-- Índices compostos para consultas frequentes
CREATE INDEX idx_leituras_sensor_data ON leituras_sensores(id_sensor, timestamp_datetime, qualidade_dados);
CREATE INDEX idx_alertas_status_data ON alertas(status, timestamp_alerta, severidade);
CREATE INDEX idx_dispositivos_status_local ON dispositivos(status, localizacao);

-- =====================================================
-- COMENTÁRIOS FINAIS
-- =====================================================

-- Este script cria um banco de dados completo para monitoramento IoT
-- com suporte a:
-- - Múltiplos dispositivos ESP32
-- - Diferentes tipos de sensores
-- - Sistema de alertas configurável
-- - Logs de auditoria
-- - Dashboards personalizáveis
-- - Relatórios automáticos
-- - Particionamento de dados por ano
-- - Views para facilitar consultas
-- - Stored procedures para operações complexas
-- - Triggers para atualizações automáticas
