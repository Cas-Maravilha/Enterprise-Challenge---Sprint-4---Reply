/*
 * Sistema de Coleta e Ingestão ESP32
 * Enterprise Challenge Sprint 3 - Reply
 * 
 * Este código implementa coleta de dados de sensores ESP32
 * com registro no Monitor Serial e envio via MQTT
 */

#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>
#include <DHT.h>
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BME280.h>

// Configurações WiFi
const char* ssid = "SEU_WIFI_SSID";
const char* password = "SUA_SENHA_WIFI";

// Configurações MQTT
const char* mqtt_server = "broker.hivemq.com";
const int mqtt_port = 1883;
const char* mqtt_topic = "industrial/sensors/ESP32_001/data";

// Configurações dos Sensores
#define DHT_PIN 4
#define DHT_TYPE DHT22
#define LDR_PIN 34
#define PIR_PIN 2
#define LED_PIN 2

// Objetos dos Sensores
DHT dht(DHT_PIN, DHT_TYPE);
Adafruit_BME280 bme;

// Cliente MQTT
WiFiClient espClient;
PubSubClient client(espClient);

// Variáveis de controle
unsigned long lastMsg = 0;
unsigned long lastSensorRead = 0;
const unsigned long sensorInterval = 1000; // 1 segundo
const unsigned long mqttInterval = 5000;   // 5 segundos

// Contador de leituras
int readingCount = 0;

// Estrutura para dados dos sensores
struct SensorData {
  float temperature;
  float humidity;
  int lightLevel;
  bool motion;
  float pressure;
  float altitude;
  float vibration_x;
  float vibration_y;
  float vibration_z;
  float batteryLevel;
  int signalStrength;
  unsigned long timestamp;
  int readingId;
};

void setup() {
  Serial.begin(115200);
  Serial.println("=== Sistema de Coleta e Ingestão ESP32 ===");
  Serial.println("Enterprise Challenge Sprint 3 - Reply");
  Serial.println("==========================================");
  
  // Inicializar pinos
  pinMode(LED_PIN, OUTPUT);
  pinMode(PIR_PIN, INPUT);
  pinMode(LDR_PIN, INPUT);
  
  // Inicializar sensores
  dht.begin();
  
  if (!bme.begin(0x76)) {
    Serial.println("Erro: Sensor BME280 não encontrado!");
  } else {
    Serial.println("Sensor BME280 inicializado com sucesso!");
  }
  
  // Conectar WiFi
  setupWiFi();
  
  // Configurar MQTT
  client.setServer(mqtt_server, mqtt_port);
  client.setCallback(callback);
  
  // Inicializar LED
  digitalWrite(LED_PIN, LOW);
  
  Serial.println("Sistema inicializado com sucesso!");
  Serial.println("Iniciando coleta de dados...");
  Serial.println();
  
  // Cabeçalho do Monitor Serial
  printHeader();
}

void loop() {
  // Reconectar MQTT se necessário
  if (!client.connected()) {
    reconnect();
  }
  client.loop();
  
  // Ler sensores a cada 1 segundo
  if (millis() - lastSensorRead >= sensorInterval) {
    readSensors();
    lastSensorRead = millis();
  }
  
  // Enviar via MQTT a cada 5 segundos
  if (millis() - lastMsg >= mqttInterval) {
    sendToMQTT();
    lastMsg = millis();
  }
  
  delay(100);
}

void setupWiFi() {
  Serial.print("Conectando ao WiFi: ");
  Serial.println(ssid);
  
  WiFi.begin(ssid, password);
  
  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts < 20) {
    delay(500);
    Serial.print(".");
    attempts++;
  }
  
  if (WiFi.status() == WL_CONNECTED) {
    Serial.println();
    Serial.println("WiFi conectado com sucesso!");
    Serial.print("IP: ");
    Serial.println(WiFi.localIP());
    Serial.print("RSSI: ");
    Serial.print(WiFi.RSSI());
    Serial.println(" dBm");
  } else {
    Serial.println();
    Serial.println("Falha na conexão WiFi!");
  }
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Tentando conectar ao MQTT...");
    
    if (client.connect("ESP32Client")) {
      Serial.println(" conectado!");
      client.subscribe("industrial/commands/ESP32_001");
    } else {
      Serial.print(" falhou, rc=");
      Serial.print(client.state());
      Serial.println(" tentando novamente em 5 segundos");
      delay(5000);
    }
  }
}

void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Mensagem recebida [");
  Serial.print(topic);
  Serial.print("]: ");
  
  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
  }
  Serial.println();
}

void readSensors() {
  SensorData data;
  
  // Incrementar contador
  readingCount++;
  data.readingId = readingCount;
  data.timestamp = millis();
  
  // Ler DHT22 (Temperatura e Umidade)
  data.temperature = dht.readTemperature();
  data.humidity = dht.readHumidity();
  
  // Verificar se a leitura do DHT22 é válida
  if (isnan(data.temperature) || isnan(data.humidity)) {
    Serial.println("Erro na leitura do DHT22!");
    data.temperature = 0.0;
    data.humidity = 0.0;
  }
  
  // Ler LDR (Luminosidade)
  int ldrValue = analogRead(LDR_PIN);
  data.lightLevel = map(ldrValue, 0, 4095, 0, 1000); // 0-1000 lux
  
  // Ler PIR (Movimento)
  data.motion = digitalRead(PIR_PIN);
  
  // Ler BME280 (Pressão e Altitude)
  if (bme.begin(0x76)) {
    data.pressure = bme.readPressure() / 100.0F; // hPa
    data.altitude = bme.readAltitude(1013.25);   // Altitude padrão
  } else {
    data.pressure = 0.0;
    data.altitude = 0.0;
  }
  
  // Simular vibração (acelerômetro)
  data.vibration_x = random(-200, 201) / 100.0; // -2.0 a 2.0
  data.vibration_y = random(-200, 201) / 100.0;
  data.vibration_z = random(-200, 201) / 100.0;
  
  // Simular nível de bateria
  data.batteryLevel = random(20, 101); // 20% a 100%
  
  // Força do sinal WiFi
  data.signalStrength = WiFi.RSSI();
  
  // Imprimir dados no Monitor Serial
  printSensorData(data);
  
  // Armazenar dados para envio MQTT
  storeSensorData(data);
}

