  /*
 * Project Name : Home Weather Station
 * Purpose : To get values from MQ-4, MQ-135, MQ-5 and MQ-2 and send to UNO via software serial
 * Created on : 12 Sep 2020
 * Created by : Sashwat K <sashwat0001@gmail.com>
 * Revision : 2
 * Last Updated by : Sashwat K <sashwat0001@gmail.com> 
 * Last updated on : 16 Sep 2020
 */

#include <ArduinoJson.h> // Library for JSON

#include <SoftwareSerial.h> // Library for Software Serial

#include "DHT.h"
#define DHTPIN 8
#define DHTTYPE DHT22

#include <Wire.h>
#include <SPI.h>
#include <Adafruit_BMP280.h>

#define BMP_SCK  (13)
#define BMP_MISO (12)
#define BMP_MOSI (11)
#define BMP_CS   (10)

SoftwareSerial sSerialToNano(7, 6); // RX, TX

DHT dht(DHTPIN, DHTTYPE);

Adafruit_BMP280 bmp; // I2C

const int rainSensorPin = A0;
const int mq7 = A1;

void setup() {
  // put your setup code here, to run once:
  
  // Initialise sensors
  pinMode(rainSensorPin, INPUT);
  pinMode(mq7, INPUT);
  dht.begin();
  
  // Initialise Serial
  Serial.begin(9600);
  
  /* Default settings from datasheet. */
  bmp.setSampling(Adafruit_BMP280::MODE_NORMAL,     /* Operating Mode. */
                  Adafruit_BMP280::SAMPLING_X2,     /* Temp. oversampling */
                  Adafruit_BMP280::SAMPLING_X16,    /* Pressure oversampling */
                  Adafruit_BMP280::FILTER_X16,      /* Filtering. */
                  Adafruit_BMP280::STANDBY_MS_500); /* Standby time. */

  bmp.begin();
  
  while (!Serial) continue;
  
  sSerialToNano.begin(4800);
}

void loop() {
  // put your main code here, to run repeatedly:
  
  int mq7_value = analogRead(mq7);
  int rainSensor_value = analogRead(rainSensorPin);
  float dhtTemp = dht.readTemperature();
  float dhtHum = dht.readHumidity();
  float heatIndex = dht.computeHeatIndex(dhtTemp, dhtHum, false);
  float bmpTemp = bmp.readTemperature();
  float bmpPres = bmp.readPressure();
  float bmpAlt = bmp.readAltitude();
  
  if (sSerialToNano.available()) {
    
    StaticJsonDocument<300> doc;
    
    // Read the JSON document from the "link" serial port
    DeserializationError err = deserializeJson(doc, sSerialToNano);
    
    if (err == DeserializationError::Ok) {
      
      int cngGas = doc["cng_gas"].as<int>();
      int apiGas = doc["aqi_gas"].as<int>();
      int lpgGas = doc["lpg_gas"].as<int>();
      int smokeGas = doc["smoke_gas"].as<int>();
      
      String finalValue;
      
      // CNG,AQI, LPG, Smoke, CO, Rain sensor, DHT Temperature, DHT Humidity, DHT HI, BMP Temperature, BMP Pressure, BMP altitude
      finalValue = "[" + String(cngGas?cngGas:0) + "," + String(apiGas?apiGas:0) + "," + String(lpgGas?lpgGas:0) + "," + String(smokeGas?smokeGas:0) + "," + String(mq7_value?mq7_value:0) + "," + String(rainSensor_value?rainSensor_value:0) + "," + String(dhtTemp?dhtTemp:0) + "," + String(dhtHum?dhtHum:0) + "," + String(heatIndex?heatIndex:0) + "," + String(bmpTemp?bmpTemp:0) + "," + String(bmpPres?bmpPres:0) + "," + String(bmpAlt?bmpAlt:0) + "]";
      Serial.println(finalValue);
    } 
    else {
      // Print error to the "debug" serial port
      Serial.print("deserializeJson() returned ");
      Serial.println(err.c_str());
  
      // Flush all bytes in the "link" serial port buffer
      while (sSerialToNano.available() > 0)
        sSerialToNano.read();
    }
  }
}
