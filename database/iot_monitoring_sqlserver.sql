-- =====================================================
-- SCHEMA SQL SERVER - SISTEMA IoT MONITORING
-- Arquivo: iot_monitoring_sqlserver.sql
-- Versão: 1.0
-- Data: 2025-01-11
-- Descrição: Schema SQL Server para sistema IoT
-- =====================================================

-- Configurações iniciais
SET ANSI_NULLS ON;
SET QUOTED_IDENTIFIER ON;
SET ANSI_PADDING ON;

-- =====================================================
-- TABELAS PRINCIPAIS
-- =====================================================

-- Tabela dispositivos
CREATE TABLE dispositivos (
    id_dispositivo INT IDENTITY(1,1) PRIMARY KEY,
    nome NVARCHAR(100) NOT NULL,
    mac_address NVARCHAR(17) NOT NULL,
    ip_address NVARCHAR(15) NULL,
    localizacao NVARCHAR(200) NULL,
    status NVARCHAR(20) NOT NULL DEFAULT 'ativo' CHECK (status IN ('ativo', 'inativo', 'manutencao')),
    data_cadastro DATETIME2 NOT NULL DEFAULT GETDATE(),
    ultima_conexao DATETIME2 NULL,
    versao_firmware NVARCHAR(20) NULL,
    observacoes NVARCHAR(MAX) NULL
);

-- Índices para dispositivos
CREATE UNIQUE INDEX uk_dispositivos_mac_address ON dispositivos(mac_address);
CREATE INDEX idx_dispositivos_status ON dispositivos(status);
CREATE INDEX idx_dispositivos_localizacao ON dispositivos(localizacao);
CREATE INDEX idx_dispositivos_ultima_conexao ON dispositivos(ultima_conexao);

-- Tabela tipos_sensor
CREATE TABLE tipos_sensor (
    id_tipo_sensor INT IDENTITY(1,1) PRIMARY KEY,
    nome NVARCHAR(50) NOT NULL,
    descricao NVARCHAR(MAX) NULL,
    unidade_medida NVARCHAR(20) NULL,
    faixa_min DECIMAL(10,3) NULL,
    faixa_max DECIMAL(10,3) NULL,
    precisao DECIMAL(8,3) NULL,
    ativo BIT NOT NULL DEFAULT 1,
    data_cadastro DATETIME2 NOT NULL DEFAULT GETDATE()
);

-- Índices para tipos_sensor
CREATE UNIQUE INDEX uk_tipos_sensor_nome ON tipos_sensor(nome);
CREATE INDEX idx_tipos_sensor_ativo ON tipos_sensor(ativo);

-- Tabela sensores
CREATE TABLE sensores (
    id_sensor INT IDENTITY(1,1) PRIMARY KEY,
    id_dispositivo INT NOT NULL,
    id_tipo_sensor INT NOT NULL,
    nome NVARCHAR(100) NOT NULL,
    pino_analogico INT NULL,
    pino_digital INT NULL,
    calibracao_min DECIMAL(10,3) NULL,
    calibracao_max DECIMAL(10,3) NULL,
    status NVARCHAR(20) NOT NULL DEFAULT 'ativo' CHECK (status IN ('ativo', 'inativo', 'falha')),
    data_instalacao DATETIME2 NOT NULL DEFAULT GETDATE(),
    ultima_calibracao DATETIME2 NULL,
    observacoes NVARCHAR(MAX) NULL,
    CONSTRAINT fk_sensores_dispositivos FOREIGN KEY (id_dispositivo) REFERENCES dispositivos(id_dispositivo) ON DELETE CASCADE,
    CONSTRAINT fk_sensores_tipos_sensor FOREIGN KEY (id_tipo_sensor) REFERENCES tipos_sensor(id_tipo_sensor) ON DELETE CASCADE
);

