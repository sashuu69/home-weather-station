/*
 * Project Name : Home Weather Station
 * Purpose : To get values from MQ-4, MQ-135, MQ-5 and MQ-2 and send to UNO via software serial
 * Created on : 12 Sep 2020
 * Created by : Sashwat K <sashwat0001@gmail.com>
 * Revision : 4
 * Last Updated by : Sashwat K <sashwat0001@gmail.com> 
 * Last updated on : 09 Oct 2020
 */

#include <ArduinoJson.h> // Library for JSON

#include <SoftwareSerial.h> // Library for Software Serial

#include "DHT.h" // Library for DHT22
#define DHTPIN 8
#define DHTTYPE DHT22

SoftwareSerial sSerialToNano(6, 7); // Software Serial with Nano (RX,TX)

DHT dht(DHTPIN, DHTTYPE); // Initialise DHT22

const int rainSensorPin = A0; // Rain sensor pin

void setup() {
  // put your setup code here, to run once:
  
  // Initialise sensors
  pinMode(rainSensorPin, INPUT);
  
  dht.begin();
  
  // Initialise Serial
  Serial.begin(9600);
  
  while (!Serial) continue;
  
  sSerialToNano.begin(4800);
}

void loop() {
  // put your main code here, to run repeatedly:
  
  int rainSensor_value = analogRead(rainSensorPin);
  float dhtTemp = dht.readTemperature();
  float dhtHum = dht.readHumidity();
  float heatIndex = dht.computeHeatIndex(dhtTemp, dhtHum, false);
  
  if (sSerialToNano.available()) {
    
    StaticJsonDocument<400> doc;
    
    // Read the JSON document from the "link" serial port
    DeserializationError err = deserializeJson(doc, sSerialToNano);
    
    if (err == DeserializationError::Ok) {
      
      double cngGas = doc["cng_gas"].as<double>();
      double apiGas = doc["aqi_gas"].as<double>();
      double lpgGas = doc["lpg_gas"].as<double>();
      double smokeGas = doc["smoke_gas"].as<double>();
      
      String finalValue;
      
      // CNG, AQI, LPG, Smoke, Rain sensor, DHT Temperature, DHT Humidity, DHT HI
      finalValue = String(cngGas?cngGas:0) + "," + String(apiGas?apiGas:0) + "," + String(lpgGas?lpgGas:0) + "," + String(smokeGas?smokeGas:0) + "," + String(rainSensor_value?rainSensor_value:0) + "," + String(dhtTemp?dhtTemp:0) + "," + String(dhtHum?dhtHum:0) + "," + String(heatIndex?heatIndex:0);
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
