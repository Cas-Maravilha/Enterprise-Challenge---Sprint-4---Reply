-- =====================================================
-- SCRIPT SQL - INSERÇÃO DE DADOS DE EXEMPLO
-- Sistema IoT Monitoring - Sprint 3
-- Arquivo: inserir_dados_exemplo.sql
-- Versão: 1.0
-- Data: 2025-01-11
-- Descrição: Script para inserir dados de exemplo no banco
-- =====================================================

USE `iot_monitoring_db`;

-- =====================================================
-- DADOS DE EXEMPLO - TIPOS DE SENSORES
-- =====================================================

INSERT INTO tipos_sensor (nome, descricao, unidade_medida, faixa_min, faixa_max, precisao) VALUES
('DHT22', 'Sensor de temperatura e umidade digital DHT22', '°C/%', -40.000, 80.000, 0.500),
('LDR', 'Sensor de luminosidade (Light Dependent Resistor)', 'lux', 0.000, 1023.000, 1.000),
('PIR', 'Sensor de movimento passivo infravermelho', 'boolean', 0.000, 1.000, 1.000),
('Pressão', 'Sensor de pressão barométrica BMP280', 'bar', 0.000, 10.000, 0.010),
('Vibração', 'Sensor de vibração triaxial MPU6050', 'g', -2.000, 2.000, 0.001),
('Nível', 'Sensor de nível ultrassônico HC-SR04', 'cm', 0.000, 200.000, 0.100),
('CO2', 'Sensor de dióxido de carbono MH-Z19', 'ppm', 0.000, 5000.000, 1.000),
('Ruído', 'Sensor de ruído analógico', 'dB', 30.000, 120.000, 1.000);

-- =====================================================
-- DADOS DE EXEMPLO - MODOS DE OPERAÇÃO
-- =====================================================

INSERT INTO modos_operacao (nome, descricao, cor_indicador) VALUES
('Normal', 'Sistema operando dentro dos parâmetros normais', '#28a745'),
('Alerta', 'Sistema com valores próximos aos limites', '#ffc107'),
('Falha', 'Sistema com falha ou valores críticos', '#dc3545'),
('Manutenção', 'Sistema em modo de manutenção programada', '#6c757d'),
('Emergência', 'Sistema em modo de emergência', '#dc3545');

-- =====================================================
-- DADOS DE EXEMPLO - USUÁRIOS
-- =====================================================

INSERT INTO usuarios (nome, email, senha_hash, perfil) VALUES
('Administrador Sistema', 'admin@iot.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/8Kz8KzK', 'admin'),
('Operador Principal', 'operador@iot.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/8Kz8KzK', 'operador'),
('Visualizador 1', 'visualizador1@iot.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/8Kz8KzK', 'visualizador'),
('Técnico Manutenção', 'tecnico@iot.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/8Kz8KzK', 'operador');

-- =====================================================
-- DADOS DE EXEMPLO - DISPOSITIVOS
-- =====================================================

INSERT INTO dispositivos (nome, mac_address, ip_address, localizacao, versao_firmware, observacoes) VALUES
('ESP32-Sala-01', 'AA:BB:CC:DD:EE:FF', '192.168.1.100', 'Sala de Controle Principal', 'v1.2.3', 'Dispositivo principal do sistema'),
('ESP32-Garagem-01', '11:22:33:44:55:66', '192.168.1.101', 'Garagem - Portão Principal', 'v1.2.3', 'Monitoramento da garagem'),
('ESP32-Cozinha-01', '22:33:44:55:66:77', '192.168.1.102', 'Cozinha - Monitoramento', 'v1.2.3', 'Sensores de cozinha'),
('ESP32-Quarto-01', '33:44:55:66:77:88', '192.168.1.103', 'Quarto Principal', 'v1.2.3', 'Monitoramento do quarto'),
('ESP32-Lavanderia-01', '44:55:66:77:88:99', '192.168.1.104', 'Lavanderia', 'v1.2.3', 'Sensores de umidade'),
('ESP32-Externo-01', '55:66:77:88:99:AA', '192.168.1.105', 'Área Externa', 'v1.2.3', 'Monitoramento externo');

