-- =====================================================
-- Sistema IoT Monitoring - Carga de Dados Iniciais
-- Enterprise Challenge Sprint 3 - Reply
-- =====================================================

USE iot_monitoring_db;

-- =====================================================
-- 1. CARGA: tipos_sensor
-- =====================================================

INSERT INTO tipos_sensor (nome, unidade_medida, range_min, range_max, descricao, ativo) VALUES
('DHT22', '°C', -40.0, 80.0, 'Sensor de temperatura e umidade DHT22', TRUE),
('DHT22', '%', 0.0, 100.0, 'Sensor de umidade DHT22', TRUE),
('LDR', 'lux', 0.0, 1000.0, 'Sensor de luminosidade LDR', TRUE),
('PIR', 'boolean', 0.0, 1.0, 'Sensor de movimento PIR', TRUE),
('BME280', 'hPa', 300.0, 1100.0, 'Sensor de pressão atmosférica BME280', TRUE),
('BME280', '°C', -40.0, 85.0, 'Sensor de temperatura BME280', TRUE),
('BME280', '%', 0.0, 100.0, 'Sensor de umidade BME280', TRUE),
('DS18B20', '°C', -55.0, 125.0, 'Sensor de temperatura DS18B20', TRUE),
('MQ135', 'ppm', 0.0, 1000.0, 'Sensor de qualidade do ar MQ135', TRUE),
('HC-SR04', 'cm', 2.0, 400.0, 'Sensor ultrassônico HC-SR04', TRUE);

-- =====================================================
-- 2. CARGA: modos_operacao
-- =====================================================

INSERT INTO modos_operacao (nome, descricao, frequencia_coleta, ativo) VALUES
('normal', 'Modo de operação normal do sistema', 1, TRUE),
('manutencao', 'Modo de manutenção com coleta reduzida', 10, TRUE),
('emergencia', 'Modo de emergência com coleta máxima', 5, TRUE),
('teste', 'Modo de teste para validação', 2, TRUE),
('standby', 'Modo de espera com coleta mínima', 60, TRUE);

-- =====================================================
-- 3. CARGA: configuracoes
-- =====================================================

INSERT INTO configuracoes (chave, valor, tipo, descricao, ativo) VALUES
('sistema.nome', 'Sistema IoT Monitoring', 'string', 'Nome do sistema', TRUE),
('sistema.versao', '1.0.0', 'string', 'Versão do sistema', TRUE),
('sistema.ambiente', 'desenvolvimento', 'string', 'Ambiente de execução', TRUE),
('coleta.frequencia_padrao', '1', 'integer', 'Frequência padrão de coleta em Hz', TRUE),
('coleta.tamanho_lote', '100', 'integer', 'Tamanho do lote para processamento', TRUE),
('coleta.timeout_serial', '5000', 'integer', 'Timeout para comunicação serial em ms', TRUE),
('alertas.temperatura_maxima', '35.0', 'decimal', 'Temperatura máxima para alerta', TRUE),
('alertas.temperatura_minima', '5.0', 'decimal', 'Temperatura mínima para alerta', TRUE),
('alertas.umidade_maxima', '90.0', 'decimal', 'Umidade máxima para alerta', TRUE),
('alertas.umidade_minima', '20.0', 'decimal', 'Umidade mínima para alerta', TRUE),
('alertas.luminosidade_maxima', '800.0', 'decimal', 'Luminosidade máxima para alerta', TRUE),
('alertas.luminosidade_minima', '100.0', 'decimal', 'Luminosidade mínima para alerta', TRUE),
('alertas.pressao_maxima', '1050.0', 'decimal', 'Pressão máxima para alerta', TRUE),
('alertas.pressao_minima', '950.0', 'decimal', 'Pressão mínima para alerta', TRUE),
('banco.retencao_dados_dias', '365', 'integer', 'Dias de retenção de dados', TRUE),
('banco.limpeza_automatica', 'true', 'boolean', 'Limpeza automática de dados antigos', TRUE),
('mqtt.broker_url', 'broker.hivemq.com', 'string', 'URL do broker MQTT', TRUE),
('mqtt.porta', '1883', 'integer', 'Porta do broker MQTT', TRUE),
('mqtt.topico_base', 'industrial/sensors', 'string', 'Tópico base para sensores', TRUE),
('mqtt.qos', '1', 'integer', 'Qualidade de serviço MQTT', TRUE),
('dashboard.atualizacao_segundos', '5', 'integer', 'Intervalo de atualização do dashboard', TRUE),
('dashboard.max_leituras_exibicao', '1000', 'integer', 'Máximo de leituras para exibição', TRUE),
('relatorios.formato_padrao', 'pdf', 'string', 'Formato padrão dos relatórios', TRUE),
('relatorios.email_destinatarios', 'admin@empresa.com', 'string', 'Emails para envio de relatórios', TRUE),
('seguranca.sessao_timeout_minutos', '30', 'integer', 'Timeout de sessão em minutos', TRUE),
('seguranca.tentativas_login_max', '3', 'integer', 'Máximo de tentativas de login', TRUE),
('performance.cache_ttl_segundos', '300', 'integer', 'TTL do cache em segundos', TRUE),
('performance.max_conexoes', '100', 'integer', 'Máximo de conexões simultâneas', TRUE),
('backup.frequencia_horas', '24', 'integer', 'Frequência de backup em horas', TRUE),
('backup.retencao_backups', '7', 'integer', 'Dias de retenção de backups', TRUE);

