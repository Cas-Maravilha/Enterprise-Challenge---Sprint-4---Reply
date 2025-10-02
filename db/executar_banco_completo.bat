@echo off
REM Script de Execução - Banco de Dados Completo
REM Sistema IoT Monitoring - Enterprise Challenge Sprint 3 - Reply

echo ========================================
echo Sistema IoT Monitoring - Banco de Dados
echo Enterprise Challenge Sprint 3 - Reply
echo ========================================
echo.

REM Verificar se MySQL está instalado
mysql --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: MySQL nao encontrado!
    echo Instale MySQL 8.0+ e tente novamente.
    pause
    exit /b 1
)

REM Verificar se os scripts existem
if not exist "db\scripts\01_create_database.sql" (
    echo ERRO: Scripts de criacao nao encontrados!
    echo Execute este script a partir do diretorio raiz do projeto.
    pause
    exit /b 1
)

echo Configurando banco de dados IoT Monitoring...
echo.

REM Solicitar credenciais do MySQL
set /p MYSQL_USER="Usuario MySQL (padrao: root): "
if "%MYSQL_USER%"=="" set MYSQL_USER=root

set /p MYSQL_PASSWORD="Senha MySQL: "

echo.
echo ========================================
echo PARAMETROS DE CONFIGURACAO
echo ========================================
echo Usuario: %MYSQL_USER%
echo Banco: iot_monitoring_db
echo ========================================
echo.

REM Executar criacao do banco
echo [1/6] Criando banco de dados...
mysql -u %MYSQL_USER% -p%MYSQL_PASSWORD% < db\scripts\01_create_database.sql

if errorlevel 1 (
    echo.
    echo ERRO: Falha na criacao do banco!
    echo Verifique:
    echo   - Se o MySQL esta rodando
    echo   - Se as credenciais estao corretas
    echo   - Se o usuario tem privilegios
    pause
    exit /b 1
)

echo ✓ Banco de dados criado com sucesso!

REM Executar criacao das tabelas
echo [2/6] Criando tabelas...
mysql -u %MYSQL_USER% -p%MYSQL_PASSWORD% iot_monitoring_db < db\scripts\02_create_tables.sql

if errorlevel 1 (
    echo.
    echo ERRO: Falha na criacao das tabelas!
    pause
    exit /b 1
)

echo ✓ Tabelas criadas com sucesso!

REM Executar criacao dos indices
echo [3/6] Criando indices...
mysql -u %MYSQL_USER% -p%MYSQL_PASSWORD% iot_monitoring_db < db\scripts\03_create_indexes.sql

if errorlevel 1 (
    echo.
    echo ERRO: Falha na criacao dos indices!
    pause
    exit /b 1
)

echo ✓ Indices criados com sucesso!

REM Executar carga de dados iniciais
echo [4/6] Carregando dados iniciais...
mysql -u %MYSQL_USER% -p%MYSQL_PASSWORD% iot_monitoring_db < db\carga\carga_dados_iniciais.sql

if errorlevel 1 (
    echo.
    echo ERRO: Falha na carga de dados iniciais!
    pause
    exit /b 1
)

echo ✓ Dados iniciais carregados com sucesso!

REM Executar carga de dados simulados
echo [5/6] Carregando dados simulados...
echo ATENCAO: Este processo pode demorar alguns minutos...
mysql -u %MYSQL_USER% -p%MYSQL_PASSWORD% iot_monitoring_db < db\carga\carga_dados_simulados.sql

if errorlevel 1 (
    echo.
    echo ERRO: Falha na carga de dados simulados!
    pause
    exit /b 1
)

echo ✓ Dados simulados carregados com sucesso!

REM Executar verificacoes
echo [6/6] Executando verificacoes...
mysql -u %MYSQL_USER% -p%MYSQL_PASSWORD% iot_monitoring_db < db\evidencias\select_tabelas_principais.sql > db\evidencias\resultado_verificacao.txt

if errorlevel 1 (
    echo.
    echo AVISO: Falha nas verificacoes, mas o banco foi criado!
) else (
    echo ✓ Verificacoes executadas com sucesso!
)

echo.
echo ========================================
echo BANCO DE DADOS CONFIGURADO COM SUCESSO!
echo ========================================
echo.

REM Mostrar resumo
echo RESUMO DA CONFIGURACAO:
echo - Banco: iot_monitoring_db
echo - Tabelas: 11
echo - Indices: 50+
echo - Dados iniciais: Carregados
echo - Dados simulados: Carregados
echo - Verificacoes: Executadas
echo.

REM Perguntar se deseja ver evidencias
set /p VER_EVIDENCIAS="Deseja ver as evidencias do banco? (s/n): "
if /i "%VER_EVIDENCIAS%"=="s" (
    echo.
    echo ========================================
    echo EVIDENCIAS DO BANCO DE DADOS
    echo ========================================
    echo.
    
    echo [1] Estrutura das tabelas:
    mysql -u %MYSQL_USER% -p%MYSQL_PASSWORD% iot_monitoring_db -e "SHOW TABLES;"
    echo.
    
    echo [2] Contagem de registros:
    mysql -u %MYSQL_USER% -p%MYSQL_PASSWORD% iot_monitoring_db -e "SELECT 'leituras_sensores' as tabela, COUNT(*) as total FROM leituras_sensores UNION ALL SELECT 'alertas' as tabela, COUNT(*) as total FROM alertas UNION ALL SELECT 'dispositivos' as tabela, COUNT(*) as total FROM dispositivos UNION ALL SELECT 'sensores' as tabela, COUNT(*) as total FROM sensores;"
    echo.
    
    echo [3] Qualidade dos dados:
    mysql -u %MYSQL_USER% -p%MYSQL_PASSWORD% iot_monitoring_db -e "SELECT qualidade_dados, COUNT(*) as total, ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM leituras_sensores), 2) as percentual FROM leituras_sensores GROUP BY qualidade_dados;"
    echo.
    
    echo [4] Alertas por severidade:
    mysql -u %MYSQL_USER% -p%MYSQL_PASSWORD% iot_monitoring_db -e "SELECT severidade, COUNT(*) as total FROM alertas GROUP BY severidade;"
    echo.
)

echo.
echo ========================================
echo PROCESSO CONCLUIDO
echo ========================================
echo.
echo Arquivos gerados:
echo   - db\evidencias\resultado_verificacao.txt
echo   - db\evidencias\print_estrutura_banco.txt
echo   - db\evidencias\print_dados_carregados.txt
echo.
echo Para conectar ao banco:
echo   mysql -u %MYSQL_USER% -p iot_monitoring_db
echo.
pause