-- =====================================================
-- DADOS DE EXEMPLO - SENSORES
-- =====================================================

-- Sensores para ESP32-Sala-01
INSERT INTO sensores (id_dispositivo, id_tipo_sensor, nome, pino_analogico, pino_digital, calibracao_min, calibracao_max, observacoes) VALUES
(1, 1, 'DHT22-Temperatura-Sala', NULL, 2, -40.0, 80.0, 'Sensor de temperatura da sala'),
(1, 1, 'DHT22-Umidade-Sala', NULL, 2, 0.0, 100.0, 'Sensor de umidade da sala'),
(1, 2, 'LDR-Luminosidade-Sala', 34, NULL, 0.0, 1023.0, 'Sensor de luminosidade da sala'),
(1, 3, 'PIR-Movimento-Sala', NULL, 4, 0.0, 1.0, 'Sensor de movimento da sala'),
(1, 4, 'Pressão-Barométrica-Sala', 36, NULL, 0.0, 10.0, 'Sensor de pressão barométrica'),
(1, 5, 'Vibração-X-Sala', 39, NULL, -2.0, 2.0, 'Sensor de vibração eixo X'),
(1, 5, 'Vibração-Y-Sala', 35, NULL, -2.0, 2.0, 'Sensor de vibração eixo Y'),
(1, 5, 'Vibração-Z-Sala', 32, NULL, -2.0, 2.0, 'Sensor de vibração eixo Z'),
(1, 6, 'Nível-Ultrassônico-Sala', 33, NULL, 0.0, 200.0, 'Sensor de nível ultrassônico'),
(1, 7, 'CO2-Sala', 25, NULL, 0.0, 5000.0, 'Sensor de CO2 da sala');

-- Sensores para ESP32-Garagem-01
INSERT INTO sensores (id_dispositivo, id_tipo_sensor, nome, pino_analogico, pino_digital, calibracao_min, calibracao_max, observacoes) VALUES
(2, 1, 'DHT22-Temperatura-Garagem', NULL, 2, -40.0, 80.0, 'Sensor de temperatura da garagem'),
(2, 1, 'DHT22-Umidade-Garagem', NULL, 2, 0.0, 100.0, 'Sensor de umidade da garagem'),
(2, 2, 'LDR-Luminosidade-Garagem', 34, NULL, 0.0, 1023.0, 'Sensor de luminosidade da garagem'),
(2, 3, 'PIR-Movimento-Garagem', NULL, 4, 0.0, 1.0, 'Sensor de movimento da garagem'),
(2, 4, 'Pressão-Barométrica-Garagem', 36, NULL, 0.0, 10.0, 'Sensor de pressão barométrica'),
(2, 5, 'Vibração-X-Garagem', 39, NULL, -2.0, 2.0, 'Sensor de vibração eixo X'),
(2, 5, 'Vibração-Y-Garagem', 35, NULL, -2.0, 2.0, 'Sensor de vibração eixo Y'),
(2, 5, 'Vibração-Z-Garagem', 32, NULL, -2.0, 2.0, 'Sensor de vibração eixo Z'),
(2, 6, 'Nível-Ultrassônico-Garagem', 33, NULL, 0.0, 200.0, 'Sensor de nível ultrassônico'),
(2, 8, 'Ruído-Garagem', 26, NULL, 30.0, 120.0, 'Sensor de ruído da garagem');

