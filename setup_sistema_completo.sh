#!/bin/bash

echo "========================================"
echo "Setup Sistema IoT Monitoring Completo"
echo "Enterprise Challenge Sprint 3 - Reply"
echo "Versão: 1.0.0"
echo "Data: $(date)"
echo "========================================"

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Função para log
log() {
    echo -e "${BLUE}[$(date +'%H:%M:%S')]${NC} $1"
}

# Função para erro
error() {
    echo -e "${RED}[ERRO]${NC} $1"
}

# Função para sucesso
success() {
    echo -e "${GREEN}[SUCESSO]${NC} $1"
}

# Função para aviso
warning() {
    echo -e "${YELLOW}[AVISO]${NC} $1"
}

# Verificar se está no diretório correto
if [ ! -f "README.md" ]; then
    error "Execute este script no diretório raiz do projeto"
    exit 1
fi

log "Iniciando setup do sistema..."

# 1. Verificar Python
log "Verificando Python..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
    success "Python encontrado: $PYTHON_VERSION"
else
    error "Python3 não encontrado. Instale Python 3.8+"
    exit 1
fi

# 2. Verificar pip
log "Verificando pip..."
if command -v pip3 &> /dev/null; then
    success "pip3 encontrado"
else
    error "pip3 não encontrado. Instale pip"
    exit 1
fi

# 3. Criar ambiente virtual
log "Criando ambiente virtual..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    success "Ambiente virtual criado"
else
    warning "Ambiente virtual já existe"
fi

# 4. Ativar ambiente virtual
log "Ativando ambiente virtual..."
source venv/bin/activate
success "Ambiente virtual ativado"

# 5. Atualizar pip
log "Atualizando pip..."
pip install --upgrade pip
success "pip atualizado"

# 6. Instalar dependências
log "Instalando dependências Python..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    success "Dependências Python instaladas"
else
    warning "Arquivo requirements.txt não encontrado"
    log "Instalando dependências básicas..."
    pip install pandas numpy matplotlib seaborn plotly mysql-connector-python streamlit scikit-learn
    success "Dependências básicas instaladas"
fi

# 7. Criar diretórios necessários
log "Criando diretórios..."
mkdir -p logs
mkdir -p data
mkdir -p models
mkdir -p configs
mkdir -p screenshots
mkdir -p reports
success "Diretórios criados"

# 8. Verificar MySQL
log "Verificando MySQL..."
if command -v mysql &> /dev/null; then
    MYSQL_VERSION=$(mysql --version 2>&1 | cut -d' ' -f3 | cut -d',' -f1)
    success "MySQL encontrado: $MYSQL_VERSION"
else
    warning "MySQL não encontrado. Instale MySQL 8.0+"
    log "Para Ubuntu/Debian: sudo apt install mysql-server"
    log "Para CentOS/RHEL: sudo yum install mysql-server"
    log "Para macOS: brew install mysql"
fi

# 9. Verificar Git
log "Verificando Git..."
if command -v git &> /dev/null; then
    GIT_VERSION=$(git --version 2>&1 | cut -d' ' -f3)
    success "Git encontrado: $GIT_VERSION"
else
    warning "Git não encontrado. Instale Git"
fi

# 10. Criar arquivos de configuração
log "Criando arquivos de configuração..."

# Configuração do banco
cat > configs/database.json << EOF
{
  "host": "localhost",
  "user": "iot_user",
  "password": "iot_password",
  "database": "iot_monitoring_db",
  "port": 3306,
  "charset": "utf8mb4",
  "pool_size": 10,
  "timeout": 30
}
EOF

# Configuração MQTT
cat > configs/mqtt.json << EOF
{
  "broker": "broker.hivemq.com",
  "port": 1883,
  "topic_base": "industrial/sensors",
  "qos": 1,
  "keepalive": 60,
  "retain": true
}
EOF

# Configuração de sensores
cat > configs/sensores.json << EOF
{
  "dht22": {
    "pino": 4,
    "tipo": "temperatura_umidade",
    "intervalo": 1000
  },
  "ldr": {
    "pino": 34,
    "tipo": "luminosidade",
    "intervalo": 1000
  },
  "pir": {
    "pino": 2,
    "tipo": "movimento",
    "intervalo": 1000
  }
}
EOF

# Configuração de thresholds
cat > configs/thresholds.json << EOF
{
  "temperatura": {
    "max": 30.0,
    "min": 15.0,
    "critico_max": 35.0,
    "critico_min": 10.0
  },
  "umidade": {
    "max": 80.0,
    "min": 30.0,
    "critico_max": 90.0,
    "critico_min": 20.0
  },
  "luminosidade": {
    "max": 800.0,
    "min": 50.0,
    "critico_max": 1000.0,
    "critico_min": 10.0
  }
}
EOF

# Configuração ML
cat > configs/ml.json << EOF
{
  "modelos": {
    "anomalia": {
      "algoritmo": "RandomForestClassifier",
      "n_estimators": 100,
      "max_depth": 10,
      "test_size": 0.2
    },
    "temperatura": {
      "algoritmo": "RandomForestRegressor",
      "n_estimators": 100,
      "max_depth": 10,
      "test_size": 0.2
    }
  },
  "features": {
    "anomalia": ["valor_atual", "valor_anterior", "media_movel", "std_movel", "tendencia"],
    "temperatura": ["hora", "dia_semana", "dia_mes", "valor_anterior", "media_movel"]
  }
}
EOF

