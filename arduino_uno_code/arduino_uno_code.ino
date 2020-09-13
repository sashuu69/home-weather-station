/*
 * Project Name : Home Weather Station
 * Purpose : To get values from MQ-4, MQ-135, MQ-5 and MQ-2 and send to UNO via software serial
 * Created on : 12 Sep 2020
 * Created by : Sashwat K <sashwat0001@gmail.com>
 * Revision : 1
 * Last Updated by : Sashwat K <sashwat0001@gmail.com> 
 * Last updated on : 12 Sep 2020
 */

#include <ArduinoJson.h> // Library for JSON
#include <SoftwareSerial.h> // Library for Software Serial
#include "DHT.h"
#define DHTPIN 8
#define DHTTYPE DHT22

SoftwareSerial sSerialToNano(7, 6); // RX, TX
DHT dht(DHTPIN, DHTTYPE);

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
  
  while (!Serial) continue;

  sSerialToNano.begin(4800);
}

void loop() {
  // put your main code here, to run repeatedly:
  int mq7_value, rainSensor_value;

  mq7_value= analogRead(mq7);
  rainSensor_value = analogRead(rainSensorPin);
  float dhtTemp = dht.readTemperature();
  float dhtHum = dht.readHumidity();
  float heatIndex = dht.computeHeatIndex(dhtTemp, dhtHum, false);
  
  if (sSerialToNano.available()) {
    
    StaticJsonDocument<300> doc;

    // Read the JSON document from the "link" serial port
    DeserializationError err = deserializeJson(doc, sSerialToNano);

    if (err == DeserializationError::Ok) 
    {
      // Print the values
      // (we must use as<T>() to resolve the ambiguity)
      Serial.println("****************************");
      
      Serial.print("CNG Gas : ");
      Serial.print(doc["cng_gas"].as<int>());
      Serial.println(" PPM");
      
      Serial.print("Air Quality Index : ");
      Serial.println(doc["aqi_gas"].as<int>());
      
      Serial.print("LGP Gas : ");
      Serial.print(doc["lpg_gas"].as<int>());
      Serial.println(" PPM");
      
      Serial.print("Smoke : ");
      Serial.print(doc["smoke_gas"].as<int>());
      Serial.println(" PPM");
      
      Serial.print("CO Gas : ");
      Serial.print(mq7_value);
      Serial.println(" PPM");
      
      Serial.print("Rain Sensor : ");
      Serial.println(rainSensor_value);
      
      Serial.print("Temperature : ");
      Serial.print(dhtTemp);
      Serial.println(" °C");
      
      Serial.print("Humidity : ");
      Serial.print(dhtHum);
      Serial.println(" % ");
      
      Serial.print("Heat Index : ");
      Serial.print(heatIndex);
      Serial.println(" °C");
      
      Serial.println("****************************\n\n");
    } 
    else 
    {
      // Print error to the "debug" serial port
      Serial.print("deserializeJson() returned ");
      Serial.println(err.c_str());
  
      // Flush all bytes in the "link" serial port buffer
      while (sSerialToNano.available() > 0)
        sSerialToNano.read();
    }
  }
}
