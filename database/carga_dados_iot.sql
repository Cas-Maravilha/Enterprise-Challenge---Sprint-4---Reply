-- =====================================================
-- SCRIPT SQL - CARGA DE DADOS
-- Sistema IoT Monitoring - Sprint 3
-- Arquivo: carga_dados_iot.sql
-- Versão: 1.0
-- Data: 2025-01-11
-- Descrição: Script para carga de dados de exemplo e teste
-- =====================================================

USE `iot_monitoring_db`;

-- =====================================================
-- CARGA DE DADOS DE EXEMPLO
-- =====================================================

-- Inserir mais tipos de sensores
INSERT INTO tipos_sensor (nome, descricao, unidade_medida, faixa_min, faixa_max, precisao) VALUES
('BME280', 'Sensor de pressão, temperatura e umidade', 'hPa/°C/%', 300.000, 1100.000, 0.100),
('MPU6050', 'Acelerômetro e giroscópio', 'g/°/s', -16.000, 16.000, 0.001),
('HC-SR04', 'Sensor ultrassônico de distância', 'cm', 2.000, 400.000, 0.300),
('MQ-2', 'Sensor de gás inflamável', 'ppm', 0.000, 10000.000, 1.000),
('TMP36', 'Sensor de temperatura analógico', '°C', -40.000, 125.000, 0.500);

-- Inserir mais modos de operação
INSERT INTO modos_operacao (nome, descricao, cor_indicador) VALUES
('Manutenção', 'Sistema em modo de manutenção', '#6c757d'),
('Calibração', 'Sistema em processo de calibração', '#17a2b8'),
('Emergência', 'Sistema em modo de emergência', '#fd7e14');

-- Inserir mais usuários
INSERT INTO usuarios (nome, email, senha_hash, perfil) VALUES
('Operador Principal', 'operador@iot.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/8Kz8KzK', 'operador'),
('Visualizador', 'visualizador@iot.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/8Kz8KzK', 'visualizador'),
('Técnico Manutenção', 'tecnico@iot.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/8Kz8KzK', 'operador');

-- Inserir mais dispositivos
INSERT INTO dispositivos (nome, mac_address, ip_address, localizacao, versao_firmware, observacoes) VALUES
('ESP32-Quarto-01', '33:44:55:66:77:88', '192.168.1.103', 'Quarto Principal - Monitoramento', 'v1.2.3', 'Dispositivo principal do quarto'),
('ESP32-Lavanderia-01', '44:55:66:77:88:99', '192.168.1.104', 'Lavanderia - Controle de Umidade', 'v1.2.3', 'Monitoramento de umidade na lavanderia'),
('ESP32-Externo-01', '55:66:77:88:99:AA', '192.168.1.105', 'Área Externa - Portão', 'v1.2.3', 'Monitoramento externo com proteção IP65'),
('ESP32-Estufa-01', '66:77:88:99:AA:BB', '192.168.1.106', 'Estufa - Controle de Ambiente', 'v1.2.3', 'Controle de temperatura e umidade para plantas');

