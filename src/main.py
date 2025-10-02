"""
Simulação de sistema de monitoramento industrial com ESP32 e 4 tipos de sensores:
1. Sensor de temperatura PT100 (simulado com potenciômetro)
2. Sensor de pressão 4-20mA (simulado com potenciômetro)
3. Sensor de vibração (simulado com joystick analógico)
4. Sensor de nível ultrassônico HC-SR04

O código lê os sensores, processa os dados e envia para um servidor MQTT.
"""

import time
import machine
import network
import ujson
from umqtt.simple import MQTTClient

# Configurações de rede e MQTT
WIFI_SSID = "Wokwi-GUEST"
WIFI_PASSWORD = ""
MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883
MQTT_TOPIC = "industrial/sensors/data"
MQTT_CLIENT_ID = "esp32_industrial_sensors"

# Configuração dos pinos
# Sensores analógicos
PT100_PIN = 33        # Potenciômetro 1 simula PT100
PRESSURE_PIN = 25     # Potenciômetro 2 simula sensor de pressão 4-20mA
VIBRATION_X_PIN = 34  # Joystick X simula vibração X
VIBRATION_Y_PIN = 35  # Joystick Y simula vibração Y
VIBRATION_BTN_PIN = 32  # Botão do joystick

# Sensor ultrassônico HC-SR04
ULTRASONIC_TRIGGER_PIN = 5
ULTRASONIC_ECHO_PIN = 18

# Chaves de controle
SWITCH1_PIN = 26
SWITCH2_PIN = 27

# LED de status
STATUS_LED_PIN = 2

# Configuração dos pinos
# ADC para sensores analógicos
adc_pt100 = machine.ADC(machine.Pin(PT100_PIN))
adc_pt100.atten(machine.ADC.ATTN_11DB)  # Escala completa: 3.3V

adc_pressure = machine.ADC(machine.Pin(PRESSURE_PIN))
adc_pressure.atten(machine.ADC.ATTN_11DB)  # Escala completa: 3.3V

adc_vibration_x = machine.ADC(machine.Pin(VIBRATION_X_PIN))
adc_vibration_x.atten(machine.ADC.ATTN_11DB)  # Escala completa: 3.3V

adc_vibration_y = machine.ADC(machine.Pin(VIBRATION_Y_PIN))
adc_vibration_y.atten(machine.ADC.ATTN_11DB)  # Escala completa: 3.3V

vibration_btn = machine.Pin(VIBRATION_BTN_PIN, machine.Pin.IN, machine.Pin.PULL_UP)

# Sensor ultrassônico
trigger = machine.Pin(ULTRASONIC_TRIGGER_PIN, machine.Pin.OUT)
echo = machine.Pin(ULTRASONIC_ECHO_PIN, machine.Pin.IN)

# Chaves de controle
switch1 = machine.Pin(SWITCH1_PIN, machine.Pin.IN, machine.Pin.PULL_UP)
switch2 = machine.Pin(SWITCH2_PIN, machine.Pin.IN, machine.Pin.PULL_UP)

# LED de status
status_led = machine.Pin(STATUS_LED_PIN, machine.Pin.OUT)

# Variáveis para simulação de falhas
simulate_sensor_failure = False
simulate_network_failure = False

def connect_wifi():
    """Conecta ao WiFi"""
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('Conectando ao WiFi...')
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)
        for _ in range(10):  # Espera até 10 segundos
            if wlan.isconnected():
                break
            time.sleep(1)
    if wlan.isconnected():
        print('Conectado ao WiFi:', wlan.ifconfig()[0])
        return True
    else:
        print('Falha na conexão WiFi')
        return False

def read_pt100():
    """Lê o sensor PT100 (simulado com potenciômetro)"""
    if simulate_sensor_failure:
        return None
    
    # Lê o valor do ADC (0-4095)
    raw_value = adc_pt100.read()
    
    # Converte para temperatura (-10°C a 120°C)
    temperature = -10 + (raw_value / 4095) * 130
    
    return temperature

def read_pressure_sensor():
    """Lê o sensor de pressão 4-20mA (simulado com potenciômetro)"""
    if simulate_sensor_failure:
        return None
    
    # Lê o valor do ADC (0-4095)
    raw_value = adc_pressure.read()
    
    # Converte para pressão (0-10 bar)
    # Simula um sensor 4-20mA onde 4mA = 0 bar e 20mA = 10 bar
    pressure = (raw_value / 4095) * 10
    
    return pressure

def read_vibration_sensor():
    """Lê o sensor de vibração (simulado com joystick)"""
    if simulate_sensor_failure:
        return None, None, None
    
    # Lê os valores do ADC (0-4095)
    x_raw = adc_vibration_x.read()
    y_raw = adc_vibration_y.read()
    btn = vibration_btn.value()
    
    # Converte para aceleração (-2g a +2g)
    # O joystick em repouso está no meio da escala (2047)
    x_g = ((x_raw - 2047) / 2047) * 2
    y_g = ((y_raw - 2047) / 2047) * 2
    
    # Simula o eixo Z (normalmente 1g quando em repouso)
    z_g = 1.0 if btn == 1 else -1.0
    
    # Calcula a magnitude da vibração
    vibration = (x_g**2 + y_g**2 + z_g**2)**0.5
    
    return x_g, y_g, z_g, vibration

