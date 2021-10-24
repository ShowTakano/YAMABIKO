/*
https://wave.hatenablog.com/entry/2017/03/11/083000
上記情報を参考にドライバーのインストールを試みた。
しかし、正常にインストールできない。
公式のHPなどを参照してもできない。
Arduino Micro COM4 になってしまい、Digisparkのドライバーに変更できない。
ドライバーを削除して、最初からやり直すといいかもしれないが、通常のArduinoのMicroのドライバーまで壊れると嫌なので、実施しない。
Arduino Microは使ったことがないので、おそらくは今回の施行で入ってしまったと思われるが。
Digisparkは使えない。
*/

// the setup routine runs once when you press reset:
void setup() {                
  // initialize the digital pin as an output.
  pinMode(0, OUTPUT); //LED on Model B
  pinMode(1, OUTPUT); //LED on Model A   
}

// the loop routine runs over and over again forever:
void loop() {
  digitalWrite(0, HIGH);   // turn the LED on (HIGH is the voltage level)
  digitalWrite(1, HIGH);
  delay(1000);               // wait for a second
  digitalWrite(0, LOW);    // turn the LED off by making the voltage LOW
  digitalWrite(1, LOW); 
  delay(1000);               // wait for a second
}