-- Inserir sensores para os novos dispositivos
INSERT INTO sensores (id_dispositivo, id_tipo_sensor, nome, pino_analogico, pino_digital, calibracao_min, calibracao_max) VALUES
-- Dispositivo 4 (Quarto)
(4, 1, 'DHT22-Temperatura-Quarto', NULL, 2, 15.000, 35.000),
(4, 1, 'DHT22-Umidade-Quarto', NULL, 2, 30.000, 80.000),
(4, 2, 'LDR-Luminosidade-Quarto', 34, NULL, 0.000, 1000.000),
(4, 3, 'PIR-Movimento-Quarto', NULL, 4, 0.000, 1.000),
(4, 4, 'Pressão-Barométrica-Quarto', 36, NULL, 950.000, 1050.000),
(4, 5, 'Vibração-X-Quarto', 39, NULL, -2.000, 2.000),
(4, 5, 'Vibração-Y-Quarto', 35, NULL, -2.000, 2.000),
(4, 5, 'Vibração-Z-Quarto', 32, NULL, -2.000, 2.000),
(4, 6, 'Nível-Ultrassônico-Quarto', 33, NULL, 0.000, 200.000),
-- Dispositivo 5 (Lavanderia)
(5, 1, 'DHT22-Temperatura-Lavanderia', NULL, 2, 15.000, 40.000),
(5, 1, 'DHT22-Umidade-Lavanderia', NULL, 2, 40.000, 90.000),
(5, 2, 'LDR-Luminosidade-Lavanderia', 34, NULL, 0.000, 1000.000),
(5, 3, 'PIR-Movimento-Lavanderia', NULL, 4, 0.000, 1.000),
(5, 4, 'Pressão-Barométrica-Lavanderia', 36, NULL, 950.000, 1050.000),
(5, 5, 'Vibração-X-Lavanderia', 39, NULL, -2.000, 2.000),
(5, 5, 'Vibração-Y-Lavanderia', 35, NULL, -2.000, 2.000),
(5, 5, 'Vibração-Z-Lavanderia', 32, NULL, -2.000, 2.000),
(5, 6, 'Nível-Ultrassônico-Lavanderia', 33, NULL, 0.000, 200.000),
-- Dispositivo 6 (Externo)
(6, 1, 'DHT22-Temperatura-Externo', NULL, 2, -10.000, 50.000),
(6, 1, 'DHT22-Umidade-Externo', NULL, 2, 20.000, 100.000),
(6, 2, 'LDR-Luminosidade-Externo', 34, NULL, 0.000, 10000.000),
(6, 3, 'PIR-Movimento-Externo', NULL, 4, 0.000, 1.000),
(6, 4, 'Pressão-Barométrica-Externo', 36, NULL, 950.000, 1050.000),
(6, 5, 'Vibração-X-Externo', 39, NULL, -2.000, 2.000),
(6, 5, 'Vibração-Y-Externo', 35, NULL, -2.000, 2.000),
(6, 5, 'Vibração-Z-Externo', 32, NULL, -2.000, 2.000),
(6, 6, 'Nível-Ultrassônico-Externo', 33, NULL, 0.000, 400.000),
-- Dispositivo 7 (Estufa)
(7, 1, 'DHT22-Temperatura-Estufa', NULL, 2, 10.000, 50.000),
(7, 1, 'DHT22-Umidade-Estufa', NULL, 2, 20.000, 95.000),
(7, 2, 'LDR-Luminosidade-Estufa', 34, NULL, 0.000, 1000.000),
(7, 3, 'PIR-Movimento-Estufa', NULL, 4, 0.000, 1.000),
(7, 4, 'Pressão-Barométrica-Estufa', 36, NULL, 950.000, 1050.000),
(7, 5, 'Vibração-X-Estufa', 39, NULL, -2.000, 2.000),
(7, 5, 'Vibração-Y-Estufa', 35, NULL, -2.000, 2.000),
(7, 5, 'Vibração-Z-Estufa', 32, NULL, -2.000, 2.000),
(7, 6, 'Nível-Ultrassônico-Estufa', 33, NULL, 0.000, 200.000);

-- =====================================================
-- CARGA DE DADOS DE LEITURAS (SIMULAÇÃO)
-- =====================================================