-- =====================================================
-- 4. CARGA: usuarios
-- =====================================================

INSERT INTO usuarios (nome, email, senha_hash, role, ativo) VALUES
('Administrador', 'admin@iotmonitoring.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/8KqKqKq', 'admin', TRUE),
('Operador Principal', 'operador@iotmonitoring.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/8KqKqKq', 'operador', TRUE),
('Visualizador', 'visualizador@iotmonitoring.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/8KqKqKq', 'visualizador', TRUE),
('Teste', 'teste@iotmonitoring.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/8KqKqKq', 'operador', TRUE);

-- =====================================================
-- 5. CARGA: dispositivos
-- =====================================================

INSERT INTO dispositivos (nome, localizacao, ip_address, mac_address, status, id_modo_operacao, ultima_comunicacao) VALUES
('ESP32-001', 'Sala de Controle Principal', '192.168.1.100', 'AA:BB:CC:DD:EE:01', 'ativo', 1, NOW()),
('ESP32-002', 'Área de Produção A', '192.168.1.101', 'AA:BB:CC:DD:EE:02', 'ativo', 1, NOW()),
('ESP32-003', 'Área de Produção B', '192.168.1.102', 'AA:BB:CC:DD:EE:03', 'ativo', 1, NOW()),
('ESP32-004', 'Almoxarifado', '192.168.1.103', 'AA:BB:CC:DD:EE:04', 'ativo', 1, NOW()),
('ESP32-005', 'Laboratório', '192.168.1.104', 'AA:BB:CC:DD:EE:05', 'ativo', 1, NOW()),
('ESP32-006', 'Escritório', '192.168.1.105', 'AA:BB:CC:DD:EE:06', 'ativo', 1, NOW()),
('ESP32-007', 'Recepção', '192.168.1.106', 'AA:BB:CC:DD:EE:07', 'ativo', 1, NOW()),
('ESP32-008', 'Estacionamento', '192.168.1.107', 'AA:BB:CC:DD:EE:08', 'ativo', 1, NOW()),
('ESP32-009', 'Manutenção', '192.168.1.108', 'AA:BB:CC:DD:EE:09', 'manutencao', 2, NOW()),
('ESP32-010', 'Teste', '192.168.1.109', 'AA:BB:CC:DD:EE:10', 'ativo', 4, NOW());

-- =====================================================
-- 6. CARGA: sensores
-- =====================================================

-- Sensores para ESP32-001 (Sala de Controle)
INSERT INTO sensores (id_dispositivo, id_tipo_sensor, nome, pino, ativo) VALUES
(1, 1, 'DHT22_Temp', '4', TRUE),
(1, 2, 'DHT22_Hum', '4', TRUE),
(1, 3, 'LDR_Light', '34', TRUE),
(1, 4, 'PIR_Motion', '2', TRUE),
(1, 5, 'BME280_Press', '21/22', TRUE);

-- Sensores para ESP32-002 (Área de Produção A)
INSERT INTO sensores (id_dispositivo, id_tipo_sensor, nome, pino, ativo) VALUES
(2, 1, 'DHT22_Temp', '4', TRUE),
(2, 2, 'DHT22_Hum', '4', TRUE),
(2, 3, 'LDR_Light', '34', TRUE),
(2, 4, 'PIR_Motion', '2', TRUE),
(2, 5, 'BME280_Press', '21/22', TRUE);

