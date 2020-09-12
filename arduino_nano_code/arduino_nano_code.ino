/*

*/

const int mq4 = A0;
const int mq135 = A1;
const int mq5 = A2;
const int mq2 = A3;

void setup() {
  pinMode(mq4, INPUT);
  pinMode(mq135, INPUT);
  pinMode(mq5, INPUT);
  pinMode(mq2, INPUT);
  Serial.begin(9600);
}

void loop() {
  int mq4_value, mq135_value, mq5_value, mq2_value;
  
  mq4_value = analogRead(mq4);
  mq135_value = analogRead(mq135);
  mq5_value = analogRead(mq5);
  mq2_value = analogRead(mq2);
  
  Serial.println("************************************");
  Serial.print("MQ-4 Value: ");Serial.print(mq4_value, DEC);Serial.println(" PPM");
  Serial.print("MQ-135 Value: ");Serial.print(mq135_value, DEC);Serial.println(" PPM");
  Serial.print("MQ-5 Value: ");Serial.print(mq5_value, DEC);Serial.println(" PPM");
  Serial.print("MQ-2 Value: ");Serial.print(mq2_value, DEC);Serial.println(" PPM");
  Serial.println("************************************\n\n");
  
  delay(1000);
}
