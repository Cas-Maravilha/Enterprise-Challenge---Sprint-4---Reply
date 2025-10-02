@echo off
echo ========================================
echo ML Basico Integrado - Sistema IoT
echo Enterprise Challenge Sprint 3 - Reply
echo ========================================
echo.

echo Instalando dependencias...
pip install pandas matplotlib seaborn scikit-learn numpy mysql-connector-python joblib

echo.
echo Escolha uma opcao:
echo 1. Executar ML basico integrado
echo 2. Analisar dataset ML
echo 3. Executar ambos
echo 4. Visualizar resultados existentes
echo.

set /p opcao="Digite sua opcao (1-4): "

if "%opcao%"=="1" (
    echo.
    echo Executando ML basico integrado...
    python ml_basico_integrado.py
    echo.
    echo ML basico executado!
) else if "%opcao%"=="2" (
    echo.
    echo Analisando dataset ML...
    python dataset_ml_analisador.py
    echo.
    echo Analise do dataset concluida!
) else if "%opcao%"=="3" (
    echo.
    echo Executando ambos...
    echo.
    echo 1. Analisando dataset...
    python dataset_ml_analisador.py
    echo.
    echo 2. Executando ML basico...
    python ml_basico_integrado.py
    echo.
    echo Ambos executados com sucesso!
) else if "%opcao%"=="4" (
    echo.
    echo Visualizando resultados existentes...
    if exist "ml_basico_visualizacoes.png" (
        echo Abrindo visualizacoes ML...
        start ml_basico_visualizacoes.png
    ) else (
        echo Arquivo de visualizacoes nao encontrado!
    )
    if exist "analise_dataset_ml.png" (
        echo Abrindo analise do dataset...
        start analise_dataset_ml.png
    ) else (
        echo Arquivo de analise do dataset nao encontrado!
    )
    echo.
    echo Visualizacoes abertas!
) else (
    echo.
    echo Opcao invalida!
)

echo.
echo Processo concluido!
pause
