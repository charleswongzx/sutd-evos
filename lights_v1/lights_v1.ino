#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
  #include <avr/power.h>
#endif

#define PIN 6 //output pin to neopixel strip

#define NUM_LEDS 60

#define BRIGHTNESS 50

// Lighting looks
int turnSignalLeft = 10; //LEDs
int turnSignalRight = NUM_LEDS - turnSignalLeft - 1;

//turn signal animation
static const int sweepTime = 150; //milliseconds
static const int holdTime = 250; //milliseconds
static const int offTime = 450;
static const int sweepMillis = sweepTime / turnSignalLeft;
static const int turnGreenVal = 100;
static const int dimLevel = 80; //brake light dim level

//INPUT PINS
static const int leftPin = 4;
static const int rightPin = 5;
static const int brakePin = 3;
static const int interruptPin = 3;

//pin state variables
boolean leftState = false;
boolean rightState = false;
boolean brakeState = false;

Adafruit_NeoPixel strip = Adafruit_NeoPixel(NUM_LEDS, PIN, NEO_GRB + NEO_KHZ800);

int gamma[] = {
    0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
    0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1,  1,  1,  1,
    1,  1,  1,  1,  1,  1,  1,  1,  1,  2,  2,  2,  2,  2,  2,  2,
    2,  3,  3,  3,  3,  3,  3,  3,  4,  4,  4,  4,  4,  5,  5,  5,
    5,  6,  6,  6,  6,  7,  7,  7,  7,  8,  8,  8,  9,  9,  9, 10,
   10, 10, 11, 11, 11, 12, 12, 13, 13, 13, 14, 14, 15, 15, 16, 16,
   17, 17, 18, 18, 19, 19, 20, 20, 21, 21, 22, 22, 23, 24, 24, 25,
   25, 26, 27, 27, 28, 29, 29, 30, 31, 32, 32, 33, 34, 35, 35, 36,
   37, 38, 39, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 50,
   51, 52, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 66, 67, 68,
   69, 70, 72, 73, 74, 75, 77, 78, 79, 81, 82, 83, 85, 86, 87, 89,
   90, 92, 93, 95, 96, 98, 99,101,102,104,105,107,109,110,112,114,
  115,117,119,120,122,124,126,127,129,131,133,135,137,138,140,142,
  144,146,148,150,152,154,156,158,160,162,164,167,169,171,173,175,
  177,180,182,184,186,189,191,193,196,198,200,203,205,208,210,213,
  215,218,220,223,225,228,231,233,236,239,241,244,247,249,252,255 };


void setup() {
  Serial.begin(115200);

  //PINMODES
  pinMode(leftPin, INPUT);
  pinMode(rightPin, INPUT);
  pinMode(brakePin, INPUT);

  //attach interrupt for brake pins
  attachInterrupt(digitalPinToInterrupt(interruptPin), checkBrake, CHANGE);

  
  // This is for Trinket 5V 16MHz, you can remove these three lines if you are not using a Trinket
  #if defined (__AVR_ATtiny85__)
    if (F_CPU == 16000000) clock_prescale_set(clock_div_1);
  #endif
  // End of trinket special code
  strip.setBrightness(BRIGHTNESS);
  strip.begin();
  strip.show(); // Initialize all pixels to 'off'
}

void loop() {
  checkTurnSignals();
  checkBrake();
  
  int sum = 0; 
  if(leftState == true){
    sum += 1;
  }
  if (rightState == true){
    sum += 2;
  }

  switch(sum){
    case 1:
      turnLeft();
      break;

    case 2:
      turnRight();
      break;

    case 3:
      hazards();
      break;
  }
}

void checkBrake(){
  //function to update the brake pin state
  if(digitalRead(brakePin) == HIGH){
    brakeState = true;
    brakeLights();
  }
  else{
    brakeState = false;
    dimLights();
  }
}