success "Arquivos de configuração criados"

# 11. Criar script de verificação
log "Criando script de verificação..."
cat > verificar_setup.py << 'EOF'
#!/usr/bin/env python3
"""
Verificador de Setup - Sistema IoT Monitoring
Enterprise Challenge Sprint 3 - Reply
"""

import sys
import os
import json
import importlib

def verificar_dependencias():
    """Verifica se todas as dependências estão instaladas"""
    dependencias = [
        'pandas', 'numpy', 'matplotlib', 'seaborn', 
        'plotly', 'mysql.connector', 'streamlit', 'sklearn'
    ]
    
    faltando = []
    for dep in dependencias:
        try:
            if dep == 'mysql.connector':
                importlib.import_module('mysql.connector')
            else:
                importlib.import_module(dep)
            print(f"✅ {dep}")
        except ImportError:
            print(f"❌ {dep}")
            faltando.append(dep)
    
    return len(faltando) == 0, faltando

def verificar_arquivos():
    """Verifica se os arquivos necessários existem"""
    arquivos_necessarios = [
        'README.md',
        'requirements.txt',
        'criar_tabelas_iot.sql',
        'ml_basico_integrado.py',
        'dashboard_visualizacao_alertas.py',
        'sistema_alertas_avancado.py'
    ]
    
    faltando = []
    for arquivo in arquivos_necessarios:
        if os.path.exists(arquivo):
            print(f"✅ {arquivo}")
        else:
            print(f"❌ {arquivo}")
            faltando.append(arquivo)
    
    return len(faltando) == 0, faltando

def verificar_diretorios():
    """Verifica se os diretórios necessários existem"""
    diretorios_necessarios = [
        'logs', 'data', 'models', 'configs', 'screenshots', 'reports'
    ]
    
    faltando = []
    for diretorio in diretorios_necessarios:
        if os.path.exists(diretorio):
            print(f"✅ {diretorio}/")
        else:
            print(f"❌ {diretorio}/")
            faltando.append(diretorio)
    
    return len(faltando) == 0, faltando

def main():
    print("=== Verificação de Setup ===")
    print("Enterprise Challenge Sprint 3 - Reply")
    print("=============================")
    
    print("\n📦 Verificando dependências Python...")
    deps_ok, deps_faltando = verificar_dependencias()
    
    print("\n📁 Verificando arquivos necessários...")
    arquivos_ok, arquivos_faltando = verificar_arquivos()
    
    print("\n📂 Verificando diretórios necessários...")
    dirs_ok, dirs_faltando = verificar_diretorios()
    
    print("\n📊 Resumo da Verificação:")
    print(f"Dependências: {'✅ OK' if deps_ok else '❌ Faltando'}")
    print(f"Arquivos: {'✅ OK' if arquivos_ok else '❌ Faltando'}")
    print(f"Diretórios: {'✅ OK' if dirs_ok else '❌ Faltando'}")
    
    if deps_ok and arquivos_ok and dirs_ok:
        print("\n🎉 Setup verificado com sucesso!")
        return 0
    else:
        print("\n⚠️  Setup incompleto. Verifique os itens faltando.")
        if deps_faltando:
            print(f"Dependências faltando: {', '.join(deps_faltando)}")
        if arquivos_faltando:
            print(f"Arquivos faltando: {', '.join(arquivos_faltando)}")
        if dirs_faltando:
            print(f"Diretórios faltando: {', '.join(dirs_faltando)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
EOF

chmod +x verificar_setup.py
success "Script de verificação criado"

# 12. Executar verificação
log "Executando verificação de setup..."
python3 verificar_setup.py

# 13. Criar arquivo de versão
log "Criando arquivo de versão..."
cat > VERSION << EOF
Sistema IoT Monitoring
Enterprise Challenge Sprint 3 - Reply
Versão: 1.0.0
Data de Setup: $(date)
Python: $(python3 --version)
Sistema: $(uname -s) $(uname -r)
EOF

success "Arquivo de versão criado"

# 14. Resumo final
echo ""
echo "========================================"
echo "🎉 SETUP CONCLUÍDO COM SUCESSO!"
echo "========================================"
echo ""
echo "📋 Próximos passos:"
echo "1. Configure o banco de dados:"
echo "   mysql -u root -p < criar_tabelas_iot.sql"
echo ""
echo "2. Execute o fluxo completo:"
echo "   ./executar_fluxo_completo.sh"
echo ""
echo "3. Ou execute etapas individuais:"
echo "   ./etapa_1_coleta.sh simulacao"
echo "   ./etapa_2_persistencia.sh"
echo "   ./etapa_3_ml.sh"
echo "   ./etapa_4_visualizacao.sh"
echo ""
echo "📚 Documentação:"
echo "   README_REPRODUTIBILIDADE_COMPLETA.md"
echo ""
echo "🔧 Verificação:"
echo "   python3 verificar_setup.py"
echo ""
echo "========================================"
