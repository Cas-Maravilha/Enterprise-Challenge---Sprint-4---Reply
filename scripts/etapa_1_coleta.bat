@echo off
setlocal enabledelayedexpansion

echo ========================================
echo ETAPA 1: COLETA DE DADOS
echo Enterprise Challenge Sprint 3 - Reply
echo Versao: 1.0.0
echo Data: %date% %time%
echo ========================================

REM Verificar parâmetros
if "%~1"=="" (
    echo Uso: %0 [hardware^|simulacao]
    echo   hardware  - Executar coleta via hardware ESP32
    echo   simulacao - Executar simulacao Wokwi
    pause
    exit /b 1
)

set MODO=%~1

REM Verificar se está no diretório correto
if not exist "README.md" (
    echo [ERRO] Execute este script no diretorio raiz do projeto
    pause
    exit /b 1
)

REM Ativar ambiente virtual se existir
if exist "venv" (
    echo [INFO] Ativando ambiente virtual...
    call venv\Scripts\activate.bat
    echo [SUCESSO] Ambiente virtual ativado
)

REM Criar diretório de evidências
set EVIDENCIAS_DIR=evidencias_coleta_%date:~6,4%%date:~3,2%%date:~0,2%_%time:~0,2%%time:~3,2%%time:~6,2%
set EVIDENCIAS_DIR=!EVIDENCIAS_DIR: =0!
mkdir "!EVIDENCIAS_DIR!"
echo [INFO] Diretorio de evidencias criado: !EVIDENCIAS_DIR!

REM Verificar arquivos de coleta
echo [INFO] Verificando arquivos de coleta...
set arquivos_coleta=coleta_ingestao_esp32.ino wokwi_simulacao_esp32.json coletor_dados_serial.py simulador_dados_esp32.py

for %%f in (%arquivos_coleta%) do (
    if exist "%%f" (
        echo [SUCESSO] Arquivo encontrado: %%f
        echo 📸 EVIDENCIA - COLETA >> "!EVIDENCIAS_DIR!\evidencias.txt"
        echo Timestamp: %date% %time% >> "!EVIDENCIAS_DIR!\evidencias.txt"
        echo Descricao: Arquivo de coleta >> "!EVIDENCIAS_DIR!\evidencias.txt"
        echo Arquivo: %%f >> "!EVIDENCIAS_DIR!\evidencias.txt"
        echo ---------------------------------------- >> "!EVIDENCIAS_DIR!\evidencias.txt"
        copy "%%f" "!EVIDENCIAS_DIR!\" >nul 2>&1
    ) else (
        echo [AVISO] Arquivo nao encontrado: %%f
    )
)