void printHeader() {
  Serial.println("==========================================");
  Serial.println("| ID | Temp | Umid | Luz | Mov | Press |");
  Serial.println("|----|------|------|-----|-----|-------|");
}

void printSensorData(SensorData data) {
  // Formato compacto para Monitor Serial
  Serial.printf("|%3d |%5.1f |%5.1f |%4d |%3s |%6.1f |\n",
                data.readingId,
                data.temperature,
                data.humidity,
                data.lightLevel,
                data.motion ? "SIM" : "NÃO",
                data.pressure);
  
  // Detalhes adicionais a cada 10 leituras
  if (data.readingId % 10 == 0) {
    Serial.println("------------------------------------------");
    Serial.printf("Leitura #%d - Timestamp: %lu ms\n", data.readingId, data.timestamp);
    Serial.printf("Temperatura: %.1f°C\n", data.temperature);
    Serial.printf("Umidade: %.1f%%\n", data.humidity);
    Serial.printf("Luminosidade: %d lux\n", data.lightLevel);
    Serial.printf("Movimento: %s\n", data.motion ? "Detectado" : "Não detectado");
    Serial.printf("Pressão: %.1f hPa\n", data.pressure);
    Serial.printf("Altitude: %.1f m\n", data.altitude);
    Serial.printf("Vibração X: %.2f, Y: %.2f, Z: %.2f\n", 
                  data.vibration_x, data.vibration_y, data.vibration_z);
    Serial.printf("Bateria: %.0f%%\n", data.batteryLevel);
    Serial.printf("RSSI: %d dBm\n", data.signalStrength);
    Serial.println("==========================================");
  }
}

// Variável global para armazenar último dado
SensorData lastSensorData;

void storeSensorData(SensorData data) {
  lastSensorData = data;
}

void sendToMQTT() {
  if (!client.connected()) {
    return;
  }
  
  // Criar JSON
  StaticJsonDocument<512> doc;
  
  doc["device_id"] = "ESP32_001";
  doc["timestamp"] = lastSensorData.timestamp;
  doc["reading_id"] = lastSensorData.readingId;
  
  JsonObject sensors = doc.createNestedObject("sensores");
  sensors["temperatura"] = lastSensorData.temperature;
  sensors["umidade"] = lastSensorData.humidity;
  sensors["luminosidade"] = lastSensorData.lightLevel;
  sensors["movimento"] = lastSensorData.motion;
  sensors["pressao"] = lastSensorData.pressure;
  sensors["altitude"] = lastSensorData.altitude;
  sensors["vibracao_x"] = lastSensorData.vibration_x;
  sensors["vibracao_y"] = lastSensorData.vibration_y;
  sensors["vibracao_z"] = lastSensorData.vibration_z;
  
  JsonObject metadata = doc.createNestedObject("metadata");
  metadata["bateria"] = lastSensorData.batteryLevel;
  metadata["rssi"] = lastSensorData.signalStrength;
  metadata["qualidade"] = 0.95;
  metadata["versao_protocolo"] = "1.0";
  
  // Serializar JSON
  String jsonString;
  serializeJson(doc, jsonString);
  
  // Enviar via MQTT
  if (client.publish(mqtt_topic, jsonString.c_str())) {
    Serial.println("Dados enviados via MQTT com sucesso!");
    digitalWrite(LED_PIN, HIGH);
    delay(100);
    digitalWrite(LED_PIN, LOW);
  } else {
    Serial.println("Falha no envio MQTT!");
  }
  
  // Imprimir JSON no Monitor Serial
  Serial.println("JSON enviado:");
  Serial.println(jsonString);
  Serial.println();
}

// Função para gerar dados de teste (quando sensores não estão disponíveis)
void generateTestData() {
  SensorData testData;
  testData.readingId = readingCount++;
  testData.timestamp = millis();
  
  // Gerar dados sintéticos realísticos
  testData.temperature = 20.0 + random(-50, 51) / 10.0; // 15-25°C
  testData.humidity = 40.0 + random(-200, 201) / 10.0;  // 20-60%
  testData.lightLevel = random(0, 1001);                // 0-1000 lux
  testData.motion = random(0, 2);                       // 0 ou 1
  testData.pressure = 1000.0 + random(-100, 101) / 10.0; // 990-1010 hPa
  testData.altitude = 100.0 + random(-200, 201) / 10.0;  // 80-120 m
  testData.vibration_x = random(-200, 201) / 100.0;
  testData.vibration_y = random(-200, 201) / 100.0;
  testData.vibration_z = random(-200, 201) / 100.0;
  testData.batteryLevel = 20.0 + random(0, 81);         // 20-100%
  testData.signalStrength = -30 - random(0, 70);        // -30 a -100 dBm
  
  printSensorData(testData);
  storeSensorData(testData);
}