-- Índices para sensores
CREATE INDEX idx_sensores_dispositivo ON sensores(id_dispositivo);
CREATE INDEX idx_sensores_tipo ON sensores(id_tipo_sensor);
CREATE INDEX idx_sensores_status ON sensores(status);

-- Tabela leituras_sensores
CREATE TABLE leituras_sensores (
    id_leitura BIGINT IDENTITY(1,1) PRIMARY KEY,
    id_sensor INT NOT NULL,
    timestamp_unix DECIMAL(15,3) NOT NULL,
    timestamp_datetime DATETIME2 NOT NULL,
    valor_numerico DECIMAL(12,6) NULL,
    valor_booleano BIT NULL,
    valor_string NVARCHAR(255) NULL,
    qualidade_dados NVARCHAR(20) NOT NULL DEFAULT 'bom' CHECK (qualidade_dados IN ('excelente', 'bom', 'regular', 'ruim')),
    anomalia_detectada BIT NOT NULL DEFAULT 0,
    data_coleta DATETIME2 NOT NULL DEFAULT GETDATE(),
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
    id_modo INT IDENTITY(1,1) PRIMARY KEY,
    nome NVARCHAR(50) NOT NULL,
    descricao NVARCHAR(MAX) NULL,
    cor_indicador NVARCHAR(7) NULL,
    ativo BIT NOT NULL DEFAULT 1,
    data_cadastro DATETIME2 NOT NULL DEFAULT GETDATE()
);

-- Índices para modos_operacao
CREATE UNIQUE INDEX uk_modos_operacao_nome ON modos_operacao(nome);
CREATE INDEX idx_modos_operacao_ativo ON modos_operacao(ativo);

-- Tabela alertas
CREATE TABLE alertas (
    id_alerta BIGINT IDENTITY(1,1) PRIMARY KEY,
    id_dispositivo INT NOT NULL,
    id_sensor INT NULL,
    id_modo INT NOT NULL,
    tipo_alerta NVARCHAR(20) NOT NULL CHECK (tipo_alerta IN ('temperatura', 'umidade', 'pressao', 'vibracao', 'nivel', 'conexao', 'geral')),
    severidade NVARCHAR(20) NOT NULL CHECK (severidade IN ('baixa', 'media', 'alta', 'critica')),
    titulo NVARCHAR(200) NOT NULL,
    descricao NVARCHAR(MAX) NULL,
    valor_atual DECIMAL(12,6) NULL,
    valor_limite DECIMAL(12,6) NULL,
    timestamp_alerta DATETIME2 NOT NULL DEFAULT GETDATE(),
    status NVARCHAR(20) NOT NULL DEFAULT 'ativo' CHECK (status IN ('ativo', 'resolvido', 'ignorado')),
    data_resolucao DATETIME2 NULL,
    usuario_resolucao NVARCHAR(100) NULL,
    observacoes_resolucao NVARCHAR(MAX) NULL,
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
    id_configuracao INT IDENTITY(1,1) PRIMARY KEY,
    id_sensor INT NOT NULL,
    tipo_limite NVARCHAR(20) NOT NULL CHECK (tipo_limite IN ('minimo', 'maximo', 'variacao')),
    valor_limite DECIMAL(12,6) NOT NULL,
    severidade NVARCHAR(20) NOT NULL CHECK (severidade IN ('baixa', 'media', 'alta', 'critica')),
    ativo BIT NOT NULL DEFAULT 1,
    data_criacao DATETIME2 NOT NULL DEFAULT GETDATE(),
    data_atualizacao DATETIME2 NOT NULL DEFAULT GETDATE(),
    usuario_criacao NVARCHAR(100) NULL,
    observacoes NVARCHAR(MAX) NULL,
    CONSTRAINT fk_configuracoes_limites_sensores FOREIGN KEY (id_sensor) REFERENCES sensores(id_sensor) ON DELETE CASCADE
);

