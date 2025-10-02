/*
 * Sistema IoT Monitoring - Coleta e Ingestão ESP32
 * Enterprise Challenge Sprint 3 - Reply
 * 
 * Este código implementa a coleta de dados de múltiplos sensores
 * no ESP32 e envia via Serial/USB e MQTT.
 * 
 * Sensores suportados:
 * - DHT22 (Temperatura e Umidade)
 * - LDR (Luminosidade)
 * - PIR (Movimento)
 * - BME280 (Pressão Atmosférica)
 * 
 * Protocolos:
 * - Serial/USB (115200 baud)
 * - MQTT (HiveMQ Cloud)
 * 
 * Frequência: 1Hz (1 leitura por segundo)
 */

#include <WiFi.h>
#include <PubSubClient.h>
#include <DHT.h>
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BME280.h>
#include <ArduinoJson.h>

// Configurações WiFi
const char* ssid = "SEU_WIFI_SSID";
const char* password = "SUA_SENHA_WIFI";

// Configurações MQTT
const char* mqtt_server = "broker.hivemq.com";
const int mqtt_port = 1883;
const char* mqtt_topic = "industrial/sensors";
const char* mqtt_client_id = "ESP32_IoT_Monitoring";

// Configurações dos sensores
#define DHT_PIN 4
#define DHT_TYPE DHT22
#define LDR_PIN 34
#define PIR_PIN 2
#define BME280_SDA 21
#define BME280_SCL 22

// Objetos dos sensores
DHT dht(DHT_PIN, DHT_TYPE);
Adafruit_BME280 bme;

// Cliente MQTT
WiFiClient espClient;
PubSubClient client(espClient);

// Variáveis de controle
unsigned long lastRead = 0;
const unsigned long readInterval = 1000; // 1 segundo
int readCount = 0;
const int maxReads = 60; // 60 leituras (1 minuto)

// Estrutura para dados dos sensores
struct SensorData {
  float temperature;
  float humidity;
  int light;
  int motion;
  float pressure;
  unsigned long timestamp;
  String quality;
};

void setup() {
  Serial.begin(115200);
  Serial.println("=== Sistema IoT Monitoring - ESP32 ===");
  Serial.println("Enterprise Challenge Sprint 3 - Reply");
  Serial.println("=====================================");
  
  // Inicializar sensores
  initializeSensors();
  
  // Conectar WiFi
  connectWiFi();
  
  // Configurar MQTT
  client.setServer(mqtt_server, mqtt_port);
  client.setCallback(mqttCallback);
  
  Serial.println("Sistema inicializado com sucesso!");
  Serial.println("Iniciando coleta de dados...");
  Serial.println();
}

void loop() {
  unsigned long currentTime = millis();
  
  // Verificar conexão MQTT
  if (!client.connected()) {
    connectMQTT();
  }
  client.loop();
  
  // Coletar dados a cada 1 segundo
  if (currentTime - lastRead >= readInterval) {
    collectAndSendData();
    lastRead = currentTime;
    readCount++;
    
    // Parar após 60 leituras (1 minuto)
    if (readCount >= maxReads) {
      Serial.println("Coleta de dados concluída!");
      Serial.println("Total de leituras: " + String(readCount));
      Serial.println("Sistema em modo de espera...");
      while(true) {
        delay(1000);
      }
    }
  }
}

void initializeSensors() {
  Serial.println("Inicializando sensores...");
  
  // Inicializar DHT22
  dht.begin();
  Serial.println("✓ DHT22 inicializado");
  
  // Inicializar BME280
  Wire.begin(BME280_SDA, BME280_SCL);
  if (bme.begin(0x76)) {
    Serial.println("✓ BME280 inicializado");
  } else {
    Serial.println("✗ Erro ao inicializar BME280");
  }
  
  // Configurar pinos
  pinMode(LDR_PIN, INPUT);
  pinMode(PIR_PIN, INPUT);
  
  Serial.println("✓ Todos os sensores inicializados");
  Serial.println();
}

void connectWiFi() {
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
    Serial.println("✓ WiFi conectado!");
    Serial.print("IP: ");
    Serial.println(WiFi.localIP());
  } else {
    Serial.println();
    Serial.println("✗ Falha na conexão WiFi");
    Serial.println("Continuando apenas com Serial...");
  }
  Serial.println();
}

void connectMQTT() {
  while (!client.connected()) {
    Serial.print("Conectando ao MQTT...");
    
    if (client.connect(mqtt_client_id)) {
      Serial.println("✓ MQTT conectado!");
      client.subscribe(mqtt_topic);
    } else {
      Serial.print("✗ Falha, rc=");
      Serial.print(client.state());
      Serial.println(" Tentando novamente em 5 segundos...");
      delay(5000);
    }
  }
}

