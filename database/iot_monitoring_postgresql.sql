-- =====================================================
-- SCHEMA POSTGRESQL - SISTEMA IoT MONITORING
-- Arquivo: iot_monitoring_postgresql.sql
-- Versão: 1.0
-- Data: 2025-01-11
-- Descrição: Schema PostgreSQL para sistema IoT
-- =====================================================

-- Configurações iniciais
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

-- Criar banco de dados
CREATE DATABASE iot_monitoring_db
    WITH 
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'pt_BR.UTF-8'
    LC_CTYPE = 'pt_BR.UTF-8'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1;

-- Conectar ao banco
\c iot_monitoring_db;

-- =====================================================
-- EXTENSÕES NECESSÁRIAS
-- =====================================================

-- Extensão para UUID
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Extensão para JSON
CREATE EXTENSION IF NOT EXISTS "btree_gin";

-- =====================================================
-- TIPOS CUSTOMIZADOS
-- =====================================================

-- Enum para status de dispositivos
CREATE TYPE status_dispositivo AS ENUM ('ativo', 'inativo', 'manutencao');

-- Enum para status de sensores
CREATE TYPE status_sensor AS ENUM ('ativo', 'inativo', 'falha');

-- Enum para qualidade de dados
CREATE TYPE qualidade_dados AS ENUM ('excelente', 'bom', 'regular', 'ruim');

-- Enum para tipos de alerta
CREATE TYPE tipo_alerta AS ENUM ('temperatura', 'umidade', 'pressao', 'vibracao', 'nivel', 'conexao', 'geral');

-- Enum para severidade
CREATE TYPE severidade AS ENUM ('baixa', 'media', 'alta', 'critica');

-- Enum para status de alerta
CREATE TYPE status_alerta AS ENUM ('ativo', 'resolvido', 'ignorado');

-- Enum para tipo de limite
CREATE TYPE tipo_limite AS ENUM ('minimo', 'maximo', 'variacao');

-- Enum para perfil de usuário
CREATE TYPE perfil_usuario AS ENUM ('admin', 'operador', 'visualizador');

-- Enum para tipo de relatório
CREATE TYPE tipo_relatorio AS ENUM ('diario', 'semanal', 'mensal', 'personalizado');

-- =====================================================
-- TABELAS PRINCIPAIS
-- =====================================================

-- Tabela dispositivos
CREATE TABLE dispositivos (
    id_dispositivo SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    mac_address VARCHAR(17) NOT NULL UNIQUE,
    ip_address INET,
    localizacao VARCHAR(200),
    status status_dispositivo NOT NULL DEFAULT 'ativo',
    data_cadastro TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    ultima_conexao TIMESTAMP WITH TIME ZONE,
    versao_firmware VARCHAR(20),
    observacoes TEXT
);

-- Índices para dispositivos
CREATE INDEX idx_dispositivos_status ON dispositivos(status);
CREATE INDEX idx_dispositivos_localizacao ON dispositivos(localizacao);
CREATE INDEX idx_dispositivos_ultima_conexao ON dispositivos(ultima_conexao);

