-- =====================================================
-- CONFIGURAÇÃO PARA PHPMYADMIN
-- Sistema IoT Monitoring - Sprint 3
-- =====================================================

-- Configurações do banco de dados
SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- Criar banco de dados
CREATE DATABASE IF NOT EXISTS `iot_monitoring_db` 
DEFAULT CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

USE `iot_monitoring_db`;

-- =====================================================
-- CONFIGURAÇÕES ESPECÍFICAS DO PHPMYADMIN
-- =====================================================

-- Configurar charset padrão
ALTER DATABASE `iot_monitoring_db` 
DEFAULT CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

-- =====================================================
-- TABELAS PRINCIPAIS
-- =====================================================

-- Tabela dispositivos
CREATE TABLE `dispositivos` (
  `id_dispositivo` int(11) NOT NULL AUTO_INCREMENT,
  `nome` varchar(100) NOT NULL,
  `mac_address` varchar(17) NOT NULL,
  `ip_address` varchar(15) DEFAULT NULL,
  `localizacao` varchar(200) DEFAULT NULL,
  `status` enum('ativo','inativo','manutencao') NOT NULL DEFAULT 'ativo',
  `data_cadastro` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `ultima_conexao` timestamp NULL DEFAULT NULL,
  `versao_firmware` varchar(20) DEFAULT NULL,
  `observacoes` text,
  PRIMARY KEY (`id_dispositivo`),
  UNIQUE KEY `uk_dispositivos_mac_address` (`mac_address`),
  KEY `idx_dispositivos_status` (`status`),
  KEY `idx_dispositivos_localizacao` (`localizacao`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabela tipos_sensor
CREATE TABLE `tipos_sensor` (
  `id_tipo_sensor` int(11) NOT NULL AUTO_INCREMENT,
  `nome` varchar(50) NOT NULL,
  `descricao` text,
  `unidade_medida` varchar(20) DEFAULT NULL,
  `faixa_min` decimal(10,3) DEFAULT NULL,
  `faixa_max` decimal(10,3) DEFAULT NULL,
  `precisao` decimal(8,3) DEFAULT NULL,
  `ativo` tinyint(1) NOT NULL DEFAULT 1,
  `data_cadastro` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_tipo_sensor`),
  UNIQUE KEY `uk_tipos_sensor_nome` (`nome`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabela sensores
CREATE TABLE `sensores` (
  `id_sensor` int(11) NOT NULL AUTO_INCREMENT,
  `id_dispositivo` int(11) NOT NULL,
  `id_tipo_sensor` int(11) NOT NULL,
  `nome` varchar(100) NOT NULL,
  `pino_analogico` int(11) DEFAULT NULL,
  `pino_digital` int(11) DEFAULT NULL,
  `calibracao_min` decimal(10,3) DEFAULT NULL,
  `calibracao_max` decimal(10,3) DEFAULT NULL,
  `status` enum('ativo','inativo','falha') NOT NULL DEFAULT 'ativo',
  `data_instalacao` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `ultima_calibracao` timestamp NULL DEFAULT NULL,
  `observacoes` text,
  PRIMARY KEY (`id_sensor`),
  KEY `fk_sensores_dispositivos` (`id_dispositivo`),
  KEY `fk_sensores_tipos_sensor` (`id_tipo_sensor`),
  KEY `idx_sensores_status` (`status`),
  CONSTRAINT `fk_sensores_dispositivos` FOREIGN KEY (`id_dispositivo`) REFERENCES `dispositivos` (`id_dispositivo`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_sensores_tipos_sensor` FOREIGN KEY (`id_tipo_sensor`) REFERENCES `tipos_sensor` (`id_tipo_sensor`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabela leituras_sensores (sem particionamento para compatibilidade)
CREATE TABLE `leituras_sensores` (
  `id_leitura` bigint(20) NOT NULL AUTO_INCREMENT,
  `id_sensor` int(11) NOT NULL,
  `timestamp_unix` decimal(15,3) NOT NULL,
  `timestamp_datetime` timestamp NOT NULL,
  `valor_numerico` decimal(12,6) DEFAULT NULL,
  `valor_booleano` tinyint(1) DEFAULT NULL,
  `valor_string` varchar(255) DEFAULT NULL,
  `qualidade_dados` enum('excelente','bom','regular','ruim') NOT NULL DEFAULT 'bom',
  `anomalia_detectada` tinyint(1) NOT NULL DEFAULT 0,
  `data_coleta` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_leitura`),
  KEY `fk_leituras_sensores` (`id_sensor`),
  KEY `idx_leituras_timestamp` (`timestamp_datetime`),
  KEY `idx_leituras_qualidade` (`qualidade_dados`),
  KEY `idx_leituras_anomalia` (`anomalia_detectada`),
  KEY `idx_leituras_sensor_timestamp` (`id_sensor`,`timestamp_datetime`),
  CONSTRAINT `fk_leituras_sensores` FOREIGN KEY (`id_sensor`) REFERENCES `sensores` (`id_sensor`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabela modos_operacao
CREATE TABLE `modos_operacao` (
  `id_modo` int(11) NOT NULL AUTO_INCREMENT,
  `nome` varchar(50) NOT NULL,
  `descricao` text,
  `cor_indicador` varchar(7) DEFAULT NULL,
  `ativo` tinyint(1) NOT NULL DEFAULT 1,
  `data_cadastro` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_modo`),
  UNIQUE KEY `uk_modos_operacao_nome` (`nome`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabela alertas
CREATE TABLE `alertas` (
  `id_alerta` bigint(20) NOT NULL AUTO_INCREMENT,
  `id_dispositivo` int(11) NOT NULL,
  `id_sensor` int(11) DEFAULT NULL,
  `id_modo` int(11) NOT NULL,
  `tipo_alerta` enum('temperatura','umidade','pressao','vibracao','nivel','conexao','geral') NOT NULL,
  `severidade` enum('baixa','media','alta','critica') NOT NULL,
  `titulo` varchar(200) NOT NULL,
  `descricao` text,
  `valor_atual` decimal(12,6) DEFAULT NULL,
  `valor_limite` decimal(12,6) DEFAULT NULL,
  `timestamp_alerta` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `status` enum('ativo','resolvido','ignorado') NOT NULL DEFAULT 'ativo',
  `data_resolucao` timestamp NULL DEFAULT NULL,
  `usuario_resolucao` varchar(100) DEFAULT NULL,
  `observacoes_resolucao` text,
  PRIMARY KEY (`id_alerta`),
  KEY `fk_alertas_dispositivos` (`id_dispositivo`),
  KEY `fk_alertas_sensores` (`id_sensor`),
  KEY `fk_alertas_modos_operacao` (`id_modo`),
  KEY `idx_alertas_timestamp` (`timestamp_alerta`),
  KEY `idx_alertas_status` (`status`),
  KEY `idx_alertas_severidade` (`severidade`),
  CONSTRAINT `fk_alertas_dispositivos` FOREIGN KEY (`id_dispositivo`) REFERENCES `dispositivos` (`id_dispositivo`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_alertas_modos_operacao` FOREIGN KEY (`id_modo`) REFERENCES `modos_operacao` (`id_modo`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_alertas_sensores` FOREIGN KEY (`id_sensor`) REFERENCES `sensores` (`id_sensor`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabela configuracoes_limites
CREATE TABLE `configuracoes_limites` (
  `id_configuracao` int(11) NOT NULL AUTO_INCREMENT,
  `id_sensor` int(11) NOT NULL,
  `tipo_limite` enum('minimo','maximo','variacao') NOT NULL,
  `valor_limite` decimal(12,6) NOT NULL,
  `severidade` enum('baixa','media','alta','critica') NOT NULL,
  `ativo` tinyint(1) NOT NULL DEFAULT 1,
  `data_criacao` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `data_atualizacao` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `usuario_criacao` varchar(100) DEFAULT NULL,
  `observacoes` text,
  PRIMARY KEY (`id_configuracao`),
  KEY `fk_configuracoes_limites_sensores` (`id_sensor`),
  KEY `idx_configuracoes_tipo_limite` (`tipo_limite`),
  KEY `idx_configuracoes_ativo` (`ativo`),
  CONSTRAINT `fk_configuracoes_limites_sensores` FOREIGN KEY (`id_sensor`) REFERENCES `sensores` (`id_sensor`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabela usuarios
CREATE TABLE `usuarios` (
  `id_usuario` int(11) NOT NULL AUTO_INCREMENT,
  `nome` varchar(100) NOT NULL,
  `email` varchar(255) NOT NULL,
  `senha_hash` varchar(255) NOT NULL,
  `perfil` enum('admin','operador','visualizador') NOT NULL,
  `ativo` tinyint(1) NOT NULL DEFAULT 1,
  `data_cadastro` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `ultimo_login` timestamp NULL DEFAULT NULL,
  `token_reset_senha` varchar(255) DEFAULT NULL,
  `data_expiracao_token` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id_usuario`),
  UNIQUE KEY `uk_usuarios_email` (`email`),
  KEY `idx_usuarios_perfil` (`perfil`),
  KEY `idx_usuarios_ativo` (`ativo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabela logs_sistema
CREATE TABLE `logs_sistema` (
  `id_log` bigint(20) NOT NULL AUTO_INCREMENT,
  `id_usuario` int(11) DEFAULT NULL,
  `acao` varchar(100) NOT NULL,
  `tabela_afetada` varchar(50) DEFAULT NULL,
  `id_registro_afetado` bigint(20) DEFAULT NULL,
  `dados_anteriores` json DEFAULT NULL,
  `dados_novos` json DEFAULT NULL,
  `ip_origem` varchar(45) DEFAULT NULL,
  `user_agent` text,
  `timestamp_log` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_log`),
  KEY `fk_logs_sistema_usuarios` (`id_usuario`),
  KEY `idx_logs_acao` (`acao`),
  KEY `idx_logs_timestamp` (`timestamp_log`),
  KEY `idx_logs_tabela` (`tabela_afetada`),
  CONSTRAINT `fk_logs_sistema_usuarios` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabela dashboards
CREATE TABLE `dashboards` (
  `id_dashboard` int(11) NOT NULL AUTO_INCREMENT,
  `id_usuario` int(11) NOT NULL,
  `nome` varchar(100) NOT NULL,
  `descricao` text,
  `configuracoes` json DEFAULT NULL,
  `publico` tinyint(1) NOT NULL DEFAULT 0,
  `ativo` tinyint(1) NOT NULL DEFAULT 1,
  `data_criacao` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `data_atualizacao` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_dashboard`),
  KEY `fk_dashboards_usuarios` (`id_usuario`),
  KEY `idx_dashboards_publico` (`publico`),
  KEY `idx_dashboards_ativo` (`ativo`),
  CONSTRAINT `fk_dashboards_usuarios` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabela relatorios
CREATE TABLE `relatorios` (
  `id_relatorio` int(11) NOT NULL AUTO_INCREMENT,
  `id_usuario` int(11) NOT NULL,
  `nome` varchar(100) NOT NULL,
  `tipo_relatorio` enum('diario','semanal','mensal','personalizado') NOT NULL,
  `configuracoes` json DEFAULT NULL,
  `frequencia` varchar(50) DEFAULT NULL,
  `ativo` tinyint(1) NOT NULL DEFAULT 1,
  `proxima_execucao` timestamp NULL DEFAULT NULL,
  `data_criacao` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_relatorio`),
  KEY `fk_relatorios_usuarios` (`id_usuario`),
  KEY `idx_relatorios_tipo` (`tipo_relatorio`),
  KEY `idx_relatorios_proxima_execucao` (`proxima_execucao`),
  CONSTRAINT `fk_relatorios_usuarios` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- VIEWS PARA PHPMYADMIN
-- =====================================================

-- View para leituras completas
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
-- DADOS INICIAIS
-- =====================================================

-- Inserir tipos de sensores
INSERT INTO `tipos_sensor` (`nome`, `descricao`, `unidade_medida`, `faixa_min`, `faixa_max`, `precisao`) VALUES
('DHT22', 'Sensor de temperatura e umidade digital', '°C/%', -40.000, 80.000, 0.500),
('LDR', 'Sensor de luminosidade (Light Dependent Resistor)', 'lux', 0.000, 1023.000, 1.000),
('PIR', 'Sensor de movimento passivo infravermelho', 'boolean', 0.000, 1.000, 1.000),
('Pressão', 'Sensor de pressão barométrica', 'bar', 0.000, 10.000, 0.010),
('Vibração', 'Sensor de vibração triaxial', 'g', -2.000, 2.000, 0.001),
('Nível', 'Sensor de nível ultrassônico', 'cm', 0.000, 200.000, 0.100);

-- Inserir modos de operação
INSERT INTO `modos_operacao` (`nome`, `descricao`, `cor_indicador`) VALUES
('Normal', 'Sistema operando dentro dos parâmetros normais', '#28a745'),
('Alerta', 'Sistema com valores próximos aos limites', '#ffc107'),
('Falha', 'Sistema com falha ou valores críticos', '#dc3545');

-- Inserir usuário administrador padrão
INSERT INTO `usuarios` (`nome`, `email`, `senha_hash`, `perfil`) VALUES
('Administrador', 'admin@iot.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/8Kz8KzK', 'admin');

-- Inserir dispositivos de exemplo
INSERT INTO `dispositivos` (`nome`, `mac_address`, `ip_address`, `localizacao`, `versao_firmware`) VALUES
('ESP32-Sala-01', 'AA:BB:CC:DD:EE:FF', '192.168.1.100', 'Sala de Controle Principal', 'v1.2.3'),
('ESP32-Garagem-01', '11:22:33:44:55:66', '192.168.1.101', 'Garagem - Portão Principal', 'v1.2.3'),
('ESP32-Cozinha-01', '22:33:44:55:66:77', '192.168.1.102', 'Cozinha - Monitoramento', 'v1.2.3');

-- Inserir sensores para os dispositivos
INSERT INTO `sensores` (`id_dispositivo`, `id_tipo_sensor`, `nome`, `pino_analogico`, `pino_digital`) VALUES
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
-- CONFIGURAÇÕES FINAIS
-- =====================================================

-- Restaurar configurações
SET FOREIGN_KEY_CHECKS = 1;

-- =====================================================
-- COMENTÁRIOS PARA PHPMYADMIN
-- =====================================================

-- Este arquivo contém o schema completo do banco de dados IoT
-- Otimizado para uso com phpMyAdmin
-- Inclui todas as tabelas, relacionamentos, índices e dados iniciais
-- Compatível com MySQL 5.7+ e MariaDB 10.2+
