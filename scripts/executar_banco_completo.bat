@echo off
echo ========================================
echo Sistema de Banco de Dados IoT Monitoring
echo Enterprise Challenge Sprint 3 - Reply
echo ========================================
echo.

echo Escolha uma opcao:
echo 1. Criar banco de dados e tabelas
echo 2. Carregar dados de exemplo
echo 3. Executar testes de integridade
echo 4. Executar todas as operacoes
echo 5. Visualizar estatisticas do banco
echo.

set /p opcao="Digite sua opcao (1-5): "

if "%opcao%"=="1" (
    echo.
    echo Executando criacao do banco de dados...
    mysql -u root -p < criar_tabelas_iot.sql
    echo.
    echo Banco de dados criado com sucesso!
) else if "%opcao%"=="2" (
    echo.
    echo Executando carga de dados...
    mysql -u root -p < carga_dados_iot.sql
    echo.
    echo Dados carregados com sucesso!
) else if "%opcao%"=="3" (
    echo.
    echo Executando testes de integridade...
    python testes_integridade_banco.py
    echo.
    echo Testes concluidos!
) else if "%opcao%"=="4" (
    echo.
    echo Executando todas as operacoes...
    echo.
    echo 1. Criando banco de dados...
    mysql -u root -p < criar_tabelas_iot.sql
    echo.
    echo 2. Carregando dados...
    mysql -u root -p < carga_dados_iot.sql
    echo.
    echo 3. Executando testes...
    python testes_integridade_banco.py
    echo.
    echo Todas as operacoes concluidas!
) else if "%opcao%"=="5" (
    echo.
    echo Visualizando estatisticas do banco...
    mysql -u root -p -e "USE iot_monitoring_db; SELECT 'Dispositivos' as tabela, COUNT(*) as total FROM dispositivos UNION ALL SELECT 'Sensores', COUNT(*) FROM sensores UNION ALL SELECT 'Leituras', COUNT(*) FROM leituras_sensores UNION ALL SELECT 'Alertas', COUNT(*) FROM alertas UNION ALL SELECT 'Usuarios', COUNT(*) FROM usuarios;"
    echo.
    echo Estatisticas exibidas!
) else (
    echo.
    echo Opcao invalida!
)

echo.
echo Processo concluido!
pause
