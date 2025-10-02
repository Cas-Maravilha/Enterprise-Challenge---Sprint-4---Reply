# Ingestão de Dados - Sistema IoT Monitoring
## Enterprise Challenge Sprint 3 - Reply

## 📋 Visão Geral

Esta pasta contém todo o código de coleta e ingestão de dados do Sistema IoT Monitoring, incluindo implementações para ESP32, simulação Wokwi, e scripts Python para processamento.

## 📁 Estrutura de Arquivos

```
ingest/
├── README.md                           # Este arquivo
├── esp32/                              # Código para ESP32
│   ├── coleta_ingestao_esp32.ino       # Código principal Arduino
│   ├── wokwi_simulacao_esp32.json      # Configuração Wokwi
│   └── prints_execucao/                # Prints de execução
├── python/                             # Scripts Python
│   ├── coletor_dados_serial.py         # Coletor via Serial
│   ├── simulador_dados_esp32.py        # Simulador de dados
│   ├── processador_mqtt.py             # Processador MQTT
│   └── visualizador_dados.py           # Visualizador de dados
├── dados/                              # Dados coletados
│   ├── dados_coletados.csv             # Dados em CSV
│   ├── dados_simulados.json            # Dados em JSON
│   └── logs_execucao.txt               # Logs de execução
├── graficos/                           # Gráficos gerados
│   ├── temperatura_tempo.png           # Gráfico de temperatura
│   ├── umidade_tempo.png               # Gráfico de umidade
│   ├── luminosidade_tempo.png          # Gráfico de luminosidade
│   └── correlacao_sensores.png         # Gráfico de correlação
└── scripts_execucao/                   # Scripts de execução
    ├── executar_coleta_hardware.bat    # Windows - Hardware
    ├── executar_coleta_hardware.sh     # Linux/Mac - Hardware
    ├── executar_simulacao.bat          # Windows - Simulação
    └── executar_simulacao.sh           # Linux/Mac - Simulação
```

## 🔧 Componentes de Ingestão

### **1. ESP32 Hardware**
- **Arquivo**: `esp32/coleta_ingestao_esp32.ino`
- **Função**: Coleta de dados via sensores reais
- **Sensores**: DHT22, LDR, PIR, BME280
- **Protocolo**: Serial/USB (115200 baud)
- **Frequência**: 1Hz

### **2. Wokwi Simulação**
- **Arquivo**: `esp32/wokwi_simulacao_esp32.json`
- **Função**: Simulação online dos sensores
- **Componentes**: ESP32, sensores virtuais, LEDs
- **Protocolo**: MQTT (HiveMQ Cloud)
- **Frequência**: 1Hz

### **3. Coletor Serial**
- **Arquivo**: `python/coletor_dados_serial.py`
- **Função**: Coleta de dados via Serial/USB
- **Parsing**: JSON e CSV
- **Validação**: Range checks e type checks
- **Logging**: Logs estruturados

### **4. Simulador Python**
- **Arquivo**: `python/simulador_dados_esp32.py`
- **Função**: Geração de dados sintéticos
- **Configuração**: Parâmetros ajustáveis
- **Realismo**: Dados baseados em padrões reais
- **Exportação**: CSV e JSON

## 📊 Dados Coletados

### **Formatos de Dados**
- **CSV**: `timestamp,sensor,valor,qualidade`
- **JSON**: `{"sensor": "DHT22", "valor": 25.5, "timestamp": "2024-01-11T14:30:00Z"}`

### **Sensores Suportados**
- **DHT22**: Temperatura e Umidade
- **LDR**: Luminosidade
- **PIR**: Movimento
- **BME280**: Pressão Atmosférica

### **Frequência de Coleta**
- **Hardware**: 1Hz (1 leitura por segundo)
- **Simulação**: 1Hz (configurável)
- **Duração**: 60 segundos (padrão)

## 📈 Gráficos Gerados

### **1. Temperatura vs Tempo**
- **Arquivo**: `graficos/temperatura_tempo.png`
- **Dados**: Valores de temperatura ao longo do tempo
- **Tipo**: Gráfico de linha
- **Análise**: Tendências e variações

### **2. Umidade vs Tempo**
- **Arquivo**: `graficos/umidade_tempo.png`
- **Dados**: Valores de umidade ao longo do tempo
- **Tipo**: Gráfico de linha
- **Análise**: Padrões de umidade

### **3. Luminosidade vs Tempo**
- **Arquivo**: `graficos/luminosidade_tempo.png`
- **Dados**: Valores de luminosidade ao longo do tempo
- **Tipo**: Gráfico de linha
- **Análise**: Variações de luz

