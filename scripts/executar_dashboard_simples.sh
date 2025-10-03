#!/bin/bash

echo "========================================"
echo "DASHBOARD COMPLETO - LINUX/MAC"
echo "Sistema IoT Monitoring - Sprint 3"
echo "========================================"
echo

echo "Verificando dependências..."
python3 -c "import flask, plotly, matplotlib, seaborn, jinja2, schedule, pandas, numpy" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Instalando dependências..."
    pip3 install flask plotly matplotlib seaborn jinja2 schedule pandas numpy
fi

echo
echo "Criando diretórios necessários..."
mkdir -p templates relatorios modelos

echo
echo "Iniciando Sistema de Dashboard..."
echo

echo "[1/4] Executando teste do sistema..."
python3 executar_dashboard_completo.py --modo teste
if [ $? -ne 0 ]; then
    echo "ERRO: Teste do sistema falhou"
    exit 1
fi

echo
echo "[2/4] Verificando status do sistema..."
python3 executar_dashboard_completo.py --modo status

echo
echo "[3/4] Gerando relatório de exemplo..."
python3 executar_dashboard_completo.py --tipo-relatorio diario

echo
echo "[4/4] Iniciando dashboard completo..."
echo "Dashboard disponível em: http://localhost:5000"
echo "Pressione Ctrl+C para parar"
echo

python3 executar_dashboard_completo.py --modo completo

echo
echo "Sistema parado."