def read_ultrasonic():
    """Lê a distância do sensor ultrassônico HC-SR04"""
    if simulate_sensor_failure:
        return None
    
    try:
        # Envia pulso de 10µs
        trigger.value(0)
        time.sleep_us(2)
        trigger.value(1)
        time.sleep_us(10)
        trigger.value(0)
        
        # Mede o tempo de retorno do eco
        pulse_start = time.ticks_us()
        pulse_end = pulse_start
        
        # Espera pelo início do pulso (timeout de 30ms)
        timeout = time.ticks_add(pulse_start, 30000)
        while echo.value() == 0:
            pulse_start = time.ticks_us()
            if time.ticks_diff(timeout, pulse_start) <= 0:
                return None  # Timeout
        
        # Espera pelo fim do pulso (timeout de 30ms)
        timeout = time.ticks_add(pulse_start, 30000)
        while echo.value() == 1:
            pulse_end = time.ticks_us()
            if time.ticks_diff(timeout, pulse_end) <= 0:
                return None  # Timeout
        
        # Calcula a distância em cm (velocidade do som = 343m/s)
        duration = time.ticks_diff(pulse_end, pulse_start)
        distance = (duration * 0.0343) / 2
        
        # Limita a distância a um valor máximo razoável (400cm)
        if distance > 400:
            return None
            
        return distance
    except Exception as e:
        print("Erro ao ler sensor ultrassônico:", e)
        return None

def check_switches():
    """Verifica o estado das chaves para simulação de falhas"""
    global simulate_sensor_failure, simulate_network_failure
    
    # Switch 1 controla falha de sensor
    simulate_sensor_failure = (switch1.value() == 0)
    
    # Switch 2 controla falha de rede
    simulate_network_failure = (switch2.value() == 0)

def blink_led(times=1, delay=0.1):
    """Pisca o LED de status"""
    for _ in range(times):
        status_led.value(1)
        time.sleep(delay)
        status_led.value(0)
        time.sleep(delay)

def publish_data(client, data):
    """Publica os dados no broker MQTT"""
    if simulate_network_failure:
        print("Simulando falha de rede - dados não enviados")
        blink_led(3, 0.2)  # Pisca 3 vezes rápido para indicar erro
        return False
    
    try:
        json_data = ujson.dumps(data)
        client.publish(MQTT_TOPIC, json_data)
        print("Dados publicados:", json_data)
        blink_led(1, 0.1)  # Pisca 1 vez para indicar envio bem-sucedido
        return True
    except Exception as e:
        print("Erro ao publicar dados:", e)
        blink_led(2, 0.2)  # Pisca 2 vezes para indicar erro
        return False

def main():
    """Função principal"""
    print("\n--- Sistema de Monitoramento Industrial com ESP32 ---")
    print("Sensores:")
    print("1. Temperatura PT100 (simulado com potenciômetro)")
    print("2. Pressão 4-20mA (simulado com potenciômetro)")
    print("3. Vibração (simulado com joystick analógico)")
    print("4. Nível ultrassônico HC-SR04")
    print("Controles:")
    print("- Switch 1: Simular falha de sensor")
    print("- Switch 2: Simular falha de rede")
    print("Iniciando...")
    
    # Conecta ao WiFi
    wifi_connected = connect_wifi()
    if not wifi_connected:
        print("Continuando sem conexão WiFi...")
    
    # Conecta ao broker MQTT
    mqtt_client = None
    if wifi_connected:
        try:
            mqtt_client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, MQTT_PORT)
            mqtt_client.connect()
            print(f"Conectado ao broker MQTT: {MQTT_BROKER}")
        except Exception as e:
            print("Erro ao conectar ao broker MQTT:", e)
            mqtt_client = None
    
    # Pisca o LED para indicar inicialização completa
    blink_led(5, 0.1)
    
    # Loop principal
    while True:
        try:
            # Verifica o estado das chaves
            check_switches()
            
            # Lê os sensores
            temperature = read_pt100()
            pressure = read_pressure_sensor()
            x_g, y_g, z_g, vibration = read_vibration_sensor()
            level = read_ultrasonic()
            
            # Prepara os dados
            timestamp = time.time()
            data = {
                "timestamp": timestamp,
                "temperature": round(temperature, 1) if temperature is not None else None,
                "pressure": round(pressure, 2) if pressure is not None else None,
                "vibration": round(vibration, 3) if vibration is not None else None,
                "level": round(level, 1) if level is not None else None,
                "accel_x": round(x_g, 3) if x_g is not None else None,
                "accel_y": round(y_g, 3) if y_g is not None else None,
                "accel_z": round(z_g, 3) if z_g is not None else None,
                "sensor_failure": simulate_sensor_failure,
                "network_failure": simulate_network_failure
            }
            
            # Exibe os dados no console
            print("-" * 40)
            print(f"Timestamp: {timestamp}")
            print(f"Temperatura: {data['temperature']} °C")
            print(f"Pressão: {data['pressure']} bar")
            print(f"Vibração: {data['vibration']} g")
            print(f"Nível: {data['level']} cm")
            print(f"Aceleração X/Y/Z: {data['accel_x']}/{data['accel_y']}/{data['accel_z']} g")
            print(f"Falha de sensor: {simulate_sensor_failure}")
            print(f"Falha de rede: {simulate_network_failure}")
            
            # Publica os dados se o MQTT estiver conectado
            if mqtt_client:
                publish_data(mqtt_client, data)
            
            # Espera antes da próxima leitura
            time.sleep(2)
            
        except Exception as e:
            print("Erro no loop principal:", e)
            blink_led(4, 0.2)  # Pisca 4 vezes para indicar erro grave
            time.sleep(2)

if __name__ == "__main__":
    main()