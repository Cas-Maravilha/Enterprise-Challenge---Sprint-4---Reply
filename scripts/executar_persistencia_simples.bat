@echo off
echo ========================================
echo PERSISTENCIA BANCO RELACIONAL - WINDOWS
echo Sistema IoT Monitoring - Sprint 3
echo ========================================
echo.

echo Verificando dependencias...
python -c "import mysql.connector, paho.mqtt.client, pandas, numpy" 2>nul
if %errorlevel% neq 0 (
    echo Instalando dependencias...
    pip install mysql-connector-python paho-mqtt pandas numpy
)

echo.
echo Verificando banco de dados...
mysql -u root -p -e "USE iot_monitoring_db;" 2>nul
if %errorlevel% neq 0 (
    echo Criando banco de dados...
    mysql -u root -p < criar_tabelas_iot.sql
)

echo.
echo Iniciando Sistema de Persistencia...
echo.

echo [1/2] Executando teste de persistencia...
python executar_persistencia_completa.py --teste
if %errorlevel% neq 0 (
    echo ERRO: Teste de persistencia falhou
    pause
    exit /b 1
)

echo.
echo [2/2] Iniciando sistema completo...
echo Pressione Ctrl+C para parar
echo.

python executar_persistencia_completa.py --modo desenvolvimento

echo.
echo Sistema parado.
pause

