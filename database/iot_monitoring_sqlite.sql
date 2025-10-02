-- =====================================================
-- SCHEMA SQLITE - SISTEMA IoT MONITORING
-- Arquivo: iot_monitoring_sqlite.sql
-- Versão: 1.0
-- Data: 2025-01-11
-- Descrição: Schema SQLite para sistema IoT
-- =====================================================

-- Configurações iniciais
PRAGMA foreign_keys = ON;
PRAGMA journal_mode = WAL;
PRAGMA synchronous = NORMAL;
PRAGMA cache_size = 1000;
PRAGMA temp_store = MEMORY;

-- =====================================================
-- TABELAS PRINCIPAIS
-- =====================================================

-- Tabela dispositivos
CREATE TABLE dispositivos (
    id_dispositivo INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    mac_address TEXT NOT NULL UNIQUE,
    ip_address TEXT,
    localizacao TEXT,
    status TEXT NOT NULL DEFAULT 'ativo' CHECK (status IN ('ativo', 'inativo', 'manutencao')),
    data_cadastro DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ultima_conexao DATETIME,
    versao_firmware TEXT,
    observacoes TEXT
);

-- Índices para dispositivos
CREATE INDEX idx_dispositivos_status ON dispositivos(status);
CREATE INDEX idx_dispositivos_localizacao ON dispositivos(localizacao);
CREATE INDEX idx_dispositivos_ultima_conexao ON dispositivos(ultima_conexao);

-- Tabela tipos_sensor
CREATE TABLE tipos_sensor (
    id_tipo_sensor INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL UNIQUE,
    descricao TEXT,
    unidade_medida TEXT,
    faixa_min REAL,
    faixa_max REAL,
    precisao REAL,
    ativo INTEGER NOT NULL DEFAULT 1 CHECK (ativo IN (0, 1)),
    data_cadastro DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Tabela sensores
CREATE TABLE sensores (
    id_sensor INTEGER PRIMARY KEY AUTOINCREMENT,
    id_dispositivo INTEGER NOT NULL,
    id_tipo_sensor INTEGER NOT NULL,
    nome TEXT NOT NULL,
    pino_analogico INTEGER,
    pino_digital INTEGER,
    calibracao_min REAL,
    calibracao_max REAL,
    status TEXT NOT NULL DEFAULT 'ativo' CHECK (status IN ('ativo', 'inativo', 'falha')),
    data_instalacao DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ultima_calibracao DATETIME,
    observacoes TEXT,
    FOREIGN KEY (id_dispositivo) REFERENCES dispositivos(id_dispositivo) ON DELETE CASCADE,
    FOREIGN KEY (id_tipo_sensor) REFERENCES tipos_sensor(id_tipo_sensor) ON DELETE CASCADE
);

-- Índices para sensores
CREATE INDEX idx_sensores_dispositivo ON sensores(id_dispositivo);
CREATE INDEX idx_sensores_tipo ON sensores(id_tipo_sensor);
CREATE INDEX idx_sensores_status ON sensores(status);

-- Tabela leituras_sensores
CREATE TABLE leituras_sensores (
    id_leitura INTEGER PRIMARY KEY AUTOINCREMENT,
    id_sensor INTEGER NOT NULL,
    timestamp_unix REAL NOT NULL,
    timestamp_datetime DATETIME NOT NULL,
    valor_numerico REAL,
    valor_booleano INTEGER CHECK (valor_booleano IN (0, 1)),
    valor_string TEXT,
    qualidade_dados TEXT NOT NULL DEFAULT 'bom' CHECK (qualidade_dados IN ('excelente', 'bom', 'regular', 'ruim')),
    anomalia_detectada INTEGER NOT NULL DEFAULT 0 CHECK (anomalia_detectada IN (0, 1)),
    data_coleta DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_sensor) REFERENCES sensores(id_sensor) ON DELETE CASCADE
);

