void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  
}

void loop() {
  delay(1000);
  char x[] = "0";
  Serial.write("b");
  for (int i = 0; i < 11; i++) {
    Serial.write(x);  
  }
  Serial.write("1");
  Serial.write("\n");
  
}