-- Sensores para ESP32-Cozinha-01
INSERT INTO sensores (id_dispositivo, id_tipo_sensor, nome, pino_analogico, pino_digital, calibracao_min, calibracao_max, observacoes) VALUES
(3, 1, 'DHT22-Temperatura-Cozinha', NULL, 2, -40.0, 80.0, 'Sensor de temperatura da cozinha'),
(3, 1, 'DHT22-Umidade-Cozinha', NULL, 2, 0.0, 100.0, 'Sensor de umidade da cozinha'),
(3, 2, 'LDR-Luminosidade-Cozinha', 34, NULL, 0.0, 1023.0, 'Sensor de luminosidade da cozinha'),
(3, 3, 'PIR-Movimento-Cozinha', NULL, 4, 0.0, 1.0, 'Sensor de movimento da cozinha'),
(3, 4, 'Pressão-Barométrica-Cozinha', 36, NULL, 0.0, 10.0, 'Sensor de pressão barométrica'),
(3, 5, 'Vibração-X-Cozinha', 39, NULL, -2.0, 2.0, 'Sensor de vibração eixo X'),
(3, 5, 'Vibração-Y-Cozinha', 35, NULL, -2.0, 2.0, 'Sensor de vibração eixo Y'),
(3, 5, 'Vibração-Z-Cozinha', 32, NULL, -2.0, 2.0, 'Sensor de vibração eixo Z'),
(3, 6, 'Nível-Ultrassônico-Cozinha', 33, NULL, 0.0, 200.0, 'Sensor de nível ultrassônico'),
(3, 7, 'CO2-Cozinha', 25, NULL, 0.0, 5000.0, 'Sensor de CO2 da cozinha'),
(3, 8, 'Ruído-Cozinha', 26, NULL, 30.0, 120.0, 'Sensor de ruído da cozinha');

-- Sensores para ESP32-Quarto-01
INSERT INTO sensores (id_dispositivo, id_tipo_sensor, nome, pino_analogico, pino_digital, calibracao_min, calibracao_max, observacoes) VALUES
(4, 1, 'DHT22-Temperatura-Quarto', NULL, 2, -40.0, 80.0, 'Sensor de temperatura do quarto'),
(4, 1, 'DHT22-Umidade-Quarto', NULL, 2, 0.0, 100.0, 'Sensor de umidade do quarto'),
(4, 2, 'LDR-Luminosidade-Quarto', 34, NULL, 0.0, 1023.0, 'Sensor de luminosidade do quarto'),
(4, 3, 'PIR-Movimento-Quarto', NULL, 4, 0.0, 1.0, 'Sensor de movimento do quarto'),
(4, 4, 'Pressão-Barométrica-Quarto', 36, NULL, 0.0, 10.0, 'Sensor de pressão barométrica'),
(4, 5, 'Vibração-X-Quarto', 39, NULL, -2.0, 2.0, 'Sensor de vibração eixo X'),
(4, 5, 'Vibração-Y-Quarto', 35, NULL, -2.0, 2.0, 'Sensor de vibração eixo Y'),
(4, 5, 'Vibração-Z-Quarto', 32, NULL, -2.0, 2.0, 'Sensor de vibração eixo Z'),
(4, 6, 'Nível-Ultrassônico-Quarto', 33, NULL, 0.0, 200.0, 'Sensor de nível ultrassônico'),
(4, 7, 'CO2-Quarto', 25, NULL, 0.0, 5000.0, 'Sensor de CO2 do quarto');