-- Função para gerar dados de leituras simuladas
DELIMITER //
CREATE PROCEDURE GerarLeiturasSimuladas(
    IN p_id_sensor INT,
    IN p_num_leituras INT,
    IN p_data_inicio TIMESTAMP
)
BEGIN
    DECLARE i INT DEFAULT 0;
    DECLARE v_timestamp TIMESTAMP;
    DECLARE v_valor_numerico DECIMAL(12,6);
    DECLARE v_valor_booleano TINYINT(1);
    DECLARE v_qualidade ENUM('excelente', 'bom', 'regular', 'ruim');
    DECLARE v_anomalia TINYINT(1);
    
    WHILE i < p_num_leituras DO
        SET v_timestamp = DATE_ADD(p_data_inicio, INTERVAL i MINUTE);
        
        -- Gerar valor numérico baseado no tipo de sensor
        SET v_valor_numerico = CASE 
            WHEN p_id_sensor IN (1, 2, 11, 12, 19, 20, 27, 28, 35, 36) THEN 
                ROUND(20 + RAND() * 15 + SIN(i * 0.1) * 3, 2) -- Temperatura
            WHEN p_id_sensor IN (3, 13, 21, 29, 37) THEN 
                ROUND(50 + RAND() * 30 + COS(i * 0.15) * 10, 2) -- Umidade
            WHEN p_id_sensor IN (4, 14, 22, 30, 38) THEN 
                ROUND(100 + RAND() * 800 + SIN(i * 0.2) * 200, 0) -- Luminosidade
            WHEN p_id_sensor IN (5, 15, 23, 31, 39) THEN 
                ROUND(RAND(), 0) -- Movimento (0 ou 1)
            WHEN p_id_sensor IN (6, 16, 24, 32, 40) THEN 
                ROUND(1000 + RAND() * 50 + COS(i * 0.05) * 10, 2) -- Pressão
            WHEN p_id_sensor IN (7, 8, 9, 17, 18, 19, 25, 26, 27, 33, 34, 35) THEN 
                ROUND(-2 + RAND() * 4, 3) -- Vibração
            WHEN p_id_sensor IN (10, 20, 30, 40) THEN 
                ROUND(50 + RAND() * 100 + SIN(i * 0.1) * 20, 1) -- Nível
            ELSE ROUND(RAND() * 100, 2)
        END;
        
        -- Gerar valor booleano para sensores PIR
        SET v_valor_booleano = CASE 
            WHEN p_id_sensor IN (5, 15, 23, 31, 39) THEN ROUND(RAND())
            ELSE NULL
        END;
        
        -- Gerar qualidade dos dados
        SET v_qualidade = CASE 
            WHEN RAND() < 0.7 THEN 'excelente'
            WHEN RAND() < 0.9 THEN 'bom'
            WHEN RAND() < 0.95 THEN 'regular'
            ELSE 'ruim'
        END;
        
        -- Gerar flag de anomalia (5% de chance)
        SET v_anomalia = CASE 
            WHEN RAND() < 0.05 THEN 1
            ELSE 0
        END;
        
        -- Inserir leitura
        INSERT INTO leituras_sensores (
            id_sensor, 
            timestamp_unix, 
            timestamp_datetime, 
            valor_numerico, 
            valor_booleano, 
            qualidade_dados, 
            anomalia_detectada
        ) VALUES (
            p_id_sensor,
            UNIX_TIMESTAMP(v_timestamp),
            v_timestamp,
            v_valor_numerico,
            v_valor_booleano,
            v_qualidade,
            v_anomalia
        );
        
        SET i = i + 1;
    END WHILE;
END //
DELIMITER ;

-- Gerar leituras para todos os sensores (últimas 24 horas)
CALL GerarLeiturasSimuladas(1, 1440, DATE_SUB(NOW(), INTERVAL 1 DAY));  -- 1 leitura por minuto
CALL GerarLeiturasSimuladas(2, 1440, DATE_SUB(NOW(), INTERVAL 1 DAY));
CALL GerarLeiturasSimuladas(3, 1440, DATE_SUB(NOW(), INTERVAL 1 DAY));
CALL GerarLeiturasSimuladas(4, 1440, DATE_SUB(NOW(), INTERVAL 1 DAY));
CALL GerarLeiturasSimuladas(5, 1440, DATE_SUB(NOW(), INTERVAL 1 DAY));
CALL GerarLeiturasSimuladas(6, 1440, DATE_SUB(NOW(), INTERVAL 1 DAY));
CALL GerarLeiturasSimuladas(7, 1440, DATE_SUB(NOW(), INTERVAL 1 DAY));
CALL GerarLeiturasSimuladas(8, 1440, DATE_SUB(NOW(), INTERVAL 1 DAY));
CALL GerarLeiturasSimuladas(9, 1440, DATE_SUB(NOW(), INTERVAL 1 DAY));
CALL GerarLeiturasSimuladas(10, 1440, DATE_SUB(NOW(), INTERVAL 1 DAY));

-- Gerar leituras para sensores dos dispositivos 2 e 3 (últimas 12 horas)
CALL GerarLeiturasSimuladas(11, 720, DATE_SUB(NOW(), INTERVAL 12 HOUR));
CALL GerarLeiturasSimuladas(12, 720, DATE_SUB(NOW(), INTERVAL 12 HOUR));
CALL GerarLeiturasSimuladas(13, 720, DATE_SUB(NOW(), INTERVAL 12 HOUR));
CALL GerarLeiturasSimuladas(14, 720, DATE_SUB(NOW(), INTERVAL 12 HOUR));
CALL GerarLeiturasSimuladas(15, 720, DATE_SUB(NOW(), INTERVAL 12 HOUR));
CALL GerarLeiturasSimuladas(16, 720, DATE_SUB(NOW(), INTERVAL 12 HOUR));
CALL GerarLeiturasSimuladas(17, 720, DATE_SUB(NOW(), INTERVAL 12 HOUR));
CALL GerarLeiturasSimuladas(18, 720, DATE_SUB(NOW(), INTERVAL 12 HOUR));
CALL GerarLeiturasSimuladas(19, 720, DATE_SUB(NOW(), INTERVAL 12 HOUR));
CALL GerarLeiturasSimuladas(20, 720, DATE_SUB(NOW(), INTERVAL 12 HOUR));

