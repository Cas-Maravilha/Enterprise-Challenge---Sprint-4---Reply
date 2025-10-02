#!/bin/bash

echo "========================================"
echo "PIPELINE INTEGRADO ESP32 - LINUX/MAC"
echo "Sistema IoT Monitoring - Sprint 3"
echo "========================================"
echo

echo "Verificando dependências..."
python3 -c "import paho.mqtt.client, pandas, numpy, sklearn, matplotlib, seaborn, mysql.connector, joblib" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Instalando dependências..."
    pip3 install -r requirements.txt
fi

echo
echo "Iniciando Pipeline Integrado..."
echo

echo "[1/3] Iniciando Pipeline Principal..."
gnome-terminal --title="Pipeline Principal" -- bash -c "python3 pipeline_integrado_esp32.py; exec bash" 2>/dev/null || \
xterm -title "Pipeline Principal" -e "python3 pipeline_integrado_esp32.py; bash" 2>/dev/null || \
osascript -e 'tell app "Terminal" to do script "python3 pipeline_integrado_esp32.py"' 2>/dev/null || \
echo "Abra um terminal e execute: python3 pipeline_integrado_esp32.py"

sleep 5

echo "[2/3] Iniciando Coletor de Dados Wokwi..."
gnome-terminal --title="Coletor Wokwi" -- bash -c "python3 coletor_dados_wokwi.py; exec bash" 2>/dev/null || \
xterm -title "Coletor Wokwi" -e "python3 coletor_dados_wokwi.py; bash" 2>/dev/null || \
osascript -e 'tell app "Terminal" to do script "python3 coletor_dados_wokwi.py"' 2>/dev/null || \
echo "Abra um terminal e execute: python3 coletor_dados_wokwi.py"

sleep 3

echo "[3/3] Iniciando Dashboard (opcional)..."
if [ -f "interactive_dashboard.py" ]; then
    gnome-terminal --title="Dashboard" -- bash -c "python3 interactive_dashboard.py; exec bash" 2>/dev/null || \
    xterm -title "Dashboard" -e "python3 interactive_dashboard.py; bash" 2>/dev/null || \
    osascript -e 'tell app "Terminal" to do script "python3 interactive_dashboard.py"' 2>/dev/null || \
    echo "Abra um terminal e execute: python3 interactive_dashboard.py"
else
    echo "Dashboard não encontrado. Continuando sem dashboard..."
fi

echo
echo "========================================"
echo "PIPELINE INICIADO COM SUCESSO!"
echo "========================================"
echo
echo "Componentes ativos:"
echo "- Pipeline Principal (Terminal 1)"
echo "- Coletor Wokwi (Terminal 2)"
echo "- Dashboard (Terminal 3, se disponível)"
echo
echo "Para parar o pipeline, feche todas as janelas de terminal."
echo
read -p "Pressione Enter para continuar..."
