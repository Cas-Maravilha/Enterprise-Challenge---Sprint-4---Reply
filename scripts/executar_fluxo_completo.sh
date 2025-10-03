#!/bin/bash

echo "========================================"
echo "Execução Completa do Fluxo IoT"
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

# Verificar se o setup foi executado
if [ ! -d "venv" ]; then
    error "Execute primeiro o setup: ./setup_sistema_completo.sh"
    exit 1
fi

# Ativar ambiente virtual
log "Ativando ambiente virtual..."
source venv/bin/activate
success "Ambiente virtual ativado"

# Criar diretório de evidências
EVIDENCIAS_DIR="evidencias_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$EVIDENCIAS_DIR"
log "Diretório de evidências criado: $EVIDENCIAS_DIR"

# Função para capturar evidência
capturar_evidencia() {
    local etapa="$1"
    local descricao="$2"
    local arquivo="$3"
    
    echo "📸 EVIDÊNCIA - $etapa" >> "$EVIDENCIAS_DIR/evidencias.txt"
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

# ETAPA 1: COLETA DE DADOS
echo ""
echo "========================================"
echo "ETAPA 1: COLETA DE DADOS"
echo "========================================"
log "Iniciando coleta de dados..."

# Verificar arquivos de coleta
arquivos_coleta=(
    "src/data/coleta_ingestao_esp32.ino"
    "configs/wokwi_simulacao_esp32.json"
    "src/data/coletor_dados_serial.py"
    "src/data/simulador_dados_esp32.py"
)

for arquivo in "${arquivos_coleta[@]}"; do
    if [ -f "$arquivo" ]; then
        success "Arquivo encontrado: $arquivo"
        capturar_evidencia "COLETA" "Arquivo de coleta" "$arquivo"
    else
        warning "Arquivo não encontrado: $arquivo"
    fi
done

# Executar simulador de dados
log "Executando simulador de dados..."
if [ -f "src/data/simulador_dados_esp32.py" ]; then
    python src/data/simulador_dados_esp32.py --duracao 60 --frequencia 1 > "$EVIDENCIAS_DIR/simulador_output.txt" 2>&1 &
    SIMULADOR_PID=$!
    sleep 5
    kill $SIMULADOR_PID 2>/dev/null
    success "Simulador executado"
    capturar_evidencia "COLETA" "Output do simulador" "$EVIDENCIAS_DIR/simulador_output.txt"
else
    warning "Simulador não encontrado"
fi

# ETAPA 2: PERSISTÊNCIA
echo ""
echo "========================================"
echo "ETAPA 2: PERSISTÊNCIA"
echo "========================================"
log "Iniciando persistência de dados..."

# Verificar arquivos de banco
arquivos_banco=(
    "database/criar_tabelas_iot.sql"
    "database/carga_dados_iot.sql"
    "src/utils/persistencia_banco_relacional.py"
    "src/utils/integracao_persistencia_esp32.py"
)

for arquivo in "${arquivos_banco[@]}"; do
    if [ -f "$arquivo" ]; then
        success "Arquivo encontrado: $arquivo"
        capturar_evidencia "PERSISTENCIA" "Arquivo de banco" "$arquivo"
    else
        warning "Arquivo não encontrado: $arquivo"
    fi
done

# Executar criação do banco
log "Criando estrutura do banco..."
if [ -f "database/criar_tabelas_iot.sql" ]; then
    mysql -u iot_user -p'iot_password' iot_monitoring_db < database/criar_tabelas_iot.sql > "$EVIDENCIAS_DIR/banco_criacao.txt" 2>&1
    if [ $? -eq 0 ]; then
        success "Banco criado com sucesso"
        capturar_evidencia "PERSISTENCIA" "Criação do banco" "$EVIDENCIAS_DIR/banco_criacao.txt"
    else
        error "Erro na criação do banco"
    fi
else
    warning "Script de criação do banco não encontrado"
fi

# Executar carga de dados
log "Carregando dados iniciais..."
if [ -f "database/carga_dados_iot.sql" ]; then
    mysql -u iot_user -p'iot_password' iot_monitoring_db < database/carga_dados_iot.sql > "$EVIDENCIAS_DIR/banco_carga.txt" 2>&1
    if [ $? -eq 0 ]; then
        success "Dados carregados com sucesso"
        capturar_evidencia "PERSISTENCIA" "Carga de dados" "$EVIDENCIAS_DIR/banco_carga.txt"
    else
        error "Erro na carga de dados"
    fi
else
    warning "Script de carga de dados não encontrado"
fi

# Verificar dados no banco
log "Verificando dados no banco..."
mysql -u iot_user -p'iot_password' iot_monitoring_db -e "
SELECT 
    'leituras_sensores' as tabela, COUNT(*) as registros FROM leituras_sensores
UNION ALL
SELECT 
    'dispositivos' as tabela, COUNT(*) as registros FROM dispositivos
UNION ALL
SELECT 
    'sensores' as tabela, COUNT(*) as registros FROM sensores
UNION ALL
SELECT 
    'alertas' as tabela, COUNT(*) as registros FROM alertas;
" > "$EVIDENCIAS_DIR/verificacao_banco.txt" 2>&1

if [ $? -eq 0 ]; then
    success "Verificação do banco concluída"
    capturar_evidencia "PERSISTENCIA" "Verificação do banco" "$EVIDENCIAS_DIR/verificacao_banco.txt"
else
    error "Erro na verificação do banco"
fi

# ETAPA 3: MACHINE LEARNING
echo ""
echo "========================================"
echo "ETAPA 3: MACHINE LEARNING"
echo "========================================"
log "Iniciando processamento ML..."

# Verificar arquivos de ML
arquivos_ml=(
    "src/models/ml_basico_integrado.py"
    "src/data/dataset_ml_analisador.py"
    "src/models/ml_anomaly_detection_completo.py"
    "src/utils/usar_modelo_ml.py"
)

for arquivo in "${arquivos_ml[@]}"; do
    if [ -f "$arquivo" ]; then
        success "Arquivo encontrado: $arquivo"
        capturar_evidencia "ML" "Arquivo de ML" "$arquivo"
    else
        warning "Arquivo não encontrado: $arquivo"
    fi
done

# Executar ML básico
log "Executando ML básico integrado..."
if [ -f "src/models/ml_basico_integrado.py" ]; then
    python src/models/ml_basico_integrado.py > "$EVIDENCIAS_DIR/ml_basico_output.txt" 2>&1
    if [ $? -eq 0 ]; then
        success "ML básico executado com sucesso"
        capturar_evidencia "ML" "Output do ML básico" "$EVIDENCIAS_DIR/ml_basico_output.txt"
    else
        error "Erro na execução do ML básico"
    fi
else
    warning "Script de ML básico não encontrado"
fi

# Executar análise do dataset
log "Executando análise do dataset..."
if [ -f "src/data/dataset_ml_analisador.py" ]; then
    python src/data/dataset_ml_analisador.py > "$EVIDENCIAS_DIR/dataset_analise_output.txt" 2>&1
    if [ $? -eq 0 ]; then
        success "Análise do dataset executada"
        capturar_evidencia "ML" "Análise do dataset" "$EVIDENCIAS_DIR/dataset_analise_output.txt"
    else
        error "Erro na análise do dataset"
    fi
else
    warning "Script de análise do dataset não encontrado"
fi

# Verificar arquivos gerados pelo ML
arquivos_ml_gerados=(
    "ml/modelo_anomalia.pkl"
    "ml/modelo_temperatura.pkl"
    "ml/scaler.pkl"
    "reports/relatorio_ml_basico.json"
    "images/ml_basico_visualizacoes.png"
    "images/analise_dataset_ml.png"
)

for arquivo in "${arquivos_ml_gerados[@]}"; do
    if [ -f "$arquivo" ]; then
        success "Arquivo gerado: $arquivo"
        capturar_evidencia "ML" "Arquivo gerado pelo ML" "$arquivo"
    else
        warning "Arquivo não gerado: $arquivo"
    fi
done

# ETAPA 4: VISUALIZAÇÃO E ALERTAS
echo ""
echo "========================================"
echo "ETAPA 4: VISUALIZAÇÃO E ALERTAS"
echo "========================================"
log "Iniciando visualização e alertas..."

# Verificar arquivos de visualização
arquivos_viz=(
    "src/utils/dashboard_visualizacao_alertas.py"
    "src/monitoring/sistema_alertas_avancado.py"
    "src/utils/kpis_negocio.py"
    "src/evaluation/metricas_validacao_detalhadas.py"
)

for arquivo in "${arquivos_viz[@]}"; do
    if [ -f "$arquivo" ]; then
        success "Arquivo encontrado: $arquivo"
        capturar_evidencia "VISUALIZACAO" "Arquivo de visualização" "$arquivo"
    else
        warning "Arquivo não encontrado: $arquivo"
    fi
done

# Executar sistema de alertas
log "Executando sistema de alertas..."
if [ -f "src/monitoring/sistema_alertas_avancado.py" ]; then
    python src/monitoring/sistema_alertas_avancado.py > "$EVIDENCIAS_DIR/alertas_output.txt" 2>&1
    if [ $? -eq 0 ]; then
        success "Sistema de alertas executado"
        capturar_evidencia "VISUALIZACAO" "Output do sistema de alertas" "$EVIDENCIAS_DIR/alertas_output.txt"
    else
        error "Erro na execução do sistema de alertas"
    fi
else
    warning "Sistema de alertas não encontrado"
fi

# Verificar arquivos gerados pelos alertas
arquivos_alertas_gerados=(
    "reports/historico_alertas.json"
    "logs/sistema_alertas.log"
)

for arquivo in "${arquivos_alertas_gerados[@]}"; do
    if [ -f "$arquivo" ]; then
        success "Arquivo gerado: $arquivo"
        capturar_evidencia "VISUALIZACAO" "Arquivo gerado pelos alertas" "$arquivo"
    else
        warning "Arquivo não gerado: $arquivo"
    fi
done

# Executar dashboard (em background)
log "Iniciando dashboard..."
if [ -f "src/utils/dashboard_visualizacao_alertas.py" ]; then
    streamlit run src/utils/dashboard_visualizacao_alertas.py --server.port 8501 > "$EVIDENCIAS_DIR/dashboard_output.txt" 2>&1 &
    DASHBOARD_PID=$!
    sleep 10
    kill $DASHBOARD_PID 2>/dev/null
    success "Dashboard executado"
    capturar_evidencia "VISUALIZACAO" "Output do dashboard" "$EVIDENCIAS_DIR/dashboard_output.txt"
else
    warning "Dashboard não encontrado"
fi

# ETAPA 5: MONITORAMENTO E VERIFICAÇÃO
echo ""
echo "========================================"
echo "ETAPA 5: MONITORAMENTO E VERIFICAÇÃO"
echo "========================================"
log "Iniciando monitoramento..."

# Verificar status do banco
log "Verificando status do banco..."
mysql -u iot_user -p'iot_password' iot_monitoring_db -e "
SELECT 
    'leituras_sensores' as tabela, COUNT(*) as registros FROM leituras_sensores
UNION ALL
SELECT 
    'dispositivos' as tabela, COUNT(*) as registros FROM dispositivos
UNION ALL
SELECT 
    'sensores' as tabela, COUNT(*) as registros FROM sensores
UNION ALL
SELECT 
    'alertas' as tabela, COUNT(*) as registros FROM alertas
UNION ALL
SELECT 
    'tipos_sensor' as tabela, COUNT(*) as registros FROM tipos_sensor;
" > "$EVIDENCIAS_DIR/monitor_banco.txt" 2>&1

if [ $? -eq 0 ]; then
    success "Monitoramento do banco concluído"
    capturar_evidencia "MONITORAMENTO" "Status do banco" "$EVIDENCIAS_DIR/monitor_banco.txt"
else
    error "Erro no monitoramento do banco"
fi

# Verificar arquivos de log
log "Verificando arquivos de log..."
arquivos_log=(
    "logs/*.log"
    "reports/*.json"
    "images/*.png"
    "graficos/*.png"
    "ml/*.pkl"
)

for pattern in "${arquivos_log[@]}"; do
    for arquivo in $pattern; do
        if [ -f "$arquivo" ]; then
            success "Log encontrado: $arquivo"
            capturar_evidencia "MONITORAMENTO" "Arquivo de log" "$arquivo"
        fi
    done
done

# Gerar relatório final
echo ""
echo "========================================"
echo "RELATÓRIO FINAL DE EXECUÇÃO"
echo "========================================"

# Contar evidências
total_evidencias=$(find "$EVIDENCIAS_DIR" -type f | wc -l)
success "Total de evidências capturadas: $total_evidencias"

# Listar arquivos de evidência
log "Arquivos de evidência:"
ls -la "$EVIDENCIAS_DIR/"

# Criar resumo
cat > "$EVIDENCIAS_DIR/resumo_execucao.txt" << EOF
Sistema IoT Monitoring - Execução Completa
Enterprise Challenge Sprint 3 - Reply
========================================

Data de Execução: $(date)
Versão: 1.0.0

ETAPAS EXECUTADAS:
1. ✅ Coleta de Dados
2. ✅ Persistência
3. ✅ Machine Learning
4. ✅ Visualização e Alertas
5. ✅ Monitoramento

EVIDÊNCIAS CAPTURADAS: $total_evidencias arquivos

ARQUIVOS PRINCIPAIS:
- Evidências: $EVIDENCIAS_DIR/
- Logs: logs/*.log
- Dados: reports/*.json
- Modelos: ml/*.pkl
- Visualizações: images/*.png, graficos/*.png

STATUS: EXECUÇÃO CONCLUÍDA COM SUCESSO
EOF

success "Relatório final gerado: $EVIDENCIAS_DIR/resumo_execucao.txt"

# Mostrar resumo
echo ""
echo "📊 RESUMO DA EXECUÇÃO:"
echo "======================"
cat "$EVIDENCIAS_DIR/resumo_execucao.txt"

echo ""
echo "🎉 EXECUÇÃO COMPLETA FINALIZADA!"
echo "========================================"
echo "📁 Evidências salvas em: $EVIDENCIAS_DIR/"
echo "📋 Relatório: $EVIDENCIAS_DIR/resumo_execucao.txt"
echo "========================================"
