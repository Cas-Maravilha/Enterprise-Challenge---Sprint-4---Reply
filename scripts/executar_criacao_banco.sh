#!/bin/bash
# =====================================================
# SCRIPT BASH - EXECUÇÃO DA CRIAÇÃO DO BANCO
# Sistema IoT Monitoring - Sprint 3
# Arquivo: executar_criacao_banco.sh
# Versão: 1.0
# Data: 2025-01-11
# =====================================================

echo ""
echo "====================================================="
echo "SISTEMA IoT MONITORING - CRIAÇÃO DO BANCO DE DADOS"
echo "====================================================="
echo ""

# Verificar se o MySQL está instalado
if ! command -v mysql &> /dev/null; then
    echo "ERRO: MySQL não encontrado!"
    echo "Por favor, instale o MySQL e adicione ao PATH"
    exit 1
fi

echo "MySQL encontrado! Versão:"
mysql --version
echo ""

# Solicitar credenciais do MySQL
read -p "Usuário MySQL (padrão: root): " MYSQL_USER
if [ -z "$MYSQL_USER" ]; then
    MYSQL_USER="root"
fi

read -s -p "Senha MySQL: " MYSQL_PASSWORD
echo ""

if [ -z "$MYSQL_PASSWORD" ]; then
    echo "Executando sem senha..."
    MYSQL_CMD="mysql -u $MYSQL_USER"
else
    MYSQL_CMD="mysql -u $MYSQL_USER -p$MYSQL_PASSWORD"
fi

echo ""
echo "====================================================="
echo "EXECUTANDO CRIAÇÃO DAS TABELAS"
echo "====================================================="
echo ""

# Executar script de criação das tabelas
echo "Executando: criar_tabelas_iot.sql"
$MYSQL_CMD < database/criar_tabelas_iot.sql
if [ $? -ne 0 ]; then
    echo "ERRO: Falha ao executar criar_tabelas_iot.sql"
    exit 1
fi

echo ""
echo "====================================================="
echo "EXECUTANDO INSERÇÃO DE DADOS DE EXEMPLO"
echo "====================================================="
echo ""

# Executar script de inserção de dados
echo "Executando: inserir_dados_exemplo.sql"
$MYSQL_CMD < database/inserir_dados_exemplo.sql
if [ $? -ne 0 ]; then
    echo "ERRO: Falha ao executar inserir_dados_exemplo.sql"
    exit 1
fi

echo ""
echo "====================================================="
echo "VERIFICANDO CRIAÇÃO DO BANCO"
echo "====================================================="
echo ""

# Verificar se as tabelas foram criadas
echo "Verificando tabelas criadas..."
$MYSQL_CMD -e "USE iot_monitoring_db; SHOW TABLES;"

echo ""
echo "====================================================="
echo "VERIFICANDO DADOS INSERIDOS"
echo "====================================================="
echo ""

# Verificar contagem de registros
echo "Contando registros inseridos..."
$MYSQL_CMD -e "USE iot_monitoring_db; SELECT 'Dispositivos' as Tabela, COUNT(*) as Registros FROM dispositivos UNION ALL SELECT 'Sensores', COUNT(*) FROM sensores UNION ALL SELECT 'Tipos Sensor', COUNT(*) FROM tipos_sensor UNION ALL SELECT 'Usuarios', COUNT(*) FROM usuarios UNION ALL SELECT 'Alertas', COUNT(*) FROM alertas UNION ALL SELECT 'Leituras', COUNT(*) FROM leituras_sensores;"

echo ""
echo "====================================================="
echo "SUCESSO!"
echo "====================================================="
echo ""
echo "Banco de dados 'iot_monitoring_db' criado com sucesso!"
echo ""
echo "Tabelas criadas:"
echo "- dispositivos"
echo "- tipos_sensor"
echo "- sensores"
echo "- leituras_sensores"
echo "- modos_operacao"
echo "- alertas"
echo "- configuracoes_limites"
echo "- usuarios"
echo "- logs_sistema"
echo "- dashboards"
echo "- relatorios"
echo ""
echo "Dados de exemplo inseridos:"
echo "- 6 dispositivos ESP32"
echo "- 50 sensores distribuídos"
echo "- 4 usuários com diferentes perfis"
echo "- Configurações de limites"
echo "- Dashboards e relatórios"
echo "- Logs e alertas de exemplo"
echo ""
echo "Para conectar ao banco:"
echo "mysql -u $MYSQL_USER -p iot_monitoring_db"
echo ""

read -p "Pressione Enter para continuar..."
