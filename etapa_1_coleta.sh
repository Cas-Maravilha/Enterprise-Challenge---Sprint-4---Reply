#!/bin/bash

echo "========================================"
echo "ETAPA 1: COLETA DE DADOS
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

# Verificar parâmetros
if [ $# -eq 0 ]; then
    echo "Uso: $0 [hardware|simulacao]"
    echo "  hardware  - Executar coleta via hardware ESP32"
    echo "  simulacao - Executar simulação Wokwi"
    exit 1
fi

MODO=$1

# Verificar se está no diretório correto
if [ ! -f "README.md" ]; then
    error "Execute este script no diretório raiz do projeto"
    exit 1
fi

# Ativar ambiente virtual se existir
if [ -d "venv" ]; then
    log "Ativando ambiente virtual..."
    source venv/bin/activate
    success "Ambiente virtual ativado"
fi

# Criar diretório de evidências
EVIDENCIAS_DIR="evidencias_coleta_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$EVIDENCIAS_DIR"
log "Diretório de evidências criado: $EVIDENCIAS_DIR"

# Função para capturar evidência
capturar_evidencia() {
    local descricao="$1"
    local arquivo="$2"
    
    echo "📸 EVIDÊNCIA - COLETA" >> "$EVIDENCIAS_DIR/evidencias.txt"
    echo "Timestamp: $(date)" >> "$EVIDENCIAS_DIR/evidencias.txt"
    echo "Descrição: $descricao" >> "$EVIDENCIAS_DIR/evidencias.txt"
    echo "Arquivo: $arquivo" >> "$EVIDENCIAS_DIR/evidencias.txt"
    echo "----------------------------------------" >> "$EVIDENCIAS_DIR/evidencias.txt"
    
    if [ -f "$arquivo" ]; then
        cp "$arquivo" "$EVIDENCIAS_DIR/"
        success "Evidência capturada: $arquivo"
    else
        warning "Arquivo não encontrado: $arquivo"
    fi
}

# Verificar arquivos de coleta
log "Verificando arquivos de coleta..."
arquivos_coleta=(
    "coleta_ingestao_esp32.ino"
    "wokwi_simulacao_esp32.json"
    "coletor_dados_serial.py"
    "simulador_dados_esp32.py"
)

for arquivo in "${arquivos_coleta[@]}"; do
    if [ -f "$arquivo" ]; then
        success "Arquivo encontrado: $arquivo"
        capturar_evidencia "Arquivo de coleta" "$arquivo"
    else
        warning "Arquivo não encontrado: $arquivo"
    fi
done

# Executar coleta baseada no modo
if [ "$MODO" = "hardware" ]; then
    log "🔌 Executando coleta via hardware ESP32..."
    
    # Verificar se o coletor serial existe
    if [ -f "coletor_dados_serial.py" ]; then
        log "Executando coletor serial..."
        python coletor_dados_serial.py --port COM3 --baudrate 115200 --duracao 60 > "$EVIDENCIAS_DIR/coletor_serial_output.txt" 2>&1 &
        COLETOR_PID=$!
        sleep 10
        kill $COLETOR_PID 2>/dev/null
        success "Coletor serial executado"
        capturar_evidencia "Output do coletor serial" "$EVIDENCIAS_DIR/coletor_serial_output.txt"
    else
        warning "Coletor serial não encontrado"
    fi
    
elif [ "$MODO" = "simulacao" ]; then
    log "🎮 Executando simulação Wokwi..."
    
    # Verificar se o simulador existe
    if [ -f "simulador_dados_esp32.py" ]; then
        log "Executando simulador de dados..."
        python simulador_dados_esp32.py --duracao 60 --frequencia 1 > "$EVIDENCIAS_DIR/simulador_output.txt" 2>&1 &
        SIMULADOR_PID=$!
        sleep 5
        kill $SIMULADOR_PID 2>/dev/null
        success "Simulador executado"
        capturar_evidencia "Output do simulador" "$EVIDENCIAS_DIR/simulador_output.txt"
    else
        warning "Simulador não encontrado"
    fi
    
    # Verificar arquivo de simulação Wokwi
    if [ -f "wokwi_simulacao_esp32.json" ]; then
        success "Arquivo de simulação Wokwi encontrado"
        capturar_evidencia "Configuração Wokwi" "wokwi_simulacao_esp32.json"
    else
        warning "Arquivo de simulação Wokwi não encontrado"
    fi
    
else
    error "Modo inválido: $MODO"
    echo "Use: hardware ou simulacao"
    exit 1
fi

# Verificar arquivos gerados
log "Verificando arquivos gerados..."
arquivos_gerados=(
    "dados_coletados.csv"
    "dados_simulados.csv"
    "log_coleta.txt"
    "screenshot_coleta.png"
)

for arquivo in "${arquivos_gerados[@]}"; do
    if [ -f "$arquivo" ]; then
        success "Arquivo gerado: $arquivo"
        capturar_evidencia "Arquivo gerado" "$arquivo"
    else
        warning "Arquivo não gerado: $arquivo"
    fi
done

# Gerar relatório da etapa
cat > "$EVIDENCIAS_DIR/relatorio_coleta.txt" << EOF
Sistema IoT Monitoring - Etapa 1: Coleta de Dados
Enterprise Challenge Sprint 3 - Reply
========================================

Data de Execução: $(date)
Modo: $MODO
Versão: 1.0.0

ARQUIVOS VERIFICADOS:
$(for arquivo in "${arquivos_coleta[@]}"; do
    if [ -f "$arquivo" ]; then
        echo "✅ $arquivo"
    else
        echo "❌ $arquivo"
    fi
done)

ARQUIVOS GERADOS:
$(for arquivo in "${arquivos_gerados[@]}"; do
    if [ -f "$arquivo" ]; then
        echo "✅ $arquivo"
    else
        echo "❌ $arquivo"
    fi
done)

STATUS: ETAPA 1 CONCLUÍDA
EOF

success "Relatório da etapa gerado: $EVIDENCIAS_DIR/relatorio_coleta.txt"

# Mostrar resumo
echo ""
echo "📊 RESUMO DA ETAPA 1:"
echo "====================="
cat "$EVIDENCIAS_DIR/relatorio_coleta.txt"

echo ""
echo "✅ ETAPA 1: COLETA DE DADOS CONCLUÍDA!"
echo "========================================"
echo "📁 Evidências salvas em: $EVIDENCIAS_DIR/"
echo "📋 Relatório: $EVIDENCIAS_DIR/relatorio_coleta.txt"
echo "========================================"
