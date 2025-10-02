#!/bin/bash

echo "========================================"
echo "PERSISTENCIA BANCO RELACIONAL - LINUX/MAC"
echo "Sistema IoT Monitoring - Sprint 3"
echo "========================================"
echo

echo "Verificando dependências..."
python3 -c "import mysql.connector, paho.mqtt.client, pandas, numpy" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Instalando dependências..."
    pip3 install mysql-connector-python paho-mqtt pandas numpy
fi

echo
echo "Verificando banco de dados..."
mysql -u root -p -e "USE iot_monitoring_db;" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Criando banco de dados..."
    mysql -u root -p < criar_tabelas_iot.sql
fi

echo
echo "Iniciando Sistema de Persistência..."
echo

echo "[1/2] Executando teste de persistência..."
python3 executar_persistencia_completa.py --teste
if [ $? -ne 0 ]; then
    echo "ERRO: Teste de persistência falhou"
    exit 1
fi

echo
echo "[2/2] Iniciando sistema completo..."
echo "Pressione Ctrl+C para parar"
echo

python3 executar_persistencia_completa.py --modo desenvolvimento

echo
echo "Sistema parado."