-- Sensores para ESP32-003 (Área de Produção B)
INSERT INTO sensores (id_dispositivo, id_tipo_sensor, nome, pino, ativo) VALUES
(3, 1, 'DHT22_Temp', '4', TRUE),
(3, 2, 'DHT22_Hum', '4', TRUE),
(3, 3, 'LDR_Light', '34', TRUE),
(3, 4, 'PIR_Motion', '2', TRUE),
(3, 5, 'BME280_Press', '21/22', TRUE);

-- Sensores para ESP32-004 (Almoxarifado)
INSERT INTO sensores (id_dispositivo, id_tipo_sensor, nome, pino, ativo) VALUES
(4, 1, 'DHT22_Temp', '4', TRUE),
(4, 2, 'DHT22_Hum', '4', TRUE),
(4, 3, 'LDR_Light', '34', TRUE),
(4, 4, 'PIR_Motion', '2', TRUE);

-- Sensores para ESP32-005 (Laboratório)
INSERT INTO sensores (id_dispositivo, id_tipo_sensor, nome, pino, ativo) VALUES
(5, 1, 'DHT22_Temp', '4', TRUE),
(5, 2, 'DHT22_Hum', '4', TRUE),
(5, 3, 'LDR_Light', '34', TRUE),
(5, 5, 'BME280_Press', '21/22', TRUE);

-- Sensores para ESP32-006 (Escritório)
INSERT INTO sensores (id_dispositivo, id_tipo_sensor, nome, pino, ativo) VALUES
(6, 1, 'DHT22_Temp', '4', TRUE),
(6, 2, 'DHT22_Hum', '4', TRUE),
(6, 3, 'LDR_Light', '34', TRUE),
(6, 4, 'PIR_Motion', '2', TRUE);

-- Sensores para ESP32-007 (Recepção)
INSERT INTO sensores (id_dispositivo, id_tipo_sensor, nome, pino, ativo) VALUES
(7, 1, 'DHT22_Temp', '4', TRUE),
(7, 2, 'DHT22_Hum', '4', TRUE),
(7, 3, 'LDR_Light', '34', TRUE),
(7, 4, 'PIR_Motion', '2', TRUE);

-- Sensores para ESP32-008 (Estacionamento)
INSERT INTO sensores (id_dispositivo, id_tipo_sensor, nome, pino, ativo) VALUES
(8, 3, 'LDR_Light', '34', TRUE),
(8, 4, 'PIR_Motion', '2', TRUE),
(8, 5, 'BME280_Press', '21/22', TRUE);

-- Sensores para ESP32-009 (Manutenção)
INSERT INTO sensores (id_dispositivo, id_tipo_sensor, nome, pino, ativo) VALUES
(9, 1, 'DHT22_Temp', '4', TRUE),
(9, 2, 'DHT22_Hum', '4', TRUE),
(9, 3, 'LDR_Light', '34', TRUE);

-- Sensores para ESP32-010 (Teste)
INSERT INTO sensores (id_dispositivo, id_tipo_sensor, nome, pino, ativo) VALUES
(10, 1, 'DHT22_Temp', '4', TRUE),
(10, 2, 'DHT22_Hum', '4', TRUE),
(10, 3, 'LDR_Light', '34', TRUE),
(10, 4, 'PIR_Motion', '2', TRUE),
(10, 5, 'BME280_Press', '21/22', TRUE);

-- =====================================================
-- 7. CARGA: relatorios
-- =====================================================

INSERT INTO relatorios (nome, tipo, configuracao, ativo, proxima_execucao) VALUES
('Relatório Diário de Sensores', 'diario', '{"horario": "08:00", "formatos": ["pdf", "html"], "email": true, "dashboards": ["temperatura", "umidade", "luminosidade"]}', TRUE, DATE_ADD(CURDATE(), INTERVAL 1 DAY) + INTERVAL 8 HOUR),
('Relatório Semanal de Performance', 'semanal', '{"dia_semana": 1, "horario": "09:00", "formatos": ["pdf", "excel"], "email": true, "dashboards": ["performance", "alertas", "tendencias"]}', TRUE, DATE_ADD(CURDATE(), INTERVAL (1 - WEEKDAY(CURDATE())) DAY) + INTERVAL 9 HOUR),
('Relatório Mensal Executivo', 'mensal', '{"dia_mes": 1, "horario": "10:00", "formatos": ["pdf"], "email": true, "dashboards": ["executivo", "kpis", "resumo"]}', TRUE, DATE_ADD(LAST_DAY(CURDATE()), INTERVAL 1 DAY) + INTERVAL 10 HOUR),
('Relatório de Alertas Críticos', 'personalizado', '{"frequencia": "hora", "formatos": ["html"], "email": true, "dashboards": ["alertas_criticos"], "filtros": {"severidade": ["critica", "alta"]}}', TRUE, NOW() + INTERVAL 1 HOUR);

