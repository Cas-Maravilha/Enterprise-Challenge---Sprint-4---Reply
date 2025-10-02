#!/bin/bash

echo "========================================"
echo "ML Básico Integrado - Sistema IoT"
echo "Enterprise Challenge Sprint 3 - Reply"
echo "========================================"
echo

echo "Instalando dependências..."
pip install pandas matplotlib seaborn scikit-learn numpy mysql-connector-python joblib

echo
echo "Escolha uma opção:"
echo "1. Executar ML básico integrado"
echo "2. Analisar dataset ML"
echo "3. Executar ambos"
echo "4. Visualizar resultados existentes"
echo

read -p "Digite sua opção (1-4): " opcao

case $opcao in
    1)
        echo
        echo "Executando ML básico integrado..."
        python3 ml_basico_integrado.py
        echo
        echo "ML básico executado!"
        ;;
    2)
        echo
        echo "Analisando dataset ML..."
        python3 dataset_ml_analisador.py
        echo
        echo "Análise do dataset concluída!"
        ;;
    3)
        echo
        echo "Executando ambos..."
        echo
        echo "1. Analisando dataset..."
        python3 dataset_ml_analisador.py
        echo
        echo "2. Executando ML básico..."
        python3 ml_basico_integrado.py
        echo
        echo "Ambos executados com sucesso!"
        ;;
    4)
        echo
        echo "Visualizando resultados existentes..."
        if [ -f "ml_basico_visualizacoes.png" ]; then
            echo "Abrindo visualizações ML..."
            xdg-open ml_basico_visualizacoes.png
        else
            echo "Arquivo de visualizações não encontrado!"
        fi
        if [ -f "analise_dataset_ml.png" ]; then
            echo "Abrindo análise do dataset..."
            xdg-open analise_dataset_ml.png
        else
            echo "Arquivo de análise do dataset não encontrado!"
        fi
        echo
        echo "Visualizações abertas!"
        ;;
    *)
        echo
        echo "Opção inválida!"
        ;;
esac

echo
echo "Processo concluído!"