-- Gerar leituras para sensores dos dispositivos 4, 5, 6, 7 (últimas 6 horas)
CALL GerarLeiturasSimuladas(21, 360, DATE_SUB(NOW(), INTERVAL 6 HOUR));
CALL GerarLeiturasSimuladas(22, 360, DATE_SUB(NOW(), INTERVAL 6 HOUR));
CALL GerarLeiturasSimuladas(23, 360, DATE_SUB(NOW(), INTERVAL 6 HOUR));
CALL GerarLeiturasSimuladas(24, 360, DATE_SUB(NOW(), INTERVAL 6 HOUR));
CALL GerarLeiturasSimuladas(25, 360, DATE_SUB(NOW(), INTERVAL 6 HOUR));
CALL GerarLeiturasSimuladas(26, 360, DATE_SUB(NOW(), INTERVAL 6 HOUR));
CALL GerarLeiturasSimuladas(27, 360, DATE_SUB(NOW(), INTERVAL 6 HOUR));
CALL GerarLeiturasSimuladas(28, 360, DATE_SUB(NOW(), INTERVAL 6 HOUR));
CALL GerarLeiturasSimuladas(29, 360, DATE_SUB(NOW(), INTERVAL 6 HOUR));
CALL GerarLeiturasSimuladas(30, 360, DATE_SUB(NOW(), INTERVAL 6 HOUR));

-- Remover procedure temporária
DROP PROCEDURE GerarLeiturasSimuladas;

-- =====================================================
-- CARGA DE CONFIGURAÇÕES DE LIMITES
-- =====================================================

-- Inserir configurações de limites para sensores de temperatura
INSERT INTO configuracoes_limites (id_sensor, tipo_limite, valor_limite, severidade, usuario_criacao) VALUES
(1, 'minimo', 15.000, 'baixa', 'admin@iot.com'),
(1, 'maximo', 30.000, 'media', 'admin@iot.com'),
(1, 'maximo', 35.000, 'alta', 'admin@iot.com'),
(2, 'minimo', 30.000, 'baixa', 'admin@iot.com'),
(2, 'maximo', 70.000, 'media', 'admin@iot.com'),
(2, 'maximo', 80.000, 'alta', 'admin@iot.com');

-- Inserir configurações de limites para sensores de luminosidade
INSERT INTO configuracoes_limites (id_sensor, tipo_limite, valor_limite, severidade, usuario_criacao) VALUES
(3, 'minimo', 50.000, 'baixa', 'admin@iot.com'),
(3, 'maximo', 800.000, 'media', 'admin@iot.com'),
(3, 'maximo', 1000.000, 'alta', 'admin@iot.com');

-- Inserir configurações de limites para sensores de pressão
INSERT INTO configuracoes_limites (id_sensor, tipo_limite, valor_limite, severidade, usuario_criacao) VALUES
(6, 'minimo', 950.000, 'baixa', 'admin@iot.com'),
(6, 'maximo', 1050.000, 'media', 'admin@iot.com'),
(6, 'minimo', 940.000, 'alta', 'admin@iot.com'),
(6, 'maximo', 1060.000, 'alta', 'admin@iot.com');

-- =====================================================
-- CARGA DE ALERTAS DE EXEMPLO
-- =====================================================

