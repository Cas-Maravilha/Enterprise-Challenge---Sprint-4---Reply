"""
Código para ESP32 com 4 tipos de sensores industriais:
- Sensor de temperatura PT100 (simulado com ADS1115)
- Sensor de pressão 4-20mA (simulado com ADS1115)
- Sensor de vibração ADXL345 (acelerômetro I2C)
- Sensor de nível ultrassônico HC-SR04

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
# ADS1115 (I2C)
I2C_SCL_PIN = 22
I2C_SDA_PIN = 21
# ADXL345 usa o mesmo barramento I2C
# HC-SR04
ULTRASONIC_TRIGGER_PIN = 5
ULTRASONIC_ECHO_PIN = 18
# LEDs de status
STATUS_LED_PIN = 2

# Endereços I2C
ADS1115_ADDR = 0x48
ADXL345_ADDR = 0x53

# Registros do ADS1115
ADS1115_REG_CONVERSION = 0x00
ADS1115_REG_CONFIG = 0x01
ADS1115_CONFIG_OS_SINGLE = 0x8000
ADS1115_CONFIG_MUX_SINGLE_0 = 0x4000
ADS1115_CONFIG_MUX_SINGLE_1 = 0x5000
ADS1115_CONFIG_PGA_4_096V = 0x0200
ADS1115_CONFIG_MODE_SINGLE = 0x0100
ADS1115_CONFIG_DR_128SPS = 0x0080
ADS1115_CONFIG_COMP_MODE_TRAD = 0x0000
ADS1115_CONFIG_COMP_POL_LOW = 0x0000
ADS1115_CONFIG_COMP_LAT_NONLAT = 0x0000
ADS1115_CONFIG_COMP_QUE_DIS = 0x0003

# Registros do ADXL345
ADXL345_REG_POWER_CTL = 0x2D
ADXL345_REG_DATA_FORMAT = 0x31
ADXL345_REG_DATAX0 = 0x32

# Configuração do LED de status
status_led = machine.Pin(STATUS_LED_PIN, machine.Pin.OUT)

# Configuração do I2C
i2c = machine.I2C(0, scl=machine.Pin(I2C_SCL_PIN), sda=machine.Pin(I2C_SDA_PIN), freq=400000)

# Configuração do sensor ultrassônico
trigger = machine.Pin(ULTRASONIC_TRIGGER_PIN, machine.Pin.OUT)
echo = machine.Pin(ULTRASONIC_ECHO_PIN, machine.Pin.IN)

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

def init_ads1115():
    """Inicializa o ADS1115"""
    try:
        # Verifica se o dispositivo está presente
        devices = i2c.scan()
        if ADS1115_ADDR not in devices:
            print(f"ADS1115 não encontrado no endereço 0x{ADS1115_ADDR:02X}")
            return False
        print(f"ADS1115 encontrado no endereço 0x{ADS1115_ADDR:02X}")
        return True
    except Exception as e:
        print("Erro ao inicializar ADS1115:", e)
        return False

def init_adxl345():
    """Inicializa o ADXL345"""
    try:
        # Verifica se o dispositivo está presente
        devices = i2c.scan()
        if ADXL345_ADDR not in devices:
            print(f"ADXL345 não encontrado no endereço 0x{ADXL345_ADDR:02X}")
            return False
        
        # Configura o ADXL345
        # Ativa o sensor
        i2c.writeto_mem(ADXL345_ADDR, ADXL345_REG_POWER_CTL, bytes([0x08]))
        # Configura o formato de dados (±4g, 10 bits)
        i2c.writeto_mem(ADXL345_ADDR, ADXL345_REG_DATA_FORMAT, bytes([0x01]))
        
        print(f"ADXL345 encontrado e configurado no endereço 0x{ADXL345_ADDR:02X}")
        return True
    except Exception as e:
        print("Erro ao inicializar ADXL345:", e)
        return False

def read_ads1115(channel):
    """Lê um canal do ADS1115"""
    try:
        # Configura o canal
        if channel == 0:
            config = ADS1115_CONFIG_OS_SINGLE | ADS1115_CONFIG_MUX_SINGLE_0
        else:
            config = ADS1115_CONFIG_OS_SINGLE | ADS1115_CONFIG_MUX_SINGLE_1
        
        # Adiciona o resto da configuração
        config |= ADS1115_CONFIG_PGA_4_096V | ADS1115_CONFIG_MODE_SINGLE
        config |= ADS1115_CONFIG_DR_128SPS | ADS1115_CONFIG_COMP_MODE_TRAD
        config |= ADS1115_CONFIG_COMP_POL_LOW | ADS1115_CONFIG_COMP_LAT_NONLAT
        config |= ADS1115_CONFIG_COMP_QUE_DIS
        
        # Envia a configuração
        i2c.writeto_mem(ADS1115_ADDR, ADS1115_REG_CONFIG, bytes([config >> 8, config & 0xFF]))
        
        # Espera pela conversão
        time.sleep(0.01)
        
        # Lê o resultado
        data = i2c.readfrom_mem(ADS1115_ADDR, ADS1115_REG_CONVERSION, 2)
        value = (data[0] << 8) | data[1]
        
        # Converte para valor com sinal
        if value > 0x7FFF:
            value -= 0x10000
        
        return value
    except Exception as e:
        print(f"Erro ao ler ADS1115 canal {channel}:", e)
        return 0

def read_adxl345():
    """Lê os dados do acelerômetro ADXL345"""
    try:
        # Lê 6 bytes de dados (X, Y, Z - 2 bytes cada)
        data = i2c.readfrom_mem(ADXL345_ADDR, ADXL345_REG_DATAX0, 6)
        
        # Converte os bytes em valores de 16 bits com sinal
        x = (data[1] << 8) | data[0]
        if x > 0x7FFF:
            x -= 0x10000
            
        y = (data[3] << 8) | data[2]
        if y > 0x7FFF:
            y -= 0x10000
            
        z = (data[5] << 8) | data[4]
        if z > 0x7FFF:
            z -= 0x10000
        
        # Converte para g (±4g range, 10 bits de resolução)
        x_g = x * 4.0 / 512
        y_g = y * 4.0 / 512
        z_g = z * 4.0 / 512
        
        return (x_g, y_g, z_g)
    except Exception as e:
        print("Erro ao ler ADXL345:", e)
        return (0, 0, 0)

def read_ultrasonic():
    """Lê a distância do sensor ultrassônico HC-SR04"""
    try:
        # Envia pulso de 10µs
        trigger.value(0)
        time.sleep_us(2)
        trigger.value(1)
        time.sleep_us(10)
        trigger.value(0)
        
        # Mede o tempo de retorno do eco
        while echo.value() == 0:
            start = time.ticks_us()
        
        while echo.value() == 1:
            end = time.ticks_us()
        
        # Calcula a distância em cm (velocidade do som = 343m/s)
        duration = time.ticks_diff(end, start)
        distance = (duration * 0.0343) / 2
        
        return distance
    except Exception as e:
        print("Erro ao ler sensor ultrassônico:", e)
        return 0

def read_pt100():
    """Lê o sensor PT100 (simulado com ADS1115 canal 0)"""
    try:
        # Lê o valor bruto do ADS1115
        raw_value = read_ads1115(0)
        
        # Simula a conversão de PT100
        # Em um sistema real, seria necessário considerar o circuito de condicionamento
        # e a curva de calibração específica do sensor
        voltage = raw_value * 4.096 / 32768  # Converte para tensão
        
        # Simula uma relação linear entre tensão e temperatura
        # PT100 tem 100 ohms a 0°C e aumenta ~0.385 ohms/°C
        temperature = (voltage - 1.0) * 100  # Simulação simplificada
        
        return temperature
    except Exception as e:
        print("Erro ao ler PT100:", e)
        return 0

def read_pressure_sensor():
    """Lê o sensor de pressão 4-20mA (simulado com ADS1115 canal 1)"""
    try:
        # Lê o valor bruto do ADS1115
        raw_value = read_ads1115(1)
        
        # Simula a conversão de 4-20mA
        # Em um sistema real, o sinal de corrente seria convertido em tensão
        # através de um resistor de precisão
        voltage = raw_value * 4.096 / 32768  # Converte para tensão
        
        # Simula uma relação linear entre tensão e pressão
        # Supondo um sensor de 0-10 bar mapeado para 4-20mA
        # 1V = 4mA, 5V = 20mA
        current_ma = (voltage / 250) * 1000  # Supondo resistor de 250 ohms
        pressure_bar = (current_ma - 4) * 10 / 16  # Mapeia 4-20mA para 0-10 bar
        
        return pressure_bar
    except Exception as e:
        print("Erro ao ler sensor de pressão:", e)
        return 0

def publish_data(client, data):
    """Publica os dados no broker MQTT"""
    try:
        json_data = ujson.dumps(data)
        client.publish(MQTT_TOPIC, json_data)
        print("Dados publicados:", json_data)
        status_led.value(1)  # Liga o LED para indicar publicação
        time.sleep(0.1)
        status_led.value(0)  # Desliga o LED
    except Exception as e:
        print("Erro ao publicar dados:", e)

def main():
    """Função principal"""
    print("Iniciando sistema de monitoramento industrial...")
    
    # Conecta ao WiFi
    if not connect_wifi():
        return
    
    # Inicializa os sensores
    ads1115_ok = init_ads1115()
    adxl345_ok = init_adxl345()
    
    # Conecta ao broker MQTT
    try:
        client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, MQTT_PORT)
        client.connect()
        print(f"Conectado ao broker MQTT: {MQTT_BROKER}")
    except Exception as e:
        print("Erro ao conectar ao broker MQTT:", e)
        return
    
    # Loop principal
    while True:
        try:
            # Lê os sensores
            temperature = read_pt100() if ads1115_ok else 25.0  # Valor padrão se falhar
            pressure = read_pressure_sensor() if ads1115_ok else 5.0  # Valor padrão se falhar
            accel = read_adxl345() if adxl345_ok else (0.0, 0.0, 1.0)  # Valor padrão se falhar
            distance = read_ultrasonic()
            
            # Calcula a vibração (magnitude da aceleração)
            vibration = (accel[0]**2 + accel[1]**2 + accel[2]**2)**0.5
            
            # Prepara os dados
            data = {
                "timestamp": time.time(),
                "temperature": round(temperature, 2),
                "pressure": round(pressure, 2),
                "vibration": round(vibration, 3),
                "level": round(distance, 1),
                "accel_x": round(accel[0], 3),
                "accel_y": round(accel[1], 3),
                "accel_z": round(accel[2], 3)
            }
            
            # Publica os dados
            publish_data(client, data)
            
            # Espera antes da próxima leitura
            time.sleep(5)
            
        except Exception as e:
            print("Erro no loop principal:", e)
            time.sleep(5)

if __name__ == "__main__":
    main()