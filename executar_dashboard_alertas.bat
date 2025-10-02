@echo off
echo ========================================
echo Dashboard e Alertas - Sistema IoT
echo Enterprise Challenge Sprint 3 - Reply
echo ========================================
echo.

echo Instalando dependencias...
pip install streamlit pandas matplotlib seaborn plotly mysql-connector-python numpy

echo.
echo Escolha uma opcao:
echo 1. Executar Dashboard Streamlit
echo 2. Executar Sistema de Alertas
echo 3. Executar ambos
echo 4. Visualizar relatorios existentes
echo.

set /p opcao="Digite sua opcao (1-4): "

if "%opcao%"=="1" (
    echo.
    echo Executando Dashboard Streamlit...
    streamlit run dashboard_visualizacao_alertas.py
    echo.
    echo Dashboard executado!
) else if "%opcao%"=="2" (
    echo.
    echo Executando Sistema de Alertas...
    python sistema_alertas_avancado.py
    echo.
    echo Sistema de alertas executado!
) else if "%opcao%"=="3" (
    echo.
    echo Executando ambos...
    echo.
    echo 1. Iniciando Dashboard em background...
    start /B streamlit run dashboard_visualizacao_alertas.py
    echo.
    echo 2. Executando Sistema de Alertas...
    python sistema_alertas_avancado.py
    echo.
    echo Ambos executados!
) else if "%opcao%"=="4" (
    echo.
    echo Visualizando relatorios existentes...
    if exist "historico_alertas.json" (
        echo Abrindo historico de alertas...
        start historico_alertas.json
    ) else (
        echo Arquivo de historico nao encontrado!
    )
    if exist "sistema_alertas.log" (
        echo Abrindo log de alertas...
        start sistema_alertas.log
    ) else (
        echo Arquivo de log nao encontrado!
    )
    echo.
    echo Relatorios abertos!
) else (
    echo.
    echo Opcao invalida!
)

echo.
echo Processo concluido!
pause