-- Sensores para ESP32-Lavanderia-01
INSERT INTO sensores (id_dispositivo, id_tipo_sensor, nome, pino_analogico, pino_digital, calibracao_min, calibracao_max, observacoes) VALUES
(5, 1, 'DHT22-Temperatura-Lavanderia', NULL, 2, -40.0, 80.0, 'Sensor de temperatura da lavanderia'),
(5, 1, 'DHT22-Umidade-Lavanderia', NULL, 2, 0.0, 100.0, 'Sensor de umidade da lavanderia'),
(5, 2, 'LDR-Luminosidade-Lavanderia', 34, NULL, 0.0, 1023.0, 'Sensor de luminosidade da lavanderia'),
(5, 3, 'PIR-Movimento-Lavanderia', NULL, 4, 0.0, 1.0, 'Sensor de movimento da lavanderia'),
(5, 4, 'Pressão-Barométrica-Lavanderia', 36, NULL, 0.0, 10.0, 'Sensor de pressão barométrica'),
(5, 5, 'Vibração-X-Lavanderia', 39, NULL, -2.0, 2.0, 'Sensor de vibração eixo X'),
(5, 5, 'Vibração-Y-Lavanderia', 35, NULL, -2.0, 2.0, 'Sensor de vibração eixo Y'),
(5, 5, 'Vibração-Z-Lavanderia', 32, NULL, -2.0, 2.0, 'Sensor de vibração eixo Z'),
(5, 6, 'Nível-Ultrassônico-Lavanderia', 33, NULL, 0.0, 200.0, 'Sensor de nível ultrassônico'),
(5, 8, 'Ruído-Lavanderia', 26, NULL, 30.0, 120.0, 'Sensor de ruído da lavanderia');

-- Sensores para ESP32-Externo-01
INSERT INTO sensores (id_dispositivo, id_tipo_sensor, nome, pino_analogico, pino_digital, calibracao_min, calibracao_max, observacoes) VALUES
(6, 1, 'DHT22-Temperatura-Externo', NULL, 2, -40.0, 80.0, 'Sensor de temperatura externa'),
(6, 1, 'DHT22-Umidade-Externo', NULL, 2, 0.0, 100.0, 'Sensor de umidade externa'),
(6, 2, 'LDR-Luminosidade-Externo', 34, NULL, 0.0, 1023.0, 'Sensor de luminosidade externa'),
(6, 3, 'PIR-Movimento-Externo', NULL, 4, 0.0, 1.0, 'Sensor de movimento externo'),
(6, 4, 'Pressão-Barométrica-Externo', 36, NULL, 0.0, 10.0, 'Sensor de pressão barométrica'),
(6, 5, 'Vibração-X-Externo', 39, NULL, -2.0, 2.0, 'Sensor de vibração eixo X'),
(6, 5, 'Vibração-Y-Externo', 35, NULL, -2.0, 2.0, 'Sensor de vibração eixo Y'),
(6, 5, 'Vibração-Z-Externo', 32, NULL, -2.0, 2.0, 'Sensor de vibração eixo Z'),
(6, 6, 'Nível-Ultrassônico-Externo', 33, NULL, 0.0, 200.0, 'Sensor de nível ultrassônico'),
(6, 8, 'Ruído-Externo', 26, NULL, 30.0, 120.0, 'Sensor de ruído externo');

-- =====================================================
-- DADOS DE EXEMPLO - CONFIGURAÇÕES DE LIMITES
-- =====================================================

-- Configurações para sensores de temperatura
INSERT INTO configuracoes_limites (id_sensor, tipo_limite, valor_limite, severidade, usuario_criacao, observacoes) VALUES
(1, 'minimo', 15.0, 'baixa', 'admin@iot.com', 'Temperatura mínima aceitável'),
(1, 'maximo', 30.0, 'baixa', 'admin@iot.com', 'Temperatura máxima aceitável'),
(1, 'minimo', 10.0, 'media', 'admin@iot.com', 'Temperatura crítica baixa'),
(1, 'maximo', 35.0, 'media', 'admin@iot.com', 'Temperatura crítica alta'),
(1, 'minimo', 5.0, 'alta', 'admin@iot.com', 'Temperatura de emergência baixa'),
(1, 'maximo', 40.0, 'alta', 'admin@iot.com', 'Temperatura de emergência alta');

