#include <DHT.h>

// Definição dos pinos
#define DHT_PIN 4
#define LDR_PIN 36
#define PIR_PIN 5
#define LED_PIN 2

#define DHT_TYPE DHT22

// Inicialização do sensor DHT
DHT dht(DHT_PIN, DHT_TYPE);

// Variáveis para armazenar as leituras
float temperatura;
float umidade;
int luminosidade;
int movimento;

// Variáveis para estatísticas
float tempMax = -40.0;
float tempMin = 80.0;
float umidMax = 0.0;
float umidMin = 100.0;
int luzMax = 0;
int luzMin = 1023;
unsigned long contadorMovimento = 0;

void setup() {
  Serial.begin(115200);
  Serial.println("Iniciando simulação de sensores...");
  
  // Configuração dos pinos
  pinMode(LED_PIN, OUTPUT);
  pinMode(PIR_PIN, INPUT);
  dht.begin();
  
  // Aguarda inicialização dos sensores
  delay(2000);
}

void loop() {
  // Leitura dos sensores
  temperatura = dht.readTemperature();
  umidade = dht.readHumidity();
  luminosidade = analogRead(LDR_PIN);
  movimento = digitalRead(PIR_PIN);
  
  // Atualização de estatísticas
  if (temperatura > tempMax) tempMax = temperatura;
  if (temperatura < tempMin) tempMin = temperatura;
  if (umidade > umidMax) umidMax = umidade;
  if (umidade < umidMin) umidMin = umidade;
  if (luminosidade > luzMax) luzMax = luminosidade;
  if (luminosidade < luzMin) luzMin = luminosidade;
  if (movimento) contadorMovimento++;
  
  // Atualiza LED baseado no movimento
  digitalWrite(LED_PIN, movimento);
  
  // Envia dados para o Serial Monitor
  Serial.println("\n=== Leituras dos Sensores ===");
  Serial.print("Temperatura: ");
  Serial.print(temperatura);
  Serial.println("°C");
  Serial.print("Umidade: ");
  Serial.print(umidade);
  Serial.println("%");
  Serial.print("Luminosidade: ");
  Serial.print(luminosidade);
  Serial.println(" (0-1023)");
  Serial.print("Movimento: ");
  Serial.println(movimento ? "Detectado" : "Nenhum");
  
  // Envia dados para o Serial Plotter
  Serial.print("TEMP:");
  Serial.print(temperatura);
  Serial.print(",");
  Serial.print("UMID:");
  Serial.print(umidade);
  Serial.print(",");
  Serial.print("LUZ:");
  Serial.println(luminosidade);
  
  // A cada 10 leituras, mostra estatísticas
  static int contador = 0;
  if (++contador >= 10) {
    Serial.println("\n=== Estatísticas ===");
    Serial.print("Temperatura - Mín: ");
    Serial.print(tempMin);
    Serial.print("°C, Máx: ");
    Serial.print(tempMax);
    Serial.println("°C");
    Serial.print("Umidade - Mín: ");
    Serial.print(umidMin);
    Serial.print("%, Máx: ");
    Serial.print(umidMax);
    Serial.println("%");
    Serial.print("Luminosidade - Mín: ");
    Serial.print(luzMin);
    Serial.print(", Máx: ");
    Serial.println(luzMax);
    Serial.print("Total de detecções de movimento: ");
    Serial.println(contadorMovimento);
    contador = 0;
  }
  
  delay(2000);
} 