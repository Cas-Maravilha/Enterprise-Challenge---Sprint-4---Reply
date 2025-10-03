# Visualização e Alertas - Sistema IoT Monitoring
## Enterprise Challenge Sprint 3 - Reply

## 🎯 Visão Geral

Este módulo implementa um **sistema completo de visualização e alertas** com dashboard interativo, KPIs do processo e sistema de alertas com thresholds simples, incluindo notificações visuais, logs e emails.

## 📋 Componentes do Sistema

### **1. Dashboard Interativo**
- **Arquivo**: `dashboard_visualizacao_alertas.py`
- **Tecnologia**: Streamlit
- **Função**: Interface web interativa com KPIs e visualizações
- **Recursos**: Filtros, gráficos em tempo real, métricas detalhadas

### **2. Sistema de Alertas Avançado**
- **Arquivo**: `sistema_alertas_avancado.py`
- **Função**: Verificação de thresholds e geração de alertas
- **Recursos**: Banners visuais, logs estruturados, emails, persistência

### **3. Scripts de Execução**
- **Windows**: `executar_dashboard_alertas.bat`
- **Linux/Mac**: `executar_dashboard_alertas.sh`
- **Função**: Automação da execução

## 📊 Dashboard Interativo (Streamlit)

### **Características Principais:**
- **Interface Web**: Acessível via navegador
- **Tempo Real**: Atualização automática de dados
- **Filtros Interativos**: Período, dispositivo, tipo de sensor
- **KPIs Principais**: Métricas em tempo real
- **Gráficos Dinâmicos**: Plotly para interatividade
- **Responsivo**: Adaptável a diferentes telas

### **Seções do Dashboard:**

#### **1. KPIs Principais**
- **Total de Leituras**: Número total de registros
- **Dispositivos Ativos**: Quantidade de dispositivos online
- **Anomalias Detectadas**: Contagem e percentual
- **Alertas Ativos**: Número de alertas em andamento
- **Média Geral**: Valor médio dos sensores

#### **2. Alertas Ativos**
- **Alertas de Alta Severidade**: Exibidos em vermelho
- **Alertas de Média Severidade**: Exibidos em amarelo
- **Informações Detalhadas**: Tipo, dispositivo, sensor, valores
- **Timestamp**: Hora exata do alerta

#### **3. Gráficos de Tempo Real**
- **Temperatura**: Valores ao longo do tempo por dispositivo
- **Umidade**: Tendências de umidade
- **Luminosidade**: Variações de luz
- **Pressão**: Monitoramento barométrico

#### **4. Distribuição dos Dados**
- **Leituras por Dispositivo**: Gráfico de barras
- **Qualidade dos Dados**: Gráfico de pizza
- **Anomalias por Dispositivo**: Distribuição de problemas

#### **5. Métricas Detalhadas**
- **Tabela Completa**: Por dispositivo e sensor
- **Estatísticas**: Média, desvio padrão, min/max
- **Contagem de Anomalias**: Por sensor

## 🚨 Sistema de Alertas

### **Thresholds Configuráveis:**
```python
thresholds = {
    'temperatura': {'max': 30.0, 'min': 15.0, 'critico_max': 35.0, 'critico_min': 10.0},
    'umidade': {'max': 80.0, 'min': 30.0, 'critico_max': 90.0, 'critico_min': 20.0},
    'luminosidade': {'max': 800.0, 'min': 50.0, 'critico_max': 1000.0, 'critico_min': 10.0},
    'pressao': {'max': 1050.0, 'min': 950.0, 'critico_max': 1100.0, 'critico_min': 900.0},
    'vibracao': {'max': 1.5, 'min': -1.5, 'critico_max': 2.0, 'critico_min': -2.0}
}
```

### **Tipos de Alertas:**
- **ALERTA ALTO**: Valor acima do limite normal
- **ALERTA BAIXO**: Valor abaixo do limite normal
- **CRÍTICO ALTO**: Valor acima do limite crítico
- **CRÍTICO BAIXO**: Valor abaixo do limite crítico

### **Níveis de Severidade:**
- **CRÍTICA**: Requer ação imediata
- **ALTA**: Requer atenção urgente
- **MÉDIA**: Requer monitoramento

## 📧 Notificações Implementadas

### **1. Banner Visual**
```
╔══════════════════════════════════════════════════════════════════════════════════╗
║                                    🚨 ALERTA CRÍTICO 🚨                          ║
╠══════════════════════════════════════════════════════════════════════════════════╣
║ Tipo: CRÍTICO ALTO        Severidade: CRÍTICA    Timestamp: 14:30:25           ║
║ Dispositivo: ESP32-Sala-01              Local: Sala de Controle Principal       ║
║ Sensor: DHT22-Temperatura  Valor: 36.50 °C       Limite: 35.00 °C              ║
║ Diferença: 1.50 °C                                                              ║
╚══════════════════════════════════════════════════════════════════════════════════╝
```

### **2. Log Estruturado**
```json
{
  "timestamp": "2024-01-11T14:30:25.123456",
  "tipo_alerta": "CRÍTICO ALTO",
  "severidade": "CRÍTICA",
  "dispositivo": "ESP32-Sala-01",
  "sensor": "DHT22-Temperatura",
  "localizacao": "Sala de Controle Principal",
  "valor_atual": 36.5,
  "valor_limite": 35.0,
  "diferenca": 1.5,
  "unidade": "°C",
  "timestamp_leitura": "2024-01-11T14:30:00.000000"
}
```

