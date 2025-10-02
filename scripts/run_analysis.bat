@echo off
REM Script para executar a análise e visualização dos dados

echo === Análise e Visualização de Dados de Sensores Industriais ===
echo.

REM Verificar se o diretório de dados existe
if not exist "data" (
    echo Diretório de dados não encontrado. Gerando dados simulados...
    python src/scenario_simulator.py --scenario all --samples 100 --output-dir data
)

REM Criar diretório para resultados
if not exist "analysis_results" mkdir analysis_results

REM Encontrar o arquivo CSV mais recente no diretório data
for /f "delims=" %%i in ('dir /b /od data\*.csv') do set LATEST_CSV=%%i

REM Executar análise estatística e visualização
echo Executando análise estatística e visualização...
echo Usando arquivo: data\%LATEST_CSV%
python src/sensor_analytics.py --input data\%LATEST_CSV% --output-dir analysis_results

REM Executar detecção de anomalias
echo.
echo Executando detecção de anomalias...
python src/anomaly_detection.py --input data\normal_*.csv --output-dir analysis_results\anomalies --method zscore
python src/anomaly_detection.py --input data\alert_*.csv --output-dir analysis_results\anomalies --method isolation_forest
python src/anomaly_detection.py --input data\failure_*.csv --output-dir analysis_results\anomalies --method multivariate

echo.
echo Análise concluída! Os resultados estão disponíveis em:
echo - Análise e visualização: ./analysis_results/
echo - Detecção de anomalias: ./analysis_results/anomalies/
echo.
echo Para iniciar o dashboard interativo, execute:
echo python src/interactive_dashboard.py
echo.

pause