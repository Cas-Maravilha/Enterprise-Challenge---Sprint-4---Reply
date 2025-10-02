# Coleta de Dados Estruturada para Sensores Industriais

Este projeto implementa uma solução completa para coleta de dados estruturada de sensores industriais, com output em formato CSV via Monitor Serial, scripts Python para automação da coleta e diferentes cenários de simulação.

## Componentes do Sistema

1. **Firmware ESP32 (`main_csv.py`)**
   - Coleta dados de 4 tipos de sensores industriais
   - Gera output em formato CSV via Monitor Serial
   - Implementa 3 cenários de simulação: normal, alerta e falha
   - Controle de cenários via chaves físicas

2. **Script de Coleta de Dados (`serial_data_collector.py`)**
   - Automatiza a coleta de dados via porta serial
   - Salva os dados em arquivos CSV
   - Suporte para coleta de diferentes cenários

3. **Script de Análise de Dados (`data_analyzer.py`)**
   - Processa os arquivos CSV coletados
   - Gera gráficos de séries temporais e distribuições
   - Produz relatórios com estatísticas

4. **Simulador de Cenários (`scenario_simulator.py`)**
   - Gera dados sintéticos para testes e análises
   - Simula cenários normal, alerta e falha
   - Permite adicionar anomalias aleatórias

5. **Scripts de Automação**
   - `run_simulation.bat` (Windows)
   - `run_simulation.sh` (Linux/Mac)

## Formato dos Dados CSV

Os dados são coletados no seguinte formato CSV:

```
timestamp,mode,temperature,pressure,vibration_x,vibration_y,vibration_z,vibration_mag,level,status
1630000000,0,25.50,5.20,0.010,0.020,0.980,0.981,120.5,NORMAL
1630000001,1,35.75,7.30,0.150,0.250,0.950,0.990,150.2,ALERT
1630000002,2,NULL,NULL,NULL,NULL,NULL,NULL,NULL,FAILURE
```

Onde:
- `timestamp`: Timestamp Unix em segundos
- `mode`: Modo de operação (0=Normal, 1=Alerta, 2=Falha)
- `temperature`: Temperatura em °C
- `pressure`: Pressão em bar
- `vibration_x/y/z`: Componentes de vibração em g
- `vibration_mag`: Magnitude da vibração em g
- `level`: Nível em cm
- `status`: Status textual (NORMAL, ALERT, FAILURE)

## Cenários de Simulação

### 1. Cenário Normal
- Temperatura: 20-30°C
- Pressão: 4-6 bar
- Vibração: 0.3-0.7g
- Nível: 80-120cm

### 2. Cenário de Alerta
- Temperatura: 30-40°C
- Pressão: 6-8 bar
- Vibração: 0.8-1.5g
- Nível: 130-170cm

### 3. Cenário de Falha
- Valores extremos ou nulos
- Temperatura: -10 a 120°C ou NULL
- Pressão: 0 a 15 bar ou NULL
- Vibração: 1.5 a 5.0g ou NULL
- Nível: 0 a 300cm ou NULL

## Como Usar

### Coleta de Dados do ESP32

1. Carregue o firmware `main_csv.py` no ESP32
2. Execute o script de coleta:

```bash
python serial_data_collector.py --port COM3 --duration 60 --output dados.csv
```

Para coletar dados de cenários específicos:

```bash
python serial_data_collector.py --port COM3 --duration 60 --scenario normal --output-dir data
```

### Simulação de Dados

Para gerar dados simulados:

```bash
python scenario_simulator.py --scenario all --samples 100 --interval 1.0 --output-dir data
```

### Análise de Dados

Para analisar os dados coletados:

```bash
python data_analyzer.py --input data --output-dir analysis
```

### Execução Completa da Simulação

No Windows:
```
run_simulation.bat
```

No Linux/Mac:
```
./run_simulation.sh
```

## Requisitos

- Python 3.6+
- Bibliotecas Python:
  - pyserial
  - pandas
  - numpy
  - matplotlib
  - seaborn
- ESP32 com MicroPython (para execução real)

## Extensões Possíveis

1. Adicionar mais tipos de sensores
2. Implementar detecção automática de anomalias
3. Criar um dashboard web para visualização em tempo real
4. Integrar com bancos de dados para armazenamento persistente
5. Adicionar suporte para comunicação sem fio (WiFi, Bluetooth)