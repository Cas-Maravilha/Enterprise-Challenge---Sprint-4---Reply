#!/bin/bash

echo "========================================"
echo "Dashboard e Alertas - Sistema IoT"
echo "Enterprise Challenge Sprint 3 - Reply"
echo "========================================"
echo

echo "Instalando dependências..."
pip install streamlit pandas matplotlib seaborn plotly mysql-connector-python numpy

echo
echo "Escolha uma opção:"
echo "1. Executar Dashboard Streamlit"
echo "2. Executar Sistema de Alertas"
echo "3. Executar ambos"
echo "4. Visualizar relatórios existentes"
echo

read -p "Digite sua opção (1-4): " opcao

case $opcao in
    1)
        echo
        echo "Executando Dashboard Streamlit..."
        streamlit run dashboard_visualizacao_alertas.py
        echo
        echo "Dashboard executado!"
        ;;
    2)
        echo
        echo "Executando Sistema de Alertas..."
        python3 sistema_alertas_avancado.py
        echo
        echo "Sistema de alertas executado!"
        ;;
    3)
        echo
        echo "Executando ambos..."
        echo
        echo "1. Iniciando Dashboard em background..."
        streamlit run dashboard_visualizacao_alertas.py &
        echo
        echo "2. Executando Sistema de Alertas..."
        python3 sistema_alertas_avancado.py
        echo
        echo "Ambos executados!"
        ;;
    4)
        echo
        echo "Visualizando relatórios existentes..."
        if [ -f "historico_alertas.json" ]; then
            echo "Abrindo histórico de alertas..."
            xdg-open historico_alertas.json
        else
            echo "Arquivo de histórico não encontrado!"
        fi
        if [ -f "sistema_alertas.log" ]; then
            echo "Abrindo log de alertas..."
            xdg-open sistema_alertas.log
        else
            echo "Arquivo de log não encontrado!"
        fi
        echo
        echo "Relatórios abertos!"
        ;;
    *)
        echo
        echo "Opção inválida!"
        ;;
esac

echo
echo "Processo concluído!"
