
void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  Serial.begin(9600);
}

void brink(){
  digitalWrite(LED_BUILTIN, HIGH);
  delay(10);
  digitalWrite(LED_BUILTIN, LOW);
  //delay(10);
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

const int Num_Cmd = 10;
String Event_Command[Num_Cmd];
int Event_IntervalSec[Num_Cmd] = {20};
long Event_MSecCounter[Num_Cmd] = {0}; // long整数型 -2,147,483,648から2,147,483,647までの数値
boolean Event_ONCE_FLG[Num_Cmd] = {false};

void initialize(int index, String command, int intervalsec, boolean flg){
  Event_Command[index] = command;
  Event_IntervalSec[index] = intervalsec;
  Event_MSecCounter[index] = 0; // 受信してセットする度にカウンターはゼロに
  Event_ONCE_FLG[index] = flg;
}

void event(){
  
  for (int idx=0; idx <= Num_Cmd; idx++){
    // この関数は1msecごとに呼ばれ、時間カウンタをインクリメントする
    Event_MSecCounter[idx] = Event_MSecCounter[idx] + 1;
    // 時間カウンタ＝インターバル判定
    if (Event_MSecCounter[idx] == Event_IntervalSec[idx] * 1000){
      // イベント発生時間
      // do 
      brink();
      // イベントを行った後には時間カウンタをゼロに戻す
      Event_MSecCounter[idx] = 0;
      // 一度しか実行しないイベントは、インターバルを-1にする
      if (Event_ONCE_FLG[idx] == true){
        Event_IntervalSec[idx] = -1;
      }
    }
  }
}

boolean initialized = false;
int index = 0;
int msec = 0;
int global_sec = 0;
int _global_sec = 0;

void loop() {
  // inside of serial loop
  if ( Serial.available() ){

    initialized = false;
    String data;
    data = Serial.readStringUntil(';');
    myprint(data, ";");

    if (data == "end"){
      index = 0;
      initialized = true;
    }

    if (initialized == false){
      // split data to task, sec, interval
      String cmds[3];
      int _idx = split(data, ',', cmds);

      // set received task, sec, interval
      String task = cmds[0];
      int sec = cmds[1].toInt(); // 0~32400 sec
      String interval_or_once = cmds[2];
      boolean once_flg = false;
      if (interval_or_once == "once"){
        once_flg = true;
      }

      initialize(index, task, sec, once_flg);

      index = index + 1;
    }
  }
  // outside of serial loop
  if (initialized == true){
    event();
    delay(1);
  }
}
