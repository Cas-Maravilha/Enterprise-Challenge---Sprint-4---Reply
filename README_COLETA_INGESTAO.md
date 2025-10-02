# Coleta e Ingestão - Sistema IoT Monitoring
## Enterprise Challenge Sprint 3 - Reply

## 🎯 Visão Geral

Este módulo implementa o sistema completo de **coleta e ingestão de dados** do ESP32, incluindo simulação no Wokwi, código para hardware real, registro de dados e visualização gráfica das séries coletadas.

## 📋 Componentes do Sistema

### **1. Código ESP32 (Hardware Real)**
- **Arquivo**: `coleta_ingestao_esp32.ino`
- **Sensores**: DHT22, LDR, PIR, BME280, Vibração
- **Protocolos**: MQTT, Serial, HTTP
- **Formato**: JSON, CSV

### **2. Simulação Wokwi**
- **Arquivo**: `wokwi_simulacao_esp32.json`
- **Ambiente**: Virtual com sensores simulados
- **Testes**: Integração e validação

### **3. Coletor Serial**
- **Arquivo**: `coletor_dados_serial.py`
- **Função**: Coleta dados via Serial/USB
- **Processamento**: Parse e validação

### **4. Simulador de Dados**
- **Arquivo**: `simulador_dados_esp32.py`
- **Função**: Gera dados sintéticos realísticos
- **Uso**: Testes sem hardware

### **5. Visualizador**
- **Arquivo**: `visualizar_dados_coletados.py`
- **Função**: Gráficos e análises
- **Formatos**: PNG, CSV, JSON

## 🚀 Como Executar

### **Windows:**
```bash
executar_coleta_ingestao.bat
```

### **Linux/Mac:**
```bash
chmod +x executar_coleta_ingestao.sh
./executar_coleta_ingestao.sh
```

### **Execução Direta:**
```bash
# Coleta via Serial
python coletor_dados_serial.py

# Simulação de dados
python simulador_dados_esp32.py

# Visualização
python visualizar_dados_coletados.py
```

## 🔌 Hardware ESP32

### **Sensores Implementados:**
- **DHT22**: Temperatura e Umidade
- **LDR**: Luminosidade
- **PIR**: Detecção de Movimento
- **BME280**: Pressão e Altitude
- **Acelerômetro**: Vibração Triaxial (simulado)

### **Conexões:**
```
DHT22:
- VCC → 3.3V
- DATA → GPIO4
- GND → GND

LDR:
- Pino 1 → GPIO34
- Pino 2 → 3.3V

PIR:
- VCC → 3.3V
- OUT → GPIO2
- GND → GND

BME280:
- VCC → 3.3V
- SDA → GPIO21
- SCL → GPIO22
- GND → GND
```

### **Configuração WiFi:**
```cpp
const char* ssid = "SEU_WIFI_SSID";
const char* password = "SUA_SENHA_WIFI";
```

### **Configuração MQTT:**
```cpp
const char* mqtt_server = "broker.hivemq.com";
const int mqtt_port = 1883;
const char* mqtt_topic = "industrial/sensors/ESP32_001/data";
```

## 📊 Monitor Serial

### **Formato de Saída:**
```
=== Sistema de Coleta e Ingestão ESP32 ===
Enterprise Challenge Sprint 3 - Reply
==========================================

==========================================
| ID | Temp | Umid | Luz | Mov | Press |
|----|------|------|-----|-----|-------|
|  1 | 23.5 | 65.2 | 450 | NÃO | 1013.2|
|  2 | 23.7 | 64.8 | 420 | SIM | 1013.1|
|  3 | 23.9 | 64.5 | 380 | NÃO | 1012.9|
...
```

### **Logs Detalhados (a cada 10 leituras):**
```
------------------------------------------
Leitura #10 - Timestamp: 2024-01-11T10:30:00Z
Temperatura: 23.5°C
Umidade: 65.2%
Luminosidade: 450 lux
Movimento: Não detectado
Pressão: 1013.2 hPa
Altitude: 100.0 m
Vibração X: 0.12, Y: -0.08, Z: 0.05
Bateria: 85%
RSSI: -45 dBm
==========================================
```

## 🌐 Simulação Wokwi

