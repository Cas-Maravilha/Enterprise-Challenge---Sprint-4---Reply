@echo off
echo ========================================
echo DASHBOARD COMPLETO - WINDOWS
echo Sistema IoT Monitoring - Sprint 3
echo ========================================
echo.

echo Verificando dependencias...
python -c "import flask, plotly, matplotlib, seaborn, jinja2, schedule, pandas, numpy" 2>nul
if %errorlevel% neq 0 (
    echo Instalando dependencias...
    pip install flask plotly matplotlib seaborn jinja2 schedule pandas numpy
)

echo.
echo Criando diretorios necessarios...
if not exist "templates" mkdir templates
if not exist "relatorios" mkdir relatorios
if not exist "modelos" mkdir modelos

echo.
echo Iniciando Sistema de Dashboard...
echo.

echo [1/4] Executando teste do sistema...
python executar_dashboard_completo.py --modo teste
if %errorlevel% neq 0 (
    echo ERRO: Teste do sistema falhou
    pause
    exit /b 1
)

echo.
echo [2/4] Verificando status do sistema...
python executar_dashboard_completo.py --modo status

echo.
echo [3/4] Gerando relatorio de exemplo...
python executar_dashboard_completo.py --tipo-relatorio diario

echo.
echo [4/4] Iniciando dashboard completo...
echo Dashboard disponivel em: http://localhost:5000
echo Pressione Ctrl+C para parar
echo.

python executar_dashboard_completo.py --modo completo

echo.
echo Sistema parado.
pause