void checkTurnSignals(){
  if(digitalRead(leftPin) == HIGH){
    leftState = true;
  }
  else{
    leftState = false;
  }
  if(digitalRead(rightPin) == HIGH){
    rightState = true;
  }
  else{
    rightState = false;
  }
}

void printPinStates(){
  Serial.print("Left = ");
  Serial.println(leftState);

  Serial.print("Right = ");
  Serial.println(rightState);

  Serial.print("Brake = ");
  Serial.println(brakeState);
}


// TEST CODE BLOCKS
void test1(){
  noLights();
  delay(1000);
  dimLights();
  delay(1000);
  turnLeft();
  delay(1000);
  turnRight();
  delay(1000);
}

void test2(){
//  turnLeft();
  Serial.println("dim");
  
  dimLights();
  delay(1000);
  brakeLights();
  
  for(int i=0; i<3; i++){
    turnLeft();
  }
  delay(1000);
  
  for(int i=0; i<3; i++){
    turnRight();
  }
  delay(1000);

  for(int i=0; i<3; i++){
    hazards();
  }
  delay(1000);
}

// END OF TEST CODE BLOCKS



void noLights(){
  for(int i=0; i<NUM_LEDS; i++){
    strip.setPixelColor(i, 0, 0, 0);
  }
  strip.show();
}

void dimLights(){
  
  int sum = 0; 
  if(leftState == true){
    sum += 1;
  }
  if (rightState == true){
    sum += 2;
  }

  switch(sum){
    case 0:
      for(int i=0; i<NUM_LEDS; i++){
        strip.setPixelColor(i, dimLevel, 0, 0);
      }
      break;

    case 1:
      for(int i=turnSignalLeft; i<NUM_LEDS; i++){
        strip.setPixelColor(i, dimLevel, 0, 0);
      }
      break;

    case 2:
      for(int i=0; i<turnSignalRight+1; i++){
        strip.setPixelColor(i, dimLevel, 0, 0);
      }
      break;

    case 3:
      for(int i=turnSignalLeft; i<turnSignalRight+1; i++){
        strip.setPixelColor(i, dimLevel, 0, 0);
      }
      break;
  }
  strip.show();
}

void brakeLights(){
  
  int sum = 0; 
  if(leftState == true){
    sum += 1;
  }
  if (rightState == true){
    sum += 2;
  }

  switch(sum){
    case 0:
      for(int i=0; i<NUM_LEDS; i++){
        strip.setPixelColor(i, 255, 0, 0);
      }
      break;

    case 1:
      for(int i=turnSignalLeft; i<NUM_LEDS; i++){
        strip.setPixelColor(i, 255, 0, 0);
      }
      break;

    case 2:
      for(int i=0; i<turnSignalRight+1; i++){
        strip.setPixelColor(i, 255, 0, 0);
      }
      break;

    case 3:
      for(int i=turnSignalLeft; i<turnSignalRight+1; i++){
        strip.setPixelColor(i, 255, 0, 0);
      }
      break;
  }
  strip.show();
}

//void reverse(){
//  for(int i=0; i<NUM_LEDS; i++){
//    strip.setPixelColor(i, 255, 255, 200);
//  }
//  strip.show();
//}

void turnLeft(){
  //turn off the turn signal LEDs except rightmost one
  for(int i=0; i<turnSignalLeft - 1; i++){
    strip.setPixelColor(i, 0 ,0 ,0);
  }
  strip.setPixelColor(turnSignalLeft - 1, 255 , turnGreenVal ,0);
  strip.show();

  delay(sweepMillis);
  
  //begin turning on LEDs
  for(int i=turnSignalLeft-2; i>=0; i--){
    //turn on the rightmost LED first
    strip.setPixelColor(i, 255, turnGreenVal, 0);
    strip.show();
    delay(sweepMillis);
  }
  
  //hold
  delay(holdTime);

  //turn off the turn signal
  for(int i=0; i<turnSignalLeft; i++){
    strip.setPixelColor(i, 0, 0, 0);
  }
  strip.show();
  delay(offTime);
}

