@echo off
REM Script para executar a simulação completa de coleta de dados

echo === Simulação de Coleta de Dados Estruturada ===
echo.

REM Criar diretórios necessários
if not exist "data" mkdir data
if not exist "analysis" mkdir analysis

REM Gerar dados simulados para todos os cenários
echo Gerando dados simulados para todos os cenários...
python src/scenario_simulator.py --scenario all --samples 100 --interval 1.0 --output-dir data --anomalies

REM Analisar os dados gerados
echo.
echo Analisando os dados simulados...
python src/data_analyzer.py --input data --output-dir analysis

echo.
echo Simulação concluída! Os resultados estão disponíveis em:
echo - Dados brutos: ./data/
echo - Análises e gráficos: ./analysis/
echo.

pause