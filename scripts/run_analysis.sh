#!/bin/bash
# Script para executar a análise e visualização dos dados

echo "=== Análise e Visualização de Dados de Sensores Industriais ==="
echo

# Verificar se o diretório de dados existe
if [ ! -d "data" ]; then
    echo "Diretório de dados não encontrado. Gerando dados simulados..."
    python3 src/scenario_simulator.py --scenario all --samples 100 --output-dir data
fi

# Criar diretório para resultados
mkdir -p analysis_results

# Executar análise estatística e visualização
echo "Executando análise estatística e visualização..."
python3 src/sensor_analytics.py --input data --output-dir analysis_results

# Executar detecção de anomalias
echo
echo "Executando detecção de anomalias..."
python3 src/anomaly_detection.py --input data/normal_*.csv --output-dir analysis_results/anomalies --method zscore
python3 src/anomaly_detection.py --input data/alert_*.csv --output-dir analysis_results/anomalies --method isolation_forest
python3 src/anomaly_detection.py --input data/failure_*.csv --output-dir analysis_results/anomalies --method multivariate

echo
echo "Análise concluída! Os resultados estão disponíveis em:"
echo "- Análise e visualização: ./analysis_results/"
echo "- Detecção de anomalias: ./analysis_results/anomalies/"
echo
echo "Para iniciar o dashboard interativo, execute:"
echo "python3 src/interactive_dashboard.py"
echo