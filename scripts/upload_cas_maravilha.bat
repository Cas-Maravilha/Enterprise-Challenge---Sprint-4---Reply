@echo off
REM =====================================================
REM SCRIPT BATCH - UPLOAD PARA GITHUB CAS-MARAVILHA
REM Enterprise Challenge - Sprint 3 - Reply
REM =====================================================

echo.
echo 🚀 UPLOAD PARA GITHUB - CAS-MARAVILHA
echo =====================================
echo.

REM Verificar se estamos no diretório correto
if not exist "README.md" (
    echo ❌ ERRO: README.md não encontrado!
    echo    Certifique-se de estar no diretório do projeto.
    echo    Diretório atual: %CD%
    pause
    exit /b 1
)

echo ✅ Diretório do projeto encontrado!
echo    Localização: %CD%
echo.

REM Verificar se Git está instalado
git --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERRO: Git não está instalado ou não está no PATH!
    echo    Instale o Git em: https://git-scm.com/
    pause
    exit /b 1
)

echo ✅ Git encontrado!
echo.

REM Verificar se já é um repositório Git
if not exist ".git" (
    echo 📁 Inicializando repositório Git...
    git init
    if errorlevel 1 (
        echo ❌ ERRO: Falha ao inicializar repositório Git!
        pause
        exit /b 1
    )
    echo ✅ Repositório Git inicializado!
) else (
    echo ✅ Repositório Git já existe!
)

echo.
echo 📊 Verificando status do Git...
git status
echo.

REM Perguntar se deseja continuar
set /p continuar="Deseja continuar com o upload? (s/n): "
if /i not "%continuar%"=="s" (
    echo ❌ Upload cancelado pelo usuário.
    pause
    exit /b 0
)

echo.
echo 🔄 Iniciando processo de upload...
echo.

REM Adicionar todos os arquivos
echo 📁 Adicionando arquivos...
git add .
if errorlevel 1 (
    echo ❌ ERRO: Falha ao adicionar arquivos!
    pause
    exit /b 1
)
echo ✅ Arquivos adicionados com sucesso!

echo.
echo 📝 Fazendo commit...
git commit -m "🚀 Sprint 3: Sistema IoT Monitoring Completo

- ✅ Atualizado nome do projeto para Sprint 3
- ✅ Implementado sistema completo de KPIs de negócio
- ✅ Adicionado dashboard executivo (9 gráficos)
- ✅ Criado documentação técnica completa
- ✅ Adicionado link do YouTube para demonstração
- ✅ Performance ML: 95.2%% accuracy, 91.8%% precision
- ✅ Banco de dados: 11 tabelas normalizadas
- ✅ Visualizações: 8+ gráficos profissionais
- ✅ Automação: Scripts para diferentes SO
- ✅ Documentação: READMEs e guias completos"

if errorlevel 1 (
    echo ❌ ERRO: Falha ao fazer commit!
    pause
    exit /b 1
)
echo ✅ Commit realizado com sucesso!

echo.
echo 🌐 Configurando repositório remoto...
git remote add origin https://github.com/Cas-Maravilha/Enterprise-Challenge-Sprint-4-Reply.git
if errorlevel 1 (
    echo ⚠️  AVISO: Repositório remoto já existe ou erro na configuração.
    echo    Tentando continuar...
)

echo.
echo 🚀 Fazendo push para o GitHub...
git push -u origin main
if errorlevel 1 (
    echo ❌ ERRO: Falha ao fazer push!
    echo    Possíveis causas:
    echo    - Repositório não existe no GitHub
    echo    - Problemas de autenticação
    echo    - Conflitos de branch
    echo.
    echo    Soluções:
    echo    1. Crie o repositório em: https://github.com/new
    echo    2. Nome: Enterprise-Challenge-Sprint-4-Reply
    echo    3. Execute este script novamente
    pause
    exit /b 1
)

echo.
echo ✅ UPLOAD CONCLUÍDO COM SUCESSO!
echo =====================================================
echo.
echo 📊 Resumo do Upload:
echo    • Usuário: Cas-Maravilha
echo    • Repositório: Enterprise-Challenge-Sprint-4-Reply
echo    • Branch: main
echo    • Status: Atualizado
echo.
echo 🌐 Acesse seu repositório:
echo    https://github.com/Cas-Maravilha/Enterprise-Challenge-Sprint-4-Reply
echo.

REM Mostrar URL do repositório
git remote -v
echo.

echo 🎯 Próximos passos:
echo    1. Verifique o repositório no GitHub
echo    2. Confirme se todos os arquivos foram carregados
echo    3. Teste o link do YouTube no README
echo    4. Compartilhe o link do repositório
echo    5. Atualize seu perfil com o novo projeto
echo.

echo 📈 Diferenciais do seu projeto:
echo    • Sistema IoT Monitoring completo
echo    • Machine Learning com 95%%+ accuracy
echo    • Dashboard executivo integrado
echo    • Documentação técnica completa
echo    • Demonstração em vídeo no YouTube
echo.

pause
