-- =====================================================
-- SCRIPT SQL - CRIAÇÃO DAS TABELAS
-- Sistema IoT Monitoring - Sprint 3
-- Arquivo: criar_tabelas_iot.sql
-- Versão: 1.0
-- Data: 2025-01-11
-- Descrição: Script completo para criação das tabelas do banco de dados
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
  `id_dispositivo` INT NOT NULL AUTO_INCREMENT COMMENT 'Identificador único do dispositivo',
  `nome` VARCHAR(100) NOT NULL COMMENT 'Nome identificador do dispositivo',
  `mac_address` VARCHAR(17) NOT NULL COMMENT 'Endereço MAC único para identificação',
  `ip_address` VARCHAR(15) NULL DEFAULT NULL COMMENT 'Endereço IP atual do dispositivo',
  `localizacao` VARCHAR(200) NULL DEFAULT NULL COMMENT 'Local físico onde o dispositivo está instalado',
  `status` ENUM('ativo', 'inativo', 'manutencao') NOT NULL DEFAULT 'ativo' COMMENT 'Estado operacional do dispositivo',
  `data_cadastro` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Data de cadastro do dispositivo',
  `ultima_conexao` TIMESTAMP NULL DEFAULT NULL COMMENT 'Timestamp da última comunicação',
  `versao_firmware` VARCHAR(20) NULL DEFAULT NULL COMMENT 'Versão do firmware instalado',
  `observacoes` TEXT NULL DEFAULT NULL COMMENT 'Observações adicionais',
  PRIMARY KEY (`id_dispositivo`),
  UNIQUE INDEX `uk_dispositivos_mac_address` (`mac_address` ASC) VISIBLE,
  INDEX `idx_dispositivos_status` (`status` ASC) VISIBLE,
  INDEX `idx_dispositivos_localizacao` (`localizacao` ASC) VISIBLE,
  INDEX `idx_dispositivos_ultima_conexao` (`ultima_conexao` ASC) VISIBLE
) ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_unicode_ci
COMMENT = 'Dispositivos ESP32 conectados ao sistema';

-- =====================================================
-- TABELA: tipos_sensor
-- Catálogo dos tipos de sensores disponíveis
-- =====================================================
CREATE TABLE `tipos_sensor` (
  `id_tipo_sensor` INT NOT NULL AUTO_INCREMENT COMMENT 'Identificador único do tipo de sensor',
  `nome` VARCHAR(50) NOT NULL COMMENT 'Nome do tipo de sensor',
  `descricao` TEXT NULL DEFAULT NULL COMMENT 'Descrição detalhada do sensor',
  `unidade_medida` VARCHAR(20) NULL DEFAULT NULL COMMENT 'Unidade de medida específica',
  `faixa_min` DECIMAL(10,3) NULL DEFAULT NULL COMMENT 'Valor mínimo da faixa operacional',
  `faixa_max` DECIMAL(10,3) NULL DEFAULT NULL COMMENT 'Valor máximo da faixa operacional',
  `precisao` DECIMAL(8,3) NULL DEFAULT NULL COMMENT 'Precisão do sensor',
  `ativo` TINYINT(1) NOT NULL DEFAULT 1 COMMENT 'Indica se o tipo está ativo',
  `data_cadastro` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Data de cadastro do tipo',
  PRIMARY KEY (`id_tipo_sensor`),
  UNIQUE INDEX `uk_tipos_sensor_nome` (`nome` ASC) VISIBLE,
  INDEX `idx_tipos_sensor_ativo` (`ativo` ASC) VISIBLE
) ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_unicode_ci
COMMENT = 'Catálogo dos tipos de sensores disponíveis';

