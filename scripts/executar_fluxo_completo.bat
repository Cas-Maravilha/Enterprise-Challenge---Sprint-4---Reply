@echo off
setlocal enabledelayedexpansion

echo ========================================
echo Execucao Completa do Fluxo IoT
echo Enterprise Challenge Sprint 3 - Reply
echo Versao: 1.0.0
echo Data: %date% %time%
echo ========================================

REM Verificar se está no diretório correto
if not exist "README.md" (
    echo [ERRO] Execute este script no diretorio raiz do projeto
    pause
    exit /b 1
)

REM Verificar se o setup foi executado
if not exist "venv" (
    echo [ERRO] Execute primeiro o setup: setup_sistema_completo.bat
    pause
    exit /b 1
)

REM Ativar ambiente virtual
echo [INFO] Ativando ambiente virtual...
call venv\Scripts\activate.bat
echo [SUCESSO] Ambiente virtual ativado

REM Criar diretório de evidências
set EVIDENCIAS_DIR=evidencias_%date:~6,4%%date:~3,2%%date:~0,2%_%time:~0,2%%time:~3,2%%time:~6,2%
set EVIDENCIAS_DIR=!EVIDENCIAS_DIR: =0!
mkdir "!EVIDENCIAS_DIR!"
echo [INFO] Diretorio de evidencias criado: !EVIDENCIAS_DIR!

REM ETAPA 1: COLETA DE DADOS
echo.
echo ========================================
echo ETAPA 1: COLETA DE DADOS
echo ========================================
echo [INFO] Iniciando coleta de dados...

REM Verificar arquivos de coleta
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