void mqttCallback(char* topic, byte* payload, unsigned int length) {
  // Callback para mensagens MQTT recebidas
  Serial.print("Mensagem MQTT recebida: ");
  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
  }
  Serial.println();
}

void collectAndSendData() {
  // Coletar dados dos sensores
  SensorData data = readSensors();
  
  // Calcular qualidade dos dados
  data.quality = calculateDataQuality(data);
  
  // Enviar via Serial (JSON)
  sendSerialData(data);
  
  // Enviar via MQTT (se conectado)
  if (WiFi.status() == WL_CONNECTED && client.connected()) {
    sendMQTTData(data);
  }
  
  // Imprimir resumo
  printDataSummary(data);
}

SensorData readSensors() {
  SensorData data;
  data.timestamp = millis();
  
  // Ler DHT22 (Temperatura e Umidade)
  data.temperature = dht.readTemperature();
  data.humidity = dht.readHumidity();
  
  // Verificar se a leitura do DHT22 é válida
  if (isnan(data.temperature) || isnan(data.humidity)) {
    data.temperature = 0.0;
    data.humidity = 0.0;
  }
  
  // Ler LDR (Luminosidade)
  int ldrValue = analogRead(LDR_PIN);
  data.light = map(ldrValue, 0, 4095, 0, 1000); // Mapear para 0-1000 lux
  
  // Ler PIR (Movimento)
  data.motion = digitalRead(PIR_PIN);
  
  // Ler BME280 (Pressão)
  data.pressure = bme.readPressure() / 100.0; // Converter para hPa
  
  return data;
}

String calculateDataQuality(SensorData data) {
  int qualityScore = 100;
  
  // Verificar temperatura (0-50°C)
  if (data.temperature < 0 || data.temperature > 50) {
    qualityScore -= 30;
  }
  
  // Verificar umidade (0-100%)
  if (data.humidity < 0 || data.humidity > 100) {
    qualityScore -= 30;
  }
  
  // Verificar luminosidade (0-1000 lux)
  if (data.light < 0 || data.light > 1000) {
    qualityScore -= 20;
  }
  
  // Verificar pressão (900-1100 hPa)
  if (data.pressure < 900 || data.pressure > 1100) {
    qualityScore -= 20;
  }
  
  if (qualityScore >= 90) return "excelente";
  if (qualityScore >= 70) return "boa";
  if (qualityScore >= 50) return "regular";
  return "ruim";
}

void sendSerialData(SensorData data) {
  // Criar JSON
  StaticJsonDocument<200> doc;
  doc["device"] = "ESP32-IoT-Monitoring";
  doc["timestamp"] = data.timestamp;
  doc["sensors"]["DHT22"]["temperature"] = data.temperature;
  doc["sensors"]["DHT22"]["humidity"] = data.humidity;
  doc["sensors"]["LDR"]["light"] = data.light;
  doc["sensors"]["PIR"]["motion"] = data.motion;
  doc["sensors"]["BME280"]["pressure"] = data.pressure;
  doc["quality"] = data.quality;
  doc["read_count"] = readCount;
  
  // Enviar via Serial
  serializeJson(doc, Serial);
  Serial.println();
}

void sendMQTTData(SensorData data) {
  // Criar JSON para MQTT
  StaticJsonDocument<200> doc;
  doc["device"] = "ESP32-IoT-Monitoring";
  doc["timestamp"] = data.timestamp;
  doc["sensors"]["DHT22"]["temperature"] = data.temperature;
  doc["sensors"]["DHT22"]["humidity"] = data.humidity;
  doc["sensors"]["LDR"]["light"] = data.light;
  doc["sensors"]["PIR"]["motion"] = data.motion;
  doc["sensors"]["BME280"]["pressure"] = data.pressure;
  doc["quality"] = data.quality;
  doc["read_count"] = readCount;
  
  // Serializar e enviar
  char jsonBuffer[200];
  serializeJson(doc, jsonBuffer);
  client.publish(mqtt_topic, jsonBuffer);
}

void printDataSummary(SensorData data) {
  Serial.println("--- Dados Coletados ---");
  Serial.print("Leitura #");
  Serial.print(readCount);
  Serial.print(" | Tempo: ");
  Serial.print(data.timestamp);
  Serial.println("ms");
  Serial.print("🌡️  Temperatura: ");
  Serial.print(data.temperature);
  Serial.println("°C");
  Serial.print("💧 Umidade: ");
  Serial.print(data.humidity);
  Serial.println("%");
  Serial.print("💡 Luminosidade: ");
  Serial.print(data.light);
  Serial.println(" lux");
  Serial.print("👁️  Movimento: ");
  Serial.println(data.motion ? "SIM" : "NÃO");
  Serial.print("🌬️  Pressão: ");
  Serial.print(data.pressure);
  Serial.println(" hPa");
  Serial.print("⭐ Qualidade: ");
  Serial.println(data.quality);
  Serial.println("----------------------");
  Serial.println();
}
