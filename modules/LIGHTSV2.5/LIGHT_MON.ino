#include <Adafruit_NeoPixel.h>
#define PINF_L 7//output pin to front
#define PINF_R 6 //output pin to front  
#define PINR 5 //output pin to rear
#define NUM_LEDS_F 31
#define NUM_LEDS_R 132
Adafruit_NeoPixel strip_f_l = Adafruit_NeoPixel(NUM_LEDS_F, PINF_L, NEO_GRB + NEO_KHZ800);
Adafruit_NeoPixel strip_f_r = Adafruit_NeoPixel(NUM_LEDS_F, PINF_R, NEO_GRB + NEO_KHZ800);
Adafruit_NeoPixel strip_r = Adafruit_NeoPixel(NUM_LEDS_R, PINR, NEO_GRB + NEO_KHZ800);
unsigned long time_stamp;
//ARRAY FOR INDIV LED CONTROL
//INFO : FRONT - TOP 15LED BOT 16
int const_f[]={0,1,2,3,4,5,6,7,8,9,10,11,12,13,14};
int const_r[]={16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115};
int ind_f[]={15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30};
int ind_R_L1[]={50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65};
int ind_R_L2[]={81,80,79,78,77,76,75,74,73,72,71,70,69,68,67,66};
int ind_R_R1[]={15,14,13,12,11,10,9,8,7,6,5,4,3,2,1,0};
int ind_R_R2[]={116,117,118,119,120,121,122,123,124,125,126,127,128,129,130,131};
#define BRIGHTNESS 50
#define ELEMENTS(x)   (sizeof(x) / sizeof(x[0]))
int ON=0;
// this constant won't change:
const int  buttonPin = 2;    // the pin that the pushbutton is attached to

// Variables will change:
int buttonPushCounter = 0;   // counter for the number of button presses
int buttonState = 0;         // current state of the button
int lastButtonState = 0;     // previous state of the button
//COLOUR PALLETE
uint32_t amber = strip_r.Color(255, 51, 0);
uint32_t halfred = strip_r.Color(122, 0, 0);
uint32_t fullred = strip_r.Color(255, 0, 0);
uint32_t fullwhite= strip_r.Color(255,255,255);
uint32_t halfwhite=strip_r.Color(127,127,127);



void setup() {
  // initialize the button pin as a input:
  time_stamp=millis();
  pinMode(buttonPin, INPUT);
    //SERIAL SETUP FOR RASPI COMMS
  Serial.begin(9600);
  //INIT LIGHTS TO NULL STATE
  strip_f_l.begin();
  strip_f_r.begin();
  strip_r.begin();
  for(int i=0; i<NUM_LEDS_F; i++){
    strip_f_l.setPixelColor(i, 0, 0, 0);
    }  
  for(int i=0; i<NUM_LEDS_F; i++){
    strip_f_r.setPixelColor(i, 0,0,0);
    }
  for(int i=0; i<NUM_LEDS_R; i++){
    strip_r.setPixelColor(i, 0, 0, 0);
    }
  strip_f_l.show();
  strip_f_r.show();
  strip_r.show();
}


void loop() {
  unsigned long currentMillis=millis();
  // read the pushbutton input pin:
  buttonState = digitalRead(buttonPin);

  // compare the buttonState to its previous state
  if (buttonState != lastButtonState  && (currentMillis - time_stamp)>300) {
    // if the state has changed, increment the counter
    if (buttonState == LOW) {
      // if the current state is HIGH then the button went from off to on:
      buttonPushCounter++;
      if (ON==0){
        ON++;
        headlights();
        Serial.println(ON);
      }
      else if (ON==1){
        ON--;
        noLights();
        Serial.println(ON);
      }

      Serial.print("number of button pushes: ");
      Serial.println(buttonPushCounter);
    } else {
      // if the current state is LOW then the button went from on to off:
      Serial.println("off");
    }
    // Delay a little bit to avoid bouncing
    time_stamp=millis();
  }
  // save the current state as the last state, for next time through the loop
  lastButtonState = buttonState;


  // turns on the LED every four button pushes by checking the modulo of the
  // button push counter. the modulo function gives you the remainder of the
  // division of two numbers:
//  if (buttonPushCounter % 4 == 0) {
//    noLights();
//    Serial.print("void");
//  } else {
//    headlights();
//    Serial.print("HL");
//  }

}


void noLights(){
  for(int i=0; i<NUM_LEDS_F; i++){
    strip_f_l.setPixelColor(i, 0, 0, 0);
    strip_f_r.setPixelColor(i ,0, 0, 0);
  }
  for (int i=0; i<NUM_LEDS_R; i++){
    strip_r.setPixelColor(i, 0, 0, 0);
  }
  strip_f_l.show();
  strip_f_r.show();
  strip_r.show();
  }
void headlights(){
  for(int i=0; i<NUM_LEDS_F; i++){
    strip_f_l.setPixelColor(i, fullwhite);
    strip_f_r.setPixelColor(i, fullwhite);
  }
  for (int i=0; i<NUM_LEDS_R; i++){
    strip_r.setPixelColor(i,halfred);
  }
  strip_f_l.show();
  strip_f_r.show();
  strip_r.show();
 }

void rainbowCycle(uint8_t wait) {
  uint16_t i, j;

  for(j=0; j<256*5; j++) { // 5 cycles of all colors on wheel
    for(i=0; i< NUM_LEDS_R; i++) {
      strip_r.setPixelColor(i, Wheel(((i * 256 / NUM_LEDS_F) + j) & 255));
    }
    for(i=0; i< NUM_LEDS_F; i++) {
      strip_f_l.setPixelColor(i, Wheel(((i * 256 / NUM_LEDS_F) + j) & 255));
      strip_f_r.setPixelColor(i, Wheel(((i * 256 / NUM_LEDS_F) + j) & 255));
    }    
    strip_r.show();
    strip_f_l.show();
    strip_f_r.show();
    delay(wait);
  }
}

// Input a value 0 to 255 to get a color value.
// The colours are a transition r - g - b - back to r.
uint32_t Wheel(byte WheelPos) {
  WheelPos = 255 - WheelPos;
  if(WheelPos < 85) {
    return strip_f_l.Color(255 - WheelPos * 3, 0, WheelPos * 3,0);
  }
  if(WheelPos < 170) {
    WheelPos -= 85;
    return strip_f_l.Color(0, WheelPos * 3, 255 - WheelPos * 3,0);
  }
  WheelPos -= 170;
  return strip_f_l.Color(WheelPos * 3, 255 - WheelPos * 3, 0,0);
}


