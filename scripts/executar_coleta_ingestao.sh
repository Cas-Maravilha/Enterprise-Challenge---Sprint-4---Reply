#!/bin/bash

echo "========================================"
echo "Coleta e Ingestão ESP32 - Sistema IoT"
echo "Enterprise Challenge Sprint 3 - Reply"
echo "========================================"
echo

echo "Instalando dependências..."
pip install pandas matplotlib numpy pyserial

echo
echo "Escolha uma opção:"
echo "1. Coletar dados via Serial (ESP32 real)"
echo "2. Simular dados (sem hardware)"
echo "3. Visualizar dados existentes"
echo

read -p "Digite sua opção (1-3): " opcao

case $opcao in
    1)
        echo
        echo "Executando coleta via Serial..."
        python3 coletor_dados_serial.py
        ;;
    2)
        echo
        echo "Executando simulação de dados..."
        python3 simulador_dados_esp32.py
        ;;
    3)
        echo
        echo "Visualizando dados existentes..."
        python3 visualizar_dados_coletados.py
        ;;
    *)
        echo
        echo "Opção inválida!"
        ;;
esac

echo
echo "Processo concluído!"
