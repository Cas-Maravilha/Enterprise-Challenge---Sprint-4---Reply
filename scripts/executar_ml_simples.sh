#!/bin/bash

echo "========================================"
echo "SISTEMA ML COMPLETO - LINUX/MAC"
echo "Sistema IoT Monitoring - Sprint 3"
echo "========================================"
echo

echo "Verificando dependências..."
python3 -c "import sklearn, pandas, numpy, joblib, paho.mqtt.client, mysql.connector" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Instalando dependências..."
    pip3 install scikit-learn pandas numpy joblib paho-mqtt mysql-connector-python
fi

echo
echo "Criando diretório de modelos..."
mkdir -p modelos

echo
echo "Iniciando Sistema ML Completo..."
echo

echo "[1/4] Executando teste do sistema..."
python3 executar_ml_completo.py --modo teste
if [ $? -ne 0 ]; then
    echo "ERRO: Teste do sistema falhou"
    exit 1
fi

echo
echo "[2/4] Executando demonstração..."
python3 executar_ml_completo.py --modo demo

echo
echo "[3/4] Iniciando sistema integrado..."
echo "Pressione Ctrl+C para parar"
echo

python3 executar_ml_completo.py --modo integrado

echo
echo "Sistema parado."