-- Índices para configuracoes_limites
CREATE INDEX idx_configuracoes_sensor ON configuracoes_limites(id_sensor);
CREATE INDEX idx_configuracoes_tipo_limite ON configuracoes_limites(tipo_limite);
CREATE INDEX idx_configuracoes_ativo ON configuracoes_limites(ativo);

-- Tabela usuarios
CREATE TABLE usuarios (
    id_usuario INT IDENTITY(1,1) PRIMARY KEY,
    nome NVARCHAR(100) NOT NULL,
    email NVARCHAR(255) NOT NULL,
    senha_hash NVARCHAR(255) NOT NULL,
    perfil NVARCHAR(20) NOT NULL CHECK (perfil IN ('admin', 'operador', 'visualizador')),
    ativo BIT NOT NULL DEFAULT 1,
    data_cadastro DATETIME2 NOT NULL DEFAULT GETDATE(),
    ultimo_login DATETIME2 NULL,
    token_reset_senha NVARCHAR(255) NULL,
    data_expiracao_token DATETIME2 NULL
);

-- Índices para usuarios
CREATE UNIQUE INDEX uk_usuarios_email ON usuarios(email);
CREATE INDEX idx_usuarios_perfil ON usuarios(perfil);
CREATE INDEX idx_usuarios_ativo ON usuarios(ativo);

-- Tabela logs_sistema
CREATE TABLE logs_sistema (
    id_log BIGINT IDENTITY(1,1) PRIMARY KEY,
    id_usuario INT NULL,
    acao NVARCHAR(100) NOT NULL,
    tabela_afetada NVARCHAR(50) NULL,
    id_registro_afetado BIGINT NULL,
    dados_anteriores NVARCHAR(MAX) NULL, -- JSON armazenado como NVARCHAR(MAX)
    dados_novos NVARCHAR(MAX) NULL, -- JSON armazenado como NVARCHAR(MAX)
    ip_origem NVARCHAR(45) NULL,
    user_agent NVARCHAR(MAX) NULL,
    timestamp_log DATETIME2 NOT NULL DEFAULT GETDATE(),
    CONSTRAINT fk_logs_sistema_usuarios FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE SET NULL
);

-- Índices para logs_sistema
CREATE INDEX idx_logs_usuario ON logs_sistema(id_usuario);
CREATE INDEX idx_logs_acao ON logs_sistema(acao);
CREATE INDEX idx_logs_timestamp ON logs_sistema(timestamp_log);
CREATE INDEX idx_logs_tabela ON logs_sistema(tabela_afetada);

-- Tabela dashboards
CREATE TABLE dashboards (
    id_dashboard INT IDENTITY(1,1) PRIMARY KEY,
    id_usuario INT NOT NULL,
    nome NVARCHAR(100) NOT NULL,
    descricao NVARCHAR(MAX) NULL,
    configuracoes NVARCHAR(MAX) NULL, -- JSON armazenado como NVARCHAR(MAX)
    publico BIT NOT NULL DEFAULT 0,
    ativo BIT NOT NULL DEFAULT 1,
    data_criacao DATETIME2 NOT NULL DEFAULT GETDATE(),
    data_atualizacao DATETIME2 NOT NULL DEFAULT GETDATE(),
    CONSTRAINT fk_dashboards_usuarios FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE CASCADE
);

-- Índices para dashboards
CREATE INDEX idx_dashboards_usuario ON dashboards(id_usuario);
CREATE INDEX idx_dashboards_publico ON dashboards(publico);
CREATE INDEX idx_dashboards_ativo ON dashboards(ativo);