### **3. Email de Notificação**
```html
<h2>🚨 Alerta do Sistema IoT Monitoring</h2>
<table border="1">
  <tr><td><strong>Tipo de Alerta:</strong></td><td>CRÍTICO ALTO</td></tr>
  <tr><td><strong>Severidade:</strong></td><td>CRÍTICA</td></tr>
  <tr><td><strong>Dispositivo:</strong></td><td>ESP32-Sala-01</td></tr>
  <tr><td><strong>Sensor:</strong></td><td>DHT22-Temperatura</td></tr>
  <tr><td><strong>Valor Atual:</strong></td><td>36.50 °C</td></tr>
  <tr><td><strong>Valor Limite:</strong></td><td>35.00 °C</td></tr>
  <tr><td><strong>Diferença:</strong></td><td>1.50 °C</td></tr>
</table>
```

## 📈 KPIs do Processo

### **1. KPIs Principais**
- **Total de Leituras**: Volume de dados processados
- **Dispositivos Ativos**: Cobertura do sistema
- **Anomalias Detectadas**: Qualidade dos dados
- **Alertas Ativos**: Situação operacional
- **Média Geral**: Tendência dos valores

### **2. KPIs por Sensor**
- **Leituras por Sensor**: Volume de dados
- **Média por Sensor**: Valor típico
- **Desvio Padrão**: Variabilidade
- **Mínimo/Máximo**: Faixa de valores
- **Anomalias por Sensor**: Problemas específicos

### **3. KPIs Temporais**
- **Leituras por Hora**: Distribuição temporal
- **Leituras por Dia**: Padrões diários
- **Leituras por Dispositivo**: Cobertura geográfica
- **Qualidade dos Dados**: Distribuição de qualidade

## 🎨 Visualizações Implementadas

### **1. Gráficos de Tempo Real**
- **Tecnologia**: Plotly
- **Interatividade**: Zoom, pan, hover
- **Múltiplas Séries**: Por dispositivo
- **Atualização**: Automática

### **2. Gráficos de Distribuição**
- **Barras**: Leituras por dispositivo
- **Pizza**: Qualidade dos dados
- **Histogramas**: Distribuição de valores
- **Box Plots**: Estatísticas por sensor

### **3. Métricas Visuais**
- **Cards**: KPIs principais
- **Tabelas**: Dados detalhados
- **Indicadores**: Status em tempo real
- **Cores**: Codificação por severidade

## 🚀 Como Executar

### **Windows:**
```bash
executar_dashboard_alertas.bat
```

### **Linux/Mac:**
```bash
chmod +x executar_dashboard_alertas.sh
./executar_dashboard_alertas.sh
```

### **Execução Direta:**
```bash
# Dashboard Streamlit
streamlit run dashboard_visualizacao_alertas.py

# Sistema de Alertas
python sistema_alertas_avancado.py
```

## 📊 Exemplo de Uso

### **1. Executar Dashboard:**
```bash
streamlit run dashboard_visualizacao_alertas.py
```
- Acesse: http://localhost:8501
- Interface interativa no navegador
- Dados atualizados em tempo real

### **2. Executar Sistema de Alertas:**
```bash
python sistema_alertas_avancado.py
```
- Verifica thresholds automaticamente
- Gera alertas visuais
- Salva logs estruturados
- Envia notificações

### **3. Configurar Thresholds:**
```python
# Exemplo de configuração
novos_thresholds = {
    'temperatura': {'max': 25.0, 'min': 18.0},
    'umidade': {'max': 70.0, 'min': 40.0}
}
sistema.configurar_thresholds(novos_thresholds)
```

## 📁 Arquivos Gerados

### **Dashboard:**
- Interface web interativa
- Gráficos em tempo real
- KPIs atualizados

### **Alertas:**
- `historico_alertas.json` - Histórico estruturado
- `sistema_alertas.log` - Log de execução
- Banners visuais no console
- Emails de notificação

### **Logs:**
- `dashboard_visualizacao_alertas.log` - Log do dashboard
- `sistema_alertas.log` - Log do sistema de alertas

## 🔧 Dependências

### **Python:**
```bash
pip install streamlit pandas matplotlib seaborn plotly mysql-connector-python numpy
```

### **Banco de Dados:**
- MySQL 8.0+
- Banco: `iot_monitoring_db`
- Tabelas: `leituras_sensores`, `alertas`, `dispositivos`, `sensores`

## 🎯 Benefícios da Implementação

### **Visualização Completa**
- **Dashboard Interativo**: Interface web moderna
- **KPIs em Tempo Real**: Métricas atualizadas
- **Gráficos Dinâmicos**: Visualizações interativas
- **Filtros Avançados**: Análise personalizada

### **Sistema de Alertas Robusto**
- **Thresholds Configuráveis**: Limites personalizáveis
- **Múltiplas Notificações**: Banner, log, email
- **Severidade Graduada**: Crítica, alta, média
- **Persistência**: Salvamento no banco

### **Integração Completa**
- **Banco de Dados**: Dados reais do sistema
- **Tempo Real**: Atualizações automáticas
- **Escalabilidade**: Suporte a múltiplos dispositivos
- **Manutenibilidade**: Código bem estruturado

## 📞 Suporte

Para dúvidas sobre visualização e alertas:
- **Dashboard**: Verifique se o Streamlit está instalado
- **Alertas**: Confirme as credenciais do banco
- **Thresholds**: Ajuste os limites conforme necessário
- **Notificações**: Configure os emails de destino

---

**Visualização e Alertas - Enterprise Challenge Sprint 3 - Reply**