-- Inserir alertas baseados nas leituras com anomalias
INSERT INTO alertas (
    id_dispositivo, 
    id_sensor, 
    id_modo, 
    tipo_alerta, 
    severidade, 
    titulo, 
    descricao, 
    valor_atual, 
    valor_limite, 
    timestamp_alerta
)
SELECT 
    s.id_dispositivo,
    l.id_sensor,
    2 as id_modo, -- Modo Alerta
    CASE 
        WHEN s.id_tipo_sensor = 1 THEN 'temperatura'
        WHEN s.id_tipo_sensor = 2 THEN 'umidade'
        WHEN s.id_tipo_sensor = 3 THEN 'pressao'
        WHEN s.id_tipo_sensor = 4 THEN 'vibracao'
        ELSE 'geral'
    END as tipo_alerta,
    CASE 
        WHEN l.valor_numerico > 35 THEN 'critica'
        WHEN l.valor_numerico > 30 THEN 'alta'
        WHEN l.valor_numerico < 15 THEN 'media'
        ELSE 'baixa'
    END as severidade,
    CONCAT('Anomalia detectada em ', d.nome, ' - ', ts.nome) as titulo,
    CONCAT('Valor atual: ', l.valor_numerico, ' - Data: ', l.timestamp_datetime) as descricao,
    l.valor_numerico,
    CASE 
        WHEN l.valor_numerico > 30 THEN 30.000
        WHEN l.valor_numerico < 15 THEN 15.000
        ELSE 25.000
    END as valor_limite,
    l.timestamp_datetime
FROM leituras_sensores l
JOIN sensores s ON l.id_sensor = s.id_sensor
JOIN dispositivos d ON s.id_dispositivo = d.id_dispositivo
JOIN tipos_sensor ts ON s.id_tipo_sensor = ts.id_tipo_sensor
WHERE l.anomalia_detectada = 1
AND l.timestamp_datetime >= DATE_SUB(NOW(), INTERVAL 1 DAY)
LIMIT 50;

-- =====================================================
-- CARGA DE DASHBOARDS DE EXEMPLO
-- =====================================================

-- Dashboard principal do administrador
INSERT INTO dashboards (id_usuario, nome, descricao, configuracoes, publico) VALUES
(1, 'Dashboard Principal', 'Dashboard principal com visão geral do sistema', 
'{"widgets": [{"type": "kpi", "title": "Dispositivos Ativos", "query": "SELECT COUNT(*) FROM dispositivos WHERE status = \"ativo\""}, {"type": "chart", "title": "Temperatura", "query": "SELECT timestamp_datetime, valor_numerico FROM leituras_sensores WHERE id_sensor IN (1,11,21,31) ORDER BY timestamp_datetime DESC LIMIT 100"}]}', 
1);

-- Dashboard do operador
INSERT INTO dashboards (id_usuario, nome, descricao, configuracoes, publico) VALUES
(2, 'Monitoramento Operacional', 'Dashboard focado em operações do dia a dia',
'{"widgets": [{"type": "alert", "title": "Alertas Ativos", "query": "SELECT * FROM alertas WHERE status = \"ativo\" ORDER BY timestamp_alerta DESC LIMIT 10"}, {"type": "chart", "title": "Umidade por Local", "query": "SELECT d.localizacao, AVG(l.valor_numerico) as umidade_media FROM leituras_sensores l JOIN sensores s ON l.id_sensor = s.id_sensor JOIN dispositivos d ON s.id_dispositivo = d.id_dispositivo WHERE s.id_tipo_sensor = 2 GROUP BY d.localizacao"}]}',
0);

-- =====================================================
-- CARGA DE RELATÓRIOS DE EXEMPLO
-- =====================================================

-- Relatório diário
INSERT INTO relatorios (id_usuario, nome, tipo_relatorio, configuracoes, frequencia, proxima_execucao) VALUES
(1, 'Relatório Diário - Sistema', 'diario', 
'{"template": "diario", "emails": ["admin@iot.com", "operador@iot.com"], "incluir_graficos": true, "incluir_alertas": true}',
'0 8 * * *', -- Todo dia às 8h
DATE_ADD(CURDATE(), INTERVAL 1 DAY) + INTERVAL 8 HOUR);

-- Relatório semanal
INSERT INTO relatorios (id_usuario, nome, tipo_relatorio, configuracoes, frequencia, proxima_execucao) VALUES
(1, 'Relatório Semanal - Performance', 'semanal',
'{"template": "semanal", "emails": ["admin@iot.com"], "incluir_graficos": true, "incluir_estatisticas": true, "incluir_tendencias": true}',
'0 9 * * 1', -- Toda segunda-feira às 9h
DATE_ADD(CURDATE(), INTERVAL (7 - WEEKDAY(CURDATE())) DAY) + INTERVAL 9 HOUR);

-- =====================================================
-- CARGA DE LOGS DE SISTEMA DE EXEMPLO
-- =====================================================

