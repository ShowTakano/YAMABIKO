
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

void brink_msec(int msec){
  digitalWrite(LED_BUILTIN, HIGH);
  delay(msec);
  digitalWrite(LED_BUILTIN, LOW);
  delay(500);
}

void myprint(String msg, String end_str){
  Serial.print(msg);
  Serial.print(end_str);
}

int split(String data, char delimiter, String *dst){
  int index = 0;
  int arraySize = (sizeof(data))/sizeof((data[0]));
  int datalength = data.length();
  
  for(int i = 0; i < datalength; i++){
    char tmp = data.charAt(i);
    if( tmp == delimiter ){
      index++;
      if( index > (arraySize - 1)) return -1;
    }
    else dst[index] += tmp;
  }
  return (index + 1);
}

void loop() {
  String data;
  if ( Serial.available() ){
    data = Serial.readStringUntil(';');
    myprint(data, ";");

    String cmds[2];
    int index = split(data, ',', cmds);

    // set received task and sec
    int sec = cmds[0].toInt(); // 0~32400
    String task = cmds[1];

    if (task == "mouse"){
      brink_msec(sec*1000);
      myprint("MOUSE", ";");
    }
    if (task == "click"){
      brink_msec(sec*1000);
      myprint("CLICK", ";");
    }
  }
}
