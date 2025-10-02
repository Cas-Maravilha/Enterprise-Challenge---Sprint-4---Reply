@echo off
REM Script de Execução - Coleta Hardware ESP32
REM Sistema IoT Monitoring - Enterprise Challenge Sprint 3 - Reply

echo ========================================
echo Sistema IoT Monitoring - Coleta Hardware
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

REM Verificar se o arquivo do coletor existe
if not exist "ingest\python\coletor_dados_serial.py" (
    echo ERRO: Arquivo coletor_dados_serial.py nao encontrado!
    echo Execute este script a partir do diretorio raiz do projeto.
    pause
    exit /b 1
)

REM Criar diretórios necessários
if not exist "ingest\dados" mkdir ingest\dados
if not exist "ingest\graficos" mkdir ingest\graficos

echo Configurando coleta de dados via hardware ESP32...
echo.

REM Solicitar parâmetros do usuário
set /p PORT="Porta Serial (padrão: COM3): "
if "%PORT%"=="" set PORT=COM3

set /p DURACAO="Duração em segundos (padrão: 60): "
if "%DURACAO%"=="" set DURACAO=60

set /p BAUDRATE="Baudrate (padrão: 115200): "
if "%BAUDRATE%"=="" set BAUDRATE=115200

echo.
echo ========================================
echo PARÂMETROS DE COLETA
echo ========================================
echo Porta Serial: %PORT%
echo Duração: %DURACAO% segundos
echo Baudrate: %BAUDRATE%
echo ========================================
echo.

REM Executar coletor
echo Iniciando coleta de dados...
echo.
python ingest\python\coletor_dados_serial.py --port %PORT% --baudrate %BAUDRATE% --duracao %DURACAO%

if errorlevel 1 (
    echo.
    echo ERRO: Falha na coleta de dados!
    echo Verifique:
    echo   - Se o ESP32 está conectado
    echo   - Se a porta está correta
    echo   - Se o baudrate está correto
    echo   - Se o código está rodando no ESP32
    pause
    exit /b 1
)

echo.
echo ========================================
echo COLETA CONCLUÍDA COM SUCESSO!
echo ========================================
echo.

REM Verificar se os dados foram coletados
if exist "ingest\dados\dados_coletados.csv" (
    echo Dados coletados salvos em:
    echo   - ingest\dados\dados_coletados.csv
    echo   - ingest\dados\dados_coletados.json
    echo   - ingest\dados\relatorio_coleta_serial.json
    echo   - ingest\dados\logs_coletor_serial.txt
    echo.
    
    REM Perguntar se deseja gerar gráficos
    set /p GERAR_GRAFICOS="Deseja gerar gráficos dos dados coletados? (s/n): "
    if /i "%GERAR_GRAFICOS%"=="s" (
        echo.
        echo Gerando gráficos...
        python ingest\python\visualizador_dados.py --arquivo ingest\dados\dados_coletados.csv --formato csv
        
        if errorlevel 1 (
            echo ERRO: Falha na geração de gráficos!
        ) else (
            echo.
            echo Gráficos salvos em: ingest\graficos\
        )
    )
) else (
    echo AVISO: Nenhum dado foi coletado!
    echo Verifique se o ESP32 está enviando dados.
)

echo.
echo ========================================
echo PROCESSO CONCLUÍDO
echo ========================================
echo.
pause