-- Tabela relatorios
CREATE TABLE relatorios (
    id_relatorio INT IDENTITY(1,1) PRIMARY KEY,
    id_usuario INT NOT NULL,
    nome NVARCHAR(100) NOT NULL,
    tipo_relatorio NVARCHAR(20) NOT NULL CHECK (tipo_relatorio IN ('diario', 'semanal', 'mensal', 'personalizado')),
    configuracoes NVARCHAR(MAX) NULL, -- JSON armazenado como NVARCHAR(MAX)
    frequencia NVARCHAR(50) NULL,
    ativo BIT NOT NULL DEFAULT 1,
    proxima_execucao DATETIME2 NULL,
    data_criacao DATETIME2 NOT NULL DEFAULT GETDATE(),
    CONSTRAINT fk_relatorios_usuarios FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE CASCADE
);

-- Índices para relatorios
CREATE INDEX idx_relatorios_usuario ON relatorios(id_usuario);
CREATE INDEX idx_relatorios_tipo ON relatorios(tipo_relatorio);
CREATE INDEX idx_relatorios_proxima_execucao ON relatorios(proxima_execucao);

-- =====================================================
-- TRIGGERS
-- =====================================================

-- Trigger para atualizar data_atualizacao em configuracoes_limites
CREATE TRIGGER tr_configuracoes_limites_updated_at
    ON configuracoes_limites
    AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;
    
    UPDATE configuracoes_limites 
    SET data_atualizacao = GETDATE()
    FROM configuracoes_limites cl
    INNER JOIN inserted i ON cl.id_configuracao = i.id_configuracao
    WHERE cl.data_atualizacao = i.data_atualizacao;
END;
GO

-- Trigger para atualizar data_atualizacao em dashboards
CREATE TRIGGER tr_dashboards_updated_at
    ON dashboards
    AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;
    
    UPDATE dashboards 
    SET data_atualizacao = GETDATE()
    FROM dashboards d
    INNER JOIN inserted i ON d.id_dashboard = i.id_dashboard
    WHERE d.data_atualizacao = i.data_atualizacao;
END;
GO

-- Trigger para atualizar última conexão do dispositivo
CREATE TRIGGER tr_update_ultima_conexao
    ON leituras_sensores
    AFTER INSERT
AS
BEGIN
    SET NOCOUNT ON;
    
    UPDATE d
    SET ultima_conexao = GETDATE()
    FROM dispositivos d
    INNER JOIN sensores s ON d.id_dispositivo = s.id_dispositivo
    INNER JOIN inserted i ON s.id_sensor = i.id_sensor;
END;
GO

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
GO

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
GO

-- =====================================================
-- STORED PROCEDURES
-- =====================================================

-- Procedure para inserir leitura
CREATE PROCEDURE sp_inserir_leitura
    @id_sensor INT,
    @timestamp_unix DECIMAL(15,3),
    @valor_numerico DECIMAL(12,6) = NULL,
    @valor_booleano BIT = NULL,
    @valor_string NVARCHAR(255) = NULL,
    @qualidade_dados NVARCHAR(20) = 'bom',
    @id_leitura BIGINT OUTPUT
AS
BEGIN
    SET NOCOUNT ON;
    
    DECLARE @timestamp_datetime DATETIME2;
    DECLARE @anomalia BIT = 0;
    
    -- Converte timestamp unix para datetime
    SET @timestamp_datetime = DATEADD(SECOND, @timestamp_unix, '1970-01-01 00:00:00');
    
    -- Verifica se há anomalia baseada na qualidade dos dados
    IF @qualidade_dados IN ('regular', 'ruim')
        SET @anomalia = 1;
    
    -- Insere a leitura
    INSERT INTO leituras_sensores (
        id_sensor, timestamp_unix, timestamp_datetime, 
        valor_numerico, valor_booleano, valor_string, 
        qualidade_dados, anomalia_detectada
    ) VALUES (
        @id_sensor, @timestamp_unix, @timestamp_datetime,
        @valor_numerico, @valor_booleano, @valor_string,
        @qualidade_dados, @anomalia
    );
    
    -- Retorna o ID da leitura inserida
    SET @id_leitura = SCOPE_IDENTITY();
END;
GO

