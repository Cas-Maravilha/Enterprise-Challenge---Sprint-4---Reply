"""
Código ESP32 para coleta de dados estruturada com output em formato CSV via Monitor Serial.
Implementa diferentes cenários de simulação: normal, alerta e falha.
"""
import time
import machine
import random

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
SWITCH1_PIN = 26  # Controla o modo de simulação
SWITCH2_PIN = 27  # Controla o modo de simulação

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

# Modos de simulação
MODE_NORMAL = 0
MODE_ALERT = 1
MODE_FAILURE = 2

# Cabeçalho CSV
CSV_HEADER = "timestamp,mode,temperature,pressure,vibration_x,vibration_y,vibration_z,vibration_mag,level,status"

def blink_led(times=1, delay=0.1):
    """Pisca o LED de status"""
    for _ in range(times):
        status_led.value(1)
        time.sleep(delay)
        status_led.value(0)
        time.sleep(delay)

def get_simulation_mode():
    """Determina o modo de simulação com base nas chaves"""
    sw1 = switch1.value()
    sw2 = switch2.value()
    
    if sw1 == 1 and sw2 == 1:
        return MODE_NORMAL
    elif sw1 == 0 and sw2 == 1:
        return MODE_ALERT
    else:
        return MODE_FAILURE

def read_pt100(mode):
    """Lê o sensor PT100 (simulado com potenciômetro)"""
    # Lê o valor do ADC (0-4095)
    raw_value = adc_pt100.read()
    
    # Converte para temperatura (-10°C a 120°C)
    temperature = -10 + (raw_value / 4095) * 130
    
    # Ajusta com base no modo
    if mode == MODE_ALERT:
        # Adiciona flutuação para simular alerta
        temperature += random.uniform(10, 20)
    elif mode == MODE_FAILURE:
        # Simula falha (valores extremos ou None)
        if random.random() < 0.3:
            return None
        else:
            temperature = random.choice([-20, 150])
    
    return temperature

def read_pressure_sensor(mode):
    """Lê o sensor de pressão 4-20mA (simulado com potenciômetro)"""
    # Lê o valor do ADC (0-4095)
    raw_value = adc_pressure.read()
    
    # Converte para pressão (0-10 bar)
    pressure = (raw_value / 4095) * 10
    
    # Ajusta com base no modo
    if mode == MODE_ALERT:
        # Adiciona flutuação para simular alerta
        pressure += random.uniform(1, 2)
    elif mode == MODE_FAILURE:
        # Simula falha (valores extremos ou None)
        if random.random() < 0.3:
            return None
        else:
            pressure = random.choice([-1, 15])
    
    return pressure

def read_vibration_sensor(mode):
    """Lê o sensor de vibração (simulado com joystick)"""
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
    
    # Ajusta com base no modo
    if mode == MODE_ALERT:
        # Adiciona vibração para simular alerta
        x_g += random.uniform(0.5, 1.0) * random.choice([-1, 1])
        y_g += random.uniform(0.5, 1.0) * random.choice([-1, 1])
        z_g += random.uniform(0.5, 1.0) * random.choice([-1, 1])
    elif mode == MODE_FAILURE:
        # Simula falha (valores extremos ou None)
        if random.random() < 0.3:
            return None, None, None
        else:
            x_g = random.uniform(3, 5) * random.choice([-1, 1])
            y_g = random.uniform(3, 5) * random.choice([-1, 1])
            z_g = random.uniform(3, 5) * random.choice([-1, 1])
    
    # Calcula a magnitude da vibração
    vibration_mag = (x_g**2 + y_g**2 + z_g**2)**0.5
    
    return x_g, y_g, z_g, vibration_mag

def read_ultrasonic(mode):
    """Lê a distância do sensor ultrassônico HC-SR04"""
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
        
        # Ajusta com base no modo
        if mode == MODE_ALERT:
            # Adiciona flutuação para simular alerta
            distance += random.uniform(10, 30)
        elif mode == MODE_FAILURE:
            # Simula falha (valores extremos ou None)
            if random.random() < 0.3:
                return None
            else:
                distance = random.choice([0, 500])
        
        return distance
    except:
        return None

def get_status_text(mode):
    """Retorna o texto de status com base no modo"""
    if mode == MODE_NORMAL:
        return "NORMAL"
    elif mode == MODE_ALERT:
        return "ALERT"
    else:
        return "FAILURE"

def format_csv_line(timestamp, mode, temp, press, vib_x, vib_y, vib_z, vib_mag, level):
    """Formata uma linha CSV com os dados dos sensores"""
    status = get_status_text(mode)
    
    # Formata cada valor, substituindo None por "NULL"
    temp_str = f"{temp:.2f}" if temp is not None else "NULL"
    press_str = f"{press:.2f}" if press is not None else "NULL"
    vib_x_str = f"{vib_x:.3f}" if vib_x is not None else "NULL"
    vib_y_str = f"{vib_y:.3f}" if vib_y is not None else "NULL"
    vib_z_str = f"{vib_z:.3f}" if vib_z is not None else "NULL"
    vib_mag_str = f"{vib_mag:.3f}" if vib_mag is not None else "NULL"
    level_str = f"{level:.1f}" if level is not None else "NULL"
    
    # Monta a linha CSV
    return f"{timestamp},{mode},{temp_str},{press_str},{vib_x_str},{vib_y_str},{vib_z_str},{vib_mag_str},{level_str},{status}"

def main():
    """Função principal"""
    print("\n--- Sistema de Coleta de Dados Estruturada ---")
    print("Formato CSV via Monitor Serial")
    print("Modos de simulação:")
    print("- Normal: Ambas as chaves para cima")
    print("- Alerta: Chave 1 para baixo, Chave 2 para cima")
    print("- Falha: Chave 2 para baixo (qualquer posição da Chave 1)")
    print("\nIniciando coleta de dados...")
    
    # Imprime o cabeçalho CSV
    print(CSV_HEADER)
    
    # Pisca o LED para indicar inicialização
    blink_led(3, 0.2)
    
    # Loop principal
    while True:
        try:
            # Determina o modo de simulação
            mode = get_simulation_mode()
            
            # Lê os sensores
            timestamp = time.time()
            temperature = read_pt100(mode)
            pressure = read_pressure_sensor(mode)
            
            # Lê o sensor de vibração
            vibration_values = read_vibration_sensor(mode)
            if vibration_values is not None:
                vib_x, vib_y, vib_z, vib_mag = vibration_values
            else:
                vib_x = vib_y = vib_z = vib_mag = None
            
            # Lê o sensor ultrassônico
            level = read_ultrasonic(mode)
            
            # Formata e imprime a linha CSV
            csv_line = format_csv_line(timestamp, mode, temperature, pressure, 
                                      vib_x, vib_y, vib_z, vib_mag, level)
            print(csv_line)
            
            # Pisca o LED para indicar leitura
            blink_led(1, 0.05)
            
            # Espera antes da próxima leitura
            time.sleep(1)
            
        except Exception as e:
            print(f"ERROR,{time.time()},{str(e)}")
            blink_led(5, 0.1)
            time.sleep(1)

if __name__ == "__main__":
    main()