# Simulação de Sistema de Monitoramento Industrial com ESP32

Este projeto implementa uma simulação de um sistema de monitoramento industrial utilizando ESP32 e quatro tipos de sensores industriais comuns. A simulação é executada no Wokwi, uma plataforma online para simulação de circuitos eletrônicos.

## Sensores Implementados

1. **Sensor de Temperatura PT100**
   - Simulado com potenciômetro
   - Faixa de medição: -10°C a 120°C
   - Aplicação industrial: Monitoramento de temperatura em processos industriais

2. **Sensor de Pressão 4-20mA**
   - Simulado com potenciômetro
   - Faixa de medição: 0-10 bar
   - Aplicação industrial: Monitoramento de pressão em tubulações e reservatórios

3. **Sensor de Vibração**
   - Simulado com joystick analógico (acelerômetro)
   - Medição em 3 eixos (X, Y, Z)
   - Faixa de medição: ±2g
   - Aplicação industrial: Monitoramento de vibração em máquinas rotativas

4. **Sensor de Nível Ultrassônico HC-SR04**
   - Sensor ultrassônico real
   - Faixa de medição: 2-400 cm
   - Aplicação industrial: Medição de nível em tanques e silos

## Funcionalidades

- Leitura dos quatro sensores em tempo real
- Processamento e conversão dos dados para unidades industriais
- Envio dos dados para um broker MQTT público (HiveMQ)
- Simulação de falhas de sensores e rede através de chaves
- Indicação visual de status através de LED
- Dashboard web para visualização dos dados em tempo real

## Como Usar a Simulação

### No Wokwi

1. Acesse o link da simulação: [Simulação no Wokwi](https://wokwi.com/projects/new/esp32)
2. Copie e cole os arquivos:
   - `main.py`: Código principal
   - `boot.py`: Script de inicialização
   - `diagram.json`: Configuração do circuito
   - `wokwi-project.txt`: Descrição do projeto

3. Clique em "Start" para iniciar a simulação
4. Interaja com os componentes:
   - Ajuste os potenciômetros para simular mudanças de temperatura e pressão
   - Mova o joystick para simular vibração
   - Aproxime ou afaste objetos do sensor ultrassônico
   - Use as chaves para simular falhas

### Dashboard Web

1. Abra o arquivo `dashboard.html` em um navegador web
2. O dashboard se conectará automaticamente ao broker MQTT
3. Visualize os dados dos sensores em tempo real
4. Observe os alertas gerados quando os valores ultrapassam os limites

## Estrutura do Código

- `main.py`: Código principal que lê os sensores e envia os dados
- `boot.py`: Script de inicialização do ESP32
- `diagram.json`: Configuração do circuito no Wokwi
- `dashboard.html`: Interface web para visualização dos dados

## Circuito

O circuito no Wokwi inclui:

- ESP32 DevKit V1
- 2 potenciômetros (temperatura e pressão)
- 1 joystick analógico (vibração)
- 1 sensor ultrassônico HC-SR04 (nível)
- 2 chaves deslizantes (simulação de falhas)
- 1 LED (indicação de status)
- 1 resistor de 220Ω (para o LED)

## Comunicação MQTT

- **Broker**: broker.hivemq.com
- **Porta**: 1883 (MQTT), 8000 (WebSocket)
- **Tópico**: industrial/sensors/data
- **Formato dos dados**:
  ```json
  {
    "timestamp": 1630000000,
    "temperature": 25.5,
    "pressure": 5.2,
    "vibration": 0.15,
    "level": 120.5,
    "accel_x": 0.01,
    "accel_y": 0.02,
    "accel_z": 0.98,
    "sensor_failure": false,
    "network_failure": false
  }
  ```

## Extensões Possíveis

1. Adicionar mais sensores industriais (pH, vazão, etc.)
2. Implementar algoritmos de detecção de anomalias
3. Adicionar armazenamento local de dados (SD Card)
4. Implementar comunicação com sistemas SCADA
5. Adicionar autenticação e segurança na comunicação MQTT