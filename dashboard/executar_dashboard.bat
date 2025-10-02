@echo off
REM Script de Execução - Dashboard IoT Monitoring
REM Sistema IoT Monitoring - Enterprise Challenge Sprint 3 - Reply

echo ========================================
echo Sistema IoT Monitoring - Dashboard
echo Enterprise Challenge Sprint 3 - Reply
echo ========================================
echo.

REM Verificar se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Python nao encontrado!
    echo Instale Python 3.8+ e tente novamente.
    pause
    exit /b 1
)

REM Verificar se Streamlit está instalado
python -c "import streamlit" >nul 2>&1
if errorlevel 1 (
    echo Instalando dependencias...
    pip install streamlit plotly pandas numpy mysql-connector-python sqlalchemy
    if errorlevel 1 (
        echo ERRO: Falha na instalacao das dependencias!
        pause
        exit /b 1
    )
)

REM Verificar se os scripts existem
if not exist "dashboard\app\app.py" (
    echo ERRO: Scripts do dashboard nao encontrados!
    echo Execute este script a partir do diretorio raiz do projeto.
    pause
    exit /b 1
)

echo Configurando dashboard IoT Monitoring...
echo.

REM Solicitar parâmetros
set /p MODE="Modo de execucao (app/kpis/alertas): "
if "%MODE%"=="" set MODE=app

set /p PORT="Porta (padrao: 8501): "
if "%PORT%"=="" set PORT=8501

echo.
echo ========================================
echo PARAMETROS DE CONFIGURACAO
echo ========================================
echo Modo: %MODE%
echo Porta: %PORT%
echo ========================================
echo.

REM Executar dashboard baseado no modo
if "%MODE%"=="app" (
    echo [1/1] Executando dashboard principal...
    echo.
    echo Dashboard sera aberto em: http://localhost:%PORT%
    echo.
    echo Pressione Ctrl+C para parar o servidor
    echo.
    streamlit run dashboard\app\app.py --server.port %PORT%
) else if "%MODE%"=="kpis" (
    echo [1/1] Executando dashboard de KPIs...
    echo.
    echo Dashboard sera aberto em: http://localhost:%PORT%
    echo.
    echo Pressione Ctrl+C para parar o servidor
    echo.
    streamlit run dashboard\app\dashboard_kpis.py --server.port %PORT%
) else if "%MODE%"=="alertas" (
    echo [1/1] Executando sistema de alertas...
    echo.
    echo Dashboard sera aberto em: http://localhost:%PORT%
    echo.
    echo Pressione Ctrl+C para parar o servidor
    echo.
    streamlit run dashboard\app\sistema_alertas.py --server.port %PORT%
) else (
    echo ERRO: Modo invalido! Use: app, kpis ou alertas
    pause
    exit /b 1
)

if errorlevel 1 (
    echo.
    echo ERRO: Falha na execucao do dashboard!
    echo Verifique:
    echo   - Se o banco de dados esta rodando
    echo   - Se as dependencias estao instaladas
    echo   - Se a porta %PORT% esta disponivel
    pause
    exit /b 1
)

echo.
echo ========================================
echo DASHBOARD EXECUTADO COM SUCESSO!
echo ========================================
echo.
echo Arquivos disponiveis:
echo   - dashboard\app\ - Aplicacao web
echo   - dashboard\relatorios\ - Relatorios HTML
echo   - dashboard\kpis\ - KPIs em tempo real
echo   - dashboard\alertas\ - Sistema de alertas
echo.
echo Para acessar:
echo   - Dashboard Principal: http://localhost:%PORT%
echo   - KPIs: http://localhost:%PORT% (modo kpis)
echo   - Alertas: http://localhost:%PORT% (modo alertas)
echo.
pause
