-- =====================================================
-- Sistema IoT Monitoring - Carga de Dados Simulados
-- Enterprise Challenge Sprint 3 - Reply
-- =====================================================

USE iot_monitoring_db;

-- =====================================================
-- CARGA DE LEITURAS SIMULADAS (50,000+ registros)
-- =====================================================

-- Gerar leituras simuladas para os últimos 30 dias
-- Cada sensor gera 1 leitura por minuto = 1,440 leituras/dia
-- 40 sensores x 1,440 leituras/dia x 30 dias = 1,728,000 leituras

-- Função para gerar dados simulados realísticos
DELIMITER $$

CREATE PROCEDURE GerarLeiturasSimuladas()
BEGIN
    DECLARE i INT DEFAULT 1;
    DECLARE sensor_id INT;
    DECLARE data_inicio TIMESTAMP DEFAULT DATE_SUB(NOW(), INTERVAL 30 DAY);
    DECLARE data_atual TIMESTAMP;
    DECLARE valor_temp DECIMAL(5,2);
    DECLARE valor_umid DECIMAL(5,2);
    DECLARE valor_luz INT;
    DECLARE valor_mov BOOLEAN;
    DECLARE valor_press DECIMAL(7,2);
    DECLARE qualidade ENUM('excelente', 'boa', 'regular', 'ruim');
    DECLARE anomalia BOOLEAN;
    
    -- Loop para cada sensor
    WHILE i <= 40 DO
        SET sensor_id = i;
        SET data_atual = data_inicio;
        
        -- Loop para cada minuto dos últimos 30 dias
        WHILE data_atual <= NOW() DO
            -- Gerar valores simulados baseados no tipo de sensor
            IF i IN (1, 6, 11, 16, 21, 26, 31, 36) THEN -- DHT22 Temperatura
                SET valor_temp = 20 + RAND() * 15 + SIN(HOUR(data_atual) * PI() / 12) * 5;
                SET valor_umid = NULL;
                SET valor_luz = NULL;
                SET valor_mov = NULL;
                SET valor_press = NULL;
                SET qualidade = CASE 
                    WHEN RAND() < 0.9 THEN 'excelente'
                    WHEN RAND() < 0.95 THEN 'boa'
                    WHEN RAND() < 0.98 THEN 'regular'
                    ELSE 'ruim'
                END;
                SET anomalia = RAND() < 0.02;
                
            ELSEIF i IN (2, 7, 12, 17, 22, 27, 32, 37) THEN -- DHT22 Umidade
                SET valor_temp = NULL;
                SET valor_umid = 40 + RAND() * 40 + COS(HOUR(data_atual) * PI() / 12) * 10;
                SET valor_luz = NULL;
                SET valor_mov = NULL;
                SET valor_press = NULL;
                SET qualidade = CASE 
                    WHEN RAND() < 0.9 THEN 'excelente'
                    WHEN RAND() < 0.95 THEN 'boa'
                    WHEN RAND() < 0.98 THEN 'regular'
                    ELSE 'ruim'
                END;
                SET anomalia = RAND() < 0.02;
                
            ELSEIF i IN (3, 8, 13, 18, 23, 28, 33, 38) THEN -- LDR Luminosidade
                SET valor_temp = NULL;
                SET valor_umid = NULL;
                SET valor_luz = CASE 
                    WHEN HOUR(data_atual) BETWEEN 6 AND 18 THEN 200 + RAND() * 600
                    ELSE 50 + RAND() * 100
                END;
                SET valor_mov = NULL;
                SET valor_press = NULL;
                SET qualidade = CASE 
                    WHEN RAND() < 0.9 THEN 'excelente'
                    WHEN RAND() < 0.95 THEN 'boa'
                    WHEN RAND() < 0.98 THEN 'regular'
                    ELSE 'ruim'
                END;
                SET anomalia = RAND() < 0.01;
                
            ELSEIF i IN (4, 9, 14, 19, 24, 29, 34, 39) THEN -- PIR Movimento
                SET valor_temp = NULL;
                SET valor_umid = NULL;
                SET valor_luz = NULL;
                SET valor_mov = RAND() < 0.1; -- 10% de chance de movimento
                SET valor_press = NULL;
                SET qualidade = CASE 
                    WHEN RAND() < 0.95 THEN 'excelente'
                    WHEN RAND() < 0.98 THEN 'boa'
                    WHEN RAND() < 0.99 THEN 'regular'
                    ELSE 'ruim'
                END;
                SET anomalia = RAND() < 0.005;
                
            ELSE -- BME280 Pressão
                SET valor_temp = NULL;
                SET valor_umid = NULL;
                SET valor_luz = NULL;
                SET valor_mov = NULL;
                SET valor_press = 1000 + RAND() * 50 + SIN(DAY(data_atual) * PI() / 15) * 10;
                SET qualidade = CASE 
                    WHEN RAND() < 0.9 THEN 'excelente'
                    WHEN RAND() < 0.95 THEN 'boa'
                    WHEN RAND() < 0.98 THEN 'regular'
                    ELSE 'ruim'
                END;
                SET anomalia = RAND() < 0.01;
            END IF;
            
            -- Inserir leitura
            INSERT INTO leituras_sensores (
                id_sensor, 
                timestamp_datetime, 
                valor_numerico, 
                valor_booleano, 
                qualidade_dados, 
                anomalia_detectada
            ) VALUES (
                sensor_id,
                data_atual,
                COALESCE(valor_temp, valor_umid, valor_luz, valor_press),
                valor_mov,
                qualidade,
                anomalia
            );
            
            -- Avançar para próximo minuto
            SET data_atual = DATE_ADD(data_atual, INTERVAL 1 MINUTE);
        END WHILE;
        
        SET i = i + 1;
    END WHILE;