-- =====================================================
-- TABELA: sensores
-- Sensores instalados nos dispositivos
-- =====================================================
CREATE TABLE `sensores` (
  `id_sensor` INT NOT NULL AUTO_INCREMENT COMMENT 'Identificador único do sensor',
  `id_dispositivo` INT NOT NULL COMMENT 'Referência ao dispositivo',
  `id_tipo_sensor` INT NOT NULL COMMENT 'Referência ao tipo de sensor',
  `nome` VARCHAR(100) NOT NULL COMMENT 'Nome identificador do sensor',
  `pino_analogico` INT NULL DEFAULT NULL COMMENT 'Pino analógico utilizado',
  `pino_digital` INT NULL DEFAULT NULL COMMENT 'Pino digital utilizado',
  `calibracao_min` DECIMAL(10,3) NULL DEFAULT NULL COMMENT 'Valor mínimo de calibração',
  `calibracao_max` DECIMAL(10,3) NULL DEFAULT NULL COMMENT 'Valor máximo de calibração',
  `status` ENUM('ativo', 'inativo', 'falha') NOT NULL DEFAULT 'ativo' COMMENT 'Estado operacional do sensor',
  `data_instalacao` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Data de instalação do sensor',
  `ultima_calibracao` TIMESTAMP NULL DEFAULT NULL COMMENT 'Data da última calibração',
  `observacoes` TEXT NULL DEFAULT NULL COMMENT 'Observações adicionais',
  PRIMARY KEY (`id_sensor`),
  INDEX `fk_sensores_dispositivos_idx` (`id_dispositivo` ASC) VISIBLE,
  INDEX `fk_sensores_tipos_sensor_idx` (`id_tipo_sensor` ASC) VISIBLE,
  INDEX `idx_sensores_status` (`status` ASC) VISIBLE,
  INDEX `idx_sensores_dispositivo_status` (`id_dispositivo` ASC, `status` ASC) VISIBLE,
  CONSTRAINT `fk_sensores_dispositivos`
    FOREIGN KEY (`id_dispositivo`)
    REFERENCES `dispositivos` (`id_dispositivo`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_sensores_tipos_sensor`
    FOREIGN KEY (`id_tipo_sensor`)
    REFERENCES `tipos_sensor` (`id_tipo_sensor`)
    ON DELETE CASCADE
    ON UPDATE CASCADE
) ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_unicode_ci
COMMENT = 'Sensores físicos instalados nos dispositivos';

-- =====================================================
-- TABELA: leituras_sensores
-- Dados coletados pelos sensores (tabela principal)
-- =====================================================
CREATE TABLE `leituras_sensores` (
  `id_leitura` BIGINT NOT NULL AUTO_INCREMENT COMMENT 'Identificador único da leitura',
  `id_sensor` INT NOT NULL COMMENT 'Referência ao sensor',
  `timestamp_unix` DECIMAL(15,3) NOT NULL COMMENT 'Timestamp Unix com precisão de milissegundos',
  `timestamp_datetime` TIMESTAMP NOT NULL COMMENT 'Timestamp legível para consultas',
  `valor_numerico` DECIMAL(12,6) NULL DEFAULT NULL COMMENT 'Valor numérico lido pelo sensor',
  `valor_booleano` TINYINT(1) NULL DEFAULT NULL COMMENT 'Valor booleano lido pelo sensor',
  `valor_string` VARCHAR(255) NULL DEFAULT NULL COMMENT 'Valor string lido pelo sensor',
  `qualidade_dados` ENUM('excelente', 'bom', 'regular', 'ruim') NOT NULL DEFAULT 'bom' COMMENT 'Classificação da qualidade dos dados',
  `anomalia_detectada` TINYINT(1) NOT NULL DEFAULT 0 COMMENT 'Flag indicando se anomalia foi detectada',
  `data_coleta` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Data de coleta do dado',
  PRIMARY KEY (`id_leitura`),
  INDEX `fk_leituras_sensores_idx` (`id_sensor` ASC) VISIBLE,
  INDEX `idx_leituras_timestamp` (`timestamp_datetime` ASC) VISIBLE,
  INDEX `idx_leituras_qualidade` (`qualidade_dados` ASC) VISIBLE,
  INDEX `idx_leituras_anomalia` (`anomalia_detectada` ASC) VISIBLE,
  INDEX `idx_leituras_sensor_timestamp` (`id_sensor` ASC, `timestamp_datetime` ASC) VISIBLE,
  INDEX `idx_leituras_data_coleta` (`data_coleta` ASC) VISIBLE,
  CONSTRAINT `fk_leituras_sensores`
    FOREIGN KEY (`id_sensor`)
    REFERENCES `sensores` (`id_sensor`)
    ON DELETE CASCADE
    ON UPDATE CASCADE
) ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_unicode_ci
COMMENT = 'Dados coletados pelos sensores (tabela principal)'
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
  `id_modo` INT NOT NULL AUTO_INCREMENT COMMENT 'Identificador único do modo',
  `nome` VARCHAR(50) NOT NULL COMMENT 'Nome do modo de operação',
  `descricao` TEXT NULL DEFAULT NULL COMMENT 'Descrição do modo',
  `cor_indicador` VARCHAR(7) NULL DEFAULT NULL COMMENT 'Código hexadecimal da cor para interface',
  `ativo` TINYINT(1) NOT NULL DEFAULT 1 COMMENT 'Indica se o modo está ativo',
  `data_cadastro` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Data de cadastro do modo',
  PRIMARY KEY (`id_modo`),
  UNIQUE INDEX `uk_modos_operacao_nome` (`nome` ASC) VISIBLE,
  INDEX `idx_modos_operacao_ativo` (`ativo` ASC) VISIBLE
) ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_unicode_ci
COMMENT = 'Estados de operação do sistema';

-- =====================================================
-- TABELA: alertas
-- Sistema de alertas e notificações
-- =====================================================
CREATE TABLE `alertas` (
  `id_alerta` BIGINT NOT NULL AUTO_INCREMENT COMMENT 'Identificador único do alerta',
  `id_dispositivo` INT NOT NULL COMMENT 'Referência ao dispositivo',
  `id_sensor` INT NULL DEFAULT NULL COMMENT 'Referência ao sensor (opcional)',
  `id_modo` INT NOT NULL COMMENT 'Referência ao modo de operação',
  `tipo_alerta` ENUM('temperatura', 'umidade', 'pressao', 'vibracao', 'nivel', 'conexao', 'geral') NOT NULL COMMENT 'Tipo do alerta',
  `severidade` ENUM('baixa', 'media', 'alta', 'critica') NOT NULL COMMENT 'Nível de severidade',
  `titulo` VARCHAR(200) NOT NULL COMMENT 'Título do alerta',
  `descricao` TEXT NULL DEFAULT NULL COMMENT 'Descrição detalhada do alerta',
  `valor_atual` DECIMAL(12,6) NULL DEFAULT NULL COMMENT 'Valor atual que gerou o alerta',
  `valor_limite` DECIMAL(12,6) NULL DEFAULT NULL COMMENT 'Valor limite configurado',
  `timestamp_alerta` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Timestamp do alerta',
  `status` ENUM('ativo', 'resolvido', 'ignorado') NOT NULL DEFAULT 'ativo' COMMENT 'Status do alerta',
  `data_resolucao` TIMESTAMP NULL DEFAULT NULL COMMENT 'Data de resolução do alerta',
  `usuario_resolucao` VARCHAR(100) NULL DEFAULT NULL COMMENT 'Usuário que resolveu o alerta',
  `observacoes_resolucao` TEXT NULL DEFAULT NULL COMMENT 'Observações da resolução',
  PRIMARY KEY (`id_alerta`),
  INDEX `fk_alertas_dispositivos_idx` (`id_dispositivo` ASC) VISIBLE,
  INDEX `fk_alertas_sensores_idx` (`id_sensor` ASC) VISIBLE,
  INDEX `fk_alertas_modos_operacao_idx` (`id_modo` ASC) VISIBLE,
  INDEX `idx_alertas_timestamp` (`timestamp_alerta` ASC) VISIBLE,
  INDEX `idx_alertas_status` (`status` ASC) VISIBLE,
  INDEX `idx_alertas_severidade` (`severidade` ASC) VISIBLE,
  INDEX `idx_alertas_tipo` (`tipo_alerta` ASC) VISIBLE,
  INDEX `idx_alertas_status_severidade` (`status` ASC, `severidade` ASC) VISIBLE,
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
    ON UPDATE CASCADE
) ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_unicode_ci
COMMENT = 'Sistema de alertas e notificações';

-- =====================================================
-- TABELA: configuracoes_limites
-- Configurações de limites para alertas
-- =====================================================
CREATE TABLE `configuracoes_limites` (
  `id_configuracao` INT NOT NULL AUTO_INCREMENT COMMENT 'Identificador único da configuração',
  `id_sensor` INT NOT NULL COMMENT 'Referência ao sensor',
  `tipo_limite` ENUM('minimo', 'maximo', 'variacao') NOT NULL COMMENT 'Tipo do limite',
  `valor_limite` DECIMAL(12,6) NOT NULL COMMENT 'Valor do limite',
  `severidade` ENUM('baixa', 'media', 'alta', 'critica') NOT NULL COMMENT 'Severidade do alerta',
  `ativo` TINYINT(1) NOT NULL DEFAULT 1 COMMENT 'Indica se a configuração está ativa',
  `data_criacao` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Data de criação',
  `data_atualizacao` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Data de atualização',
  `usuario_criacao` VARCHAR(100) NULL DEFAULT NULL COMMENT 'Usuário que criou a configuração',
  `observacoes` TEXT NULL DEFAULT NULL COMMENT 'Observações adicionais',
  PRIMARY KEY (`id_configuracao`),
  INDEX `fk_configuracoes_limites_sensores_idx` (`id_sensor` ASC) VISIBLE,
  INDEX `idx_configuracoes_tipo_limite` (`tipo_limite` ASC) VISIBLE,
  INDEX `idx_configuracoes_ativo` (`ativo` ASC) VISIBLE,
  INDEX `idx_configuracoes_sensor_ativo` (`id_sensor` ASC, `ativo` ASC) VISIBLE,
  CONSTRAINT `fk_configuracoes_limites_sensores`
    FOREIGN KEY (`id_sensor`)
    REFERENCES `sensores` (`id_sensor`)
    ON DELETE CASCADE
    ON UPDATE CASCADE
) ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_unicode_ci
COMMENT = 'Configurações de limites para alertas';

-- =====================================================
-- TABELA: usuarios
-- Usuários do sistema
-- =====================================================
CREATE TABLE `usuarios` (
  `id_usuario` INT NOT NULL AUTO_INCREMENT COMMENT 'Identificador único do usuário',
  `nome` VARCHAR(100) NOT NULL COMMENT 'Nome completo do usuário',
  `email` VARCHAR(255) NOT NULL COMMENT 'Email único para login',
  `senha_hash` VARCHAR(255) NOT NULL COMMENT 'Hash da senha',
  `perfil` ENUM('admin', 'operador', 'visualizador') NOT NULL COMMENT 'Perfil de acesso do usuário',
  `ativo` TINYINT(1) NOT NULL DEFAULT 1 COMMENT 'Indica se o usuário está ativo',
  `data_cadastro` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Data de cadastro',
  `ultimo_login` TIMESTAMP NULL DEFAULT NULL COMMENT 'Data do último login',
  `token_reset_senha` VARCHAR(255) NULL DEFAULT NULL COMMENT 'Token para reset de senha',
  `data_expiracao_token` TIMESTAMP NULL DEFAULT NULL COMMENT 'Data de expiração do token',
  PRIMARY KEY (`id_usuario`),
  UNIQUE INDEX `uk_usuarios_email` (`email` ASC) VISIBLE,
  INDEX `idx_usuarios_perfil` (`perfil` ASC) VISIBLE,
  INDEX `idx_usuarios_ativo` (`ativo` ASC) VISIBLE,
  INDEX `idx_usuarios_perfil_ativo` (`perfil` ASC, `ativo` ASC) VISIBLE
) ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_unicode_ci
COMMENT = 'Usuários do sistema';

-- =====================================================
-- TABELA: logs_sistema
-- Log de atividades do sistema
-- =====================================================
CREATE TABLE `logs_sistema` (
  `id_log` BIGINT NOT NULL AUTO_INCREMENT COMMENT 'Identificador único do log',
  `id_usuario` INT NULL DEFAULT NULL COMMENT 'Referência ao usuário',
  `acao` VARCHAR(100) NOT NULL COMMENT 'Ação realizada',
  `tabela_afetada` VARCHAR(50) NULL DEFAULT NULL COMMENT 'Tabela afetada pela ação',
  `id_registro_afetado` BIGINT NULL DEFAULT NULL COMMENT 'ID do registro afetado',
  `dados_anteriores` JSON NULL DEFAULT NULL COMMENT 'Dados anteriores (JSON)',
  `dados_novos` JSON NULL DEFAULT NULL COMMENT 'Dados novos (JSON)',
  `ip_origem` VARCHAR(45) NULL DEFAULT NULL COMMENT 'IP de origem da ação',
  `user_agent` TEXT NULL DEFAULT NULL COMMENT 'User agent do navegador',
  `timestamp_log` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Timestamp do log',
  PRIMARY KEY (`id_log`),
  INDEX `fk_logs_sistema_usuarios_idx` (`id_usuario` ASC) VISIBLE,
  INDEX `idx_logs_acao` (`acao` ASC) VISIBLE,
  INDEX `idx_logs_timestamp` (`timestamp_log` ASC) VISIBLE,
  INDEX `idx_logs_tabela` (`tabela_afetada` ASC) VISIBLE,
  INDEX `idx_logs_usuario_timestamp` (`id_usuario` ASC, `timestamp_log` ASC) VISIBLE,
  CONSTRAINT `fk_logs_sistema_usuarios`
    FOREIGN KEY (`id_usuario`)
    REFERENCES `usuarios` (`id_usuario`)
    ON DELETE SET NULL
    ON UPDATE CASCADE
) ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_unicode_ci
COMMENT = 'Log de atividades do sistema';

-- =====================================================
-- TABELA: dashboards
-- Configurações de dashboards personalizados
-- =====================================================
CREATE TABLE `dashboards` (
  `id_dashboard` INT NOT NULL AUTO_INCREMENT COMMENT 'Identificador único do dashboard',
  `id_usuario` INT NOT NULL COMMENT 'Referência ao usuário proprietário',
  `nome` VARCHAR(100) NOT NULL COMMENT 'Nome do dashboard',
  `descricao` TEXT NULL DEFAULT NULL COMMENT 'Descrição do dashboard',
  `configuracoes` JSON NULL DEFAULT NULL COMMENT 'Configurações do dashboard (JSON)',
  `publico` TINYINT(1) NOT NULL DEFAULT 0 COMMENT 'Indica se é público',
  `ativo` TINYINT(1) NOT NULL DEFAULT 1 COMMENT 'Indica se está ativo',
  `data_criacao` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Data de criação',
  `data_atualizacao` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Data de atualização',
  PRIMARY KEY (`id_dashboard`),
  INDEX `fk_dashboards_usuarios_idx` (`id_usuario` ASC) VISIBLE,
  INDEX `idx_dashboards_publico` (`publico` ASC) VISIBLE,
  INDEX `idx_dashboards_ativo` (`ativo` ASC) VISIBLE,
  INDEX `idx_dashboards_usuario_ativo` (`id_usuario` ASC, `ativo` ASC) VISIBLE,
  CONSTRAINT `fk_dashboards_usuarios`
    FOREIGN KEY (`id_usuario`)
    REFERENCES `usuarios` (`id_usuario`)
    ON DELETE CASCADE
    ON UPDATE CASCADE
) ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_unicode_ci
COMMENT = 'Configurações de dashboards personalizados';

-- =====================================================
-- TABELA: relatorios
-- Configurações de relatórios automáticos
-- =====================================================
CREATE TABLE `relatorios` (
  `id_relatorio` INT NOT NULL AUTO_INCREMENT COMMENT 'Identificador único do relatório',
  `id_usuario` INT NOT NULL COMMENT 'Referência ao usuário proprietário',
  `nome` VARCHAR(100) NOT NULL COMMENT 'Nome do relatório',
  `tipo_relatorio` ENUM('diario', 'semanal', 'mensal', 'personalizado') NOT NULL COMMENT 'Tipo do relatório',
  `configuracoes` JSON NULL DEFAULT NULL COMMENT 'Configurações do relatório (JSON)',
  `frequencia` VARCHAR(50) NULL DEFAULT NULL COMMENT 'Frequência de execução (cron)',
  `ativo` TINYINT(1) NOT NULL DEFAULT 1 COMMENT 'Indica se está ativo',
  `proxima_execucao` TIMESTAMP NULL DEFAULT NULL COMMENT 'Próxima execução agendada',
  `data_criacao` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Data de criação',
  PRIMARY KEY (`id_relatorio`),
  INDEX `fk_relatorios_usuarios_idx` (`id_usuario` ASC) VISIBLE,
  INDEX `idx_relatorios_tipo` (`tipo_relatorio` ASC) VISIBLE,
  INDEX `idx_relatorios_proxima_execucao` (`proxima_execucao` ASC) VISIBLE,
  INDEX `idx_relatorios_ativo` (`ativo` ASC) VISIBLE,
  CONSTRAINT `fk_relatorios_usuarios`
    FOREIGN KEY (`id_usuario`)
    REFERENCES `usuarios` (`id_usuario`)
    ON DELETE CASCADE
    ON UPDATE CASCADE
) ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_unicode_ci
COMMENT = 'Configurações de relatórios automáticos';

-- =====================================================
-- ÍNDICES ADICIONAIS PARA PERFORMANCE
-- =====================================================

-- Índices compostos para consultas frequentes
CREATE INDEX `idx_leituras_sensor_data_qualidade` ON `leituras_sensores`(`id_sensor`, `timestamp_datetime`, `qualidade_dados`);
CREATE INDEX `idx_alertas_status_data_severidade` ON `alertas`(`status`, `timestamp_alerta`, `severidade`);
CREATE INDEX `idx_dispositivos_status_local` ON `dispositivos`(`status`, `localizacao`);
CREATE INDEX `idx_sensores_dispositivo_tipo` ON `sensores`(`id_dispositivo`, `id_tipo_sensor`);

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
-- DADOS INICIAIS
-- =====================================================

-- Inserir tipos de sensores
INSERT INTO tipos_sensor (nome, descricao, unidade_medida, faixa_min, faixa_max, precisao) VALUES
('DHT22', 'Sensor de temperatura e umidade digital', '°C/%', -40.000, 80.000, 0.500),
('LDR', 'Sensor de luminosidade (Light Dependent Resistor)', 'lux', 0.000, 1023.000, 1.000),
('PIR', 'Sensor de movimento passivo infravermelho', 'boolean', 0.000, 1.000, 1.000),
('Pressão', 'Sensor de pressão barométrica', 'bar', 0.000, 10.000, 0.010),
('Vibração', 'Sensor de vibração triaxial', 'g', -2.000, 2.000, 0.001),
('Nível', 'Sensor de nível ultrassônico', 'cm', 0.000, 200.000, 0.100);

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

-- Este script cria um banco de dados completo para monitoramento IoT
-- com suporte a:
-- - 11 tabelas principais
-- - 10 relacionamentos bem definidos
-- - Índices otimizados para performance
-- - Triggers para atualizações automáticas
-- - Particionamento de dados por ano
-- - Dados iniciais para teste
-- - Comentários detalhados em cada campo
-- - Chaves primárias e estrangeiras
-- - Constraints de integridade
-- - Suporte a JSON para configurações flexíveis
