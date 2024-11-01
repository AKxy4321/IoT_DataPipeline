#include <PubSubClient.h>
#include "configuration.h"

// Create WiFi and MQTT client objects
WiFiClient espClient;
PubSubClient client(espClient);

// Function to connect to Wi-Fi
void setup_wifi() {
  WiFi.mode(WIFI_STA);
  Serial.print("Connecting to WiFi...\n");
  WiFi.begin(ssid, password);
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }
  
  Serial.println("Connected to WiFi\n");
}

// Function to reconnect to the MQTT broker
void reconnect() {
  while (!client.connected()) {
    Serial.print("\nAttempting MQTT connection...\n");
  
    // Attempt to connect
    if (client.connect("ESP32Client", user_name, pass_word)) {
      Serial.println("connected\n");
    } else {
      Serial.print("\nfailed, rc=");
      Serial.print(client.state());
      delay(2000);
    }
  }
}

// Function to publish sensor data
void publish_sensor_data() {
  float temperature = random(2000, 3000) / 100.0; // Simulated temperature (20.00 to 30.00)
  
  String payload = String("{\"temperature\":") + temperature + "}";
  client.publish(mqtt_topic, payload.c_str());
  Serial.print("IoT Device sent: ");
  Serial.println(payload);
}

void setup() {
  Serial.begin(115200);
  delay(1000);
  WiFi.disconnect();
  setup_wifi();
  Serial.print("Local IP Address: ");
  Serial.println(WiFi.localIP());
  delay(1000);
  
  client.setServer(mqtt_server, mqtt_port);
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  
  client.loop();
  publish_sensor_data();
  delay(3000); // Publish every 3 seconds
}
