@echo off
setlocal enabledelayedexpansion

echo ========================================
echo Setup Sistema IoT Monitoring Completo
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

echo [INFO] Iniciando setup do sistema...

REM 1. Verificar Python
echo [INFO] Verificando Python...
python --version >nul 2>&1
if %errorlevel% equ 0 (
    for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
    echo [SUCESSO] Python encontrado: !PYTHON_VERSION!
) else (
    echo [ERRO] Python nao encontrado. Instale Python 3.8+
    pause
    exit /b 1
)

REM 2. Verificar pip
echo [INFO] Verificando pip...
pip --version >nul 2>&1
if %errorlevel% equ 0 (
    echo [SUCESSO] pip encontrado
) else (
    echo [ERRO] pip nao encontrado. Instale pip
    pause
    exit /b 1
)

REM 3. Criar ambiente virtual
echo [INFO] Criando ambiente virtual...
if not exist "venv" (
    python -m venv venv
    echo [SUCESSO] Ambiente virtual criado
) else (
    echo [AVISO] Ambiente virtual ja existe
)

REM 4. Ativar ambiente virtual
echo [INFO] Ativando ambiente virtual...
call venv\Scripts\activate.bat
echo [SUCESSO] Ambiente virtual ativado

REM 5. Atualizar pip
echo [INFO] Atualizando pip...
python -m pip install --upgrade pip
echo [SUCESSO] pip atualizado

REM 6. Instalar dependências
echo [INFO] Instalando dependencias Python...
if exist "requirements.txt" (
    pip install -r requirements.txt
    echo [SUCESSO] Dependencias Python instaladas
) else (
    echo [AVISO] Arquivo requirements.txt nao encontrado
    echo [INFO] Instalando dependencias basicas...
    pip install pandas numpy matplotlib seaborn plotly mysql-connector-python streamlit scikit-learn
    echo [SUCESSO] Dependencias basicas instaladas
)

REM 7. Criar diretórios necessários
echo [INFO] Criando diretorios...
if not exist "logs" mkdir logs
if not exist "data" mkdir data
if not exist "models" mkdir models
if not exist "configs" mkdir configs
if not exist "screenshots" mkdir screenshots
if not exist "reports" mkdir reports
echo [SUCESSO] Diretorios criados

REM 8. Verificar MySQL
echo [INFO] Verificando MySQL...
mysql --version >nul 2>&1
if %errorlevel% equ 0 (
    for /f "tokens=3" %%i in ('mysql --version 2^>^&1') do set MYSQL_VERSION=%%i
    echo [SUCESSO] MySQL encontrado: !MYSQL_VERSION!
) else (
    echo [AVISO] MySQL nao encontrado. Instale MySQL 8.0+
    echo [INFO] Para Windows: Baixe do site oficial do MySQL
)

REM 9. Verificar Git
echo [INFO] Verificando Git...
git --version >nul 2>&1
if %errorlevel% equ 0 (
    for /f "tokens=3" %%i in ('git --version 2^>^&1') do set GIT_VERSION=%%i
    echo [SUCESSO] Git encontrado: !GIT_VERSION!
) else (
    echo [AVISO] Git nao encontrado. Instale Git
)

REM 10. Criar arquivos de configuração
echo [INFO] Criando arquivos de configuracao...

REM Configuração do banco
(
echo {
echo   "host": "localhost",
echo   "user": "iot_user",
echo   "password": "iot_password",
echo   "database": "iot_monitoring_db",
echo   "port": 3306,
echo   "charset": "utf8mb4",
echo   "pool_size": 10,
echo   "timeout": 30
echo }
) > configs\database.json

REM Configuração MQTT
(
echo {
echo   "broker": "broker.hivemq.com",
echo   "port": 1883,
echo   "topic_base": "industrial/sensors",
echo   "qos": 1,
echo   "keepalive": 60,
echo   "retain": true
echo }
) > configs\mqtt.json

REM Configuração de sensores
(
echo {
echo   "dht22": {
echo     "pino": 4,
echo     "tipo": "temperatura_umidade",
echo     "intervalo": 1000
echo   },
echo   "ldr": {
echo     "pino": 34,
echo     "tipo": "luminosidade",
echo     "intervalo": 1000
echo   },
echo   "pir": {
echo     "pino": 2,
echo     "tipo": "movimento",
echo     "intervalo": 1000
echo   }
echo }
) > configs\sensores.json

REM Configuração de thresholds
(
echo {
echo   "temperatura": {
echo     "max": 30.0,
echo     "min": 15.0,
echo     "critico_max": 35.0,
echo     "critico_min": 10.0
echo   },
echo   "umidade": {
echo     "max": 80.0,
echo     "min": 30.0,
echo     "critico_max": 90.0,
echo     "critico_min": 20.0
echo   },
echo   "luminosidade": {
echo     "max": 800.0,
echo     "min": 50.0,
echo     "critico_max": 1000.0,
echo     "critico_min": 10.0
echo   }
echo }
) > configs\thresholds.json

REM Configuração ML
(
echo {
echo   "modelos": {
echo     "anomalia": {
echo       "algoritmo": "RandomForestClassifier",
echo       "n_estimators": 100,
echo       "max_depth": 10,
echo       "test_size": 0.2
echo     },
echo     "temperatura": {
echo       "algoritmo": "RandomForestRegressor",
echo       "n_estimators": 100,
echo       "max_depth": 10,
echo       "test_size": 0.2
echo     }
echo   },
echo   "features": {
echo     "anomalia": ["valor_atual", "valor_anterior", "media_movel", "std_movel", "tendencia"],
echo     "temperatura": ["hora", "dia_semana", "dia_mes", "valor_anterior", "media_movel"]
echo   }
echo }
) > configs\ml.json

