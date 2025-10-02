@echo off
REM Script de Execução - Machine Learning Completo
REM Sistema IoT Monitoring - Enterprise Challenge Sprint 3 - Reply

echo ========================================
echo Sistema IoT Monitoring - Machine Learning
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

REM Verificar se os scripts existem
if not exist "ml\scripts\treinar_modelo_ml.py" (
    echo ERRO: Scripts de ML nao encontrados!
    echo Execute este script a partir do diretorio raiz do projeto.
    pause
    exit /b 1
)

echo Configurando sistema de Machine Learning...
echo.

REM Solicitar parâmetros
set /p LIMIT_TREINO="Limite de dados para treino (padrao: 10000): "
if "%LIMIT_TREINO%"=="" set LIMIT_TREINO=10000

set /p LIMIT_AVALIACAO="Limite de dados para avaliacao (padrao: 5000): "
if "%LIMIT_AVALIACAO%"=="" set LIMIT_AVALIACAO=5000

set /p LIMIT_INFERENCIA="Limite de dados para inferencia (padrao: 1000): "
if "%LIMIT_INFERENCIA%"=="" set LIMIT_INFERENCIA=1000

echo.
echo ========================================
echo PARAMETROS DE CONFIGURACAO
echo ========================================
echo Treino: %LIMIT_TREINO% registros
echo Avaliacao: %LIMIT_AVALIACAO% registros
echo Inferencia: %LIMIT_INFERENCIA% registros
echo ========================================
echo.

REM 1. Treinar modelo
echo [1/3] Treinando modelo de Machine Learning...
python ml\scripts\treinar_modelo_ml.py --limit %LIMIT_TREINO%

if errorlevel 1 (
    echo.
    echo ERRO: Falha no treinamento do modelo!
    echo Verifique:
    echo   - Se o banco de dados esta rodando
    echo   - Se as dependencias Python estao instaladas
    echo   - Se os dados estao disponiveis
    pause
    exit /b 1
)

echo ✓ Modelo treinado com sucesso!

REM 2. Avaliar modelo
echo [2/3] Avaliando modelo treinado...
python ml\scripts\avaliar_modelo.py --limit %LIMIT_AVALIACAO%

if errorlevel 1 (
    echo.
    echo AVISO: Falha na avaliacao, mas o modelo foi treinado!
) else (
    echo ✓ Modelo avaliado com sucesso!
)

REM 3. Executar inferencia
echo [3/3] Executando inferencia em tempo real...
python ml\scripts\inferencia_tempo_real.py --mode batch --limit %LIMIT_INFERENCIA%

if errorlevel 1 (
    echo.
    echo AVISO: Falha na inferencia, mas o modelo foi treinado!
) else (
    echo ✓ Inferencia executada com sucesso!
)

echo.
echo ========================================
echo SISTEMA ML CONFIGURADO COM SUCESSO!
echo ========================================
echo.

REM Mostrar resumo
echo RESUMO DA CONFIGURACAO:
echo - Modelo treinado: Random Forest
echo - Dados de treino: %LIMIT_TREINO% registros
echo - Dados de avaliacao: %LIMIT_AVALIACAO% registros
echo - Dados de inferencia: %LIMIT_INFERENCIA% registros
echo - Modelos salvos: ml\modelos\
echo - Metricas salvas: ml\metricas\
echo - Visualizacoes: ml\visualizacoes\
echo.

REM Perguntar se deseja ver resultados
set /p VER_RESULTADOS="Deseja ver os resultados do ML? (s/n): "
if /i "%VER_RESULTADOS%"=="s" (
    echo.
    echo ========================================
    echo RESULTADOS DO MACHINE LEARNING
    echo ========================================
    echo.
    
    echo [1] Metricas principais:
    if exist "ml\metricas\model_metrics.json" (
        type ml\metricas\model_metrics.json
    ) else (
        echo Arquivo de metricas nao encontrado.
    )
    echo.
    
    echo [2] Metricas de avaliacao:
    if exist "ml\metricas\evaluation_metrics.json" (
        type ml\metricas\evaluation_metrics.json
    ) else (
        echo Arquivo de avaliacao nao encontrado.
    )
    echo.
    
    echo [3] Lista de arquivos gerados:
    if exist "ml\modelos\" (
        echo Modelos:
        dir ml\modelos\ /b
    )
    echo.
    
    if exist "ml\metricas\" (
        echo Metricas:
        dir ml\metricas\ /b
    )
    echo.
    
    if exist "ml\visualizacoes\" (
        echo Visualizacoes:
        dir ml\visualizacoes\ /b
    )
    echo.
)

echo.
echo ========================================
echo PROCESSO CONCLUIDO
echo ========================================
echo.
echo Arquivos gerados:
echo   - ml\modelos\ - Modelos treinados (.pkl)
echo   - ml\metricas\ - Metricas de avaliacao (.json)
echo   - ml\visualizacoes\ - Graficos e visualizacoes (.png)
echo.
echo Para executar inferencia em tempo real:
echo   python ml\scripts\inferencia_tempo_real.py --mode realtime
echo.
echo Para executar processamento em lote:
echo   python ml\scripts\inferencia_tempo_real.py --mode batch
echo.
pause
