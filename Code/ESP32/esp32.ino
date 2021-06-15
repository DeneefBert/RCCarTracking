#include <Wire.h>
#include <PubSubClient.h>
#include <WiFi.h>
#include <DS18B20.h>
#include <Adafruit_NeoPixel.h>

//char* ssid = "Howest-IoT";
//char* wifi_password = "LZe5buMyZUcDpLY";
char* ssid = "FroeFroe";
char* wifi_password = "visa_visa_uno_punto_berlingo_berlingo";

char* mqtt_server = "192.168.0.251";  // IP of the MQTT broker
char* accx_topic = "sensors/accx";
char* accy_topic = "sensors/accy";
char* accz_topic = "sensors/accz";
char* ldr_topic = "sensors/ldr";
char* temp_topic = "sensors/temp";
char* timing = "sensors/timing";
char* mqtt_username = "fluvisol"; // MQTT username
char* mqtt_password = "fluvisol"; // MQTT password
char* clientID = "client_car"; // MQTT client ID

char* topics[] = {accx_topic, accy_topic, accz_topic, ldr_topic, temp_topic};
float vals[] = {0, 0, 0, 0, 0};
int setups[] = { 0, 0, 0};
int temp = 0;
int ldr = 34;
int ldrVal;
int red = 0;
int green = 0;
int blue = 0;
float test = 40.0;
float intensity = 50.0;
bool alarmOn = false;
bool lightOverride = false;
DS18B20 ds(4);


WiFiClient espClient;
PubSubClient client(espClient);
Adafruit_NeoPixel pixels(16, 23, NEO_GRB + NEO_KHZ800);
long lastMsg = 0;

void setup() {
  Serial.begin(9600);
  Wire.begin();
  Wire.beginTransmission(0x68);
  Wire.write(0x1C);  // set acc range to +- 4g
  Wire.write(0x08);
  Wire.endTransmission(true);
  Wire.beginTransmission(0x68);
  Wire.write(0x6B);  // end sleep
  Wire.write(0);
  Wire.endTransmission(true);
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
  pixels.begin();
  Serial.println("Setup complete");
  // Determine calibration bytes
  for (int j = 0; j < 10; j++) {
    readValsSetup();
    for (int i = 0; i < 3; i++) {
      setups[i] += vals[i];
    }
  }
  for (int i = 0; i < 3; i++) {
    setups[i] = setups[i] / 10;
  }
  ledcSetup(0, 1E5, 12);
  ledcAttachPin(18, 0);
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();
  long now = millis();
  if (now - lastMsg > 1000) {
    int t = now - lastMsg;
    readVals();
    if (alarmOn) {
      ledcWriteTone(0, 0);
      alarmOn = false;
    } else if (vals[4] > test) {
      ledcWriteTone(0, 800);
      alarmOn = true;
    }
    for (int i = 0; i < 5; i++) {
      if (client.publish(topics[i], String(vals[i]).c_str())) {
        //        Serial.println("AccByte sent!");
      }
    }
    if (client.publish(timing, String(t).c_str())) {
      //      Serial.println("Timing sent!");
    }
    lastMsg = now;
  }
  if (lightOverride) {
    for (int i = 0; i < 16; i++) {
      pixels.setPixelColor(i, pixels.Color(red, green, blue));
    }
    if (red + green + blue == 0) {
      pixels.clear();
      pixels.show();
      //    Serial.println("Pixels off");
    } else {
      pixels.show();
    }
  } else if (vals[3] < intensity) {
    if (red + green + blue == 0) {
      for (int i = 0; i < 16; i++) {
        pixels.setPixelColor(i, pixels.Color(255, 255, 255));
      }
    } else {
      for (int i = 0; i < 16; i++) {
        pixels.setPixelColor(i, pixels.Color(red, green, blue));
      }
    }
    pixels.show();
  } else {
    pixels.clear();
    pixels.show();
  }
}

void setup_wifi() {
  delay(10);
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, wifi_password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void readVals() {
  Wire.beginTransmission(0x68);
  Wire.write(0x3B);
  Wire.endTransmission(true);
  Wire.beginTransmission(0x68);
  Wire.requestFrom(0x68, 6, true);
  temp = (Wire.read() << 8) | Wire.read();
  if (temp & 0x8000) {
    temp -= 65536;
  }
  vals[0] = temp - setups[0];
  temp = (Wire.read() << 8) | Wire.read();
  if (temp & 0x8000) {
    temp -= 65536;
  }
  vals[1] = temp - setups[1];
  temp = (Wire.read() << 8) | Wire.read();
  if (temp & 0x8000) {
    temp -= 65536;
  }
  vals[2] = temp - setups[2];
  ldrVal = analogRead(ldr);
  vals[3] = calc(ldrVal);
  vals[4] = ds.getTempC();
}

void readValsSetup() {
  Wire.beginTransmission(0x68);
  Wire.write(0x3B);
  Wire.endTransmission(true);
  Wire.beginTransmission(0x68);
  Wire.requestFrom(0x68, 6, true);
  temp = (Wire.read() << 8) | Wire.read();
  if (temp & 0x8000) {
    temp -= 65536;
  }
  vals[0] = temp;
  temp = (Wire.read() << 8) | Wire.read();
  if (temp & 0x8000) {
    temp -= 65536;
  }
  vals[1] = temp;
  temp = (Wire.read() << 8) | Wire.read();
  if (temp & 0x8000) {
    temp -= 65536;
  }
  vals[2] = temp;
}

void callback(char* topic, byte* message, unsigned int length) {
  String messageTemp;
  for (int i = 0; i < length; i++) {
    messageTemp += (char)message[i];
  }
  int index = messageTemp.toInt();

  if (String(topic) == "actuators/lights") {
    int index = messageTemp.toInt();
    red = ((index & 0xff0000) >> 16);
    green = ((index & 0xff00) >> 8);
    blue = index & 0xff;
  } else if (String(topic) == "actuators/sounds") {
    float index = messageTemp.toInt() / 10.0;
    test = index;
  } else if (String(topic) == "actuators/intensity") {
    int index = messageTemp.toInt();
    intensity = index;
  } else if (String(topic) == "actuators/override") {
    lightOverride = messageTemp.toInt();
  }
}

void reconnect() {
  // loop for connection
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // connect
    if (client.connect(clientID, mqtt_username, mqtt_password)) {
      Serial.println("connected");
      // Subscribe
      client.subscribe("actuators/lights");
      client.subscribe("actuators/sounds");
      client.subscribe("actuators/intensity");
      client.subscribe("actuators/override");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}

float calc(int val) {
  float result = 100.0 - ((val - 800.0) / 3295.0 * 100.0);
  if (result > 100) {
    result = 100;
  }
  return result;
}