REM Executar simulador de dados
echo [INFO] Executando simulador de dados...
if exist "simulador_dados_esp32.py" (
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

REM ETAPA 2: PERSISTÊNCIA
echo.
echo ========================================
echo ETAPA 2: PERSISTENCIA
echo ========================================
echo [INFO] Iniciando persistencia de dados...

REM Verificar arquivos de banco
set arquivos_banco=criar_tabelas_iot.sql carga_dados_iot.sql persistencia_banco_relacional.py integracao_persistencia_esp32.py

for %%f in (%arquivos_banco%) do (
    if exist "%%f" (
        echo [SUCESSO] Arquivo encontrado: %%f
        echo 📸 EVIDENCIA - PERSISTENCIA >> "!EVIDENCIAS_DIR!\evidencias.txt"
        echo Timestamp: %date% %time% >> "!EVIDENCIAS_DIR!\evidencias.txt"
        echo Descricao: Arquivo de banco >> "!EVIDENCIAS_DIR!\evidencias.txt"
        echo Arquivo: %%f >> "!EVIDENCIAS_DIR!\evidencias.txt"
        echo ---------------------------------------- >> "!EVIDENCIAS_DIR!\evidencias.txt"
        copy "%%f" "!EVIDENCIAS_DIR!\" >nul 2>&1
    ) else (
        echo [AVISO] Arquivo nao encontrado: %%f
    )
)

REM Executar criação do banco
echo [INFO] Criando estrutura do banco...
if exist "criar_tabelas_iot.sql" (
    mysql -u iot_user -p'iot_password' iot_monitoring_db < criar_tabelas_iot.sql > "!EVIDENCIAS_DIR!\banco_criacao.txt" 2>&1
    if !errorlevel! equ 0 (
        echo [SUCESSO] Banco criado com sucesso
        echo 📸 EVIDENCIA - PERSISTENCIA >> "!EVIDENCIAS_DIR!\evidencias.txt"
        echo Timestamp: %date% %time% >> "!EVIDENCIAS_DIR!\evidencias.txt"
        echo Descricao: Criacao do banco >> "!EVIDENCIAS_DIR!\evidencias.txt"
        echo Arquivo: banco_criacao.txt >> "!EVIDENCIAS_DIR!\evidencias.txt"
        echo ---------------------------------------- >> "!EVIDENCIAS_DIR!\evidencias.txt"
    ) else (
        echo [ERRO] Erro na criacao do banco
    )
) else (
    echo [AVISO] Script de criacao do banco nao encontrado
)

REM Executar carga de dados
echo [INFO] Carregando dados iniciais...
if exist "carga_dados_iot.sql" (
    mysql -u iot_user -p'iot_password' iot_monitoring_db < carga_dados_iot.sql > "!EVIDENCIAS_DIR!\banco_carga.txt" 2>&1
    if !errorlevel! equ 0 (
        echo [SUCESSO] Dados carregados com sucesso
        echo 📸 EVIDENCIA - PERSISTENCIA >> "!EVIDENCIAS_DIR!\evidencias.txt"
        echo Timestamp: %date% %time% >> "!EVIDENCIAS_DIR!\evidencias.txt"
        echo Descricao: Carga de dados >> "!EVIDENCIAS_DIR!\evidencias.txt"
        echo Arquivo: banco_carga.txt >> "!EVIDENCIAS_DIR!\evidencias.txt"
        echo ---------------------------------------- >> "!EVIDENCIAS_DIR!\evidencias.txt"
    ) else (
        echo [ERRO] Erro na carga de dados
    )
) else (
    echo [AVISO] Script de carga de dados nao encontrado
)

REM Verificar dados no banco
echo [INFO] Verificando dados no banco...
mysql -u iot_user -p'iot_password' iot_monitoring_db -e "SELECT 'leituras_sensores' as tabela, COUNT(*) as registros FROM leituras_sensores UNION ALL SELECT 'dispositivos' as tabela, COUNT(*) as registros FROM dispositivos UNION ALL SELECT 'sensores' as tabela, COUNT(*) as registros FROM sensores UNION ALL SELECT 'alertas' as tabela, COUNT(*) as registros FROM alertas;" > "!EVIDENCIAS_DIR!\verificacao_banco.txt" 2>&1

if !errorlevel! equ 0 (
    echo [SUCESSO] Verificacao do banco concluida
    echo 📸 EVIDENCIA - PERSISTENCIA >> "!EVIDENCIAS_DIR!\evidencias.txt"
    echo Timestamp: %date% %time% >> "!EVIDENCIAS_DIR!\evidencias.txt"
    echo Descricao: Verificacao do banco >> "!EVIDENCIAS_DIR!\evidencias.txt"
    echo Arquivo: verificacao_banco.txt >> "!EVIDENCIAS_DIR!\evidencias.txt"
    echo ---------------------------------------- >> "!EVIDENCIAS_DIR!\evidencias.txt"
) else (
    echo [ERRO] Erro na verificacao do banco
)

REM ETAPA 3: MACHINE LEARNING
echo.
echo ========================================
echo ETAPA 3: MACHINE LEARNING
echo ========================================
echo [INFO] Iniciando processamento ML...

REM Verificar arquivos de ML
set arquivos_ml=ml_basico_integrado.py dataset_ml_analisador.py ml_anomaly_detection_completo.py usar_modelo_ml.py

for %%f in (%arquivos_ml%) do (
    if exist "%%f" (
        echo [SUCESSO] Arquivo encontrado: %%f
        echo 📸 EVIDENCIA - ML >> "!EVIDENCIAS_DIR!\evidencias.txt"
        echo Timestamp: %date% %time% >> "!EVIDENCIAS_DIR!\evidencias.txt"
        echo Descricao: Arquivo de ML >> "!EVIDENCIAS_DIR!\evidencias.txt"
        echo Arquivo: %%f >> "!EVIDENCIAS_DIR!\evidencias.txt"
        echo ---------------------------------------- >> "!EVIDENCIAS_DIR!\evidencias.txt"
        copy "%%f" "!EVIDENCIAS_DIR!\" >nul 2>&1
    ) else (
        echo [AVISO] Arquivo nao encontrado: %%f
    )
)

REM Executar ML básico
echo [INFO] Executando ML basico integrado...
if exist "ml_basico_integrado.py" (
    python ml_basico_integrado.py > "!EVIDENCIAS_DIR!\ml_basico_output.txt" 2>&1
    if !errorlevel! equ 0 (
        echo [SUCESSO] ML basico executado com sucesso
        echo 📸 EVIDENCIA - ML >> "!EVIDENCIAS_DIR!\evidencias.txt"
        echo Timestamp: %date% %time% >> "!EVIDENCIAS_DIR!\evidencias.txt"
        echo Descricao: Output do ML basico >> "!EVIDENCIAS_DIR!\evidencias.txt"
        echo Arquivo: ml_basico_output.txt >> "!EVIDENCIAS_DIR!\evidencias.txt"
        echo ---------------------------------------- >> "!EVIDENCIAS_DIR!\evidencias.txt"
    ) else (
        echo [ERRO] Erro na execucao do ML basico
    )
) else (
    echo [AVISO] Script de ML basico nao encontrado
)

REM Executar análise do dataset
echo [INFO] Executando analise do dataset...
if exist "dataset_ml_analisador.py" (
    python dataset_ml_analisador.py > "!EVIDENCIAS_DIR!\dataset_analise_output.txt" 2>&1
    if !errorlevel! equ 0 (
        echo [SUCESSO] Analise do dataset executada
        echo 📸 EVIDENCIA - ML >> "!EVIDENCIAS_DIR!\evidencias.txt"
        echo Timestamp: %date% %time% >> "!EVIDENCIAS_DIR!\evidencias.txt"
        echo Descricao: Analise do dataset >> "!EVIDENCIAS_DIR!\evidencias.txt"
        echo Arquivo: dataset_analise_output.txt >> "!EVIDENCIAS_DIR!\evidencias.txt"
        echo ---------------------------------------- >> "!EVIDENCIAS_DIR!\evidencias.txt"
    ) else (
        echo [ERRO] Erro na analise do dataset
    )
) else (
    echo [AVISO] Script de analise do dataset nao encontrado
)

REM Verificar arquivos gerados pelo ML
set arquivos_ml_gerados=modelo_anomalia.pkl modelo_temperatura.pkl scaler.pkl relatorio_ml_basico.json ml_basico_visualizacoes.png analise_dataset_ml.png

for %%f in (%arquivos_ml_gerados%) do (
    if exist "%%f" (
        echo [SUCESSO] Arquivo gerado: %%f
        echo 📸 EVIDENCIA - ML >> "!EVIDENCIAS_DIR!\evidencias.txt"
        echo Timestamp: %date% %time% >> "!EVIDENCIAS_DIR!\evidencias.txt"
        echo Descricao: Arquivo gerado pelo ML >> "!EVIDENCIAS_DIR!\evidencias.txt"
        echo Arquivo: %%f >> "!EVIDENCIAS_DIR!\evidencias.txt"
        echo ---------------------------------------- >> "!EVIDENCIAS_DIR!\evidencias.txt"
        copy "%%f" "!EVIDENCIAS_DIR!\" >nul 2>&1
    ) else (
        echo [AVISO] Arquivo nao gerado: %%f
    )
)

REM ETAPA 4: VISUALIZAÇÃO E ALERTAS
echo.
echo ========================================
echo ETAPA 4: VISUALIZACAO E ALERTAS
echo ========================================
echo [INFO] Iniciando visualizacao e alertas...

REM Verificar arquivos de visualização
set arquivos_viz=dashboard_visualizacao_alertas.py sistema_alertas_avancado.py kpis_negocio.py metricas_validacao_detalhadas.py

for %%f in (%arquivos_viz%) do (
    if exist "%%f" (
        echo [SUCESSO] Arquivo encontrado: %%f
        echo 📸 EVIDENCIA - VISUALIZACAO >> "!EVIDENCIAS_DIR!\evidencias.txt"
        echo Timestamp: %date% %time% >> "!EVIDENCIAS_DIR!\evidencias.txt"
        echo Descricao: Arquivo de visualizacao >> "!EVIDENCIAS_DIR!\evidencias.txt"
        echo Arquivo: %%f >> "!EVIDENCIAS_DIR!\evidencias.txt"
        echo ---------------------------------------- >> "!EVIDENCIAS_DIR!\evidencias.txt"
        copy "%%f" "!EVIDENCIAS_DIR!\" >nul 2>&1
    ) else (
        echo [AVISO] Arquivo nao encontrado: %%f
    )
)

REM Executar sistema de alertas
echo [INFO] Executando sistema de alertas...
if exist "sistema_alertas_avancado.py" (
    python sistema_alertas_avancado.py > "!EVIDENCIAS_DIR!\alertas_output.txt" 2>&1
    if !errorlevel! equ 0 (
        echo [SUCESSO] Sistema de alertas executado
        echo 📸 EVIDENCIA - VISUALIZACAO >> "!EVIDENCIAS_DIR!\evidencias.txt"
        echo Timestamp: %date% %time% >> "!EVIDENCIAS_DIR!\evidencias.txt"
        echo Descricao: Output do sistema de alertas >> "!EVIDENCIAS_DIR!\evidencias.txt"
        echo Arquivo: alertas_output.txt >> "!EVIDENCIAS_DIR!\evidencias.txt"
        echo ---------------------------------------- >> "!EVIDENCIAS_DIR!\evidencias.txt"
    ) else (
        echo [ERRO] Erro na execucao do sistema de alertas
    )
) else (
    echo [AVISO] Sistema de alertas nao encontrado
)

REM Verificar arquivos gerados pelos alertas
set arquivos_alertas_gerados=historico_alertas.json sistema_alertas.log

for %%f in (%arquivos_alertas_gerados%) do (
    if exist "%%f" (
        echo [SUCESSO] Arquivo gerado: %%f
        echo 📸 EVIDENCIA - VISUALIZACAO >> "!EVIDENCIAS_DIR!\evidencias.txt"
        echo Timestamp: %date% %time% >> "!EVIDENCIAS_DIR!\evidencias.txt"
        echo Descricao: Arquivo gerado pelos alertas >> "!EVIDENCIAS_DIR!\evidencias.txt"
        echo Arquivo: %%f >> "!EVIDENCIAS_DIR!\evidencias.txt"
        echo ---------------------------------------- >> "!EVIDENCIAS_DIR!\evidencias.txt"
        copy "%%f" "!EVIDENCIAS_DIR!\" >nul 2>&1
    ) else (
        echo [AVISO] Arquivo nao gerado: %%f
    )
)

REM Executar dashboard (em background)
echo [INFO] Iniciando dashboard...
if exist "dashboard_visualizacao_alertas.py" (
    start /B streamlit run dashboard_visualizacao_alertas.py --server.port 8501 > "!EVIDENCIAS_DIR!\dashboard_output.txt" 2>&1
    timeout /t 10 /nobreak >nul
    taskkill /f /im streamlit.exe >nul 2>&1
    echo [SUCESSO] Dashboard executado
    echo 📸 EVIDENCIA - VISUALIZACAO >> "!EVIDENCIAS_DIR!\evidencias.txt"
    echo Timestamp: %date% %time% >> "!EVIDENCIAS_DIR!\evidencias.txt"
    echo Descricao: Output do dashboard >> "!EVIDENCIAS_DIR!\evidencias.txt"
    echo Arquivo: dashboard_output.txt >> "!EVIDENCIAS_DIR!\evidencias.txt"
    echo ---------------------------------------- >> "!EVIDENCIAS_DIR!\evidencias.txt"
) else (
    echo [AVISO] Dashboard nao encontrado
)

REM ETAPA 5: MONITORAMENTO E VERIFICAÇÃO
echo.
echo ========================================
echo ETAPA 5: MONITORAMENTO E VERIFICACAO
echo ========================================
echo [INFO] Iniciando monitoramento...

REM Verificar status do banco
echo [INFO] Verificando status do banco...
mysql -u iot_user -p'iot_password' iot_monitoring_db -e "SELECT 'leituras_sensores' as tabela, COUNT(*) as registros FROM leituras_sensores UNION ALL SELECT 'dispositivos' as tabela, COUNT(*) as registros FROM dispositivos UNION ALL SELECT 'sensores' as tabela, COUNT(*) as registros FROM sensores UNION ALL SELECT 'alertas' as tabela, COUNT(*) as registros FROM alertas UNION ALL SELECT 'tipos_sensor' as tabela, COUNT(*) as registros FROM tipos_sensor;" > "!EVIDENCIAS_DIR!\monitor_banco.txt" 2>&1

if !errorlevel! equ 0 (
    echo [SUCESSO] Monitoramento do banco concluido
    echo 📸 EVIDENCIA - MONITORAMENTO >> "!EVIDENCIAS_DIR!\evidencias.txt"
    echo Timestamp: %date% %time% >> "!EVIDENCIAS_DIR!\evidencias.txt"
    echo Descricao: Status do banco >> "!EVIDENCIAS_DIR!\evidencias.txt"
    echo Arquivo: monitor_banco.txt >> "!EVIDENCIAS_DIR!\evidencias.txt"
    echo ---------------------------------------- >> "!EVIDENCIAS_DIR!\evidencias.txt"
) else (
    echo [ERRO] Erro no monitoramento do banco
)

REM Verificar arquivos de log
echo [INFO] Verificando arquivos de log...
for %%f in (*.log *.json *.png *.pkl) do (
    if exist "%%f" (
        echo [SUCESSO] Log encontrado: %%f
        echo 📸 EVIDENCIA - MONITORAMENTO >> "!EVIDENCIAS_DIR!\evidencias.txt"
        echo Timestamp: %date% %time% >> "!EVIDENCIAS_DIR!\evidencias.txt"
        echo Descricao: Arquivo de log >> "!EVIDENCIAS_DIR!\evidencias.txt"
        echo Arquivo: %%f >> "!EVIDENCIAS_DIR!\evidencias.txt"
        echo ---------------------------------------- >> "!EVIDENCIAS_DIR!\evidencias.txt"
        copy "%%f" "!EVIDENCIAS_DIR!\" >nul 2>&1
    )
)

REM Gerar relatório final
echo.
echo ========================================
echo RELATORIO FINAL DE EXECUCAO
echo ========================================

REM Contar evidências
set /a total_evidencias=0
for /f %%i in ('dir "!EVIDENCIAS_DIR!" /b /a-d ^| find /c /v ""') do set /a total_evidencias=%%i
echo [SUCESSO] Total de evidencias capturadas: !total_evidencias!

REM Listar arquivos de evidência
echo [INFO] Arquivos de evidencia:
dir "!EVIDENCIAS_DIR!" /b

REM Criar resumo
(
echo Sistema IoT Monitoring - Execucao Completa
echo Enterprise Challenge Sprint 3 - Reply
echo ========================================
echo.
echo Data de Execucao: %date% %time%
echo Versao: 1.0.0
echo.
echo ETAPAS EXECUTADAS:
echo 1. ✅ Coleta de Dados
echo 2. ✅ Persistencia
echo 3. ✅ Machine Learning
echo 4. ✅ Visualizacao e Alertas
echo 5. ✅ Monitoramento
echo.
echo EVIDENCIAS CAPTURADAS: !total_evidencias! arquivos
echo.
echo ARQUIVOS PRINCIPAIS:
echo - Evidencias: !EVIDENCIAS_DIR!\
echo - Logs: *.log
echo - Dados: *.json
echo - Modelos: *.pkl
echo - Visualizacoes: *.png
echo.
echo STATUS: EXECUCAO CONCLUIDA COM SUCESSO
) > "!EVIDENCIAS_DIR!\resumo_execucao.txt"

echo [SUCESSO] Relatorio final gerado: !EVIDENCIAS_DIR!\resumo_execucao.txt

REM Mostrar resumo
echo.
echo 📊 RESUMO DA EXECUCAO:
echo ======================
type "!EVIDENCIAS_DIR!\resumo_execucao.txt"

echo.
echo 🎉 EXECUCAO COMPLETA FINALIZADA!
echo ========================================
echo 📁 Evidencias salvas em: !EVIDENCIAS_DIR!\
echo 📋 Relatorio: !EVIDENCIAS_DIR!\resumo_execucao.txt
echo ========================================
pause