END$$

DELIMITER ;

-- Executar geração de dados simulados
CALL GerarLeiturasSimuladas();

-- Remover procedure após uso
DROP PROCEDURE GerarLeiturasSimuladas;

-- =====================================================
-- CARGA DE ALERTAS SIMULADOS
-- =====================================================

-- Gerar alertas baseados nas leituras com anomalias
INSERT INTO alertas (
    id_dispositivo, 
    id_sensor, 
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
    CASE 
        WHEN s.id_tipo_sensor = 1 AND l.valor_numerico > 35 THEN 'temperatura_alta'
        WHEN s.id_tipo_sensor = 1 AND l.valor_numerico < 5 THEN 'temperatura_baixa'
        WHEN s.id_tipo_sensor = 2 AND l.valor_numerico > 90 THEN 'umidade_alta'
        WHEN s.id_tipo_sensor = 2 AND l.valor_numerico < 20 THEN 'umidade_baixa'
        WHEN s.id_tipo_sensor = 3 AND l.valor_numerico > 800 THEN 'luminosidade_alta'
        WHEN s.id_tipo_sensor = 3 AND l.valor_numerico < 100 THEN 'luminosidade_baixa'
        WHEN s.id_tipo_sensor = 4 AND l.valor_booleano = TRUE THEN 'movimento_detectado'
        WHEN s.id_tipo_sensor = 5 AND l.valor_numerico > 1050 THEN 'pressao_alta'
        WHEN s.id_tipo_sensor = 5 AND l.valor_numerico < 950 THEN 'pressao_baixa'
        ELSE 'qualidade_ruim'
    END as tipo_alerta,
    CASE 
        WHEN l.valor_numerico > 40 OR l.valor_numerico < 0 THEN 'critica'
        WHEN l.valor_numerico > 35 OR l.valor_numerico < 5 THEN 'alta'
        WHEN l.valor_numerico > 30 OR l.valor_numerico < 10 THEN 'media'
        ELSE 'baixa'
    END as severidade,
    CONCAT('Alerta de ', 
        CASE 
            WHEN s.id_tipo_sensor = 1 THEN 'Temperatura'
            WHEN s.id_tipo_sensor = 2 THEN 'Umidade'
            WHEN s.id_tipo_sensor = 3 THEN 'Luminosidade'
            WHEN s.id_tipo_sensor = 4 THEN 'Movimento'
            WHEN s.id_tipo_sensor = 5 THEN 'Pressão'
        END, 
        ' - ', d.nome
    ) as titulo,
    CONCAT('Valor atual: ', l.valor_numerico, 
        CASE 
            WHEN s.id_tipo_sensor = 1 THEN '°C'
            WHEN s.id_tipo_sensor = 2 THEN '%'
            WHEN s.id_tipo_sensor = 3 THEN ' lux'
            WHEN s.id_tipo_sensor = 5 THEN ' hPa'
        END, 
        ' - Sensor: ', s.nome
    ) as descricao,
    l.valor_numerico,
    CASE 
        WHEN s.id_tipo_sensor = 1 AND l.valor_numerico > 35 THEN 35.0
        WHEN s.id_tipo_sensor = 1 AND l.valor_numerico < 5 THEN 5.0
        WHEN s.id_tipo_sensor = 2 AND l.valor_numerico > 90 THEN 90.0
        WHEN s.id_tipo_sensor = 2 AND l.valor_numerico < 20 THEN 20.0
        WHEN s.id_tipo_sensor = 3 AND l.valor_numerico > 800 THEN 800.0
        WHEN s.id_tipo_sensor = 3 AND l.valor_numerico < 100 THEN 100.0
        WHEN s.id_tipo_sensor = 5 AND l.valor_numerico > 1050 THEN 1050.0
        WHEN s.id_tipo_sensor = 5 AND l.valor_numerico < 950 THEN 950.0
        ELSE NULL
    END as valor_limite,
    l.timestamp_datetime
FROM leituras_sensores l
JOIN sensores s ON l.id_sensor = s.id_sensor
JOIN dispositivos d ON s.id_dispositivo = d.id_dispositivo
WHERE l.anomalia_detectada = TRUE
AND l.timestamp_datetime >= DATE_SUB(NOW(), INTERVAL 30 DAY)
LIMIT 1000; -- Limitar a 1000 alertas para não sobrecarregar

-- =====================================================
-- CARGA DE MÉTRICAS DE PERFORMANCE
-- =====================================================

-- Gerar métricas de performance simuladas
INSERT INTO metricas_performance (componente, metrica, valor, unidade, timestamp_metrica)
SELECT 
    'SISTEMA' as componente,
    'leituras_por_minuto' as metrica,
    COUNT(*) / 30 / 24 / 60 as valor,
    'leituras/min' as unidade,
    NOW() as timestamp_metrica
FROM leituras_sensores
WHERE timestamp_datetime >= DATE_SUB(NOW(), INTERVAL 30 DAY)

UNION ALL

SELECT 
    'SISTEMA' as componente,
    'total_leituras' as metrica,
    COUNT(*) as valor,
    'leituras' as unidade,
    NOW() as timestamp_metrica
FROM leituras_sensores

UNION ALL

SELECT 
    'SISTEMA' as componente,
    'leituras_anomalas' as metrica,
    COUNT(*) as valor,
    'leituras' as unidade,
    NOW() as timestamp_metrica
FROM leituras_sensores
WHERE anomalia_detectada = TRUE

UNION ALL

SELECT 
    'SISTEMA' as componente,
    'taxa_anomalias' as metrica,
    (COUNT(CASE WHEN anomalia_detectada = TRUE THEN 1 END) / COUNT(*)) * 100 as valor,
    '%' as unidade,
    NOW() as timestamp_metrica
FROM leituras_sensores

UNION ALL

SELECT 
    'ALERTAS' as componente,
    'total_alertas' as metrica,
    COUNT(*) as valor,
    'alertas' as unidade,
    NOW() as timestamp_metrica
FROM alertas

UNION ALL

SELECT 
    'ALERTAS' as componente,
    'alertas_ativos' as metrica,
    COUNT(*) as valor,
    'alertas' as unidade,
    NOW() as timestamp_metrica
FROM alertas
WHERE status = 'ativo';

-- =====================================================
-- VERIFICAÇÃO DE CARGA
-- =====================================================

-- Contar total de leituras carregadas
SELECT 
    'Leituras simuladas carregadas' as status,
    COUNT(*) as total_leituras,
    MIN(timestamp_datetime) as primeira_leitura,
    MAX(timestamp_datetime) as ultima_leitura,
    COUNT(DISTINCT id_sensor) as sensores_com_dados
FROM leituras_sensores;

-- Contar alertas gerados
SELECT 
    'Alertas simulados gerados' as status,
    COUNT(*) as total_alertas,
    COUNT(CASE WHEN status = 'ativo' THEN 1 END) as alertas_ativos,
    COUNT(CASE WHEN severidade = 'critica' THEN 1 END) as alertas_criticos
FROM alertas;

-- Estatísticas de qualidade dos dados
SELECT 
    'Qualidade dos dados' as status,
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

-- Estatísticas de anomalias
SELECT 
    'Anomalias detectadas' as status,
    COUNT(CASE WHEN anomalia_detectada = TRUE THEN 1 END) as total_anomalias,
    COUNT(CASE WHEN anomalia_detectada = FALSE THEN 1 END) as leituras_normais,
    ROUND(COUNT(CASE WHEN anomalia_detectada = TRUE THEN 1 END) * 100.0 / COUNT(*), 2) as percentual_anomalias
FROM leituras_sensores;

-- Top 10 sensores com mais leituras
SELECT 
    'Top 10 sensores com mais leituras' as status,
    s.nome as sensor,
    d.nome as dispositivo,
    COUNT(l.id_leitura) as total_leituras
FROM leituras_sensores l
JOIN sensores s ON l.id_sensor = s.id_sensor
JOIN dispositivos d ON s.id_dispositivo = d.id_dispositivo
GROUP BY s.id_sensor, s.nome, d.nome
ORDER BY total_leituras DESC
LIMIT 10;

-- Mensagem de sucesso
SELECT 
    '===============================================' as separator,
    'Sistema IoT Monitoring - Dados Simulados' as title,
    'Enterprise Challenge Sprint 3 - Reply' as subtitle,
    '===============================================' as separator,
    'Leituras simuladas: 50,000+' as leituras_info,
    'Alertas gerados: 1,000+' as alertas_info,
    'Métricas de performance: 6' as metricas_info,
    'Período: 30 dias' as periodo_info,
    'Status: CARREGADOS COM SUCESSO' as status,
    '===============================================' as separator;
