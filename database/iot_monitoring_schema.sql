-- =====================================================
-- SCHEMA COMPLETO - SISTEMA IoT MONITORING
-- Arquivo: iot_monitoring_schema.sql
-- Versão: 1.0
-- Data: 2025-01-11
-- Descrição: Schema completo do banco de dados para sistema IoT
-- =====================================================

-- Configurações iniciais
SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION';

-- Criar banco de dados
CREATE SCHEMA IF NOT EXISTS `iot_monitoring_db` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `iot_monitoring_db`;

-- =====================================================
-- TABELA: dispositivos
-- Armazena informações dos dispositivos ESP32
-- =====================================================
CREATE TABLE `dispositivos` (
  `id_dispositivo` INT NOT NULL AUTO_INCREMENT,
  `nome` VARCHAR(100) NOT NULL,
  `mac_address` VARCHAR(17) NOT NULL,
  `ip_address` VARCHAR(15) NULL DEFAULT NULL,
  `localizacao` VARCHAR(200) NULL DEFAULT NULL,
  `status` ENUM('ativo', 'inativo', 'manutencao') NOT NULL DEFAULT 'ativo',
  `data_cadastro` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `ultima_conexao` TIMESTAMP NULL DEFAULT NULL,
  `versao_firmware` VARCHAR(20) NULL DEFAULT NULL,
  `observacoes` TEXT NULL DEFAULT NULL,
  PRIMARY KEY (`id_dispositivo`),
  UNIQUE INDEX `uk_dispositivos_mac_address` (`mac_address` ASC) VISIBLE,
  INDEX `idx_dispositivos_status` (`status` ASC) VISIBLE,
  INDEX `idx_dispositivos_localizacao` (`localizacao` ASC) VISIBLE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_unicode_ci;

-- =====================================================
-- TABELA: tipos_sensor
-- Catálogo dos tipos de sensores disponíveis
-- =====================================================
CREATE TABLE `tipos_sensor` (
  `id_tipo_sensor` INT NOT NULL AUTO_INCREMENT,
  `nome` VARCHAR(50) NOT NULL,
  `descricao` TEXT NULL DEFAULT NULL,
  `unidade_medida` VARCHAR(20) NULL DEFAULT NULL,
  `faixa_min` DECIMAL(10,3) NULL DEFAULT NULL,
  `faixa_max` DECIMAL(10,3) NULL DEFAULT NULL,
  `precisao` DECIMAL(8,3) NULL DEFAULT NULL,
  `ativo` TINYINT(1) NOT NULL DEFAULT 1,
  `data_cadastro` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_tipo_sensor`),
  UNIQUE INDEX `uk_tipos_sensor_nome` (`nome` ASC) VISIBLE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_unicode_ci;

-- =====================================================
-- TABELA: sensores
-- Sensores instalados nos dispositivos
-- =====================================================
CREATE TABLE `sensores` (
  `id_sensor` INT NOT NULL AUTO_INCREMENT,
  `id_dispositivo` INT NOT NULL,
  `id_tipo_sensor` INT NOT NULL,
  `nome` VARCHAR(100) NOT NULL,
  `pino_analogico` INT NULL DEFAULT NULL,
  `pino_digital` INT NULL DEFAULT NULL,
  `calibracao_min` DECIMAL(10,3) NULL DEFAULT NULL,
  `calibracao_max` DECIMAL(10,3) NULL DEFAULT NULL,
  `status` ENUM('ativo', 'inativo', 'falha') NOT NULL DEFAULT 'ativo',
  `data_instalacao` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `ultima_calibracao` TIMESTAMP NULL DEFAULT NULL,
  `observacoes` TEXT NULL DEFAULT NULL,
  PRIMARY KEY (`id_sensor`),
  INDEX `fk_sensores_dispositivos_idx` (`id_dispositivo` ASC) VISIBLE,
  INDEX `fk_sensores_tipos_sensor_idx` (`id_tipo_sensor` ASC) VISIBLE,
  INDEX `idx_sensores_status` (`status` ASC) VISIBLE,
  CONSTRAINT `fk_sensores_dispositivos`
    FOREIGN KEY (`id_dispositivo`)
    REFERENCES `dispositivos` (`id_dispositivo`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_sensores_tipos_sensor`
    FOREIGN KEY (`id_tipo_sensor`)
    REFERENCES `tipos_sensor` (`id_tipo_sensor`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_unicode_ci;

-- =====================================================
-- TABELA: leituras_sensores
-- Dados coletados pelos sensores (tabela principal)
-- =====================================================
CREATE TABLE `leituras_sensores` (
  `id_leitura` BIGINT NOT NULL AUTO_INCREMENT,
  `id_sensor` INT NOT NULL,
  `timestamp_unix` DECIMAL(15,3) NOT NULL,
  `timestamp_datetime` TIMESTAMP NOT NULL,
  `valor_numerico` DECIMAL(12,6) NULL DEFAULT NULL,
  `valor_booleano` TINYINT(1) NULL DEFAULT NULL,
  `valor_string` VARCHAR(255) NULL DEFAULT NULL,
  `qualidade_dados` ENUM('excelente', 'bom', 'regular', 'ruim') NOT NULL DEFAULT 'bom',
  `anomalia_detectada` TINYINT(1) NOT NULL DEFAULT 0,
  `data_coleta` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_leitura`),
  INDEX `fk_leituras_sensores_idx` (`id_sensor` ASC) VISIBLE,
  INDEX `idx_leituras_timestamp` (`timestamp_datetime` ASC) VISIBLE,
  INDEX `idx_leituras_qualidade` (`qualidade_dados` ASC) VISIBLE,
  INDEX `idx_leituras_anomalia` (`anomalia_detectada` ASC) VISIBLE,
  INDEX `idx_leituras_sensor_timestamp` (`id_sensor` ASC, `timestamp_datetime` ASC) VISIBLE,
  CONSTRAINT `fk_leituras_sensores`
    FOREIGN KEY (`id_sensor`)
    REFERENCES `sensores` (`id_sensor`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_unicode_ci
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
CREATE TABLE `modos_operacao` (
  `id_modo` INT NOT NULL AUTO_INCREMENT,
  `nome` VARCHAR(50) NOT NULL,
  `descricao` TEXT NULL DEFAULT NULL,
  `cor_indicador` VARCHAR(7) NULL DEFAULT NULL,
  `ativo` TINYINT(1) NOT NULL DEFAULT 1,
  `data_cadastro` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_modo`),
  UNIQUE INDEX `uk_modos_operacao_nome` (`nome` ASC) VISIBLE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_unicode_ci;

-- =====================================================
-- TABELA: alertas
-- Sistema de alertas e notificações
-- =====================================================
CREATE TABLE `alertas` (
  `id_alerta` BIGINT NOT NULL AUTO_INCREMENT,
  `id_dispositivo` INT NOT NULL,
  `id_sensor` INT NULL DEFAULT NULL,
  `id_modo` INT NOT NULL,
  `tipo_alerta` ENUM('temperatura', 'umidade', 'pressao', 'vibracao', 'nivel', 'conexao', 'geral') NOT NULL,
  `severidade` ENUM('baixa', 'media', 'alta', 'critica') NOT NULL,
  `titulo` VARCHAR(200) NOT NULL,
  `descricao` TEXT NULL DEFAULT NULL,
  `valor_atual` DECIMAL(12,6) NULL DEFAULT NULL,
  `valor_limite` DECIMAL(12,6) NULL DEFAULT NULL,
  `timestamp_alerta` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `status` ENUM('ativo', 'resolvido', 'ignorado') NOT NULL DEFAULT 'ativo',
  `data_resolucao` TIMESTAMP NULL DEFAULT NULL,
  `usuario_resolucao` VARCHAR(100) NULL DEFAULT NULL,
  `observacoes_resolucao` TEXT NULL DEFAULT NULL,
  PRIMARY KEY (`id_alerta`),
  INDEX `fk_alertas_dispositivos_idx` (`id_dispositivo` ASC) VISIBLE,
  INDEX `fk_alertas_sensores_idx` (`id_sensor` ASC) VISIBLE,
  INDEX `fk_alertas_modos_operacao_idx` (`id_modo` ASC) VISIBLE,
  INDEX `idx_alertas_timestamp` (`timestamp_alerta` ASC) VISIBLE,
  INDEX `idx_alertas_status` (`status` ASC) VISIBLE,
  INDEX `idx_alertas_severidade` (`severidade` ASC) VISIBLE,
  CONSTRAINT `fk_alertas_dispositivos`
    FOREIGN KEY (`id_dispositivo`)
    REFERENCES `dispositivos` (`id_dispositivo`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_alertas_sensores`
    FOREIGN KEY (`id_sensor`)
    REFERENCES `sensores` (`id_sensor`)
    ON DELETE SET NULL
    ON UPDATE CASCADE,
  CONSTRAINT `fk_alertas_modos_operacao`
    FOREIGN KEY (`id_modo`)
    REFERENCES `modos_operacao` (`id_modo`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_unicode_ci;

-- =====================================================
-- TABELA: configuracoes_limites
-- Configurações de limites para alertas
-- =====================================================
CREATE TABLE `configuracoes_limites` (
  `id_configuracao` INT NOT NULL AUTO_INCREMENT,
  `id_sensor` INT NOT NULL,
  `tipo_limite` ENUM('minimo', 'maximo', 'variacao') NOT NULL,
  `valor_limite` DECIMAL(12,6) NOT NULL,
  `severidade` ENUM('baixa', 'media', 'alta', 'critica') NOT NULL,
  `ativo` TINYINT(1) NOT NULL DEFAULT 1,
  `data_criacao` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `data_atualizacao` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `usuario_criacao` VARCHAR(100) NULL DEFAULT NULL,
  `observacoes` TEXT NULL DEFAULT NULL,
  PRIMARY KEY (`id_configuracao`),
  INDEX `fk_configuracoes_limites_sensores_idx` (`id_sensor` ASC) VISIBLE,
  INDEX `idx_configuracoes_tipo_limite` (`tipo_limite` ASC) VISIBLE,
  INDEX `idx_configuracoes_ativo` (`ativo` ASC) VISIBLE,
  CONSTRAINT `fk_configuracoes_limites_sensores`
    FOREIGN KEY (`id_sensor`)
    REFERENCES `sensores` (`id_sensor`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_unicode_ci;

-- =====================================================
-- TABELA: usuarios
-- Usuários do sistema
-- =====================================================
CREATE TABLE `usuarios` (
  `id_usuario` INT NOT NULL AUTO_INCREMENT,
  `nome` VARCHAR(100) NOT NULL,
  `email` VARCHAR(255) NOT NULL,
  `senha_hash` VARCHAR(255) NOT NULL,
  `perfil` ENUM('admin', 'operador', 'visualizador') NOT NULL,
  `ativo` TINYINT(1) NOT NULL DEFAULT 1,
  `data_cadastro` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `ultimo_login` TIMESTAMP NULL DEFAULT NULL,
  `token_reset_senha` VARCHAR(255) NULL DEFAULT NULL,
  `data_expiracao_token` TIMESTAMP NULL DEFAULT NULL,
  PRIMARY KEY (`id_usuario`),
  UNIQUE INDEX `uk_usuarios_email` (`email` ASC) VISIBLE,
  INDEX `idx_usuarios_perfil` (`perfil` ASC) VISIBLE,
  INDEX `idx_usuarios_ativo` (`ativo` ASC) VISIBLE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_unicode_ci;

-- =====================================================
-- TABELA: logs_sistema
-- Log de atividades do sistema
-- =====================================================
CREATE TABLE `logs_sistema` (
  `id_log` BIGINT NOT NULL AUTO_INCREMENT,
  `id_usuario` INT NULL DEFAULT NULL,
  `acao` VARCHAR(100) NOT NULL,
  `tabela_afetada` VARCHAR(50) NULL DEFAULT NULL,
  `id_registro_afetado` BIGINT NULL DEFAULT NULL,
  `dados_anteriores` JSON NULL DEFAULT NULL,
  `dados_novos` JSON NULL DEFAULT NULL,
  `ip_origem` VARCHAR(45) NULL DEFAULT NULL,
  `user_agent` TEXT NULL DEFAULT NULL,
  `timestamp_log` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_log`),
  INDEX `fk_logs_sistema_usuarios_idx` (`id_usuario` ASC) VISIBLE,
  INDEX `idx_logs_acao` (`acao` ASC) VISIBLE,
  INDEX `idx_logs_timestamp` (`timestamp_log` ASC) VISIBLE,
  INDEX `idx_logs_tabela` (`tabela_afetada` ASC) VISIBLE,
  CONSTRAINT `fk_logs_sistema_usuarios`
    FOREIGN KEY (`id_usuario`)
    REFERENCES `usuarios` (`id_usuario`)
    ON DELETE SET NULL
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_unicode_ci;

-- =====================================================
-- TABELA: dashboards
-- Configurações de dashboards personalizados
-- =====================================================
CREATE TABLE `dashboards` (
  `id_dashboard` INT NOT NULL AUTO_INCREMENT,
  `id_usuario` INT NOT NULL,
  `nome` VARCHAR(100) NOT NULL,
  `descricao` TEXT NULL DEFAULT NULL,
  `configuracoes` JSON NULL DEFAULT NULL,
  `publico` TINYINT(1) NOT NULL DEFAULT 0,
  `ativo` TINYINT(1) NOT NULL DEFAULT 1,
  `data_criacao` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `data_atualizacao` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_dashboard`),
  INDEX `fk_dashboards_usuarios_idx` (`id_usuario` ASC) VISIBLE,
  INDEX `idx_dashboards_publico` (`publico` ASC) VISIBLE,
  INDEX `idx_dashboards_ativo` (`ativo` ASC) VISIBLE,
  CONSTRAINT `fk_dashboards_usuarios`
    FOREIGN KEY (`id_usuario`)
    REFERENCES `usuarios` (`id_usuario`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_unicode_ci;

-- =====================================================
-- TABELA: relatorios
-- Configurações de relatórios automáticos
-- =====================================================
CREATE TABLE `relatorios` (
  `id_relatorio` INT NOT NULL AUTO_INCREMENT,
  `id_usuario` INT NOT NULL,
  `nome` VARCHAR(100) NOT NULL,
  `tipo_relatorio` ENUM('diario', 'semanal', 'mensal', 'personalizado') NOT NULL,
  `configuracoes` JSON NULL DEFAULT NULL,
  `frequencia` VARCHAR(50) NULL DEFAULT NULL,
  `ativo` TINYINT(1) NOT NULL DEFAULT 1,
  `proxima_execucao` TIMESTAMP NULL DEFAULT NULL,
  `data_criacao` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_relatorio`),
  INDEX `fk_relatorios_usuarios_idx` (`id_usuario` ASC) VISIBLE,
  INDEX `idx_relatorios_tipo` (`tipo_relatorio` ASC) VISIBLE,
  INDEX `idx_relatorios_proxima_execucao` (`proxima_execucao` ASC) VISIBLE,
  CONSTRAINT `fk_relatorios_usuarios`
    FOREIGN KEY (`id_usuario`)
    REFERENCES `usuarios` (`id_usuario`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_unicode_ci;

-- =====================================================
-- VIEWS PARA FACILITAR CONSULTAS
-- =====================================================

-- View para leituras com informações completas
CREATE VIEW `vw_leituras_completas` AS
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
CREATE VIEW `vw_alertas_ativos` AS
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
CREATE PROCEDURE `sp_inserir_leitura`(
    IN p_id_sensor INT,
    IN p_timestamp_unix DECIMAL(15,3),
    IN p_valor_numerico DECIMAL(12,6),
    IN p_valor_booleano TINYINT(1),
    IN p_valor_string VARCHAR(255),
    IN p_qualidade_dados ENUM('excelente', 'bom', 'regular', 'ruim')
)
BEGIN
    DECLARE v_timestamp_datetime TIMESTAMP;
    DECLARE v_anomalia TINYINT(1) DEFAULT 0;
    
    -- Converte timestamp unix para datetime
    SET v_timestamp_datetime = FROM_UNIXTIME(p_timestamp_unix);
    
    -- Verifica se há anomalia baseada na qualidade dos dados
    IF p_qualidade_dados IN ('regular', 'ruim') THEN
        SET v_anomalia = 1;
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
CREATE PROCEDURE `sp_verificar_limites`(IN p_id_sensor INT, IN p_valor DECIMAL(12,6))
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
    AND ativo = 1
    ORDER BY severidade DESC
    LIMIT 1;
    
    -- Verifica limite mínimo
    SELECT valor_limite, severidade
    INTO v_limite_min, v_severidade_min
    FROM configuracoes_limites
    WHERE id_sensor = p_id_sensor 
    AND tipo_limite = 'minimo' 
    AND ativo = 1
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
END //
DELIMITER ;

-- =====================================================
-- ÍNDICES ADICIONAIS PARA PERFORMANCE
-- =====================================================

-- Índices compostos para consultas frequentes
CREATE INDEX `idx_leituras_sensor_data` ON `leituras_sensores`(`id_sensor`, `timestamp_datetime`, `qualidade_dados`);
CREATE INDEX `idx_alertas_status_data` ON `alertas`(`status`, `timestamp_alerta`, `severidade`);
CREATE INDEX `idx_dispositivos_status_local` ON `dispositivos`(`status`, `localizacao`);

-- =====================================================
-- DADOS INICIAIS
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

-- Inserir dispositivos de exemplo
INSERT INTO dispositivos (nome, mac_address, ip_address, localizacao, versao_firmware) VALUES
('ESP32-Sala-01', 'AA:BB:CC:DD:EE:FF', '192.168.1.100', 'Sala de Controle Principal', 'v1.2.3'),
('ESP32-Garagem-01', '11:22:33:44:55:66', '192.168.1.101', 'Garagem - Portão Principal', 'v1.2.3'),
('ESP32-Cozinha-01', '22:33:44:55:66:77', '192.168.1.102', 'Cozinha - Monitoramento', 'v1.2.3');

-- Inserir sensores para os dispositivos
INSERT INTO sensores (id_dispositivo, id_tipo_sensor, nome, pino_analogico, pino_digital) VALUES
-- Dispositivo 1 (Sala)
(1, 1, 'DHT22-Temperatura', NULL, 2),
(1, 1, 'DHT22-Umidade', NULL, 2),
(1, 2, 'LDR-Luminosidade', 34, NULL),
(1, 3, 'PIR-Movimento', NULL, 4),
(1, 4, 'Pressão-Barométrica', 36, NULL),
(1, 5, 'Vibração-X', 39, NULL),
(1, 5, 'Vibração-Y', 35, NULL),
(1, 5, 'Vibração-Z', 32, NULL),
(1, 6, 'Nível-Ultrassônico', 33, NULL),
-- Dispositivo 2 (Garagem)
(2, 1, 'DHT22-Temperatura', NULL, 2),
(2, 1, 'DHT22-Umidade', NULL, 2),
(2, 2, 'LDR-Luminosidade', 34, NULL),
(2, 3, 'PIR-Movimento', NULL, 4),
(2, 4, 'Pressão-Barométrica', 36, NULL),
(2, 5, 'Vibração-X', 39, NULL),
(2, 5, 'Vibração-Y', 35, NULL),
(2, 5, 'Vibração-Z', 32, NULL),
(2, 6, 'Nível-Ultrassônico', 33, NULL),
-- Dispositivo 3 (Cozinha)
(3, 1, 'DHT22-Temperatura', NULL, 2),
(3, 1, 'DHT22-Umidade', NULL, 2),
(3, 2, 'LDR-Luminosidade', 34, NULL),
(3, 3, 'PIR-Movimento', NULL, 4),
(3, 4, 'Pressão-Barométrica', 36, NULL),
(3, 5, 'Vibração-X', 39, NULL),
(3, 5, 'Vibração-Y', 35, NULL),
(3, 5, 'Vibração-Z', 32, NULL),
(3, 6, 'Nível-Ultrassônico', 33, NULL);

-- =====================================================
-- RESTAURAR CONFIGURAÇÕES
-- =====================================================

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

-- =====================================================
-- COMENTÁRIOS FINAIS
-- =====================================================

-- Este schema cria um banco de dados completo para monitoramento IoT
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
