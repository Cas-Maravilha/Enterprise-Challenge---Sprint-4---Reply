@echo off
echo ========================================
echo Coleta e Ingestao ESP32 - Sistema IoT
echo Enterprise Challenge Sprint 3 - Reply
echo ========================================
echo.

echo Instalando dependencias...
pip install pandas matplotlib numpy pyserial

echo.
echo Escolha uma opcao:
echo 1. Coletar dados via Serial (ESP32 real)
echo 2. Simular dados (sem hardware)
echo 3. Visualizar dados existentes
echo.

set /p opcao="Digite sua opcao (1-3): "

if "%opcao%"=="1" (
    echo.
    echo Executando coleta via Serial...
    python coletor_dados_serial.py
) else if "%opcao%"=="2" (
    echo.
    echo Executando simulacao de dados...
    python simulador_dados_esp32.py
) else if "%opcao%"=="3" (
    echo.
    echo Visualizando dados existentes...
    python visualizar_dados_coletados.py
) else (
    echo.
    echo Opcao invalida!
)

echo.
echo Processo concluido!
pause