//void turnLeft1(){ //ASYNC FUNCTION UNDER DEVELOPMENT.
//  
//  //CLEAR THE RIGHT SIGNAL FIRST, CODE BELOW IS WRONG.
//  for(int i=0; i<turnSignalLeft - 1; i++){
//    strip.setPixelColor(i, 0 ,0 ,0);
//  }
//  
//  static startLeftTime = millis();
//  static leftStep = 0;
//  for(int i=0; i<turnSignalLeft - 1; i++){
//    strip.setPixelColor(i, 0 ,0 ,0);
//  }
//  strip.setPixelColor(turnSignalLeft - 1, 255 , turnGreenVal ,0);
//  strip.show();
//  
//
//  if(millis() - startLeftTime >= ){
//    strip.setPixelColor(
//    strip.show();
//    leftStep++;
//  }
//}

void turnRight(){ // NOT IMPLEMENTED YET
  //turn off the turn signal LEDs except leftmost one
  for(int i=NUM_LEDS-1; i>turnSignalRight + 1; i--){
    strip.setPixelColor(i, 0 ,0 ,0);
  }
  strip.setPixelColor(turnSignalRight + 1, 255 ,turnGreenVal ,0);
  strip.show();

  delay(sweepMillis);
  
  //begin turning on LEDs
  for(int i=turnSignalRight+2; i<NUM_LEDS; i++){
    //turn on the rightmost LED first
    strip.setPixelColor(i, 255, turnGreenVal, 0);
    strip.show();
    delay(sweepMillis);
  }
  
  //hold
  delay(holdTime);

  //turn off the turn signal
  for(int i=NUM_LEDS; i>turnSignalRight; i--){
    strip.setPixelColor(i, 0, 0, 0);
  }
  strip.show();
  delay(offTime);
}

void hazards(){
  //turn off the turn signal LEDs except rightmost one
  for(int i=0; i<turnSignalLeft - 1; i++){
    strip.setPixelColor(i, 0 ,0 ,0);
  }
  strip.setPixelColor(turnSignalLeft - 1, 255 , turnGreenVal ,0);

  //turn off the turn signal LEDs except leftmost one
  for(int i=NUM_LEDS-1; i>turnSignalRight + 1; i--){
    strip.setPixelColor(i, 0 ,0 ,0);
  }
  strip.setPixelColor(turnSignalRight + 1, 255 ,turnGreenVal ,0);
  strip.show();

  delay(sweepMillis);
  
  //begin turning on LEDs
  for(int i=1; i<=turnSignalLeft; i++){
    //turn on the rightmost LED first
    strip.setPixelColor(turnSignalLeft-i, 255, turnGreenVal, 0);
    strip.setPixelColor(turnSignalRight+i, 255, turnGreenVal, 0);
    strip.show();
    delay(sweepMillis);
  }
  
  //hold
  delay(holdTime);

  //turn off the turn signal
  for(int i=0; i<turnSignalLeft; i++){
    strip.setPixelColor(i, 0, 0, 0);
  }
  for(int i=NUM_LEDS; i>turnSignalRight; i--){
    strip.setPixelColor(i, 0, 0, 0);
  }
  strip.show();
  delay(offTime);
}

// Input a value 0 to 255 to get a color value.
// The colours are a transition r - g - b - back to r.
uint32_t Wheel(byte WheelPos) {
  WheelPos = 255 - WheelPos;
  if(WheelPos < 85) {
    return strip.Color(255 - WheelPos * 3, 0, WheelPos * 3,0);
  }
  if(WheelPos < 170) {
    WheelPos -= 85;
    return strip.Color(0, WheelPos * 3, 255 - WheelPos * 3,0);
  }
  WheelPos -= 170;
  return strip.Color(WheelPos * 3, 255 - WheelPos * 3, 0,0);
}

uint8_t red(uint32_t c) {
  return (c >> 8);
}
uint8_t green(uint32_t c) {
  return (c >> 16);
}
uint8_t blue(uint32_t c) {
  return (c);
}


