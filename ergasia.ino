

 #include <WiFi.h>
#include "secrets.h"
#include "ThingSpeak.h"  // Include ThingSpeak header file

#include <DHTesp.h>
#define LIGHT_SENSOR_PIN 1 
int TempLimit = 0;
int humLimit = 0;

char ssid[] = SECRET_SSID;     // Your network SSID (name)
char pass[] = SECRET_PASS;     // Your network password

WiFiClient client;

unsigned long myChannelNumber = SECRET_CH_ID;     // ThingSpeak Channel ID
const char * myWriteAPIKey = SECRET_WRITE_APIKEY;  // Correct Write API Key


#define DHTPIN 0         // Digital pin connected to the DHT sensor
#define DHTTYPE DHT22

DHTesp dht;

void setup() {
  
  Serial.begin(115200);
   while (!Serial) {
    ; 
  }

  Serial.println("Connecting to WiFi...");
  WiFi.mode(WIFI_STA);   
  WiFi.begin(ssid, pass);  // Connect to WiFi

  // Wait until the WiFi is connected
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  
  Serial.println("");
  Serial.println("Connected to WiFi");
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());

  ThingSpeak.begin(client);  // Initialize ThingSpeak
  delay(1000);
  dht.setup(DHTPIN, DHTesp::DHT22);

  // set the ADC attenuation to 11 dB (up to ~3.3V input)
  analogSetAttenuation(ADC_11db);
}

void loop() {

 // Check WiFi status and reconnect if necessary
  if(WiFi.status() != WL_CONNECTED){
    Serial.println("WiFi connection lost. Reconnecting...");
    while(WiFi.status() != WL_CONNECTED){
      WiFi.begin(ssid, pass); // Reconnect to WiFi
      delay(5000);
      Serial.print(".");
    } 
    Serial.println("Reconnected to WiFi");
  }

  // reads the input on analog pin (value between 0 and 4095)
  int analogValue = analogRead(LIGHT_SENSOR_PIN);
  TempAndHumidity newValues = dht.getTempAndHumidity();
  
  // Set multiple fields
  ThingSpeak.setField(1, analogValue);
  ThingSpeak.setField(2, newValues.temperature);
  ThingSpeak.setField(3, newValues.humidity);

  Serial.print("LIGHT VALUE_FIELD1 = ");
  Serial.print(analogValue);   // the raw analog reading
  

  Serial.print(F(" Temperature_FIELD2: "));
  Serial.println(newValues.temperature);  // display temperature

  Serial.print(F(" Humidity_FIELD3: "));
  Serial.println(newValues.humidity);     // display humidity


  // We'll have a few threshholds, qualitatively determined
  if (analogValue < 850) {
    Serial.println(" => Dark");
  } else if (analogValue < 1000) {
    Serial.println(" => Dim");
  } else if (analogValue < 1200) {
    Serial.println(" => Light");
  } else if (analogValue < 1500) {
    Serial.println(" => Bright");
  } else {
    Serial.println(" => Very bright");
  }

  int x = ThingSpeak.writeFields(myChannelNumber, myWriteAPIKey);

    if(x == 200){
    Serial.println("Channel update successful.");
  }
  else{
    Serial.print("Problem updating channel. HTTP error code ");
    Serial.println(x);
    Serial.println("Error message: ");
    if (x == 401) {
      Serial.println("Unauthorized - Please check the API key.");
    } else if (x == 400) {
      Serial.println("Bad Request - Check field number and API format.");
    } else {
      Serial.println("Other error occurred.");
    }
  }


  delay(10000);
}