-- Inserir logs de sistema simulados
INSERT INTO logs_sistema (id_usuario, acao, tabela_afetada, id_registro_afetado, dados_anteriores, dados_novos, ip_origem) VALUES
(1, 'INSERT', 'dispositivos', 1, NULL, '{"nome": "ESP32-Sala-01", "mac_address": "AA:BB:CC:DD:EE:FF"}', '192.168.1.100'),
(1, 'INSERT', 'sensores', 1, NULL, '{"nome": "DHT22-Temperatura", "id_dispositivo": 1}', '192.168.1.100'),
(2, 'UPDATE', 'dispositivos', 1, '{"status": "ativo"}', '{"status": "manutencao"}', '192.168.1.101'),
(1, 'INSERT', 'alertas', 1, NULL, '{"tipo_alerta": "temperatura", "severidade": "alta"}', '192.168.1.100'),
(3, 'SELECT', 'leituras_sensores', NULL, NULL, NULL, '192.168.1.102'),
(1, 'DELETE', 'configuracoes_limites', 1, '{"id_configuracao": 1}', NULL, '192.168.1.100');

-- =====================================================
-- ATUALIZAÇÕES PÓS-CARGA
-- =====================================================

-- Atualizar estatísticas das tabelas
ANALYZE TABLE dispositivos;
ANALYZE TABLE sensores;
ANALYZE TABLE leituras_sensores;
ANALYZE TABLE alertas;
ANALYZE TABLE usuarios;
ANALYZE TABLE logs_sistema;

-- Atualizar última conexão dos dispositivos baseado nas leituras
UPDATE dispositivos d
SET ultima_conexao = (
    SELECT MAX(l.timestamp_datetime)
    FROM leituras_sensores l
    JOIN sensores s ON l.id_sensor = s.id_sensor
    WHERE s.id_dispositivo = d.id_dispositivo
);

-- =====================================================
-- VERIFICAÇÕES DE INTEGRIDADE
-- =====================================================

-- Verificar se todas as chaves estrangeiras estão válidas
SELECT 'Verificação de Integridade - Chaves Estrangeiras' as verificacao;

-- Verificar dispositivos órfãos
SELECT COUNT(*) as dispositivos_sem_sensores
FROM dispositivos d
LEFT JOIN sensores s ON d.id_dispositivo = s.id_dispositivo
WHERE s.id_sensor IS NULL;

-- Verificar sensores órfãos
SELECT COUNT(*) as sensores_sem_leituras
FROM sensores s
LEFT JOIN leituras_sensores l ON s.id_sensor = l.id_sensor
WHERE l.id_leitura IS NULL;

-- Verificar alertas órfãos
SELECT COUNT(*) as alertas_sem_dispositivo
FROM alertas a
LEFT JOIN dispositivos d ON a.id_dispositivo = d.id_dispositivo
WHERE d.id_dispositivo IS NULL;

-- =====================================================
-- ESTATÍSTICAS FINAIS
-- =====================================================

SELECT 'Estatísticas Finais do Banco de Dados' as titulo;

SELECT 
    'Dispositivos' as tabela,
    COUNT(*) as total_registros
FROM dispositivos
UNION ALL
SELECT 
    'Sensores' as tabela,
    COUNT(*) as total_registros
FROM sensores
UNION ALL
SELECT 
    'Leituras' as tabela,
    COUNT(*) as total_registros
FROM leituras_sensores
UNION ALL
SELECT 
    'Alertas' as tabela,
    COUNT(*) as total_registros
FROM alertas
UNION ALL
SELECT 
    'Usuários' as tabela,
    COUNT(*) as total_registros
FROM usuarios
UNION ALL
SELECT 
    'Logs' as tabela,
    COUNT(*) as total_registros
FROM logs_sistema;

-- =====================================================
-- COMENTÁRIOS FINAIS
-- =====================================================

-- Este script de carga inclui:
-- - Dados de exemplo para todas as tabelas
-- - Leituras simuladas com padrões realísticos
-- - Configurações de limites para alertas
-- - Alertas baseados em anomalias detectadas
-- - Dashboards e relatórios de exemplo
-- - Logs de sistema simulados
-- - Verificações de integridade
-- - Estatísticas finais do banco
-- - Atualizações de timestamps
-- - Análise de performance das tabelas