### **Configuração:**
1. Acesse [wokwi.com](https://wokwi.com)
2. Importe o arquivo `wokwi_simulacao_esp32.json`
3. Configure o código `coleta_ingestao_esp32.ino`
4. Execute a simulação

### **Componentes Virtuais:**
- **ESP32**: Microcontrolador principal
- **DHT22**: Sensor de temperatura e umidade
- **LDR**: Sensor de luminosidade
- **PIR**: Sensor de movimento
- **BME280**: Sensor de pressão
- **LEDs**: Indicadores visuais
- **Serial Monitor**: Visualização de dados

## 📈 Visualizações Geradas

### **1. Gráficos Principais**
- **Temperatura**: Linha temporal com tendência
- **Umidade**: Linha temporal com tendência
- **Luminosidade**: Gráfico de barras
- **Pressão**: Linha temporal com tendência

### **2. Distribuição**
- **Histogramas**: Distribuição de cada variável
- **Estatísticas**: Média, desvio padrão, min/max
- **Linhas de referência**: ±1σ, média

### **3. Correlação**
- **Heatmap**: Matriz de correlação
- **Valores**: Correlação entre variáveis
- **Cores**: Intensidade da correlação

### **4. Tempo Real**
- **Simulação**: Dados como se fossem tempo real
- **Média Móvel**: Suavização de tendências
- **Múltiplas Variáveis**: Sincronizadas

## 📊 Formatos de Dados

### **JSON (MQTT)**
```json
{
  "device_id": "ESP32_001",
  "timestamp": "2024-01-11T10:30:00Z",
  "reading_id": 1,
  "sensores": {
    "temperatura": 23.5,
    "umidade": 65.2,
    "luminosidade": 450,
    "movimento": false,
    "pressao": 1013.2,
    "altitude": 100.0,
    "vibracao_x": 0.12,
    "vibracao_y": -0.08,
    "vibracao_z": 0.05
  },
  "metadata": {
    "bateria": 85.0,
    "rssi": -45,
    "qualidade": 0.95,
    "versao_protocolo": "1.0"
  }
}
```

### **CSV (Serial)**
```csv
id,device_id,timestamp,temperatura,umidade,luminosidade,movimento,pressao
1,ESP32_001,2024-01-11T10:30:00Z,23.5,65.2,450,False,1013.2
2,ESP32_001,2024-01-11T10:30:01Z,23.7,64.8,420,True,1013.1
```

## ⏰ Periodicidades

### **Coleta de Dados**
- **ESP32 Real**: 1Hz (1 vez por segundo)
- **Simulação Wokwi**: 0.5Hz (1 vez a cada 2 segundos)
- **Serial**: 1Hz (1 vez por segundo)

### **Envio MQTT**
- **Frequência**: 5 segundos
- **QoS**: 1 (At Least Once)
- **Retenção**: 24 horas

### **Logs Detalhados**
- **Intervalo**: A cada 10 leituras
- **Conteúdo**: Dados completos + metadados

## 🔧 Dependências

### **ESP32 (Arduino IDE)**
```cpp
#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>
#include <DHT.h>
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BME280.h>
```

### **Python**
```bash
pip install pandas matplotlib numpy pyserial
```

## 📁 Arquivos Gerados

### **Dados**
- `dados_coletados.csv` - Dados em formato CSV
- `dados_coletados.json` - Dados em formato JSON
- `dados_simulados.csv` - Dados simulados CSV
- `dados_simulados.json` - Dados simulados JSON

### **Gráficos**
- `graficos_dados_coletados.png` - Gráficos principais
- `graficos_dados_simulados.png` - Gráficos simulados
- `analise_dados_coletados.png` - Análise completa
- `distribuicao_dados_coletados.png` - Distribuições
- `correlacao_dados_coletados.png` - Correlações
- `tempo_real_dados_coletados.png` - Tempo real
- `vibracao_3d_simulada.png` - Vibração 3D

### **Logs**
- `coleta_serial.log` - Log da coleta serial
- `simulador_dados.log` - Log da simulação

## 🎯 Exemplo de Execução

### **1. Coleta via Serial:**
```bash
python coletor_dados_serial.py
# Digite a porta serial (ex: COM3, /dev/ttyUSB0)
# Aguarde a coleta de 100 leituras
# Verifique os arquivos gerados
```

### **2. Simulação:**
```bash
python simulador_dados_esp32.py
# Digite o número de leituras (padrão: 100)
# Aguarde a simulação
# Verifique os arquivos gerados
```

### **3. Visualização:**
```bash
python visualizar_dados_coletados.py
# Detecta automaticamente arquivos de dados
# Gera gráficos e análises
# Exibe relatório estatístico
```

## 📊 Saída do Monitor Serial

```
=== Sistema de Coleta e Ingestão ESP32 ===
Enterprise Challenge Sprint 3 - Reply
==========================================

WiFi conectado com sucesso!
IP: 192.168.1.100
RSSI: -45 dBm
Sensor BME280 inicializado com sucesso!
Sistema inicializado com sucesso!
Iniciando coleta de dados...

==========================================
| ID | Temp | Umid | Luz | Mov | Press |
|----|------|------|-----|-----|-------|
|  1 | 23.5 | 65.2 | 450 | NÃO | 1013.2|
|  2 | 23.7 | 64.8 | 420 | SIM | 1013.1|
|  3 | 23.9 | 64.5 | 380 | NÃO | 1012.9|
|  4 | 24.1 | 64.2 | 350 | NÃO | 1012.8|
|  5 | 24.3 | 63.9 | 320 | NÃO | 1012.7|
|  6 | 24.5 | 63.6 | 290 | SIM | 1012.6|
|  7 | 24.7 | 63.3 | 260 | NÃO | 1012.5|
|  8 | 24.9 | 63.0 | 230 | NÃO | 1012.4|
|  9 | 25.1 | 62.7 | 200 | NÃO | 1012.3|
| 10 | 25.3 | 62.4 | 170 | NÃO | 1012.2|
------------------------------------------
Leitura #10 - Timestamp: 2024-01-11T10:30:10Z
Temperatura: 25.3°C
Umidade: 62.4%
Luminosidade: 170 lux
Movimento: Não detectado
Pressão: 1012.2 hPa
Altitude: 100.0 m
Vibração X: 0.15, Y: -0.12, Z: 0.08
Bateria: 84%
RSSI: -45 dBm
==========================================
```

## 🎯 Próximos Passos

1. **Conectar Hardware**: Configure o ESP32 com os sensores
2. **Testar Serial**: Execute a coleta via Serial/USB
3. **Simular Wokwi**: Teste no ambiente virtual
4. **Analisar Dados**: Visualize as séries coletadas
5. **Integrar Pipeline**: Conecte com o sistema completo

## 📞 Suporte

Para dúvidas sobre a coleta e ingestão:
- **Hardware**: Verifique as conexões dos sensores
- **Serial**: Confirme a porta e baudrate
- **WiFi**: Verifique as credenciais
- **MQTT**: Teste a conectividade
- **Dados**: Analise os logs gerados

---

**Coleta e Ingestão - Enterprise Challenge Sprint 3 - Reply**