-- Configurações para sensores de umidade
INSERT INTO configuracoes_limites (id_sensor, tipo_limite, valor_limite, severidade, usuario_criacao, observacoes) VALUES
(2, 'minimo', 30.0, 'baixa', 'admin@iot.com', 'Umidade mínima aceitável'),
(2, 'maximo', 70.0, 'baixa', 'admin@iot.com', 'Umidade máxima aceitável'),
(2, 'minimo', 20.0, 'media', 'admin@iot.com', 'Umidade crítica baixa'),
(2, 'maximo', 80.0, 'media', 'admin@iot.com', 'Umidade crítica alta'),
(2, 'minimo', 10.0, 'alta', 'admin@iot.com', 'Umidade de emergência baixa'),
(2, 'maximo', 90.0, 'alta', 'admin@iot.com', 'Umidade de emergência alta');

-- Configurações para sensores de luminosidade
INSERT INTO configuracoes_limites (id_sensor, tipo_limite, valor_limite, severidade, usuario_criacao, observacoes) VALUES
(3, 'minimo', 50.0, 'baixa', 'admin@iot.com', 'Luminosidade mínima aceitável'),
(3, 'maximo', 800.0, 'baixa', 'admin@iot.com', 'Luminosidade máxima aceitável'),
(3, 'minimo', 20.0, 'media', 'admin@iot.com', 'Luminosidade crítica baixa'),
(3, 'maximo', 1000.0, 'media', 'admin@iot.com', 'Luminosidade crítica alta');

-- Configurações para sensores de pressão
INSERT INTO configuracoes_limites (id_sensor, tipo_limite, valor_limite, severidade, usuario_criacao, observacoes) VALUES
(5, 'minimo', 0.5, 'baixa', 'admin@iot.com', 'Pressão mínima aceitável'),
(5, 'maximo', 8.0, 'baixa', 'admin@iot.com', 'Pressão máxima aceitável'),
(5, 'minimo', 0.3, 'media', 'admin@iot.com', 'Pressão crítica baixa'),
(5, 'maximo', 9.5, 'media', 'admin@iot.com', 'Pressão crítica alta');

-- Configurações para sensores de vibração
INSERT INTO configuracoes_limites (id_sensor, tipo_limite, valor_limite, severidade, usuario_criacao, observacoes) VALUES
(6, 'maximo', 0.5, 'baixa', 'admin@iot.com', 'Vibração máxima aceitável'),
(6, 'maximo', 1.0, 'media', 'admin@iot.com', 'Vibração crítica'),
(6, 'maximo', 1.5, 'alta', 'admin@iot.com', 'Vibração de emergência');

-- Configurações para sensores de CO2
INSERT INTO configuracoes_limites (id_sensor, tipo_limite, valor_limite, severidade, usuario_criacao, observacoes) VALUES
(10, 'maximo', 1000.0, 'baixa', 'admin@iot.com', 'CO2 máximo aceitável'),
(10, 'maximo', 2000.0, 'media', 'admin@iot.com', 'CO2 crítico'),
(10, 'maximo', 5000.0, 'alta', 'admin@iot.com', 'CO2 de emergência');

-- =====================================================
-- DADOS DE EXEMPLO - DASHBOARDS
-- =====================================================

INSERT INTO dashboards (id_usuario, nome, descricao, configuracoes, publico, observacoes) VALUES
(1, 'Dashboard Principal', 'Dashboard principal do sistema', '{"widgets": ["temperatura", "umidade", "luminosidade", "movimento"], "refresh": 30}', 1, 'Dashboard público principal'),
(1, 'Dashboard Técnico', 'Dashboard para técnicos', '{"widgets": ["vibracao", "pressao", "co2", "ruido"], "refresh": 10}', 0, 'Dashboard técnico privado'),
(2, 'Dashboard Operacional', 'Dashboard para operadores', '{"widgets": ["alertas", "status_dispositivos", "leituras_recentes"], "refresh": 15}', 0, 'Dashboard operacional'),
(3, 'Dashboard Visualização', 'Dashboard para visualizadores', '{"widgets": ["graficos_tendencia", "resumo_geral"], "refresh": 60}', 0, 'Dashboard de visualização');

-- =====================================================
-- DADOS DE EXEMPLO - RELATÓRIOS
-- =====================================================

