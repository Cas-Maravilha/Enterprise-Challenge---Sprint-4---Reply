# Guia de Hardware

Este documento fornece informações detalhadas sobre o hardware utilizado no Sistema de Monitoramento Industrial com ESP32, incluindo especificações dos sensores, diagramas de circuito e considerações para implementação em ambiente industrial real.

## Índice

1. [ESP32](#esp32)
2. [Sensores Industriais](#sensores-industriais)
3. [Circuito Completo](#circuito-completo)
4. [Considerações para Ambiente Industrial](#considerações-para-ambiente-industrial)
5. [Alternativas de Hardware](#alternativas-de-hardware)
6. [Expansões Possíveis](#expansões-possíveis)

## ESP32

### Especificações

O ESP32 é um microcontrolador de baixo custo e baixo consumo com Wi-Fi e Bluetooth integrados.

- **Processador**: Dual-core Tensilica Xtensa LX6, até 240MHz
- **Memória**: 520KB SRAM
- **Conectividade**: Wi-Fi 802.11 b/g/n, Bluetooth 4.2 BR/EDR e BLE
- **GPIO**: 36 pinos
- **ADC**: 18 canais de 12 bits
- **DAC**: 2 canais de 8 bits
- **Interfaces**: SPI, I2C, I2S, UART, CAN, Ethernet MAC
- **Tensão de operação**: 3.3V

### Pinagem

![Pinagem do ESP32](https://via.placeholder.com/800x600/0078D7/FFFFFF?text=Pinagem+do+ESP32)

| Categoria | Pinos |
|-----------|-------|
| ADC | GPIO32-GPIO39 |
| DAC | GPIO25, GPIO26 |
| Touch | GPIO4, GPIO0, GPIO2, GPIO15, GPIO13, GPIO12, GPIO14, GPIO27, GPIO33, GPIO32 |
| SPI | GPIO23 (MOSI), GPIO19 (MISO), GPIO18 (CLK), GPIO5 (CS) |
| I2C | GPIO21 (SDA), GPIO22 (SCL) |
| UART | GPIO1, GPIO3 (UART0), GPIO16, GPIO17 (UART2) |

## Sensores Industriais

### Sensor de Temperatura PT100

O PT100 é um sensor de temperatura de resistência de platina (RTD) amplamente utilizado em aplicações industriais.

- **Faixa de medição**: -200°C a 850°C
- **Precisão**: Classe A (±0.15°C a 0°C)
- **Resistência a 0°C**: 100Ω
- **Coeficiente de temperatura**: 0.00385Ω/Ω/°C
- **Conexão**: 2, 3 ou 4 fios

#### Circuito de Condicionamento

Para conectar um PT100 ao ESP32, é necessário um circuito de condicionamento:

1. **Ponte de Wheatstone**: Para converter variação de resistência em tensão
2. **Amplificador de Instrumentação**: Para amplificar o sinal diferencial
3. **Conversor ADC**: Para converter o sinal analógico em digital

Alternativamente, pode-se usar um módulo MAX31865 que simplifica a interface com o ESP32 via SPI.

### Sensor de Pressão 4-20mA

Sensores de pressão industriais geralmente utilizam o padrão de corrente 4-20mA.

- **Faixa de medição**: Varia conforme o sensor (ex: 0-10 bar)
- **Precisão**: Tipicamente 0.5% a 1% do fundo de escala
- **Sinal de saída**: 4mA (0% da escala) a 20mA (100% da escala)
- **Alimentação**: 24V DC (típico)

#### Circuito de Condicionamento

Para conectar um sensor 4-20mA ao ESP32:

1. **Resistor de precisão**: 250Ω para converter 4-20mA em 1-5V
2. **Divisor de tensão**: Para adequar a faixa de 1-5V para 0-3.3V do ESP32
3. **Proteção**: Diodo Zener para proteção contra sobretensão

### Acelerômetro ADXL345

O ADXL345 é um acelerômetro digital de 3 eixos adequado para medição de vibração.

- **Faixa de medição**: ±2g, ±4g, ±8g, ±16g (selecionável)
- **Resolução**: 10 bits (até 13 bits em certos modos)
- **Interface**: I2C ou SPI
- **Tensão de operação**: 2.0-3.6V
- **Consumo**: 23μA em modo de medição, 0.1μA em standby

#### Conexão com ESP32

Para conectar o ADXL345 ao ESP32 via I2C:

1. Conecte VCC do ADXL345 ao 3.3V do ESP32
2. Conecte GND do ADXL345 ao GND do ESP32
3. Conecte SDA do ADXL345 ao GPIO21 do ESP32
4. Conecte SCL do ADXL345 ao GPIO22 do ESP32
5. Conecte CS do ADXL345 ao 3.3V para modo I2C

### Sensor Ultrassônico HC-SR04

O HC-SR04 é um sensor ultrassônico para medição de distância.

- **Faixa de medição**: 2cm a 400cm
- **Resolução**: 0.3cm
- **Ângulo de medição**: 15°
- **Frequência de trabalho**: 40kHz
- **Tensão de operação**: 5V

#### Conexão com ESP32

Para conectar o HC-SR04 ao ESP32:

1. Conecte VCC do HC-SR04 ao 5V do ESP32 (ou fonte externa)
2. Conecte GND do HC-SR04 ao GND do ESP32
3. Conecte TRIG do HC-SR04 ao GPIO5 do ESP32
4. Conecte ECHO do HC-SR04 ao GPIO18 do ESP32 através de um divisor de tensão (5V para 3.3V)

## Circuito Completo

### Diagrama Esquemático

![Diagrama Esquemático](https://via.placeholder.com/800x600/0078D7/FFFFFF?text=Diagrama+Esquemático)

### Lista de Materiais (BOM)

| Quantidade | Componente | Descrição |
|------------|------------|-----------|
| 1 | ESP32 DevKit V1 | Microcontrolador |
| 1 | PT100 + MAX31865 | Sensor de temperatura |
| 1 | Sensor de pressão 4-20mA | Sensor de pressão |
| 1 | ADXL345 | Acelerômetro |
| 1 | HC-SR04 | Sensor ultrassônico |
| 2 | Chave deslizante | Controle de modo |
| 1 | LED | Indicação de status |
| 1 | Resistor 220Ω | Para o LED |
| 1 | Resistor 250Ω 0.1% | Para o sensor 4-20mA |
| 2 | Resistor 10kΩ | Para divisor de tensão |
| 1 | Protoboard | Para montagem |
| N | Jumpers | Para conexões |

## Considerações para Ambiente Industrial

### Proteção e Isolamento

Para uso em ambiente industrial real, considere:

1. **Isolamento Galvânico**: Use optoacopladores ou isoladores digitais para proteger o ESP32
2. **Proteção contra Surtos**: Adicione supressores de transientes (TVS) nas entradas
3. **Filtros EMI/RFI**: Para reduzir interferência eletromagnética
4. **Caixa de Proteção**: Use caixa com grau de proteção adequado (IP65 ou superior)
5. **Fonte de Alimentação**: Use fonte industrial com proteções

### Certificações Relevantes

Para aplicações industriais, considere as certificações:

- **CE**: Conformidade Europeia
- **UL**: Underwriters Laboratories
- **CSA**: Canadian Standards Association
- **ATEX**: Para ambientes explosivos (quando aplicável)
- **IEC 61010**: Segurança para equipamentos de medição
- **IEC 61326**: Compatibilidade eletromagnética

## Alternativas de Hardware

### Alternativas ao ESP32

- **ESP8266**: Mais barato, mas com menos recursos
- **Raspberry Pi**: Mais poderoso, adequado para edge computing
- **Arduino + Shield Ethernet/WiFi**: Solução mais simples
- **PLCs industriais**: Para aplicações críticas
- **Gateways IoT industriais**: Soluções prontas para uso industrial

### Alternativas aos Sensores

- **Temperatura**: Termopar, NTC, LM35
- **Pressão**: Sensores resistivos, capacitivos
- **Vibração**: MPU6050, MPU9250
- **Nível**: Sensores capacitivos, sensores de pressão diferencial

## Expansões Possíveis

### Sensores Adicionais

- **Sensor de Vazão**: Para monitoramento de fluidos
- **Sensor de Corrente**: Para monitoramento de consumo elétrico
- **Sensor de Gases**: Para detecção de gases tóxicos ou combustíveis
- **Câmera**: Para inspeção visual

### Interfaces de Comunicação

- **RS-485/Modbus**: Para integração com equipamentos industriais
- **CAN Bus**: Para comunicação robusta em ambientes ruidosos
- **LoRaWAN**: Para comunicação de longo alcance e baixo consumo
- **Ethernet Industrial**: Para integração com redes industriais

### Atuadores

- **Relés**: Para controle de equipamentos
- **Válvulas Solenoides**: Para controle de fluidos
- **Inversores de Frequência**: Para controle de motores
- **Alarmes Sonoros/Visuais**: Para alertas locais