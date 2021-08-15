/*
https://learn.adafruit.com/adafruit-neo-trinkey
に従い、ドライバーをインストールする。
https://learn.adafruit.com/adafruit-neo-trinkey/arduino-ide-setup
ドライバーインストール作業途中、post_install.batの実行をスキップしたメッセージが出てしまうが、そのまま次に進むことができる。
https://learn.adafruit.com/adafruit-neo-trinkey/arduino-example
に従い、ライブラリをインストールする。
当サンプルスクリプトを実行すすることができた。
書き込みを行うと、ブートローダリセットがかかるため、windowsからの認識が一瞬おかしくなる。
しかし、公式にartifactが発生する旨は記述があり、正常動作である。
NeoTrinkeyを抜いたり挿したりしなくても、いつでも書き込んで良い。また、挿入したらすぐにHIDとして認識されるようだ。
全角半角の設定を治すコマンドを用意して仕込んでおかないといけないだろう。
Adafruitはさすがに優秀である。採用。
*/
/*
  Keyboard Message test
  For the Adafruit Neo Trinkey
  Sends a text string when a one touchpad is pressed, opens up Notepad if the other is pressed
*/

#include <Adafruit_NeoPixel.h>
#include "Adafruit_FreeTouch.h"
#include "Keyboard.h"

// Create the neopixel strip with the built in definitions NUM_NEOPIXEL and PIN_NEOPIXEL
Adafruit_NeoPixel strip = Adafruit_NeoPixel(NUM_NEOPIXEL, PIN_NEOPIXEL, NEO_GRB + NEO_KHZ800);

// Create the two touch pads on pins 1 and 2:
Adafruit_FreeTouch qt_1 = Adafruit_FreeTouch(1, OVERSAMPLE_4, RESISTOR_50K, FREQ_MODE_NONE);
Adafruit_FreeTouch qt_2 = Adafruit_FreeTouch(2, OVERSAMPLE_4, RESISTOR_50K, FREQ_MODE_NONE);


bool previousTouch1State = false;   // for checking the state of touch 1
bool previousTouch2State = false;   // for checking the state of touch 1
int touch1counter = 0;              // touch 1 counter

void setup() {
  Serial.begin(9600);
  //while (!Serial) delay(10);
  
  strip.begin(); // start pixels
  strip.setBrightness(20); // not too bright!
  strip.show(); // Initialize all pixels to 'off'

  if (! qt_1.begin())  
    Serial.println("Failed to begin qt on pin 1");
  if (! qt_2.begin())  
    Serial.println("Failed to begin qt on pin 2");
    
  // initialize control over the keyboard:
  Keyboard.begin();
}

void loop() {
  
  // measure the captouches
  uint16_t touch1 = qt_1.measure();
  uint16_t touch2 = qt_2.measure();
  // whether we think they are being touched
  bool Touch1State, Touch2State;

  // print out the touch readings
  Serial.print("QT 1: "); Serial.print(touch1);
  Serial.print("\t\tQT 2: "); Serial.println(touch2);

  // If the first pad is touched, turn on the #2 and #3 pixel red
  if (touch1 > 500) {
    Touch1State = true;  // is touched
    strip.setPixelColor(2, 0xFF0000);
    strip.setPixelColor(3, 0xFF0000);
  } else {
    // turn them off
    Touch1State = false;  // is not touched
    strip.setPixelColor(2, 0x0);
    strip.setPixelColor(3, 0x0);    
  }


  // If the second pad is touched, turn on the #0 and #1 pixel blue
  if (touch2 > 500) {
    Touch2State = true;  // is touched
    strip.setPixelColor(0, 0x0000FF);
    strip.setPixelColor(1, 0x0000FF);
  } else {
    // turn them off
    Touch2State = false;  // is not touched
    strip.setPixelColor(0, 0x0);
    strip.setPixelColor(1, 0x0);
  }
  
  strip.show(); // display pixel changes

  // If we are now touching #1, and we weren't before...
  if (Touch1State and !previousTouch1State) {
    touch1counter++; // increment the touch counter
    // type out a message
    Keyboard.print("You touched the captouch #1 ");
    Keyboard.print(touch1counter);
    Keyboard.println(" times.");
  }
  // save the current touch state for comparison next time:
  previousTouch1State = Touch1State;

  // If we are now touching #2, and we weren't before...
  if (Touch2State and !previousTouch2State) {
    // make a complex collection of commands for windows!
    Keyboard.press(KEY_LEFT_GUI);
    delay(100);
    Keyboard.releaseAll();
    delay(100);
    // run notepad
    Keyboard.print("notepad");
    delay(100);
    Keyboard.press(KEY_RETURN);
    delay(100);
    Keyboard.releaseAll();
    delay(1000); // wait for it to run
    Keyboard.println("hello world!");
  }
  // save the current touch state for comparison next time:
  previousTouch2State = Touch2State;
  
  delay(10);  // and pause a moment
}