-- Tabela tipos_sensor
CREATE TABLE tipos_sensor (
    id_tipo_sensor SERIAL PRIMARY KEY,
    nome VARCHAR(50) NOT NULL UNIQUE,
    descricao TEXT,
    unidade_medida VARCHAR(20),
    faixa_min DECIMAL(10,3),
    faixa_max DECIMAL(10,3),
    precisao DECIMAL(8,3),
    ativo BOOLEAN NOT NULL DEFAULT TRUE,
    data_cadastro TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

-- Tabela sensores
CREATE TABLE sensores (
    id_sensor SERIAL PRIMARY KEY,
    id_dispositivo INTEGER NOT NULL REFERENCES dispositivos(id_dispositivo) ON DELETE CASCADE,
    id_tipo_sensor INTEGER NOT NULL REFERENCES tipos_sensor(id_tipo_sensor) ON DELETE CASCADE,
    nome VARCHAR(100) NOT NULL,
    pino_analogico INTEGER,
    pino_digital INTEGER,
    calibracao_min DECIMAL(10,3),
    calibracao_max DECIMAL(10,3),
    status status_sensor NOT NULL DEFAULT 'ativo',
    data_instalacao TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    ultima_calibracao TIMESTAMP WITH TIME ZONE,
    observacoes TEXT
);

-- Índices para sensores
CREATE INDEX idx_sensores_dispositivo ON sensores(id_dispositivo);
CREATE INDEX idx_sensores_tipo ON sensores(id_tipo_sensor);
CREATE INDEX idx_sensores_status ON sensores(status);

-- Tabela leituras_sensores (com particionamento)
CREATE TABLE leituras_sensores (
    id_leitura BIGSERIAL,
    id_sensor INTEGER NOT NULL REFERENCES sensores(id_sensor) ON DELETE CASCADE,
    timestamp_unix DECIMAL(15,3) NOT NULL,
    timestamp_datetime TIMESTAMP WITH TIME ZONE NOT NULL,
    valor_numerico DECIMAL(12,6),
    valor_booleano BOOLEAN,
    valor_string VARCHAR(255),
    qualidade_dados qualidade_dados NOT NULL DEFAULT 'bom',
    anomalia_detectada BOOLEAN NOT NULL DEFAULT FALSE,
    data_coleta TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    PRIMARY KEY (id_leitura, timestamp_datetime)
) PARTITION BY RANGE (timestamp_datetime);

-- Partições para leituras_sensores
CREATE TABLE leituras_sensores_2024 PARTITION OF leituras_sensores
    FOR VALUES FROM ('2024-01-01') TO ('2025-01-01');

CREATE TABLE leituras_sensores_2025 PARTITION OF leituras_sensores
    FOR VALUES FROM ('2025-01-01') TO ('2026-01-01');

CREATE TABLE leituras_sensores_2026 PARTITION OF leituras_sensores
    FOR VALUES FROM ('2026-01-01') TO ('2027-01-01');

CREATE TABLE leituras_sensores_future PARTITION OF leituras_sensores
    FOR VALUES FROM ('2027-01-01') TO (MAXVALUE);

-- Índices para leituras_sensores
CREATE INDEX idx_leituras_sensor ON leituras_sensores(id_sensor);
CREATE INDEX idx_leituras_timestamp ON leituras_sensores(timestamp_datetime);
CREATE INDEX idx_leituras_qualidade ON leituras_sensores(qualidade_dados);
CREATE INDEX idx_leituras_anomalia ON leituras_sensores(anomalia_detectada);
CREATE INDEX idx_leituras_sensor_timestamp ON leituras_sensores(id_sensor, timestamp_datetime);

-- Tabela modos_operacao
CREATE TABLE modos_operacao (
    id_modo SERIAL PRIMARY KEY,
    nome VARCHAR(50) NOT NULL UNIQUE,
    descricao TEXT,
    cor_indicador VARCHAR(7),
    ativo BOOLEAN NOT NULL DEFAULT TRUE,
    data_cadastro TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

-- Tabela alertas
CREATE TABLE alertas (
    id_alerta BIGSERIAL PRIMARY KEY,
    id_dispositivo INTEGER NOT NULL REFERENCES dispositivos(id_dispositivo) ON DELETE CASCADE,
    id_sensor INTEGER REFERENCES sensores(id_sensor) ON DELETE SET NULL,
    id_modo INTEGER NOT NULL REFERENCES modos_operacao(id_modo) ON DELETE CASCADE,
    tipo_alerta tipo_alerta NOT NULL,
    severidade severidade NOT NULL,
    titulo VARCHAR(200) NOT NULL,
    descricao TEXT,
    valor_atual DECIMAL(12,6),
    valor_limite DECIMAL(12,6),
    timestamp_alerta TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    status status_alerta NOT NULL DEFAULT 'ativo',
    data_resolucao TIMESTAMP WITH TIME ZONE,
    usuario_resolucao VARCHAR(100),
    observacoes_resolucao TEXT
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
    id_configuracao SERIAL PRIMARY KEY,
    id_sensor INTEGER NOT NULL REFERENCES sensores(id_sensor) ON DELETE CASCADE,
    tipo_limite tipo_limite NOT NULL,
    valor_limite DECIMAL(12,6) NOT NULL,
    severidade severidade NOT NULL,
    ativo BOOLEAN NOT NULL DEFAULT TRUE,
    data_criacao TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    data_atualizacao TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    usuario_criacao VARCHAR(100),
    observacoes TEXT
);

-- Índices para configuracoes_limites
CREATE INDEX idx_configuracoes_sensor ON configuracoes_limites(id_sensor);
CREATE INDEX idx_configuracoes_tipo_limite ON configuracoes_limites(tipo_limite);
CREATE INDEX idx_configuracoes_ativo ON configuracoes_limites(ativo);

-- Tabela usuarios
CREATE TABLE usuarios (
    id_usuario SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    senha_hash VARCHAR(255) NOT NULL,
    perfil perfil_usuario NOT NULL,
    ativo BOOLEAN NOT NULL DEFAULT TRUE,
    data_cadastro TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    ultimo_login TIMESTAMP WITH TIME ZONE,
    token_reset_senha VARCHAR(255),
    data_expiracao_token TIMESTAMP WITH TIME ZONE
);

-- Índices para usuarios
CREATE INDEX idx_usuarios_perfil ON usuarios(perfil);
CREATE INDEX idx_usuarios_ativo ON usuarios(ativo);
CREATE INDEX idx_usuarios_email ON usuarios(email);

-- Tabela logs_sistema
CREATE TABLE logs_sistema (
    id_log BIGSERIAL PRIMARY KEY,
    id_usuario INTEGER REFERENCES usuarios(id_usuario) ON DELETE SET NULL,
    acao VARCHAR(100) NOT NULL,
    tabela_afetada VARCHAR(50),
    id_registro_afetado BIGINT,
    dados_anteriores JSONB,
    dados_novos JSONB,
    ip_origem INET,
    user_agent TEXT,
    timestamp_log TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

-- Índices para logs_sistema
CREATE INDEX idx_logs_usuario ON logs_sistema(id_usuario);
CREATE INDEX idx_logs_acao ON logs_sistema(acao);
CREATE INDEX idx_logs_timestamp ON logs_sistema(timestamp_log);
CREATE INDEX idx_logs_tabela ON logs_sistema(tabela_afetada);
CREATE INDEX idx_logs_dados_anteriores ON logs_sistema USING GIN (dados_anteriores);
CREATE INDEX idx_logs_dados_novos ON logs_sistema USING GIN (dados_novos);

-- Tabela dashboards
CREATE TABLE dashboards (
    id_dashboard SERIAL PRIMARY KEY,
    id_usuario INTEGER NOT NULL REFERENCES usuarios(id_usuario) ON DELETE CASCADE,
    nome VARCHAR(100) NOT NULL,
    descricao TEXT,
    configuracoes JSONB,
    publico BOOLEAN NOT NULL DEFAULT FALSE,
    ativo BOOLEAN NOT NULL DEFAULT TRUE,
    data_criacao TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    data_atualizacao TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

-- Índices para dashboards
CREATE INDEX idx_dashboards_usuario ON dashboards(id_usuario);
CREATE INDEX idx_dashboards_publico ON dashboards(publico);
CREATE INDEX idx_dashboards_ativo ON dashboards(ativo);
CREATE INDEX idx_dashboards_configuracoes ON dashboards USING GIN (configuracoes);

-- Tabela relatorios
CREATE TABLE relatorios (
    id_relatorio SERIAL PRIMARY KEY,
    id_usuario INTEGER NOT NULL REFERENCES usuarios(id_usuario) ON DELETE CASCADE,
    nome VARCHAR(100) NOT NULL,
    tipo_relatorio tipo_relatorio NOT NULL,
    configuracoes JSONB,
    frequencia VARCHAR(50),
    ativo BOOLEAN NOT NULL DEFAULT TRUE,
    proxima_execucao TIMESTAMP WITH TIME ZONE,
    data_criacao TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

-- Índices para relatorios
CREATE INDEX idx_relatorios_usuario ON relatorios(id_usuario);
CREATE INDEX idx_relatorios_tipo ON relatorios(tipo_relatorio);
CREATE INDEX idx_relatorios_proxima_execucao ON relatorios(proxima_execucao);
CREATE INDEX idx_relatorios_configuracoes ON relatorios USING GIN (configuracoes);

-- =====================================================
-- TRIGGERS E FUNÇÕES
-- =====================================================

-- Função para atualizar data_atualizacao
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.data_atualizacao = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Trigger para configuracoes_limites
CREATE TRIGGER update_configuracoes_limites_updated_at
    BEFORE UPDATE ON configuracoes_limites
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Trigger para dashboards
CREATE TRIGGER update_dashboards_updated_at
    BEFORE UPDATE ON dashboards
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Função para atualizar última conexão
CREATE OR REPLACE FUNCTION update_ultima_conexao()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE dispositivos 
    SET ultima_conexao = NOW()
    WHERE id_dispositivo = (
        SELECT id_dispositivo 
        FROM sensores 
        WHERE id_sensor = NEW.id_sensor
    );
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Trigger para leituras_sensores
CREATE TRIGGER update_ultima_conexao_trigger
    AFTER INSERT ON leituras_sensores
    FOR EACH ROW
    EXECUTE FUNCTION update_ultima_conexao();

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
LEFT JOIN modos_operacao mo ON ls.qualidade_dados::text = mo.nome;

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
-- FUNÇÕES STORED
-- =====================================================

-- Função para inserir leitura
CREATE OR REPLACE FUNCTION sp_inserir_leitura(
    p_id_sensor INTEGER,
    p_timestamp_unix DECIMAL(15,3),
    p_valor_numerico DECIMAL(12,6),
    p_valor_booleano BOOLEAN,
    p_valor_string VARCHAR(255),
    p_qualidade_dados qualidade_dados
)
RETURNS BIGINT AS $$
DECLARE
    v_id_leitura BIGINT;
    v_timestamp_datetime TIMESTAMP WITH TIME ZONE;
    v_anomalia BOOLEAN := FALSE;
BEGIN
    -- Converte timestamp unix para datetime
    v_timestamp_datetime := to_timestamp(p_timestamp_unix);
    
    -- Verifica se há anomalia baseada na qualidade dos dados
    IF p_qualidade_dados IN ('regular', 'ruim') THEN
        v_anomalia := TRUE;
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
    ) RETURNING id_leitura INTO v_id_leitura;
    
    -- Retorna o ID da leitura inserida
    RETURN v_id_leitura;
END;
$$ LANGUAGE plpgsql;

-- Função para verificar limites
CREATE OR REPLACE FUNCTION sp_verificar_limites(
    p_id_sensor INTEGER, 
    p_valor DECIMAL(12,6)
)
RETURNS VOID AS $$
DECLARE
    v_limite_max DECIMAL(12,6);
    v_limite_min DECIMAL(12,6);
    v_severidade_max severidade;
    v_severidade_min severidade;
    v_id_dispositivo INTEGER;
    v_tipo_sensor VARCHAR(50);
BEGIN
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
    ORDER BY 
        CASE severidade 
            WHEN 'critica' THEN 4
            WHEN 'alta' THEN 3
            WHEN 'media' THEN 2
            WHEN 'baixa' THEN 1
        END DESC
    LIMIT 1;
    
    -- Verifica limite mínimo
    SELECT valor_limite, severidade
    INTO v_limite_min, v_severidade_min
    FROM configuracoes_limites
    WHERE id_sensor = p_id_sensor 
    AND tipo_limite = 'minimo' 
    AND ativo = TRUE
    ORDER BY 
        CASE severidade 
            WHEN 'critica' THEN 4
            WHEN 'alta' THEN 3
            WHEN 'media' THEN 2
            WHEN 'baixa' THEN 1
        END DESC
    LIMIT 1;
    
    -- Cria alerta se excedeu limite máximo
    IF v_limite_max IS NOT NULL AND p_valor > v_limite_max THEN
        INSERT INTO alertas (
            id_dispositivo, id_sensor, id_modo, tipo_alerta, severidade,
            titulo, descricao, valor_atual, valor_limite
        ) VALUES (
            v_id_dispositivo, p_id_sensor, 2, -- Modo de falha
            v_tipo_sensor::tipo_alerta, v_severidade_max,
            'Valor excedeu limite máximo: ' || v_tipo_sensor,
            'Valor atual: ' || p_valor || ' | Limite: ' || v_limite_max,
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
            v_tipo_sensor::tipo_alerta, v_severidade_min,
            'Valor abaixo do limite mínimo: ' || v_tipo_sensor,
            'Valor atual: ' || p_valor || ' | Limite: ' || v_limite_min,
            p_valor, v_limite_min
        );
    END IF;
END;
$$ LANGUAGE plpgsql;

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
-- COMENTÁRIOS FINAIS
-- =====================================================

-- Este schema PostgreSQL cria um banco de dados completo para monitoramento IoT
-- com suporte a:
-- - Múltiplos dispositivos ESP32
-- - Diferentes tipos de sensores
-- - Sistema de alertas configurável
-- - Logs de auditoria
-- - Dashboards personalizáveis
-- - Relatórios automáticos
-- - Particionamento de dados por ano
-- - Views para facilitar consultas
-- - Funções stored para operações complexas
-- - Triggers para atualizações automáticas
-- - Tipos customizados para melhor integridade
-- - Índices otimizados para performance