-- =====================================================
-- 8. CARGA: logs_sistema (Logs iniciais)
-- =====================================================

INSERT INTO logs_sistema (nivel, componente, mensagem, dados_extras) VALUES
('INFO', 'SISTEMA', 'Sistema IoT Monitoring iniciado', '{"versao": "1.0.0", "ambiente": "desenvolvimento"}'),
('INFO', 'BANCO_DADOS', 'Banco de dados conectado com sucesso', '{"host": "localhost", "porta": 3306, "database": "iot_monitoring_db"}'),
('INFO', 'CONFIGURACAO', 'Configurações carregadas', '{"total_configuracoes": 30}'),
('INFO', 'USUARIOS', 'Usuários iniciais criados', '{"total_usuarios": 4}'),
('INFO', 'DISPOSITIVOS', 'Dispositivos iniciais registrados', '{"total_dispositivos": 10}'),
('INFO', 'SENSORES', 'Sensores iniciais configurados', '{"total_sensores": 40}'),
('INFO', 'RELATORIOS', 'Relatórios automáticos configurados', '{"total_relatorios": 4}'),
('WARNING', 'SISTEMA', 'Aguardando primeira coleta de dados', '{"status": "aguardando_dados"}');

-- =====================================================
-- VERIFICAÇÃO DE CARGA
-- =====================================================

-- Contar registros por tabela
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
    'relatorios' as tabela,
    COUNT(*) as total_registros
FROM relatorios
UNION ALL
SELECT 
    'logs_sistema' as tabela,
    COUNT(*) as total_registros
FROM logs_sistema;

-- Verificar relacionamentos
SELECT 
    'Dispositivos com sensores' as verificacao,
    COUNT(DISTINCT d.id_dispositivo) as dispositivos,
    COUNT(s.id_sensor) as sensores,
    ROUND(COUNT(s.id_sensor) / COUNT(DISTINCT d.id_dispositivo), 2) as media_sensores_por_dispositivo
FROM dispositivos d
LEFT JOIN sensores s ON d.id_dispositivo = s.id_dispositivo;

-- Verificar configurações ativas
SELECT 
    'Configurações ativas' as verificacao,
    COUNT(*) as total,
    COUNT(CASE WHEN tipo = 'string' THEN 1 END) as string,
    COUNT(CASE WHEN tipo = 'integer' THEN 1 END) as integer,
    COUNT(CASE WHEN tipo = 'decimal' THEN 1 END) as decimal,
    COUNT(CASE WHEN tipo = 'boolean' THEN 1 END) as boolean,
    COUNT(CASE WHEN tipo = 'json' THEN 1 END) as json
FROM configuracoes
WHERE ativo = TRUE;

-- Verificar usuários por role
SELECT 
    role,
    COUNT(*) as total_usuarios,
    COUNT(CASE WHEN ativo = TRUE THEN 1 END) as usuarios_ativos
FROM usuarios
GROUP BY role;

-- Mensagem de sucesso
SELECT 
    '===============================================' as separator,
    'Sistema IoT Monitoring - Dados Iniciais' as title,
    'Enterprise Challenge Sprint 3 - Reply' as subtitle,
    '===============================================' as separator,
    'Tipos de sensor: 10' as tipos_sensor_info,
    'Modos de operação: 5' as modos_operacao_info,
    'Configurações: 30' as configuracoes_info,
    'Usuários: 4' as usuarios_info,
    'Dispositivos: 10' as dispositivos_info,
    'Sensores: 40' as sensores_info,
    'Relatórios: 4' as relatorios_info,
    'Logs: 8' as logs_info,
    'Status: CARREGADOS COM SUCESSO' as status,
    '===============================================' as separator;
