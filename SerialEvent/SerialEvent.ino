
void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  Serial.begin(9600);
}

void brink(){
  digitalWrite(LED_BUILTIN, HIGH);
  delay(1000);
  digitalWrite(LED_BUILTIN, LOW);
  delay(500);
}

void loop() {
  byte data;
  if ( Serial.available() ){
    data = (byte)Serial.read();
    Serial.write(data);
    if (data == 1){
      brink();
  }
    if (data == 2){
      brink();
      brink();
    }
  }
}
