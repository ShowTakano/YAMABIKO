#include <EEPROM.h>
// Uno,  Leonardo 1k=1024byte=1000文字

const int Num_Cmd = 10;
const int Max_Str_Len = 100;
String Event_Command[Num_Cmd];
long Event_IntervalSec[Num_Cmd] = {-1};
long Event_MSecCounter[Num_Cmd] = {0}; // long整数型 -2,147,483,648から2,147,483,647までの数値
String Event_Interval_Or_Once[Num_Cmd];
boolean initialized = false;
int index = 0;
int msec = 0;
int global_sec = 0;
int _global_sec = 0;

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  Serial.begin(9600);
  for (int index = 0; index < Num_Cmd; index++){
    initializeFromEEPROM(index * Max_Str_Len);
  }
}

void zeroPadToEEPROM(){
  for (int i = 0; i < Num_Cmd * Max_Str_Len; i++){
    String zero = "";
    byte len = zero.length();
    EEPROM.put(i, 0);
  }
}

void writeStringToEEPROM(int addrOffset, const String &strToWrite)
{
  byte len = strToWrite.length();
  EEPROM.write(addrOffset, len);

  for (int i = 0; i < len; i++)
  {
    EEPROM.write(addrOffset + 1 + i, strToWrite[i]);
  }
}

String readStringFromEEPROM(int addrOffset)
{
  int newStrLen = EEPROM.read(addrOffset);
  char data[newStrLen];

  for (int i = 0; i < newStrLen; i++)
  {
    data[i] = EEPROM.read(addrOffset + 1 + i);
  }

  return String(data);
}

void initializeFromEEPROM(int addrOffset)
{
  int newStrLen = EEPROM.read(addrOffset);
  if (0 < newStrLen){
    // any data 工場出荷時EEPROMｈ-1もしくは、serialを受信したときに全箇所0にしている。commandを受信した箇所は文字数を入れている
    char _data[newStrLen];

    for (int i = 0; i < newStrLen; i++)
    {
      _data[i] = EEPROM.read(addrOffset + 1 + i);
    }

    String data = String(_data);
    // initializeのためにdataをparse
    String command;
    int intervalsec;
    String interval_or_once;
    parseStringToInitialize(data, command, intervalsec, interval_or_once);
    // initialize
    int index = addrOffset / Max_Str_Len;
    initialize(index, command, intervalsec, interval_or_once);
    initialized = true;
  }
}

void parseStringToInitialize(String data, String &command, int &intervalsec, String &interval_or_once){
  // split data to task, sec, interval
  String cmds[3];
  int _ = split(data, ',', cmds);

  // set received task, sec, interval
  String task = cmds[0];

  int task_is_type;
  task_is_type = task.indexOf("type"); // typeが含まれていれば0~。含まれていなければ-1。
  if (task_is_type != -1){
    // taskがtypeなので、taskをstrsに上書き
    // type:strでtaskに入っているので、:で二つに分割し、strsに代入
    String strs[2];
    int _ = split(task, ':', strs);
    task = strs[1];
  }
  command = task;
  // sec, intervalをparse
  intervalsec = cmds[1].toInt(); // 0~32400 sec
  interval_or_once = cmds[2];
  int is_once;
  is_once = interval_or_once.indexOf("once"); // onceが含まれていれば0~。含まれてなければ-1。
  if (is_once != -1){
    // onceなのでonceを返す
    String once = "once";
    interval_or_once = once;
  }
  else{
    // intervalなのでintervalを返す
    String interval = "interval";
    interval_or_once = interval;
  }
}

void brink(){
  digitalWrite(LED_BUILTIN, HIGH);
  delay(10);
  digitalWrite(LED_BUILTIN, LOW);
  //delay(10);
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


void initialize(int index, String command, int intervalsec, String interval_or_once){
  Event_Command[index] = command;
  Event_IntervalSec[index] = (long)intervalsec;
  Event_MSecCounter[index] = 0; // 受信してセットする度にカウンターはゼロに
  Event_Interval_Or_Once[index] = interval_or_once;
}

void event(){
  
  for (int idx=0; idx < Num_Cmd; idx++){
    // この関数は1msecごとに呼ばれ、時間カウンタをインクリメントする
    Event_MSecCounter[idx] = Event_MSecCounter[idx] + 1;
    // 時間カウンタ＝インターバル判定
    if (Event_MSecCounter[idx] == Event_IntervalSec[idx] * 1000){
      // イベント発生時間
      // do 
      brink();
      Serial.print(readStringFromEEPROM(idx * Max_Str_Len));
      Serial.print(";");
      // イベントを行った後には時間カウンタをゼロに戻す
      Event_MSecCounter[idx] = 0;
      // 一度しか実行しないイベントは、インターバルを-1にする
      if (Event_Interval_Or_Once[idx] == "once"){
        Event_IntervalSec[idx] = -1;
      }
    }
  }
}


void loop() {
  // inside of serial loop
  if ( Serial.available() ){

    initialized = false;
    String data;
    data = Serial.readStringUntil(';');
    Serial.print("inputdata ");
    Serial.print(data);

    if (index == 0){
      // 受信して最初の一度目は、EEPROMを初期かする
      zeroPadToEEPROM();
    }

    if (data == "end"){
      // endに到達
      index = 0;
      initialized = true;
    }

    if (initialized == false){
      // initializeのためにdataをparse
      String command;
      int intervalsec;
      String interval_or_once;
      parseStringToInitialize(data, command, intervalsec, interval_or_once);
      // initialize
      initialize(index, command, intervalsec, interval_or_once);
      // EEPROMに登録
      writeStringToEEPROM(index * Max_Str_Len, data);

      index = index + 1;
    }
  }
  // outside of serial loop
  if (initialized == true){
    event();
    delay(1);
  }
}