INSERT INTO relatorios (id_usuario, nome, tipo_relatorio, configuracoes, frequencia, proxima_execucao) VALUES
(1, 'Relatório Diário', 'diario', '{"tabelas": ["leituras_sensores", "alertas"], "periodo": "24h"}', '0 8 * * *', '2025-01-12 08:00:00'),
(1, 'Relatório Semanal', 'semanal', '{"tabelas": ["leituras_sensores", "alertas", "dispositivos"], "periodo": "7d"}', '0 9 * * 1', '2025-01-13 09:00:00'),
(1, 'Relatório Mensal', 'mensal', '{"tabelas": ["leituras_sensores", "alertas", "dispositivos", "usuarios"], "periodo": "30d"}', '0 10 1 * *', '2025-02-01 10:00:00'),
(2, 'Relatório Operacional', 'diario', '{"tabelas": ["alertas", "leituras_sensores"], "periodo": "24h", "filtros": {"status": "ativo"}}', '0 7 * * *', '2025-01-12 07:00:00');

-- =====================================================
-- DADOS DE EXEMPLO - LOGS DO SISTEMA
-- =====================================================

INSERT INTO logs_sistema (id_usuario, acao, tabela_afetada, id_registro_afetado, dados_anteriores, dados_novos, ip_origem, user_agent) VALUES
(1, 'INSERT', 'dispositivos', 1, NULL, '{"nome": "ESP32-Sala-01", "mac_address": "AA:BB:CC:DD:EE:FF"}', '192.168.1.100', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'),
(1, 'INSERT', 'sensores', 1, NULL, '{"nome": "DHT22-Temperatura-Sala", "id_dispositivo": 1}', '192.168.1.100', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'),
(1, 'INSERT', 'configuracoes_limites', 1, NULL, '{"id_sensor": 1, "tipo_limite": "minimo", "valor_limite": 15.0}', '192.168.1.100', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'),
(2, 'UPDATE', 'dispositivos', 1, '{"status": "ativo"}', '{"status": "manutencao"}', '192.168.1.101', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'),
(2, 'INSERT', 'alertas', 1, NULL, '{"id_dispositivo": 1, "tipo_alerta": "temperatura", "severidade": "media"}', '192.168.1.101', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36');

-- =====================================================
-- DADOS DE EXEMPLO - LEITURAS DE SENSORES (ÚLTIMAS 24H)
-- =====================================================

-- Gerar leituras de exemplo para os últimos 24 horas
-- (Este é um exemplo simplificado - em produção, os dados viriam dos sensores reais)

INSERT INTO leituras_sensores (id_sensor, timestamp_unix, timestamp_datetime, valor_numerico, valor_booleano, valor_string, qualidade_dados, anomalia_detectada) VALUES
-- Leituras do sensor de temperatura (ID 1)
(1, 1705056000.000, '2025-01-11 10:00:00', 22.5, NULL, NULL, 'bom', 0),
(1, 1705056060.000, '2025-01-11 10:01:00', 22.7, NULL, NULL, 'bom', 0),
(1, 1705056120.000, '2025-01-11 10:02:00', 22.3, NULL, NULL, 'bom', 0),
(1, 1705056180.000, '2025-01-11 10:03:00', 22.8, NULL, NULL, 'bom', 0),
(1, 1705056240.000, '2025-01-11 10:04:00', 23.1, NULL, NULL, 'bom', 0),

-- Leituras do sensor de umidade (ID 2)
(2, 1705056000.000, '2025-01-11 10:00:00', 45.2, NULL, NULL, 'bom', 0),
(2, 1705056060.000, '2025-01-11 10:01:00', 45.8, NULL, NULL, 'bom', 0),
(2, 1705056120.000, '2025-01-11 10:02:00', 46.1, NULL, NULL, 'bom', 0),
(2, 1705056180.000, '2025-01-11 10:03:00', 45.9, NULL, NULL, 'bom', 0),
(2, 1705056240.000, '2025-01-11 10:04:00', 46.3, NULL, NULL, 'bom', 0),

-- Leituras do sensor de luminosidade (ID 3)
(3, 1705056000.000, '2025-01-11 10:00:00', 350.0, NULL, NULL, 'bom', 0),
(3, 1705056060.000, '2025-01-11 10:01:00', 355.0, NULL, NULL, 'bom', 0),
(3, 1705056120.000, '2025-01-11 10:02:00', 360.0, NULL, NULL, 'bom', 0),
(3, 1705056180.000, '2025-01-11 10:03:00', 365.0, NULL, NULL, 'bom', 0),
(3, 1705056240.000, '2025-01-11 10:04:00', 370.0, NULL, NULL, 'bom', 0),

-- Leituras do sensor de movimento (ID 4)
(4, 1705056000.000, '2025-01-11 10:00:00', NULL, 0, NULL, 'bom', 0),
(4, 1705056060.000, '2025-01-11 10:01:00', NULL, 0, NULL, 'bom', 0),
(4, 1705056120.000, '2025-01-11 10:02:00', NULL, 1, NULL, 'bom', 0),
(4, 1705056180.000, '2025-01-11 10:03:00', NULL, 0, NULL, 'bom', 0),
(4, 1705056240.000, '2025-01-11 10:04:00', NULL, 0, NULL, 'bom', 0),

-- Leituras do sensor de pressão (ID 5)
(5, 1705056000.000, '2025-01-11 10:00:00', 1.013, NULL, NULL, 'bom', 0),
(5, 1705056060.000, '2025-01-11 10:01:00', 1.014, NULL, NULL, 'bom', 0),
(5, 1705056120.000, '2025-01-11 10:02:00', 1.013, NULL, NULL, 'bom', 0),
(5, 1705056180.000, '2025-01-11 10:03:00', 1.015, NULL, NULL, 'bom', 0),
(5, 1705056240.000, '2025-01-11 10:04:00', 1.014, NULL, NULL, 'bom', 0);

-- =====================================================
-- DADOS DE EXEMPLO - ALERTAS
-- =====================================================

INSERT INTO alertas (id_dispositivo, id_sensor, id_modo, tipo_alerta, severidade, titulo, descricao, valor_atual, valor_limite, status) VALUES
(1, 1, 2, 'temperatura', 'media', 'Temperatura elevada na sala', 'Temperatura acima do limite configurado', 32.5, 30.0, 'ativo'),
(2, 11, 2, 'umidade', 'baixa', 'Umidade baixa na garagem', 'Umidade abaixo do limite mínimo', 25.0, 30.0, 'ativo'),
(3, 21, 3, 'pressao', 'alta', 'Pressão crítica na cozinha', 'Pressão acima do limite crítico', 9.8, 9.5, 'ativo'),
(4, 31, 2, 'co2', 'media', 'CO2 elevado no quarto', 'Concentração de CO2 acima do normal', 1500.0, 1000.0, 'resolvido'),
(5, 41, 2, 'ruido', 'baixa', 'Ruído excessivo na lavanderia', 'Nível de ruído acima do aceitável', 85.0, 80.0, 'ativo');

-- =====================================================
-- COMENTÁRIOS FINAIS
-- =====================================================

-- Este script insere dados de exemplo no banco de dados
-- Inclui:
-- - 8 tipos de sensores diferentes
-- - 5 modos de operação
-- - 4 usuários com diferentes perfis
-- - 6 dispositivos ESP32
-- - 50 sensores distribuídos pelos dispositivos
-- - Configurações de limites para alertas
-- - 4 dashboards personalizados
-- - 4 relatórios automáticos
-- - Logs de atividades do sistema
-- - Leituras de sensores de exemplo
-- - 5 alertas de exemplo
-- 
-- Os dados são realistas e representam um sistema IoT completo
-- em funcionamento com múltiplos sensores e dispositivos