echo [SUCESSO] Arquivos de configuracao criados

REM 11. Criar script de verificação
echo [INFO] Criando script de verificacao...
(
echo #!/usr/bin/env python3
echo """
echo Verificador de Setup - Sistema IoT Monitoring
echo Enterprise Challenge Sprint 3 - Reply
echo """
echo 
echo import sys
echo import os
echo import json
echo import importlib
echo 
echo def verificar_dependencias^(^):
echo     """Verifica se todas as dependencias estao instaladas"""
echo     dependencias = [
echo         'pandas', 'numpy', 'matplotlib', 'seaborn', 
echo         'plotly', 'mysql.connector', 'streamlit', 'sklearn'
echo     ]
echo     
echo     faltando = []
echo     for dep in dependencias:
echo         try:
echo             if dep == 'mysql.connector':
echo                 importlib.import_module^('mysql.connector'^)
echo             else:
echo                 importlib.import_module^(dep^)
echo             print^(f"✅ {dep}"^)
echo         except ImportError:
echo             print^(f"❌ {dep}"^)
echo             faltando.append^(dep^)
echo     
echo     return len^(faltando^) == 0, faltando
echo 
echo def verificar_arquivos^(^):
echo     """Verifica se os arquivos necessarios existem"""
echo     arquivos_necessarios = [
echo         'README.md',
echo         'requirements.txt',
echo         'criar_tabelas_iot.sql',
echo         'ml_basico_integrado.py',
echo         'dashboard_visualizacao_alertas.py',
echo         'sistema_alertas_avancado.py'
echo     ]
echo     
echo     faltando = []
echo     for arquivo in arquivos_necessarios:
echo         if os.path.exists^(arquivo^):
echo             print^(f"✅ {arquivo}"^)
echo         else:
echo             print^(f"❌ {arquivo}"^)
echo             faltando.append^(arquivo^)
echo     
echo     return len^(faltando^) == 0, faltando
echo 
echo def verificar_diretorios^(^):
echo     """Verifica se os diretorios necessarios existem"""
echo     diretorios_necessarios = [
echo         'logs', 'data', 'models', 'configs', 'screenshots', 'reports'
echo     ]
echo     
echo     faltando = []
echo     for diretorio in diretorios_necessarios:
echo         if os.path.exists^(diretorio^):
echo             print^(f"✅ {diretorio}/"^)
echo         else:
echo             print^(f"❌ {diretorio}/"^)
echo             faltando.append^(diretorio^)
echo     
echo     return len^(faltando^) == 0, faltando
echo 
echo def main^(^):
echo     print^("=== Verificacao de Setup ==="^)
echo     print^("Enterprise Challenge Sprint 3 - Reply"^)
echo     print^("============================="^)
echo     
echo     print^("\n📦 Verificando dependencias Python..."^)
echo     deps_ok, deps_faltando = verificar_dependencias^(^)
echo     
echo     print^("\n📁 Verificando arquivos necessarios..."^)
echo     arquivos_ok, arquivos_faltando = verificar_arquivos^(^)
echo     
echo     print^("\n📂 Verificando diretorios necessarios..."^)
echo     dirs_ok, dirs_faltando = verificar_diretorios^(^)
echo     
echo     print^("\n📊 Resumo da Verificacao:"^)
echo     print^(f"Dependencias: {'✅ OK' if deps_ok else '❌ Faltando'}"^)
echo     print^(f"Arquivos: {'✅ OK' if arquivos_ok else '❌ Faltando'}"^)
echo     print^(f"Diretorios: {'✅ OK' if dirs_ok else '❌ Faltando'}"^)
echo     
echo     if deps_ok and arquivos_ok and dirs_ok:
echo         print^("\n🎉 Setup verificado com sucesso!"^)
echo         return 0
echo     else:
echo         print^("\n⚠️  Setup incompleto. Verifique os itens faltando."^)
echo         if deps_faltando:
echo             print^(f"Dependencias faltando: {', '.join^(deps_faltando^)}"^)
echo         if arquivos_faltando:
echo             print^(f"Arquivos faltando: {', '.join^(arquivos_faltando^)}"^)
echo         if dirs_faltando:
echo             print^(f"Diretorios faltando: {', '.join^(dirs_faltando^)}"^)
echo         return 1
echo 
echo if __name__ == "__main__":
echo     sys.exit^(main^(^)^)
) > verificar_setup.py

echo [SUCESSO] Script de verificacao criado

REM 12. Executar verificação
echo [INFO] Executando verificacao de setup...
python verificar_setup.py

REM 13. Criar arquivo de versão
echo [INFO] Criando arquivo de versao...
(
echo Sistema IoT Monitoring
echo Enterprise Challenge Sprint 3 - Reply
echo Versao: 1.0.0
echo Data de Setup: %date% %time%
echo Python: 
python --version
echo Sistema: Windows
) > VERSION

echo [SUCESSO] Arquivo de versao criado

REM 14. Resumo final
echo.
echo ========================================
echo 🎉 SETUP CONCLUIDO COM SUCESSO!
echo ========================================
echo.
echo 📋 Proximos passos:
echo 1. Configure o banco de dados:
echo    mysql -u root -p ^< criar_tabelas_iot.sql
echo.
echo 2. Execute o fluxo completo:
echo    executar_fluxo_completo.bat
echo.
echo 3. Ou execute etapas individuais:
echo    etapa_1_coleta.bat simulacao
echo    etapa_2_persistencia.bat
echo    etapa_3_ml.bat
echo    etapa_4_visualizacao.bat
echo.
echo 📚 Documentacao:
echo    README_REPRODUTIBILIDADE_COMPLETA.md
echo.
echo 🔧 Verificacao:
echo    python verificar_setup.py
echo.
echo ========================================
pause