-- Procedure para verificar limites
CREATE PROCEDURE sp_verificar_limites
    @id_sensor INT,
    @valor DECIMAL(12,6)
AS
BEGIN
    SET NOCOUNT ON;
    
    DECLARE @limite_max DECIMAL(12,6);
    DECLARE @limite_min DECIMAL(12,6);
    DECLARE @severidade_max NVARCHAR(20);
    DECLARE @severidade_min NVARCHAR(20);
    DECLARE @id_dispositivo INT;
    DECLARE @tipo_sensor NVARCHAR(50);
    
    -- Obtém informações do sensor
    SELECT @id_dispositivo = s.id_dispositivo, @tipo_sensor = ts.nome
    FROM sensores s
    JOIN tipos_sensor ts ON s.id_tipo_sensor = ts.id_tipo_sensor
    WHERE s.id_sensor = @id_sensor;
    
    -- Verifica limite máximo
    SELECT TOP 1 @limite_max = valor_limite, @severidade_max = severidade
    FROM configuracoes_limites
    WHERE id_sensor = @id_sensor 
    AND tipo_limite = 'maximo' 
    AND ativo = 1
    ORDER BY 
        CASE severidade 
            WHEN 'critica' THEN 4
            WHEN 'alta' THEN 3
            WHEN 'media' THEN 2
            WHEN 'baixa' THEN 1
        END DESC;
    
    -- Verifica limite mínimo
    SELECT TOP 1 @limite_min = valor_limite, @severidade_min = severidade
    FROM configuracoes_limites
    WHERE id_sensor = @id_sensor 
    AND tipo_limite = 'minimo' 
    AND ativo = 1
    ORDER BY 
        CASE severidade 
            WHEN 'critica' THEN 4
            WHEN 'alta' THEN 3
            WHEN 'media' THEN 2
            WHEN 'baixa' THEN 1
        END DESC;
    
    -- Cria alerta se excedeu limite máximo
    IF @limite_max IS NOT NULL AND @valor > @limite_max
    BEGIN
        INSERT INTO alertas (
            id_dispositivo, id_sensor, id_modo, tipo_alerta, severidade,
            titulo, descricao, valor_atual, valor_limite
        ) VALUES (
            @id_dispositivo, @id_sensor, 2, -- Modo de falha
            @tipo_sensor, @severidade_max,
            'Valor excedeu limite máximo: ' + @tipo_sensor,
            'Valor atual: ' + CAST(@valor AS NVARCHAR(20)) + ' | Limite: ' + CAST(@limite_max AS NVARCHAR(20)),
            @valor, @limite_max
        );
    END;
    
    -- Cria alerta se excedeu limite mínimo
    IF @limite_min IS NOT NULL AND @valor < @limite_min
    BEGIN
        INSERT INTO alertas (
            id_dispositivo, id_sensor, id_modo, tipo_alerta, severidade,
            titulo, descricao, valor_atual, valor_limite
        ) VALUES (
            @id_dispositivo, @id_sensor, 2, -- Modo de falha
            @tipo_sensor, @severidade_min,
            'Valor abaixo do limite mínimo: ' + @tipo_sensor,
            'Valor atual: ' + CAST(@valor AS NVARCHAR(20)) + ' | Limite: ' + CAST(@limite_min AS NVARCHAR(20)),
            @valor, @limite_min
        );
    END;
END;
GO

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

-- Este schema SQL Server cria um banco de dados completo para monitoramento IoT
-- com suporte a:
-- - Múltiplos dispositivos ESP32
-- - Diferentes tipos de sensores
-- - Sistema de alertas configurável
-- - Logs de auditoria
-- - Dashboards personalizáveis
-- - Relatórios automáticos
-- - Views para facilitar consultas
-- - Stored procedures para operações complexas
-- - Triggers para atualizações automáticas
-- - Índices otimizados para performance
-- - Compatível com SQL Server 2012+
