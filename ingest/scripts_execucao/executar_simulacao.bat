@echo off
REM Script de Execução - Simulação de Dados
REM Sistema IoT Monitoring - Enterprise Challenge Sprint 3 - Reply

echo ========================================
echo Sistema IoT Monitoring - Simulação
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

REM Verificar se o arquivo do simulador existe
if not exist "ingest\python\simulador_dados_esp32.py" (
    echo ERRO: Arquivo simulador_dados_esp32.py nao encontrado!
    echo Execute este script a partir do diretorio raiz do projeto.
    pause
    exit /b 1
)

REM Criar diretórios necessários
if not exist "ingest\dados" mkdir ingest\dados
if not exist "ingest\graficos" mkdir ingest\graficos

echo Configurando simulação de dados...
echo.

REM Solicitar parâmetros do usuário
set /p DURACAO="Duração em segundos (padrão: 60): "
if "%DURACAO%"=="" set DURACAO=60

set /p FREQUENCIA="Frequência em Hz (padrão: 1): "
if "%FREQUENCIA%"=="" set FREQUENCIA=1

echo.
echo Sensores disponíveis: DHT22, LDR, PIR, BME280
set /p SENSORES="Sensores a simular (separados por espaço, padrão: todos): "
if "%SENSORES%"=="" set SENSORES=DHT22 LDR PIR BME280

echo.
echo ========================================
echo PARÂMETROS DE SIMULAÇÃO
echo ========================================
echo Duração: %DURACAO% segundos
echo Frequência: %FREQUENCIA% Hz
echo Sensores: %SENSORES%
echo ========================================
echo.

REM Executar simulador
echo Iniciando simulação de dados...
echo.
python ingest\python\simulador_dados_esp32.py --duracao %DURACAO% --frequencia %FREQUENCIA% --sensores %SENSORES%

if errorlevel 1 (
    echo.
    echo ERRO: Falha na simulação de dados!
    echo Verifique:
    echo   - Se as dependências Python estão instaladas
    echo   - Se os parâmetros estão corretos
    echo   - Se há espaço em disco suficiente
    pause
    exit /b 1
)

echo.
echo ========================================
echo SIMULAÇÃO CONCLUÍDA COM SUCESSO!
echo ========================================
echo.

REM Verificar se os dados foram gerados
if exist "ingest\dados\dados_simulados.csv" (
    echo Dados simulados salvos em:
    echo   - ingest\dados\dados_simulados.csv
    echo   - ingest\dados\dados_simulados.json
    echo   - ingest\dados\relatorio_simulacao.json
    echo   - ingest\dados\logs_simulador.txt
    echo.
    
    REM Perguntar se deseja gerar gráficos
    set /p GERAR_GRAFICOS="Deseja gerar gráficos dos dados simulados? (s/n): "
    if /i "%GERAR_GRAFICOS%"=="s" (
        echo.
        echo Gerando gráficos...
        python ingest\python\visualizador_dados.py --arquivo ingest\dados\dados_simulados.csv --formato csv
        
        if errorlevel 1 (
            echo ERRO: Falha na geração de gráficos!
        ) else (
            echo.
            echo Gráficos salvos em: ingest\graficos\
        )
    )
) else (
    echo AVISO: Nenhum dado foi simulado!
    echo Verifique os logs para mais detalhes.
)

echo.
echo ========================================
echo PROCESSO CONCLUÍDO
echo ========================================
echo.
pause
