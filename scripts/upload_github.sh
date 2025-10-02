#!/bin/bash
# =====================================================
# SCRIPT BASH - UPLOAD PARA GITHUB
# Enterprise Challenge - Sprint 3 - Reply
# =====================================================

echo ""
echo "🚀 UPLOAD PARA GITHUB - ENTERPRISE CHALLENGE SPRINT 3"
echo "====================================================="
echo ""

# Verificar se estamos no diretório correto
if [ ! -f "README.md" ]; then
    echo "❌ ERRO: README.md não encontrado!"
    echo "   Certifique-se de estar no diretório do projeto."
    exit 1
fi

echo "✅ Diretório do projeto encontrado!"
echo ""

# Verificar se Git está instalado
if ! command -v git &> /dev/null; then
    echo "❌ ERRO: Git não está instalado!"
    echo "   Instale o Git: sudo apt-get install git (Ubuntu/Debian)"
    echo "   ou: brew install git (macOS)"
    exit 1
fi

echo "✅ Git encontrado!"
echo ""

# Verificar status do Git
echo "📊 Verificando status do Git..."
git status
echo ""

# Perguntar se deseja continuar
read -p "Deseja continuar com o upload? (s/n): " continuar
if [[ ! $continuar =~ ^[Ss]$ ]]; then
    echo "❌ Upload cancelado pelo usuário."
    exit 0
fi

echo ""
echo "🔄 Iniciando processo de upload..."
echo ""

# Adicionar todos os arquivos
echo "📁 Adicionando arquivos..."
git add .
if [ $? -ne 0 ]; then
    echo "❌ ERRO: Falha ao adicionar arquivos!"
    exit 1
fi
echo "✅ Arquivos adicionados com sucesso!"

echo ""
echo "📝 Fazendo commit..."
git commit -m "🚀 Sprint 3: Sistema IoT Monitoring Completo

- ✅ Atualizado nome do projeto para Sprint 3
- ✅ Implementado sistema completo de KPIs de negócio
- ✅ Adicionado dashboard executivo (9 gráficos)
- ✅ Criado documentação técnica completa
- ✅ Adicionado link do YouTube para demonstração
- ✅ Performance ML: 95.2% accuracy, 91.8% precision
- ✅ Banco de dados: 11 tabelas normalizadas
- ✅ Visualizações: 8+ gráficos profissionais
- ✅ Automação: Scripts para diferentes SO
- ✅ Documentação: READMEs e guias completos"

if [ $? -ne 0 ]; then
    echo "❌ ERRO: Falha ao fazer commit!"
    exit 1
fi
echo "✅ Commit realizado com sucesso!"

echo ""
echo "🚀 Fazendo push para o GitHub..."
git push origin main
if [ $? -ne 0 ]; then
    echo "❌ ERRO: Falha ao fazer push!"
    echo "   Verifique sua conexão e credenciais do GitHub."
    exit 1
fi

echo ""
echo "✅ UPLOAD CONCLUÍDO COM SUCESSO!"
echo "====================================================="
echo ""
echo "📊 Resumo do Upload:"
echo "   • Repositório: Enterprise Challenge - Sprint 3 - Reply"
echo "   • Branch: main"
echo "   • Status: Atualizado"
echo ""
echo "🌐 Acesse seu repositório no GitHub para verificar!"
echo ""

# Mostrar URL do repositório (se configurado)
git remote -v
echo ""

echo "🎯 Próximos passos:"
echo "   1. Verifique o repositório no GitHub"
echo "   2. Confirme se todos os arquivos foram carregados"
echo "   3. Teste o link do YouTube no README"
echo "   4. Compartilhe o link do repositório"
echo ""

read -p "Pressione Enter para continuar..."
