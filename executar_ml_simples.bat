@echo off
echo ========================================
echo SISTEMA ML COMPLETO - WINDOWS
echo Sistema IoT Monitoring - Sprint 3
echo ========================================
echo.

echo Verificando dependencias...
python -c "import sklearn, pandas, numpy, joblib, paho.mqtt.client, mysql.connector" 2>nul
if %errorlevel% neq 0 (
    echo Instalando dependencias...
    pip install scikit-learn pandas numpy joblib paho-mqtt mysql-connector-python
)

echo.
echo Criando diretorio de modelos...
if not exist "modelos" mkdir modelos

echo.
echo Iniciando Sistema ML Completo...
echo.

echo [1/4] Executando teste do sistema...
python executar_ml_completo.py --modo teste
if %errorlevel% neq 0 (
    echo ERRO: Teste do sistema falhou
    pause
    exit /b 1
)

echo.
echo [2/4] Executando demonstracao...
python executar_ml_completo.py --modo demo

echo.
echo [3/4] Iniciando sistema integrado...
echo Pressione Ctrl+C para parar
echo.

python executar_ml_completo.py --modo integrado

echo.
echo Sistema parado.
pause

