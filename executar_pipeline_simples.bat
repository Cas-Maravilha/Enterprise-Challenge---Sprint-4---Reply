@echo off
echo ========================================
echo PIPELINE INTEGRADO ESP32 - WINDOWS
echo Sistema IoT Monitoring - Sprint 3
echo ========================================
echo.

echo Verificando dependencias...
python -c "import paho.mqtt.client, pandas, numpy, sklearn, matplotlib, seaborn, mysql.connector, joblib" 2>nul
if %errorlevel% neq 0 (
    echo Instalando dependencias...
    pip install -r requirements.txt
)

echo.
echo Iniciando Pipeline Integrado...
echo.

echo [1/3] Iniciando Pipeline Principal...
start "Pipeline Principal" cmd /k "python pipeline_integrado_esp32.py"

timeout /t 5 /nobreak >nul

echo [2/3] Iniciando Coletor de Dados Wokwi...
start "Coletor Wokwi" cmd /k "python coletor_dados_wokwi.py"

timeout /t 3 /nobreak >nul

echo [3/3] Iniciando Dashboard (opcional)...
if exist "interactive_dashboard.py" (
    start "Dashboard" cmd /k "python interactive_dashboard.py"
) else (
    echo Dashboard nao encontrado. Continuando sem dashboard...
)

echo.
echo ========================================
echo PIPELINE INICIADO COM SUCESSO!
echo ========================================
echo.
echo Componentes ativos:
echo - Pipeline Principal (Terminal 1)
echo - Coletor Wokwi (Terminal 2)
echo - Dashboard (Terminal 3, se disponivel)
echo.
echo Para parar o pipeline, feche todas as janelas de terminal.
echo.
pause
