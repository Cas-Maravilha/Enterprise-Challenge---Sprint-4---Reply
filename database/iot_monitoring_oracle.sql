-- =====================================================
-- SCHEMA ORACLE - SISTEMA IoT MONITORING
-- Arquivo: iot_monitoring_oracle.sql
-- Versão: 1.0
-- Data: 2025-01-11
-- Descrição: Schema Oracle para sistema IoT
-- =====================================================

-- Configurações iniciais
ALTER SESSION SET NLS_DATE_FORMAT = 'YYYY-MM-DD HH24:MI:SS';
ALTER SESSION SET NLS_TIMESTAMP_FORMAT = 'YYYY-MM-DD HH24:MI:SS.FF3';

-- =====================================================
-- SEQUÊNCIAS
-- =====================================================

-- Sequência para dispositivos
CREATE SEQUENCE seq_dispositivos
    START WITH 1
    INCREMENT BY 1
    NOCACHE
    NOCYCLE;

-- Sequência para tipos_sensor
CREATE SEQUENCE seq_tipos_sensor
    START WITH 1
    INCREMENT BY 1
    NOCACHE
    NOCYCLE;

-- Sequência para sensores
CREATE SEQUENCE seq_sensores
    START WITH 1
    INCREMENT BY 1
    NOCACHE
    NOCYCLE;

-- Sequência para leituras_sensores
CREATE SEQUENCE seq_leituras_sensores
    START WITH 1
    INCREMENT BY 1
    NOCACHE
    NOCYCLE;

-- Sequência para modos_operacao
CREATE SEQUENCE seq_modos_operacao
    START WITH 1
    INCREMENT BY 1
    NOCACHE
    NOCYCLE;

-- Sequência para alertas
CREATE SEQUENCE seq_alertas
    START WITH 1
    INCREMENT BY 1
    NOCACHE
    NOCYCLE;

-- Sequência para configuracoes_limites
CREATE SEQUENCE seq_configuracoes_limites
    START WITH 1
    INCREMENT BY 1
    NOCACHE
    NOCYCLE;

-- Sequência para usuarios
CREATE SEQUENCE seq_usuarios
    START WITH 1
    INCREMENT BY 1
    NOCACHE
    NOCYCLE;

-- Sequência para logs_sistema
CREATE SEQUENCE seq_logs_sistema
    START WITH 1
    INCREMENT BY 1
    NOCACHE
    NOCYCLE;

-- Sequência para dashboards
CREATE SEQUENCE seq_dashboards
    START WITH 1
    INCREMENT BY 1
    NOCACHE
    NOCYCLE;

-- Sequência para relatorios
CREATE SEQUENCE seq_relatorios
    START WITH 1
    INCREMENT BY 1
    NOCACHE
    NOCYCLE;

-- =====================================================
-- TABELAS PRINCIPAIS
-- =====================================================

-- Tabela dispositivos
CREATE TABLE dispositivos (
    id_dispositivo NUMBER(10) PRIMARY KEY,
    nome VARCHAR2(100) NOT NULL,
    mac_address VARCHAR2(17) NOT NULL,
    ip_address VARCHAR2(15),
    localizacao VARCHAR2(200),
    status VARCHAR2(20) NOT NULL DEFAULT 'ativo' CHECK (status IN ('ativo', 'inativo', 'manutencao')),
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ultima_conexao TIMESTAMP,
    versao_firmware VARCHAR2(20),
    observacoes CLOB
);

-- Índices para dispositivos
CREATE UNIQUE INDEX uk_dispositivos_mac_address ON dispositivos(mac_address);
CREATE INDEX idx_dispositivos_status ON dispositivos(status);
CREATE INDEX idx_dispositivos_localizacao ON dispositivos(localizacao);
CREATE INDEX idx_dispositivos_ultima_conexao ON dispositivos(ultima_conexao);

