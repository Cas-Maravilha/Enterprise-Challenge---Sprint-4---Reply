#!/bin/bash

echo "========================================"
echo "Sistema de Banco de Dados IoT Monitoring"
echo "Enterprise Challenge Sprint 3 - Reply"
echo "========================================"
echo

echo "Escolha uma opção:"
echo "1. Criar banco de dados e tabelas"
echo "2. Carregar dados de exemplo"
echo "3. Executar testes de integridade"
echo "4. Executar todas as operações"
echo "5. Visualizar estatísticas do banco"
echo

read -p "Digite sua opção (1-5): " opcao

case $opcao in
    1)
        echo
        echo "Executando criação do banco de dados..."
        mysql -u root -p < criar_tabelas_iot.sql
        echo
        echo "Banco de dados criado com sucesso!"
        ;;
    2)
        echo
        echo "Executando carga de dados..."
        mysql -u root -p < carga_dados_iot.sql
        echo
        echo "Dados carregados com sucesso!"
        ;;
    3)
        echo
        echo "Executando testes de integridade..."
        python3 testes_integridade_banco.py
        echo
        echo "Testes concluídos!"
        ;;
    4)
        echo
        echo "Executando todas as operações..."
        echo
        echo "1. Criando banco de dados..."
        mysql -u root -p < criar_tabelas_iot.sql
        echo
        echo "2. Carregando dados..."
        mysql -u root -p < carga_dados_iot.sql
        echo
        echo "3. Executando testes..."
        python3 testes_integridade_banco.py
        echo
        echo "Todas as operações concluídas!"
        ;;
    5)
        echo
        echo "Visualizando estatísticas do banco..."
        mysql -u root -p -e "USE iot_monitoring_db; SELECT 'Dispositivos' as tabela, COUNT(*) as total FROM dispositivos UNION ALL SELECT 'Sensores', COUNT(*) FROM sensores UNION ALL SELECT 'Leituras', COUNT(*) FROM leituras_sensores UNION ALL SELECT 'Alertas', COUNT(*) FROM alertas UNION ALL SELECT 'Usuarios', COUNT(*) FROM usuarios;"
        echo
        echo "Estatísticas exibidas!"
        ;;
    *)
        echo
        echo "Opção inválida!"
        ;;
esac

echo
echo "Processo concluído!"
