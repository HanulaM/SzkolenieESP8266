/*
 *   This sketch is combined from ADAfruit DHT sensor and tdicola for dht.h library
 *   Along with some  esp8266 NodeMCU specifics from teos009 
 *   
 *   https://learn.adafruit.com/dht/overview
 *   https://gist.github.com/teos0009/acad7d1e54b97f4b2a88
 */

#include "ESP8266WiFi.h"
#include "DHT.h"
#define DHTPIN 2    // what digital pin we're connected to  pin2 to  D4 on esp board

// Uncomment whatever DHT sensor type you're using!
#define DHTTYPE DHT11  // DHT 11
//#define DHTTYPE DHT21  // DHT 21
//#define DHTTYPE DHT22  // DHT 22

DHT dht(DHTPIN,DHTTYPE);

//const char* server = "api.thingspeak.com";
String apiKey ="Your API key From ThingSpeak"; // api from ts
const char* MY_SSID = "yourSSID";
const char* MY_PWD = "YourPasword";

#define WEBSITE "api.thingspeak.com"
//or const char* WEBSITE = "api.thingspeak.com"; if you prefer


void setup()
{
  Serial.begin(115200);
  dht.begin();
  Serial.print("Connecting to "+*MY_SSID);
  WiFi.begin(MY_SSID, MY_PWD);

  while (WiFi.status() != WL_CONNECTED) //not connected,  ...waiting to connect
    {
      delay(1000);
      Serial.print(".");
    }

  Serial.println("");
  Serial.println("Credentials accepted! Connected to wifi\n ");
  Serial.println("");
}


void loop()
{
  // Wait a few seconds between measurements.
  delay(2000);

  float h = dht.readHumidity();
  // Read temperature as Celsius (the default)
  float t = dht.readTemperature();
  // Read temperature as Fahrenheit (isFahrenheit = true)
  float f = dht.readTemperature(true);

  // Check if any reads failed and exit early (to try again).
  if (isnan(h) || isnan(t) || isnan(f))
  {
    Serial.println("Failed to read from DHT sensor!");
    return;
  }

  // Compute heat index in Fahrenheit (the default)
  float hif = dht.computeHeatIndex(f, h);
  // Compute heat index in Celsius (isFahreheit = false)
  float hic = dht.computeHeatIndex(t, h, false);

  Serial.print("Humidity: ");
  Serial.print(h);
  Serial.print(" %\t");
  Serial.print("Temperature: ");
  Serial.print(t);
  Serial.print(" *C ");
  Serial.print(f);
  Serial.print(" *F\t");
  Serial.print("Heat index: ");
  Serial.print(hic);
  Serial.print(" *C ");
  Serial.print(hif);
  Serial.println(" *F\n");


WiFiClient client;

  if (client.connect(WEBSITE, 80))
    { 
          Serial.println("WiFi Client connected ");

          client.print(F("POST "));
          client.print("/update?key=apiKey&field1=" 
          +            (String) h
          +"&field2=" +(String) t
          +"&field3=" +(String) f
          +"&field4=" +(String) hic
          +"&field5=" +(String) hif
                                   );
          

          String tsData = "field1="   //need the length of our data string to give to ThingSpeak
          +            (String) h
          +"&field2=" +(String) t
          +"&field3=" +(String) f
          +"&field4=" +(String) hic
          +"&field5=" +(String) hif;

          client.print("POST /update HTTP/1.1\n");  //alternate sans 'update'client.print(F(" HTTP/1.1\r\n"));
          client.print("Host: api.thingspeak.com\n");
          client.print("Connection: close\n");
          client.print("X-THINGSPEAKAPIKEY: " + apiKey + "\n");
          client.print("Content-Type: application/x-www-form-urlencoded\n");
          client.print("Content-Length: ");
          client.print(tsData.length());  //send out data string legth to ts
          client.print("\n\n");
          client.print(tsData);

          delay(1000);
    } //end client connect

  else Serial.print("couldnt connect to ThingSpeak\n");  //if client connect failed
 
  client.stop();
}