-- Tabela tipos_sensor
CREATE TABLE tipos_sensor (
    id_tipo_sensor NUMBER(10) PRIMARY KEY,
    nome VARCHAR2(50) NOT NULL,
    descricao CLOB,
    unidade_medida VARCHAR2(20),
    faixa_min NUMBER(10,3),
    faixa_max NUMBER(10,3),
    precisao NUMBER(8,3),
    ativo NUMBER(1) NOT NULL DEFAULT 1 CHECK (ativo IN (0, 1)),
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Índices para tipos_sensor
CREATE UNIQUE INDEX uk_tipos_sensor_nome ON tipos_sensor(nome);
CREATE INDEX idx_tipos_sensor_ativo ON tipos_sensor(ativo);

-- Tabela sensores
CREATE TABLE sensores (
    id_sensor NUMBER(10) PRIMARY KEY,
    id_dispositivo NUMBER(10) NOT NULL,
    id_tipo_sensor NUMBER(10) NOT NULL,
    nome VARCHAR2(100) NOT NULL,
    pino_analogico NUMBER(10),
    pino_digital NUMBER(10),
    calibracao_min NUMBER(10,3),
    calibracao_max NUMBER(10,3),
    status VARCHAR2(20) NOT NULL DEFAULT 'ativo' CHECK (status IN ('ativo', 'inativo', 'falha')),
    data_instalacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ultima_calibracao TIMESTAMP,
    observacoes CLOB,
    CONSTRAINT fk_sensores_dispositivos FOREIGN KEY (id_dispositivo) REFERENCES dispositivos(id_dispositivo) ON DELETE CASCADE,
    CONSTRAINT fk_sensores_tipos_sensor FOREIGN KEY (id_tipo_sensor) REFERENCES tipos_sensor(id_tipo_sensor) ON DELETE CASCADE
);

-- Índices para sensores
CREATE INDEX idx_sensores_dispositivo ON sensores(id_dispositivo);
CREATE INDEX idx_sensores_tipo ON sensores(id_tipo_sensor);
CREATE INDEX idx_sensores_status ON sensores(status);

-- Tabela leituras_sensores
CREATE TABLE leituras_sensores (
    id_leitura NUMBER(19) PRIMARY KEY,
    id_sensor NUMBER(10) NOT NULL,
    timestamp_unix NUMBER(15,3) NOT NULL,
    timestamp_datetime TIMESTAMP NOT NULL,
    valor_numerico NUMBER(12,6),
    valor_booleano NUMBER(1) CHECK (valor_booleano IN (0, 1)),
    valor_string VARCHAR2(255),
    qualidade_dados VARCHAR2(20) NOT NULL DEFAULT 'bom' CHECK (qualidade_dados IN ('excelente', 'bom', 'regular', 'ruim')),
    anomalia_detectada NUMBER(1) NOT NULL DEFAULT 0 CHECK (anomalia_detectada IN (0, 1)),
    data_coleta TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_leituras_sensores FOREIGN KEY (id_sensor) REFERENCES sensores(id_sensor) ON DELETE CASCADE
);

-- Índices para leituras_sensores
CREATE INDEX idx_leituras_sensor ON leituras_sensores(id_sensor);
CREATE INDEX idx_leituras_timestamp ON leituras_sensores(timestamp_datetime);
CREATE INDEX idx_leituras_qualidade ON leituras_sensores(qualidade_dados);
CREATE INDEX idx_leituras_anomalia ON leituras_sensores(anomalia_detectada);
CREATE INDEX idx_leituras_sensor_timestamp ON leituras_sensores(id_sensor, timestamp_datetime);

-- Tabela modos_operacao
CREATE TABLE modos_operacao (
    id_modo NUMBER(10) PRIMARY KEY,
    nome VARCHAR2(50) NOT NULL,
    descricao CLOB,
    cor_indicador VARCHAR2(7),
    ativo NUMBER(1) NOT NULL DEFAULT 1 CHECK (ativo IN (0, 1)),
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Índices para modos_operacao
CREATE UNIQUE INDEX uk_modos_operacao_nome ON modos_operacao(nome);
CREATE INDEX idx_modos_operacao_ativo ON modos_operacao(ativo);

-- Tabela alertas
CREATE TABLE alertas (
    id_alerta NUMBER(19) PRIMARY KEY,
    id_dispositivo NUMBER(10) NOT NULL,
    id_sensor NUMBER(10),
    id_modo NUMBER(10) NOT NULL,
    tipo_alerta VARCHAR2(20) NOT NULL CHECK (tipo_alerta IN ('temperatura', 'umidade', 'pressao', 'vibracao', 'nivel', 'conexao', 'geral')),
    severidade VARCHAR2(20) NOT NULL CHECK (severidade IN ('baixa', 'media', 'alta', 'critica')),
    titulo VARCHAR2(200) NOT NULL,
    descricao CLOB,
    valor_atual NUMBER(12,6),
    valor_limite NUMBER(12,6),
    timestamp_alerta TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR2(20) NOT NULL DEFAULT 'ativo' CHECK (status IN ('ativo', 'resolvido', 'ignorado')),
    data_resolucao TIMESTAMP,
    usuario_resolucao VARCHAR2(100),
    observacoes_resolucao CLOB,
    CONSTRAINT fk_alertas_dispositivos FOREIGN KEY (id_dispositivo) REFERENCES dispositivos(id_dispositivo) ON DELETE CASCADE,
    CONSTRAINT fk_alertas_sensores FOREIGN KEY (id_sensor) REFERENCES sensores(id_sensor) ON DELETE SET NULL,
    CONSTRAINT fk_alertas_modos_operacao FOREIGN KEY (id_modo) REFERENCES modos_operacao(id_modo) ON DELETE CASCADE
);

-- Índices para alertas
CREATE INDEX idx_alertas_dispositivo ON alertas(id_dispositivo);
CREATE INDEX idx_alertas_sensor ON alertas(id_sensor);
CREATE INDEX idx_alertas_modo ON alertas(id_modo);
CREATE INDEX idx_alertas_timestamp ON alertas(timestamp_alerta);
CREATE INDEX idx_alertas_status ON alertas(status);
CREATE INDEX idx_alertas_severidade ON alertas(severidade);
CREATE INDEX idx_alertas_tipo ON alertas(tipo_alerta);

-- Tabela configuracoes_limites
CREATE TABLE configuracoes_limites (
    id_configuracao NUMBER(10) PRIMARY KEY,
    id_sensor NUMBER(10) NOT NULL,
    tipo_limite VARCHAR2(20) NOT NULL CHECK (tipo_limite IN ('minimo', 'maximo', 'variacao')),
    valor_limite NUMBER(12,6) NOT NULL,
    severidade VARCHAR2(20) NOT NULL CHECK (severidade IN ('baixa', 'media', 'alta', 'critica')),
    ativo NUMBER(1) NOT NULL DEFAULT 1 CHECK (ativo IN (0, 1)),
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario_criacao VARCHAR2(100),
    observacoes CLOB,
    CONSTRAINT fk_configuracoes_limites_sensores FOREIGN KEY (id_sensor) REFERENCES sensores(id_sensor) ON DELETE CASCADE
);

-- Índices para configuracoes_limites
CREATE INDEX idx_configuracoes_sensor ON configuracoes_limites(id_sensor);
CREATE INDEX idx_configuracoes_tipo_limite ON configuracoes_limites(tipo_limite);
CREATE INDEX idx_configuracoes_ativo ON configuracoes_limites(ativo);

-- Tabela usuarios
CREATE TABLE usuarios (
    id_usuario NUMBER(10) PRIMARY KEY,
    nome VARCHAR2(100) NOT NULL,
    email VARCHAR2(255) NOT NULL,
    senha_hash VARCHAR2(255) NOT NULL,
    perfil VARCHAR2(20) NOT NULL CHECK (perfil IN ('admin', 'operador', 'visualizador')),
    ativo NUMBER(1) NOT NULL DEFAULT 1 CHECK (ativo IN (0, 1)),
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ultimo_login TIMESTAMP,
    token_reset_senha VARCHAR2(255),
    data_expiracao_token TIMESTAMP
);

-- Índices para usuarios
CREATE UNIQUE INDEX uk_usuarios_email ON usuarios(email);
CREATE INDEX idx_usuarios_perfil ON usuarios(perfil);
CREATE INDEX idx_usuarios_ativo ON usuarios(ativo);

-- Tabela logs_sistema
CREATE TABLE logs_sistema (
    id_log NUMBER(19) PRIMARY KEY,
    id_usuario NUMBER(10),
    acao VARCHAR2(100) NOT NULL,
    tabela_afetada VARCHAR2(50),
    id_registro_afetado NUMBER(19),
    dados_anteriores CLOB, -- JSON armazenado como CLOB
    dados_novos CLOB, -- JSON armazenado como CLOB
    ip_origem VARCHAR2(45),
    user_agent CLOB,
    timestamp_log TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_logs_sistema_usuarios FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE SET NULL
);

-- Índices para logs_sistema
CREATE INDEX idx_logs_usuario ON logs_sistema(id_usuario);
CREATE INDEX idx_logs_acao ON logs_sistema(acao);
CREATE INDEX idx_logs_timestamp ON logs_sistema(timestamp_log);
CREATE INDEX idx_logs_tabela ON logs_sistema(tabela_afetada);

-- Tabela dashboards
CREATE TABLE dashboards (
    id_dashboard NUMBER(10) PRIMARY KEY,
    id_usuario NUMBER(10) NOT NULL,
    nome VARCHAR2(100) NOT NULL,
    descricao CLOB,
    configuracoes CLOB, -- JSON armazenado como CLOB
    publico NUMBER(1) NOT NULL DEFAULT 0 CHECK (publico IN (0, 1)),
    ativo NUMBER(1) NOT NULL DEFAULT 1 CHECK (ativo IN (0, 1)),
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_dashboards_usuarios FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE CASCADE
);

-- Índices para dashboards
CREATE INDEX idx_dashboards_usuario ON dashboards(id_usuario);
CREATE INDEX idx_dashboards_publico ON dashboards(publico);
CREATE INDEX idx_dashboards_ativo ON dashboards(ativo);

-- Tabela relatorios
CREATE TABLE relatorios (
    id_relatorio NUMBER(10) PRIMARY KEY,
    id_usuario NUMBER(10) NOT NULL,
    nome VARCHAR2(100) NOT NULL,
    tipo_relatorio VARCHAR2(20) NOT NULL CHECK (tipo_relatorio IN ('diario', 'semanal', 'mensal', 'personalizado')),
    configuracoes CLOB, -- JSON armazenado como CLOB
    frequencia VARCHAR2(50),
    ativo NUMBER(1) NOT NULL DEFAULT 1 CHECK (ativo IN (0, 1)),
    proxima_execucao TIMESTAMP,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_relatorios_usuarios FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE CASCADE
);

-- Índices para relatorios
CREATE INDEX idx_relatorios_usuario ON relatorios(id_usuario);
CREATE INDEX idx_relatorios_tipo ON relatorios(tipo_relatorio);
CREATE INDEX idx_relatorios_proxima_execucao ON relatorios(proxima_execucao);

-- =====================================================
-- TRIGGERS
-- =====================================================

-- Trigger para sequência dispositivos
CREATE OR REPLACE TRIGGER tr_dispositivos_id
    BEFORE INSERT ON dispositivos
    FOR EACH ROW
BEGIN
    IF :NEW.id_dispositivo IS NULL THEN
        :NEW.id_dispositivo := seq_dispositivos.NEXTVAL;
    END IF;
END;
/

-- Trigger para sequência tipos_sensor
CREATE OR REPLACE TRIGGER tr_tipos_sensor_id
    BEFORE INSERT ON tipos_sensor
    FOR EACH ROW
BEGIN
    IF :NEW.id_tipo_sensor IS NULL THEN
        :NEW.id_tipo_sensor := seq_tipos_sensor.NEXTVAL;
    END IF;
END;
/

-- Trigger para sequência sensores
CREATE OR REPLACE TRIGGER tr_sensores_id
    BEFORE INSERT ON sensores
    FOR EACH ROW
BEGIN
    IF :NEW.id_sensor IS NULL THEN
        :NEW.id_sensor := seq_sensores.NEXTVAL;
    END IF;
END;
/

-- Trigger para sequência leituras_sensores
CREATE OR REPLACE TRIGGER tr_leituras_sensores_id
    BEFORE INSERT ON leituras_sensores
    FOR EACH ROW
BEGIN
    IF :NEW.id_leitura IS NULL THEN
        :NEW.id_leitura := seq_leituras_sensores.NEXTVAL;
    END IF;
END;
/

-- Trigger para sequência modos_operacao
CREATE OR REPLACE TRIGGER tr_modos_operacao_id
    BEFORE INSERT ON modos_operacao
    FOR EACH ROW
BEGIN
    IF :NEW.id_modo IS NULL THEN
        :NEW.id_modo := seq_modos_operacao.NEXTVAL;
    END IF;
END;
/

-- Trigger para sequência alertas
CREATE OR REPLACE TRIGGER tr_alertas_id
    BEFORE INSERT ON alertas
    FOR EACH ROW
BEGIN
    IF :NEW.id_alerta IS NULL THEN
        :NEW.id_alerta := seq_alertas.NEXTVAL;
    END IF;
END;
/

-- Trigger para sequência configuracoes_limites
CREATE OR REPLACE TRIGGER tr_configuracoes_limites_id
    BEFORE INSERT ON configuracoes_limites
    FOR EACH ROW
BEGIN
    IF :NEW.id_configuracao IS NULL THEN
        :NEW.id_configuracao := seq_configuracoes_limites.NEXTVAL;
    END IF;
END;
/

-- Trigger para sequência usuarios
CREATE OR REPLACE TRIGGER tr_usuarios_id
    BEFORE INSERT ON usuarios
    FOR EACH ROW
BEGIN
    IF :NEW.id_usuario IS NULL THEN
        :NEW.id_usuario := seq_usuarios.NEXTVAL;
    END IF;
END;
/

-- Trigger para sequência logs_sistema
CREATE OR REPLACE TRIGGER tr_logs_sistema_id
    BEFORE INSERT ON logs_sistema
    FOR EACH ROW
BEGIN
    IF :NEW.id_log IS NULL THEN
        :NEW.id_log := seq_logs_sistema.NEXTVAL;
    END IF;
END;
/

-- Trigger para sequência dashboards
CREATE OR REPLACE TRIGGER tr_dashboards_id
    BEFORE INSERT ON dashboards
    FOR EACH ROW
BEGIN
    IF :NEW.id_dashboard IS NULL THEN
        :NEW.id_dashboard := seq_dashboards.NEXTVAL;
    END IF;
END;
/

-- Trigger para sequência relatorios
CREATE OR REPLACE TRIGGER tr_relatorios_id
    BEFORE INSERT ON relatorios
    FOR EACH ROW
BEGIN
    IF :NEW.id_relatorio IS NULL THEN
        :NEW.id_relatorio := seq_relatorios.NEXTVAL;
    END IF;
END;
/

-- Trigger para atualizar data_atualizacao em configuracoes_limites
CREATE OR REPLACE TRIGGER tr_configuracoes_limites_updated_at
    BEFORE UPDATE ON configuracoes_limites
    FOR EACH ROW
BEGIN
    :NEW.data_atualizacao := CURRENT_TIMESTAMP;
END;
/

-- Trigger para atualizar data_atualizacao em dashboards
CREATE OR REPLACE TRIGGER tr_dashboards_updated_at
    BEFORE UPDATE ON dashboards
    FOR EACH ROW
BEGIN
    :NEW.data_atualizacao := CURRENT_TIMESTAMP;
END;
/

-- Trigger para atualizar última conexão do dispositivo
CREATE OR REPLACE TRIGGER tr_update_ultima_conexao
    AFTER INSERT ON leituras_sensores
    FOR EACH ROW
DECLARE
    v_id_dispositivo NUMBER(10);
BEGIN
    SELECT id_dispositivo INTO v_id_dispositivo
    FROM sensores
    WHERE id_sensor = :NEW.id_sensor;
    
    UPDATE dispositivos 
    SET ultima_conexao = CURRENT_TIMESTAMP
    WHERE id_dispositivo = v_id_dispositivo;
END;
/

-- =====================================================
-- VIEWS
-- =====================================================

-- View para leituras completas
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
-- PROCEDURES
-- =====================================================

-- Procedure para inserir leitura
CREATE OR REPLACE PROCEDURE sp_inserir_leitura(
    p_id_sensor IN NUMBER,
    p_timestamp_unix IN NUMBER,
    p_valor_numerico IN NUMBER DEFAULT NULL,
    p_valor_booleano IN NUMBER DEFAULT NULL,
    p_valor_string IN VARCHAR2 DEFAULT NULL,
    p_qualidade_dados IN VARCHAR2 DEFAULT 'bom',
    p_id_leitura OUT NUMBER
) AS
    v_timestamp_datetime TIMESTAMP;
    v_anomalia NUMBER(1) := 0;
BEGIN
    -- Converte timestamp unix para datetime
    v_timestamp_datetime := TO_TIMESTAMP('1970-01-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS') + 
                           (p_timestamp_unix / 86400);
    
    -- Verifica se há anomalia baseada na qualidade dos dados
    IF p_qualidade_dados IN ('regular', 'ruim') THEN
        v_anomalia := 1;
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
    ) RETURNING id_leitura INTO p_id_leitura;
    
    COMMIT;
END;
/

-- Procedure para verificar limites
CREATE OR REPLACE PROCEDURE sp_verificar_limites(
    p_id_sensor IN NUMBER, 
    p_valor IN NUMBER
) AS
    v_limite_max NUMBER(12,6);
    v_limite_min NUMBER(12,6);
    v_severidade_max VARCHAR2(20);
    v_severidade_min VARCHAR2(20);
    v_id_dispositivo NUMBER(10);
    v_tipo_sensor VARCHAR2(50);
BEGIN
    -- Obtém informações do sensor
    SELECT s.id_dispositivo, ts.nome
    INTO v_id_dispositivo, v_tipo_sensor
    FROM sensores s
    JOIN tipos_sensor ts ON s.id_tipo_sensor = ts.id_tipo_sensor
    WHERE s.id_sensor = p_id_sensor;
    
    -- Verifica limite máximo
    BEGIN
        SELECT valor_limite, severidade
        INTO v_limite_max, v_severidade_max
        FROM configuracoes_limites
        WHERE id_sensor = p_id_sensor 
        AND tipo_limite = 'maximo' 
        AND ativo = 1
        ORDER BY 
            CASE severidade 
                WHEN 'critica' THEN 4
                WHEN 'alta' THEN 3
                WHEN 'media' THEN 2
                WHEN 'baixa' THEN 1
            END DESC
        FETCH FIRST 1 ROW ONLY;
        
        -- Cria alerta se excedeu limite máximo
        IF p_valor > v_limite_max THEN
            INSERT INTO alertas (
                id_dispositivo, id_sensor, id_modo, tipo_alerta, severidade,
                titulo, descricao, valor_atual, valor_limite
            ) VALUES (
                v_id_dispositivo, p_id_sensor, 2, -- Modo de falha
                v_tipo_sensor, v_severidade_max,
                'Valor excedeu limite máximo: ' || v_tipo_sensor,
                'Valor atual: ' || p_valor || ' | Limite: ' || v_limite_max,
                p_valor, v_limite_max
            );
        END IF;
    EXCEPTION
        WHEN NO_DATA_FOUND THEN
            NULL; -- Não há limite máximo configurado
    END;
    
    -- Verifica limite mínimo
    BEGIN
        SELECT valor_limite, severidade
        INTO v_limite_min, v_severidade_min
        FROM configuracoes_limites
        WHERE id_sensor = p_id_sensor 
        AND tipo_limite = 'minimo' 
        AND ativo = 1
        ORDER BY 
            CASE severidade 
                WHEN 'critica' THEN 4
                WHEN 'alta' THEN 3
                WHEN 'media' THEN 2
                WHEN 'baixa' THEN 1
            END DESC
        FETCH FIRST 1 ROW ONLY;
        
        -- Cria alerta se excedeu limite mínimo
        IF p_valor < v_limite_min THEN
            INSERT INTO alertas (
                id_dispositivo, id_sensor, id_modo, tipo_alerta, severidade,
                titulo, descricao, valor_atual, valor_limite
            ) VALUES (
                v_id_dispositivo, p_id_sensor, 2, -- Modo de falha
                v_tipo_sensor, v_severidade_min,
                'Valor abaixo do limite mínimo: ' || v_tipo_sensor,
                'Valor atual: ' || p_valor || ' | Limite: ' || v_limite_min,
                p_valor, v_limite_min
            );
        END IF;
    EXCEPTION
        WHEN NO_DATA_FOUND THEN
            NULL; -- Não há limite mínimo configurado
    END;
    
    COMMIT;
END;
/

-- =====================================================
-- DADOS INICIAIS
-- =====================================================

-- Inserir tipos de sensores
INSERT INTO tipos_sensor (nome, descricao, unidade_medida, faixa_min, faixa_max, precisao) VALUES
('DHT22', 'Sensor de temperatura e umidade digital', '°C/%', -40.0, 80.0, 0.5);
INSERT INTO tipos_sensor (nome, descricao, unidade_medida, faixa_min, faixa_max, precisao) VALUES
('LDR', 'Sensor de luminosidade (Light Dependent Resistor)', 'lux', 0.0, 1023.0, 1.0);
INSERT INTO tipos_sensor (nome, descricao, unidade_medida, faixa_min, faixa_max, precisao) VALUES
('PIR', 'Sensor de movimento passivo infravermelho', 'boolean', 0.0, 1.0, 1.0);
INSERT INTO tipos_sensor (nome, descricao, unidade_medida, faixa_min, faixa_max, precisao) VALUES
('Pressão', 'Sensor de pressão barométrica', 'bar', 0.0, 10.0, 0.01);
INSERT INTO tipos_sensor (nome, descricao, unidade_medida, faixa_min, faixa_max, precisao) VALUES
('Vibração', 'Sensor de vibração triaxial', 'g', -2.0, 2.0, 0.001);
INSERT INTO tipos_sensor (nome, descricao, unidade_medida, faixa_min, faixa_max, precisao) VALUES
('Nível', 'Sensor de nível ultrassônico', 'cm', 0.0, 200.0, 0.1);

-- Inserir modos de operação
INSERT INTO modos_operacao (nome, descricao, cor_indicador) VALUES
('Normal', 'Sistema operando dentro dos parâmetros normais', '#28a745');
INSERT INTO modos_operacao (nome, descricao, cor_indicador) VALUES
('Alerta', 'Sistema com valores próximos aos limites', '#ffc107');
INSERT INTO modos_operacao (nome, descricao, cor_indicador) VALUES
('Falha', 'Sistema com falha ou valores críticos', '#dc3545');

-- Inserir usuário administrador padrão
INSERT INTO usuarios (nome, email, senha_hash, perfil) VALUES
('Administrador', 'admin@iot.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/8Kz8KzK', 'admin');

-- Inserir dispositivos de exemplo
INSERT INTO dispositivos (nome, mac_address, ip_address, localizacao, versao_firmware) VALUES
('ESP32-Sala-01', 'AA:BB:CC:DD:EE:FF', '192.168.1.100', 'Sala de Controle Principal', 'v1.2.3');
INSERT INTO dispositivos (nome, mac_address, ip_address, localizacao, versao_firmware) VALUES
('ESP32-Garagem-01', '11:22:33:44:55:66', '192.168.1.101', 'Garagem - Portão Principal', 'v1.2.3');
INSERT INTO dispositivos (nome, mac_address, ip_address, localizacao, versao_firmware) VALUES
('ESP32-Cozinha-01', '22:33:44:55:66:77', '192.168.1.102', 'Cozinha - Monitoramento', 'v1.2.3');

-- Inserir sensores para os dispositivos
INSERT INTO sensores (id_dispositivo, id_tipo_sensor, nome, pino_analogico, pino_digital) VALUES
(1, 1, 'DHT22-Temperatura', NULL, 2);
INSERT INTO sensores (id_dispositivo, id_tipo_sensor, nome, pino_analogico, pino_digital) VALUES
(1, 1, 'DHT22-Umidade', NULL, 2);
INSERT INTO sensores (id_dispositivo, id_tipo_sensor, nome, pino_analogico, pino_digital) VALUES
(1, 2, 'LDR-Luminosidade', 34, NULL);
INSERT INTO sensores (id_dispositivo, id_tipo_sensor, nome, pino_analogico, pino_digital) VALUES
(1, 3, 'PIR-Movimento', NULL, 4);
INSERT INTO sensores (id_dispositivo, id_tipo_sensor, nome, pino_analogico, pino_digital) VALUES
(1, 4, 'Pressão-Barométrica', 36, NULL);
INSERT INTO sensores (id_dispositivo, id_tipo_sensor, nome, pino_analogico, pino_digital) VALUES
(1, 5, 'Vibração-X', 39, NULL);
INSERT INTO sensores (id_dispositivo, id_tipo_sensor, nome, pino_analogico, pino_digital) VALUES
(1, 5, 'Vibração-Y', 35, NULL);
INSERT INTO sensores (id_dispositivo, id_tipo_sensor, nome, pino_analogico, pino_digital) VALUES
(1, 5, 'Vibração-Z', 32, NULL);
INSERT INTO sensores (id_dispositivo, id_tipo_sensor, nome, pino_analogico, pino_digital) VALUES
(1, 6, 'Nível-Ultrassônico', 33, NULL);

-- =====================================================
-- COMENTÁRIOS FINAIS
-- =====================================================

-- Este schema Oracle cria um banco de dados completo para monitoramento IoT
-- com suporte a:
-- - Múltiplos dispositivos ESP32
-- - Diferentes tipos de sensores
-- - Sistema de alertas configurável
-- - Logs de auditoria
-- - Dashboards personalizáveis
-- - Relatórios automáticos
-- - Views para facilitar consultas
-- - Procedures para operações complexas
-- - Triggers para atualizações automáticas
-- - Sequências para IDs únicos
-- - Índices otimizados para performance
-- - Compatível com Oracle 11g+
