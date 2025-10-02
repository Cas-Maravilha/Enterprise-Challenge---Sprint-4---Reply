@echo off
REM =====================================================
REM SCRIPT BATCH - EXECUÇÃO DA CRIAÇÃO DO BANCO
REM Sistema IoT Monitoring - Sprint 3
REM Arquivo: executar_criacao_banco.bat
REM Versão: 1.0
REM Data: 2025-01-11
REM =====================================================

echo.
echo =====================================================
echo SISTEMA IoT MONITORING - CRIACAO DO BANCO DE DADOS
echo =====================================================
echo.

REM Verificar se o MySQL está instalado
mysql --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERRO: MySQL nao encontrado!
    echo Por favor, instale o MySQL e adicione ao PATH
    pause
    exit /b 1
)

echo MySQL encontrado! Versao:
mysql --version
echo.

REM Solicitar credenciais do MySQL
set /p MYSQL_USER="Usuario MySQL (padrao: root): "
if "%MYSQL_USER%"=="" set MYSQL_USER=root

set /p MYSQL_PASSWORD="Senha MySQL: "
if "%MYSQL_PASSWORD%"=="" (
    echo Executando sem senha...
    set MYSQL_CMD=mysql -u %MYSQL_USER%
) else (
    set MYSQL_CMD=mysql -u %MYSQL_USER% -p%MYSQL_PASSWORD%
)

echo.
echo =====================================================
echo EXECUTANDO CRIACAO DAS TABELAS
echo =====================================================
echo.

REM Executar script de criação das tabelas
echo Executando: criar_tabelas_iot.sql
%MYSQL_CMD% < database\criar_tabelas_iot.sql
if %errorlevel% neq 0 (
    echo ERRO: Falha ao executar criar_tabelas_iot.sql
    pause
    exit /b 1
)

echo.
echo =====================================================
echo EXECUTANDO INSERCAO DE DADOS DE EXEMPLO
echo =====================================================
echo.

REM Executar script de inserção de dados
echo Executando: inserir_dados_exemplo.sql
%MYSQL_CMD% < database\inserir_dados_exemplo.sql
if %errorlevel% neq 0 (
    echo ERRO: Falha ao executar inserir_dados_exemplo.sql
    pause
    exit /b 1
)

echo.
echo =====================================================
echo VERIFICANDO CRIACAO DO BANCO
echo =====================================================
echo.

REM Verificar se as tabelas foram criadas
echo Verificando tabelas criadas...
%MYSQL_CMD% -e "USE iot_monitoring_db; SHOW TABLES;"

echo.
echo =====================================================
echo VERIFICANDO DADOS INSERIDOS
echo =====================================================
echo.

REM Verificar contagem de registros
echo Contando registros inseridos...
%MYSQL_CMD% -e "USE iot_monitoring_db; SELECT 'Dispositivos' as Tabela, COUNT(*) as Registros FROM dispositivos UNION ALL SELECT 'Sensores', COUNT(*) FROM sensores UNION ALL SELECT 'Tipos Sensor', COUNT(*) FROM tipos_sensor UNION ALL SELECT 'Usuarios', COUNT(*) FROM usuarios UNION ALL SELECT 'Alertas', COUNT(*) FROM alertas UNION ALL SELECT 'Leituras', COUNT(*) FROM leituras_sensores;"

echo.
echo =====================================================
echo SUCESSO!
echo =====================================================
echo.
echo Banco de dados 'iot_monitoring_db' criado com sucesso!
echo.
echo Tabelas criadas:
echo - dispositivos
echo - tipos_sensor
echo - sensores
echo - leituras_sensores
echo - modos_operacao
echo - alertas
echo - configuracoes_limites
echo - usuarios
echo - logs_sistema
echo - dashboards
echo - relatorios
echo.
echo Dados de exemplo inseridos:
echo - 6 dispositivos ESP32
echo - 50 sensores distribuidos
echo - 4 usuarios com diferentes perfis
echo - Configuracoes de limites
echo - Dashboards e relatorios
echo - Logs e alertas de exemplo
echo.
echo Para conectar ao banco:
echo mysql -u %MYSQL_USER% -p iot_monitoring_db
echo.

pause
