/*
 * Project Name : Home Weather Station
 * Purpose : To get values from MQ-4, MQ-135, MQ-5 and MQ-2 and send to UNO via software serial as PPM
 * Created on : 12 Sep 2020
 * Created by : Sashwat K <sashwat0001@gmail.com>
 * Revision : 3
 * Last Updated by : Sashwat K <sashwat0001@gmail.com> 
 * Last updated on : 04 Oct 2020
 */

#include <ArduinoJson.h> // Library for JSON

#include <SoftwareSerial.h> // Library for Software Serial

SoftwareSerial sSerialToUNO(6, 7); //RX, TX

const int mq4 = A0; // CNG gas
const int mq135 = A1; // Air Quality Index
const int mq5 = A2; // LPG gas
const int mq2 = A3; // Smoke

// For Gas sensors
float m = -0.6527; //Slope 
float b = 1.30; //Y-Intercept 
float R0 = 21.91; //Sensor Resistance in fresh air from previous code

void setup() {
  // put your setup code here, to run once:
  
  // Initialise sensors
  pinMode(mq4, INPUT); // MQ4 for CNG gas
  pinMode(mq135, INPUT); // MQ4 for Air Quality Index
  pinMode(mq5, INPUT); // MQ5 for LNG gas
  pinMode(mq2, INPUT); // MQ2 for smoke

  // Initialise Serial
  Serial.begin(9600);
  
  while (!Serial) continue; // Check if Serial is available or not
  
  sSerialToUNO.begin(4800); // Begin software Serial
}

void loop() {
  // put your main code here, to run repeatedly:

  // Get values from Sensor in PPM
  double mq4_value = analogToPPM(analogRead(mq4));
  double mq135_value = analogToPPM(analogRead(mq135));
  double mq5_value = analogToPPM(analogRead(mq5));
  double mq2_value = analogToPPM(analogRead(mq2));

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

// Function to convert analog values from gas sensors to PPM
double analogToPPM(int aValue) {
  float sensor_volt; //Define variable for sensor voltage 
  float RS_gas; //Define variable for sensor resistance  
  float ratio; //Define variable for ratio
  int sensorValue = aValue; //Read analog values of sensor

  sensor_volt = sensorValue*(5.0/1023.0); //Convert analog values to voltage 
  RS_gas = ((5.0*10.0)/sensor_volt)-10.0; //Get value of RS in a gas
  ratio = RS_gas/R0;  // Get ratio RS_gas/RS_air

  double ppm_log = (log10(ratio)-b)/m; //Get ppm value in linear scale according to the the ratio value  
  double ppm = pow(10, ppm_log); //Convert ppm value to log scale 

  return ppm;
}