REM Executar coleta baseada no modo
if "%MODO%"=="hardware" (
    echo [INFO] 🔌 Executando coleta via hardware ESP32...
    
    REM Verificar se o coletor serial existe
    if exist "coletor_dados_serial.py" (
        echo [INFO] Executando coletor serial...
        python coletor_dados_serial.py --port COM3 --baudrate 115200 --duracao 60 > "!EVIDENCIAS_DIR!\coletor_serial_output.txt" 2>&1
        echo [SUCESSO] Coletor serial executado
        echo 📸 EVIDENCIA - COLETA >> "!EVIDENCIAS_DIR!\evidencias.txt"
        echo Timestamp: %date% %time% >> "!EVIDENCIAS_DIR!\evidencias.txt"
        echo Descricao: Output do coletor serial >> "!EVIDENCIAS_DIR!\evidencias.txt"
        echo Arquivo: coletor_serial_output.txt >> "!EVIDENCIAS_DIR!\evidencias.txt"
        echo ---------------------------------------- >> "!EVIDENCIAS_DIR!\evidencias.txt"
    ) else (
        echo [AVISO] Coletor serial nao encontrado
    )
    
) else if "%MODO%"=="simulacao" (
    echo [INFO] 🎮 Executando simulacao Wokwi...
    
    REM Verificar se o simulador existe
    if exist "simulador_dados_esp32.py" (
        echo [INFO] Executando simulador de dados...
        python simulador_dados_esp32.py --duracao 60 --frequencia 1 > "!EVIDENCIAS_DIR!\simulador_output.txt" 2>&1
        echo [SUCESSO] Simulador executado
        echo 📸 EVIDENCIA - COLETA >> "!EVIDENCIAS_DIR!\evidencias.txt"
        echo Timestamp: %date% %time% >> "!EVIDENCIAS_DIR!\evidencias.txt"
        echo Descricao: Output do simulador >> "!EVIDENCIAS_DIR!\evidencias.txt"
        echo Arquivo: simulador_output.txt >> "!EVIDENCIAS_DIR!\evidencias.txt"
        echo ---------------------------------------- >> "!EVIDENCIAS_DIR!\evidencias.txt"
    ) else (
        echo [AVISO] Simulador nao encontrado
    )
    
    REM Verificar arquivo de simulação Wokwi
    if exist "wokwi_simulacao_esp32.json" (
        echo [SUCESSO] Arquivo de simulacao Wokwi encontrado
        echo 📸 EVIDENCIA - COLETA >> "!EVIDENCIAS_DIR!\evidencias.txt"
        echo Timestamp: %date% %time% >> "!EVIDENCIAS_DIR!\evidencias.txt"
        echo Descricao: Configuracao Wokwi >> "!EVIDENCIAS_DIR!\evidencias.txt"
        echo Arquivo: wokwi_simulacao_esp32.json >> "!EVIDENCIAS_DIR!\evidencias.txt"
        echo ---------------------------------------- >> "!EVIDENCIAS_DIR!\evidencias.txt"
        copy "wokwi_simulacao_esp32.json" "!EVIDENCIAS_DIR!\" >nul 2>&1
    ) else (
        echo [AVISO] Arquivo de simulacao Wokwi nao encontrado
    )
    
) else (
    echo [ERRO] Modo invalido: %MODO%
    echo Use: hardware ou simulacao
    pause
    exit /b 1
)

REM Verificar arquivos gerados
echo [INFO] Verificando arquivos gerados...
set arquivos_gerados=dados_coletados.csv dados_simulados.csv log_coleta.txt screenshot_coleta.png

for %%f in (%arquivos_gerados%) do (
    if exist "%%f" (
        echo [SUCESSO] Arquivo gerado: %%f
        echo 📸 EVIDENCIA - COLETA >> "!EVIDENCIAS_DIR!\evidencias.txt"
        echo Timestamp: %date% %time% >> "!EVIDENCIAS_DIR!\evidencias.txt"
        echo Descricao: Arquivo gerado >> "!EVIDENCIAS_DIR!\evidencias.txt"
        echo Arquivo: %%f >> "!EVIDENCIAS_DIR!\evidencias.txt"
        echo ---------------------------------------- >> "!EVIDENCIAS_DIR!\evidencias.txt"
        copy "%%f" "!EVIDENCIAS_DIR!\" >nul 2>&1
    ) else (
        echo [AVISO] Arquivo nao gerado: %%f
    )
)

REM Gerar relatório da etapa
(
echo Sistema IoT Monitoring - Etapa 1: Coleta de Dados
echo Enterprise Challenge Sprint 3 - Reply
echo ========================================
echo.
echo Data de Execucao: %date% %time%
echo Modo: %MODO%
echo Versao: 1.0.0
echo.
echo ARQUIVOS VERIFICADOS:
for %%f in (%arquivos_coleta%) do (
    if exist "%%f" (
        echo ✅ %%f
    ) else (
        echo ❌ %%f
    )
)
echo.
echo ARQUIVOS GERADOS:
for %%f in (%arquivos_gerados%) do (
    if exist "%%f" (
        echo ✅ %%f
    ) else (
        echo ❌ %%f
    )
)
echo.
echo STATUS: ETAPA 1 CONCLUIDA
) > "!EVIDENCIAS_DIR!\relatorio_coleta.txt"

echo [SUCESSO] Relatorio da etapa gerado: !EVIDENCIAS_DIR!\relatorio_coleta.txt

REM Mostrar resumo
echo.
echo 📊 RESUMO DA ETAPA 1:
echo ======================
type "!EVIDENCIAS_DIR!\relatorio_coleta.txt"

echo.
echo ✅ ETAPA 1: COLETA DE DADOS CONCLUIDA!
echo ========================================
echo 📁 Evidencias salvas em: !EVIDENCIAS_DIR!\
echo 📋 Relatorio: !EVIDENCIAS_DIR!\relatorio_coleta.txt
echo ========================================
pause
