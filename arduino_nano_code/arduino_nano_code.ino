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

SoftwareSerial sSerialToUNO(6, 7); //RX, TX

const int mq4 = A0; // CNG gas
const int mq135 = A1; // Air Quality Index
const int mq5 = A2; // LPG gas
const int mq2 = A3; // Smoke

void setup() {
  // put your setup code here, to run once:
  
  // Initialise sensors
  pinMode(mq4, INPUT);
  pinMode(mq135, INPUT);
  pinMode(mq5, INPUT);
  pinMode(mq2, INPUT);

  // Initialise Serial
  Serial.begin(9600);
  
  while (!Serial) continue;
  
  sSerialToUNO.begin(4800);
}

void loop() {
  // put your main code here, to run repeatedly:

  // Get values from Sensor in PPM
  int mq4_value = analogRead(mq4);
  int mq135_value = analogRead(mq135);
  int mq5_value = analogRead(mq5);
  int mq2_value = analogRead(mq2);

  // Create JSON data
  StaticJsonDocument<200> doc;
  doc["cng_gas"] = mq4_value;
  doc["aqi_gas"] = mq135_value;
  doc["lpg_gas"] = mq5_value;
  doc["smoke_gas"] = mq2_value;
  serializeJson(doc, sSerialToUNO); // Send JSON via Serial

  // Display data for Debugging
  Serial.println("************************************");
  Serial.print("MQ-4 Value: ");Serial.print(mq4_value, DEC);Serial.println(" PPM");
  Serial.print("MQ-135 Value: ");Serial.print(mq135_value, DEC);Serial.println(" PPM");
  Serial.print("MQ-5 Value: ");Serial.print(mq5_value, DEC);Serial.println(" PPM");
  Serial.print("MQ-2 Value: ");Serial.print(mq2_value, DEC);Serial.println(" PPM");
  Serial.println("************************************\n\n");
  
  delay(30000); // 30 Seconds
}
