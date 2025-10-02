# Guia de Configuração

Este documento fornece instruções detalhadas para configurar o Sistema de Monitoramento Industrial com ESP32, tanto para hardware real quanto para simulação no Wokwi.

## Índice

1. [Configuração do Hardware](#configuração-do-hardware)
2. [Configuração do ESP32](#configuração-do-esp32)
3. [Configuração do Ambiente de Desenvolvimento](#configuração-do-ambiente-de-desenvolvimento)
4. [Simulação no Wokwi](#simulação-no-wokwi)
5. [Configuração do Broker MQTT](#configuração-do-broker-mqtt)
6. [Configuração do Dashboard](#configuração-do-dashboard)
7. [Troubleshooting](#troubleshooting)

## Configuração do Hardware

### Lista de Componentes

- 1x ESP32 DevKit V1
- 1x Sensor de temperatura PT100 (ou potenciômetro para simulação)
- 1x Sensor de pressão 4-20mA (ou potenciômetro para simulação)
- 1x Acelerômetro ADXL345 (ou joystick analógico para simulação)
- 1x Sensor ultrassônico HC-SR04
- 2x Chaves deslizantes (para controle de modo)
- 1x LED (para indicação de status)
- 1x Resistor de 220Ω (para o LED)
- Jumpers e protoboard

### Diagrama de Conexões

| Componente | Pino ESP32 | Descrição |
|------------|------------|-----------|
| PT100 / Potenciômetro | GPIO33 (ADC1_CH5) | Sensor de temperatura |
| Pressão / Potenciômetro | GPIO25 (ADC2_CH8) | Sensor de pressão |
| ADXL345 / Joystick X | GPIO34 (ADC1_CH6) | Vibração X |
| ADXL345 / Joystick Y | GPIO35 (ADC1_CH7) | Vibração Y |
| ADXL345 / Joystick BTN | GPIO32 | Botão do joystick |
| HC-SR04 TRIG | GPIO5 | Trigger do sensor ultrassônico |
| HC-SR04 ECHO | GPIO18 | Echo do sensor ultrassônico |
| Chave 1 | GPIO26 | Controle de modo 1 |
| Chave 2 | GPIO27 | Controle de modo 2 |
| LED | GPIO2 | LED de status |

### Montagem Passo a Passo

1. Conecte o ESP32 à protoboard
2. Conecte o sensor de temperatura (PT100) ou potenciômetro ao GPIO33
3. Conecte o sensor de pressão ou potenciômetro ao GPIO25
4. Conecte o acelerômetro ADXL345 ou joystick:
   - Eixo X ao GPIO34
   - Eixo Y ao GPIO35
   - Botão ao GPIO32
5. Conecte o sensor ultrassônico HC-SR04:
   - Pino TRIG ao GPIO5
   - Pino ECHO ao GPIO18
6. Conecte as chaves de controle:
   - Chave 1 ao GPIO26
   - Chave 2 ao GPIO27
7. Conecte o LED de status:
   - Ânodo ao GPIO2 através do resistor de 220Ω
   - Cátodo ao GND

## Configuração do ESP32

### Instalação do MicroPython

1. Baixe o firmware MicroPython para ESP32:
   - Acesse [micropython.org/download](https://micropython.org/download/esp32/)
   - Baixe a versão mais recente do firmware

2. Instale o esptool:
   ```bash
   pip install esptool
   ```

3. Apague a flash do ESP32:
   ```bash
   esptool.py --port COM3 erase_flash
   ```

4. Instale o firmware MicroPython:
   ```bash
   esptool.py --port COM3 --baud 460800 write_flash -z 0x1000 esp32-20220117-v1.18.bin
   ```

### Transferência dos Arquivos

1. Instale o ampy:
   ```bash
   pip install adafruit-ampy
   ```

2. Transfira os arquivos para o ESP32:
   ```bash
   ampy --port COM3 put main.py
   ampy --port COM3 put boot.py
   ```

## Configuração do Ambiente de Desenvolvimento

### Instalação das Dependências

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/sistema-monitoramento-industrial.git
   cd sistema-monitoramento-industrial
   ```

2. Crie um ambiente virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

## Simulação no Wokwi

### Configuração do Projeto

1. Acesse [Wokwi](https://wokwi.com/projects/new/esp32)
2. Clique em "Library Manager" e adicione os componentes:
   - ESP32 DevKit V1
   - Potentiometer (2x)
   - Analog Joystick
   - HC-SR04 Ultrasonic Distance Sensor
   - LED
   - Slide Switch (2x)
   - Resistor (220Ω)

3. Importe o arquivo `wokwi_diagram.json`:
   - Clique em "Project" > "Load Diagram"
   - Selecione o arquivo `wokwi_diagram.json`

4. Copie o código de `main.py` para o editor

5. Clique em "Start" para iniciar a simulação

### Configuração do Monitor Serial

1. Clique no ícone do monitor serial no canto inferior direito
2. Defina a velocidade para 115200 baud
3. O monitor exibirá os dados em formato CSV

## Configuração do Broker MQTT

### Broker Público (HiveMQ)

O código está configurado para usar o broker público HiveMQ:
- Host: broker.hivemq.com
- Porta: 1883 (MQTT) / 8000 (WebSocket)
- Tópico: industrial/sensors/data

### Broker Local (Mosquitto)

Para configurar um broker local:

1. Instale o Mosquitto:
   - Linux: `sudo apt install mosquitto mosquitto-clients`
   - Windows: Baixe o instalador em [mosquitto.org](https://mosquitto.org/download/)

2. Inicie o serviço:
   - Linux: `sudo systemctl start mosquitto`
   - Windows: Inicie o serviço pelo Gerenciador de Serviços

3. Altere a configuração no código:
   ```python
   MQTT_BROKER = "localhost"
   ```

## Configuração do Dashboard

### Inicialização do Dashboard

1. Execute o script do dashboard:
   ```bash
   python analysis/interactive_dashboard.py
   ```

2. Acesse o dashboard no navegador:
   - URL: http://localhost:8050

### Personalização do Dashboard

Para personalizar o dashboard, edite o arquivo `interactive_dashboard.py`:

- Altere o layout modificando a estrutura HTML/CSS
- Adicione novos gráficos criando funções adicionais
- Modifique os algoritmos de detecção de anomalias

## Troubleshooting

### Problemas Comuns

1. **ESP32 não conecta ao WiFi**
   - Verifique as credenciais WiFi
   - Certifique-se de que o ESP32 está no alcance do roteador
   - Tente reiniciar o ESP32

2. **Dados não aparecem no monitor serial**
   - Verifique se a velocidade (baud rate) está correta (115200)
   - Verifique se os sensores estão conectados corretamente
   - Reinicie o ESP32

3. **Dados não são publicados no MQTT**
   - Verifique a conexão com o broker MQTT
   - Verifique se o tópico está correto
   - Verifique se o broker permite publicações anônimas

4. **Erros na simulação do Wokwi**
   - Verifique se o diagrama está correto
   - Verifique se o código não tem erros de sintaxe
   - Tente recarregar a página

5. **Dashboard não exibe dados**
   - Verifique se os arquivos CSV estão no formato correto
   - Verifique se o caminho para os arquivos está correto
   - Verifique se as bibliotecas estão instaladas corretamente