-- Índices para leituras_sensores
CREATE INDEX idx_leituras_sensor ON leituras_sensores(id_sensor);
CREATE INDEX idx_leituras_timestamp ON leituras_sensores(timestamp_datetime);
CREATE INDEX idx_leituras_qualidade ON leituras_sensores(qualidade_dados);
CREATE INDEX idx_leituras_anomalia ON leituras_sensores(anomalia_detectada);
CREATE INDEX idx_leituras_sensor_timestamp ON leituras_sensores(id_sensor, timestamp_datetime);

-- Tabela modos_operacao
CREATE TABLE modos_operacao (
    id_modo INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL UNIQUE,
    descricao TEXT,
    cor_indicador TEXT,
    ativo INTEGER NOT NULL DEFAULT 1 CHECK (ativo IN (0, 1)),
    data_cadastro DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Tabela alertas
CREATE TABLE alertas (
    id_alerta INTEGER PRIMARY KEY AUTOINCREMENT,
    id_dispositivo INTEGER NOT NULL,
    id_sensor INTEGER,
    id_modo INTEGER NOT NULL,
    tipo_alerta TEXT NOT NULL CHECK (tipo_alerta IN ('temperatura', 'umidade', 'pressao', 'vibracao', 'nivel', 'conexao', 'geral')),
    severidade TEXT NOT NULL CHECK (severidade IN ('baixa', 'media', 'alta', 'critica')),
    titulo TEXT NOT NULL,
    descricao TEXT,
    valor_atual REAL,
    valor_limite REAL,
    timestamp_alerta DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    status TEXT NOT NULL DEFAULT 'ativo' CHECK (status IN ('ativo', 'resolvido', 'ignorado')),
    data_resolucao DATETIME,
    usuario_resolucao TEXT,
    observacoes_resolucao TEXT,
    FOREIGN KEY (id_dispositivo) REFERENCES dispositivos(id_dispositivo) ON DELETE CASCADE,
    FOREIGN KEY (id_sensor) REFERENCES sensores(id_sensor) ON DELETE SET NULL,
    FOREIGN KEY (id_modo) REFERENCES modos_operacao(id_modo) ON DELETE CASCADE
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
    id_configuracao INTEGER PRIMARY KEY AUTOINCREMENT,
    id_sensor INTEGER NOT NULL,
    tipo_limite TEXT NOT NULL CHECK (tipo_limite IN ('minimo', 'maximo', 'variacao')),
    valor_limite REAL NOT NULL,
    severidade TEXT NOT NULL CHECK (severidade IN ('baixa', 'media', 'alta', 'critica')),
    ativo INTEGER NOT NULL DEFAULT 1 CHECK (ativo IN (0, 1)),
    data_criacao DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    usuario_criacao TEXT,
    observacoes TEXT,
    FOREIGN KEY (id_sensor) REFERENCES sensores(id_sensor) ON DELETE CASCADE
);

-- Índices para configuracoes_limites
CREATE INDEX idx_configuracoes_sensor ON configuracoes_limites(id_sensor);
CREATE INDEX idx_configuracoes_tipo_limite ON configuracoes_limites(tipo_limite);
CREATE INDEX idx_configuracoes_ativo ON configuracoes_limites(ativo);

-- Tabela usuarios
CREATE TABLE usuarios (
    id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    senha_hash TEXT NOT NULL,
    perfil TEXT NOT NULL CHECK (perfil IN ('admin', 'operador', 'visualizador')),
    ativo INTEGER NOT NULL DEFAULT 1 CHECK (ativo IN (0, 1)),
    data_cadastro DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ultimo_login DATETIME,
    token_reset_senha TEXT,
    data_expiracao_token DATETIME
);

-- Índices para usuarios
CREATE INDEX idx_usuarios_perfil ON usuarios(perfil);
CREATE INDEX idx_usuarios_ativo ON usuarios(ativo);
CREATE INDEX idx_usuarios_email ON usuarios(email);

-- Tabela logs_sistema
CREATE TABLE logs_sistema (
    id_log INTEGER PRIMARY KEY AUTOINCREMENT,
    id_usuario INTEGER,
    acao TEXT NOT NULL,
    tabela_afetada TEXT,
    id_registro_afetado INTEGER,
    dados_anteriores TEXT, -- JSON armazenado como TEXT
    dados_novos TEXT, -- JSON armazenado como TEXT
    ip_origem TEXT,
    user_agent TEXT,
    timestamp_log DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE SET NULL
);

-- Índices para logs_sistema
CREATE INDEX idx_logs_usuario ON logs_sistema(id_usuario);
CREATE INDEX idx_logs_acao ON logs_sistema(acao);
CREATE INDEX idx_logs_timestamp ON logs_sistema(timestamp_log);
CREATE INDEX idx_logs_tabela ON logs_sistema(tabela_afetada);

-- Tabela dashboards
CREATE TABLE dashboards (
    id_dashboard INTEGER PRIMARY KEY AUTOINCREMENT,
    id_usuario INTEGER NOT NULL,
    nome TEXT NOT NULL,
    descricao TEXT,
    configuracoes TEXT, -- JSON armazenado como TEXT
    publico INTEGER NOT NULL DEFAULT 0 CHECK (publico IN (0, 1)),
    ativo INTEGER NOT NULL DEFAULT 1 CHECK (ativo IN (0, 1)),
    data_criacao DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE CASCADE
);

-- Índices para dashboards
CREATE INDEX idx_dashboards_usuario ON dashboards(id_usuario);
CREATE INDEX idx_dashboards_publico ON dashboards(publico);
CREATE INDEX idx_dashboards_ativo ON dashboards(ativo);

-- Tabela relatorios
CREATE TABLE relatorios (
    id_relatorio INTEGER PRIMARY KEY AUTOINCREMENT,
    id_usuario INTEGER NOT NULL,
    nome TEXT NOT NULL,
    tipo_relatorio TEXT NOT NULL CHECK (tipo_relatorio IN ('diario', 'semanal', 'mensal', 'personalizado')),
    configuracoes TEXT, -- JSON armazenado como TEXT
    frequencia TEXT,
    ativo INTEGER NOT NULL DEFAULT 1 CHECK (ativo IN (0, 1)),
    proxima_execucao DATETIME,
    data_criacao DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE CASCADE
);

-- Índices para relatorios
CREATE INDEX idx_relatorios_usuario ON relatorios(id_usuario);
CREATE INDEX idx_relatorios_tipo ON relatorios(tipo_relatorio);
CREATE INDEX idx_relatorios_proxima_execucao ON relatorios(proxima_execucao);

-- =====================================================
-- TRIGGERS
-- =====================================================

-- Trigger para atualizar data_atualizacao em configuracoes_limites
CREATE TRIGGER update_configuracoes_limites_updated_at
    AFTER UPDATE ON configuracoes_limites
    FOR EACH ROW
    WHEN NEW.data_atualizacao = OLD.data_atualizacao
BEGIN
    UPDATE configuracoes_limites 
    SET data_atualizacao = CURRENT_TIMESTAMP 
    WHERE id_configuracao = NEW.id_configuracao;
END;

-- Trigger para atualizar data_atualizacao em dashboards
CREATE TRIGGER update_dashboards_updated_at
    AFTER UPDATE ON dashboards
    FOR EACH ROW
    WHEN NEW.data_atualizacao = OLD.data_atualizacao
BEGIN
    UPDATE dashboards 
    SET data_atualizacao = CURRENT_TIMESTAMP 
    WHERE id_dashboard = NEW.id_dashboard;
END;

-- Trigger para atualizar última conexão do dispositivo
CREATE TRIGGER update_ultima_conexao
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
END;

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
-- COMENTÁRIOS FINAIS
-- =====================================================

-- Este schema SQLite cria um banco de dados completo para monitoramento IoT
-- com suporte a:
-- - Múltiplos dispositivos ESP32
-- - Diferentes tipos de sensores
-- - Sistema de alertas configurável
-- - Logs de auditoria
-- - Dashboards personalizáveis
-- - Relatórios automáticos
-- - Views para facilitar consultas
-- - Triggers para atualizações automáticas
-- - Índices otimizados para performance
-- - Compatível com SQLite 3.8+