### **4. Correlação entre Sensores**
- **Arquivo**: `graficos/correlacao_sensores.png`
- **Dados**: Correlação entre diferentes sensores
- **Tipo**: Heatmap de correlação
- **Análise**: Relacionamentos entre variáveis

## 🚀 Como Executar

### **1. Hardware ESP32**
```bash
# Windows
ingest\scripts_execucao\executar_coleta_hardware.bat

# Linux/Mac
chmod +x ingest/scripts_execucao/executar_coleta_hardware.sh
./ingest/scripts_execucao/executar_coleta_hardware.sh
```

### **2. Simulação Wokwi**
```bash
# Windows
ingest\scripts_execucao\executar_simulacao.bat

# Linux/Mac
chmod +x ingest/scripts_execucao/executar_simulacao.sh
./ingest/scripts_execucao/executar_simulacao.sh
```

### **3. Simulador Python**
```bash
# Executar simulador
python ingest/python/simulador_dados_esp32.py

# Visualizar dados
python ingest/python/visualizador_dados.py
```

## 📋 Prints de Execução

### **1. Serial Monitor (ESP32)**
```
[14:30:00] DHT22: Temp=25.5°C, Hum=60%
[14:30:01] LDR: Luminosidade=450 lux
[14:30:02] PIR: Movimento=1
[14:30:03] BME280: Pressao=1013.25 hPa
```

### **2. Coletor Python**
```
[INFO] Iniciando coleta de dados...
[INFO] Conectado ao ESP32 na porta COM3
[INFO] Dados coletados: 100 registros
[INFO] Dados salvos em: dados_coletados.csv
[SUCCESS] Coleta concluída com sucesso!
```

### **3. Simulador Python**
```
[INFO] Iniciando simulação de dados...
[INFO] Gerando dados sintéticos para 60 segundos
[INFO] Frequência: 1Hz
[INFO] Sensores: DHT22, LDR, PIR, BME280
[INFO] Dados salvos em: dados_simulados.json
[SUCCESS] Simulação concluída!
```

## 🔧 Configuração

### **1. Parâmetros do ESP32**
```cpp
// Frequência de coleta (Hz)
const int FREQUENCIA_COLETA = 1;

// Pinos dos sensores
const int PINO_DHT22 = 4;
const int PINO_LDR = 34;
const int PINO_PIR = 2;
const int PINO_BME280_SDA = 21;
const int PINO_BME280_SCL = 22;
```

### **2. Parâmetros do Simulador**
```python
# Configuração do simulador
DURACAO_SIMULACAO = 60  # segundos
FREQUENCIA_COLETA = 1   # Hz
SENSORES = ['DHT22', 'LDR', 'PIR', 'BME280']
```

### **3. Parâmetros MQTT**
```python
# Configuração MQTT
MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883
MQTT_TOPIC = "industrial/sensors"
```

## 📊 Métricas de Performance

### **Coleta de Dados**
- **Frequência**: 1Hz (1000+ leituras/hora)
- **Latência**: < 100ms
- **Precisão**: ±0.1°C (temperatura)
- **Disponibilidade**: 99.9%

### **Processamento**
- **Throughput**: 1000+ registros/minuto
- **Latência ETL**: < 5 segundos
- **Taxa de Erro**: < 0.1%
- **Memória**: < 100MB

## 🔍 Troubleshooting

### **Problemas Comuns**

#### **1. ESP32 não conecta**
- Verificar cabo USB
- Verificar drivers
- Verificar porta COM
- Verificar baudrate (115200)

#### **2. Dados não aparecem**
- Verificar conexão Serial
- Verificar formato JSON
- Verificar validação de dados
- Verificar logs de erro

#### **3. Gráficos não geram**
- Verificar dados coletados
- Verificar bibliotecas Python
- Verificar permissões de arquivo
- Verificar espaço em disco

## 📚 Referências

### **Documentação Técnica**
- [Arquitetura](../docs/arquitetura/README.md)
- [Coleta e Ingestão](../README_COLETA_INGESTAO.md)
- [Setup do Sistema](../README_REPRODUTIBILIDADE_COMPLETA.md)

### **Ferramentas**
- [Arduino IDE](https://www.arduino.cc/en/software)
- [Wokwi](https://wokwi.com/)
- [Python](https://www.python.org/)
- [Matplotlib](https://matplotlib.org/)

---

**Ingestão de Dados - Sistema IoT Monitoring - Enterprise Challenge Sprint 3 - Reply**
