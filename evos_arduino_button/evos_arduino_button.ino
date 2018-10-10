
#include <RBD_Timer.h>

#include <PinChangeInterrupt.h>
#include <PinChangeInterruptBoards.h>
#include <PinChangeInterruptPins.h>
#include <PinChangeInterruptSettings.h>

#include <Adafruit_NeoPixel.h>

// Timer for indicator scroll
RBD::Timer timer;

// Steering wheel pins
const int leftSignalPin = 13;
const int rightSignalPin = 2;
const int hornPin = 0;
const int lapCounterPin = 3;
const int PTTPin = 4;

// Button cluster pins
const int hazardPin = 5;
const int wiperPin = 7;
const int headlightPin = 6;
const int ignitionPin = 8;

// Limit switch pins
const int brakeLimitPin = A3;
const int clutchLimitPin = A4;

// LED strip control pins
const int leftFrontLEDPin = 9;
const int rightFrontLEDPin = 10;
const int rearLEDPin = 11;
const int starterLEDPin = 12;

// Relay control pins
const int ignitionRelayPin = 14;
const int hornRelayPin = 15;
const int wiperRelayPin = 16;

//LED Settings
#define LED_BRIGHTNESS 128
#define NUM_LEDS_FRONT 31
#define NUM_LEDS_FRONT_TOP 15
#define NUM_LEDS_REAR 132
#define NUM_LEDS_REAR_TOP 66
#define NUM_LEDS_REAR_TOP_SIDE 15
#define NUM_LEDS_STARTER 36

const int rearLeftTopLEDs[]={50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65};
const int rearLeftBottomLEDs[]={81,80,79,78,77,76,75,74,73,72,71,70,69,68,67,66};
const int rearRightTopLEDs[]={15,14,13,12,11,10,9,8,7,6,5,4,3,2,1,0};
const int rearRightBottomLEDs[]={116,117,118,119,120,121,122,123,124,125,126,127,128,129,130,131};

const int frontTopRow = 15;
const int rearTopRow = 100;

Adafruit_NeoPixel stripStarter = Adafruit_NeoPixel(NUM_LEDS_STARTER, starterLEDPin, NEO_GRB + NEO_KHZ800);
Adafruit_NeoPixel stripFrontLeft = Adafruit_NeoPixel(NUM_LEDS_FRONT, leftFrontLEDPin, NEO_GRB + NEO_KHZ800);
Adafruit_NeoPixel stripFrontRight = Adafruit_NeoPixel(NUM_LEDS_FRONT, rightFrontLEDPin, NEO_GRB + NEO_KHZ800);
Adafruit_NeoPixel stripRear = Adafruit_NeoPixel(NUM_LEDS_REAR, rearLEDPin, NEO_GRB + NEO_KHZ800);

uint32_t amber = stripRear.Color(255, 51, 0);
uint32_t halfred = stripRear.Color(50, 0, 0);
uint32_t fullred = stripRear.Color(255, 0, 0);
uint32_t fullwhite = stripRear.Color(255,255,255);
uint32_t halfwhite = stripRear.Color(127,127,127);

// DEVICE STATES
bool wiperState = false;
bool hornState = false;
bool ignitionState = false;
bool clutchState = false;

// LED STATES
const int BLANK = 0;
const int HAZARD = 1;
const int LEFT = 2;
const int RIGHT = 3;
const int HL = 4;
const int HL_HAZARD = 5;
const int HL_LEFT = 6;
const int HL_RIGHT = 7;

bool hazardState = false;
bool headlightState = false;
bool brakeState = true;
bool leftState = false;
bool rightState = false;
bool stateChanged = false;
int ledState = 0;
int amberCount = 0;

void setup() {
  Serial.begin(9600);

  // STEERING WHEEL PINS
  pinMode(leftSignalPin, INPUT_PULLUP);
  digitalWrite(leftSignalPin, HIGH);
  attachPinChangeInterrupt(digitalPinToPCINT(leftSignalPin), leftSignalTrigger, FALLING);
  pinMode(rightSignalPin, INPUT_PULLUP);
  attachPinChangeInterrupt(digitalPinToPCINT(rightSignalPin), rightSignalTrigger, FALLING);
  pinMode(hornPin, INPUT_PULLUP);
  attachPinChangeInterrupt(digitalPinToPCINT(hornPin), hornTrigger, CHANGE);
//  attachPinChangeInterrupt(digitalPinToPCINT(hornPin), hornReleaseTrigger, RISING);
  pinMode(lapCounterPin, INPUT_PULLUP);
  attachPinChangeInterrupt(digitalPinToPCINT(lapCounterPin), lapCounterTrigger, FALLING);
  pinMode(PTTPin, INPUT_PULLUP);
  attachPinChangeInterrupt(digitalPinToPCINT(PTTPin), PTTTrigger, FALLING);

  // BUTTON CLUSTER PINS
  pinMode(ignitionPin, INPUT_PULLUP);
  attachPinChangeInterrupt(digitalPinToPCINT(ignitionPin), ignitionTrigger, CHANGE);
//  attachPinChangeInterrupt(digitalPinToPCINT(ignitionPin), ignitionReleaseTrigger, RISING);
  pinMode(hazardPin, INPUT_PULLUP);
  attachPinChangeInterrupt(digitalPinToPCINT(hazardPin), hazardTrigger, FALLING);
  pinMode(wiperPin, INPUT_PULLUP);
  attachPinChangeInterrupt(digitalPinToPCINT(wiperPin), wiperTrigger, FALLING);
  pinMode(headlightPin, INPUT_PULLUP);
  attachPinChangeInterrupt(digitalPinToPCINT(headlightPin), headlightTrigger, FALLING);

  // LIMIT SWITCH PINS
  pinMode(brakeLimitPin, INPUT_PULLUP);
  attachPinChangeInterrupt(digitalPinToPCINT(brakeLimitPin), brakeTrigger, CHANGE);
  pinMode(clutchLimitPin, INPUT_PULLUP);
  attachPinChangeInterrupt(digitalPinToPCINT(clutchLimitPin), clutchTrigger, CHANGE);

  // RELAY CONTROL PINS
  pinMode(ignitionRelayPin, OUTPUT);
  digitalWrite(ignitionRelayPin, HIGH);
  pinMode(hornRelayPin, OUTPUT);
  digitalWrite(hornRelayPin, HIGH);
  pinMode(wiperRelayPin, OUTPUT);
  digitalWrite(wiperRelayPin, HIGH);

  // LED STRIP PREP
  stripStarter.begin();
  stripStarter.show();
  stripFrontLeft.begin();
  stripFrontLeft.show();
  stripFrontRight.begin();
  stripFrontRight.show();
  stripRear.begin();
  stripRear.show();

  // INDICATOR SCROLL TIMING
  timer.setHertz(32);
}

void loop() {
  if(timer.onRestart()) {
    updateAmbers();
  }
  if(stateChanged){
    stateChanged = false;
    parseLEDState();
    updateLEDs();
  }
}


void updateAmbers() {
  if(amberCount == NUM_LEDS_FRONT_TOP+1){
    amberCount = 0;
  }
  amberCount++;
  stateChanged = true;
}


void updateLEDs() {
  stripStarter.clear();
  stripFrontLeft.clear();
  stripFrontRight.clear();
  stripRear.clear();
  
  switch(ledState) {
    case BLANK:
      // do nothing
      break;
      
    case HAZARD:
      for (int i = 0; i < amberCount; i++){
        stripFrontLeft.setPixelColor(NUM_LEDS_FRONT_TOP-i, amber);
        stripFrontRight.setPixelColor(NUM_LEDS_FRONT_TOP-i, amber);
      }
      for (int i = 0; i < amberCount; i++){
        stripRear.setPixelColor(rearLeftTopLEDs[i], amber);
        stripRear.setPixelColor(rearLeftBottomLEDs[i], amber);
        stripRear.setPixelColor(rearRightTopLEDs[i], amber);
        stripRear.setPixelColor(rearRightBottomLEDs[i], amber);
      }
      break;
      
    case LEFT:
      for (int i = 0; i < amberCount; i++){
        stripFrontLeft.setPixelColor(NUM_LEDS_FRONT_TOP-i, amber);
      }
      for (int i = 0; i < amberCount; i++){
        stripRear.setPixelColor(rearLeftTopLEDs[i], amber);
        stripRear.setPixelColor(rearLeftBottomLEDs[i], amber);
      }
      break;
      
    case RIGHT:
      for (int i = 0; i < amberCount; i++){
        stripFrontRight.setPixelColor(NUM_LEDS_FRONT_TOP-i, amber);
      }
      for (int i = 0; i < amberCount; i++){
        stripRear.setPixelColor(rearRightTopLEDs[i], amber);
        stripRear.setPixelColor(rearRightBottomLEDs[i], amber);
      }
      break;
      
    case HL:
      for (int i = 0; i < NUM_LEDS_FRONT; i++){
        stripFrontRight.setPixelColor(i, fullwhite);
        stripFrontLeft.setPixelColor(i, fullwhite);
      }
      for (int i = 0; i < NUM_LEDS_REAR; i++){
        stripRear.setPixelColor(i, halfred);
      }
      break;
      
    case HL_HAZARD:
      for (int i = 0; i < NUM_LEDS_FRONT; i++){
        stripFrontRight.setPixelColor(i, fullwhite);
        stripFrontLeft.setPixelColor(i, fullwhite);
      }
      for (int i = 0; i < NUM_LEDS_REAR; i++){
        stripRear.setPixelColor(i, halfred);
      }
      for (int i = 0; i < amberCount; i++){
        stripFrontLeft.setPixelColor(NUM_LEDS_FRONT_TOP-i, amber);
        stripFrontRight.setPixelColor(NUM_LEDS_FRONT_TOP-i, amber);
      }
      for (int i = 0; i < amberCount; i++){
        stripRear.setPixelColor(rearLeftTopLEDs[i], amber);
        stripRear.setPixelColor(rearLeftBottomLEDs[i], amber);
        stripRear.setPixelColor(rearRightTopLEDs[i], amber);
        stripRear.setPixelColor(rearRightBottomLEDs[i], amber);
      }
      break;
      
    case HL_LEFT:
      for (int i = 0; i < NUM_LEDS_FRONT; i++){
        stripFrontRight.setPixelColor(i, fullwhite);
        stripFrontLeft.setPixelColor(i, fullwhite);
      }
      for (int i = 0; i < NUM_LEDS_REAR; i++){
        stripRear.setPixelColor(i, halfred);
      }
      for (int i = 0; i < amberCount; i++){
        stripFrontLeft.setPixelColor(NUM_LEDS_FRONT_TOP-i, amber);
      }
      for (int i = 0; i < amberCount; i++){
        stripRear.setPixelColor(rearLeftTopLEDs[i], amber);
        stripRear.setPixelColor(rearLeftBottomLEDs[i], amber);
      }
    case HL_RIGHT:
      for (int i = 0; i < NUM_LEDS_FRONT; i++){
        stripFrontRight.setPixelColor(i, fullwhite);
        stripFrontLeft.setPixelColor(i, fullwhite);
      }
      for (int i = 0; i < NUM_LEDS_REAR; i++){
        stripRear.setPixelColor(i, halfred);
      }
      for (int i = 0; i < amberCount; i++){
        stripFrontRight.setPixelColor(NUM_LEDS_FRONT_TOP-i, amber);
      }
      for (int i = 0; i < amberCount; i++){
        stripRear.setPixelColor(rearRightTopLEDs[i], amber);
        stripRear.setPixelColor(rearRightBottomLEDs[i], amber);
      }
  }

  if (brakeState) {
    for (int i = 0; i < NUM_LEDS_REAR; i++){
        stripRear.setPixelColor(i, fullred);
      }
  }
  stripStarter.show();
  stripFrontLeft.show();
  stripFrontRight.show();
  stripRear.show();
}

void parseLEDState() {
  if(!headlightState) {  // headlights off
      if(hazardState) {
        ledState = HAZARD;
      } else if (leftState) {
        ledState = LEFT;
      } else if (rightState) {
        ledState = RIGHT;
      } else {
        ledState = BLANK;
      }
    } else {  // headlights on
      if(hazardState) {
        ledState = HL_HAZARD;
      } else if (leftState) {
        ledState = HL_LEFT;
      } else if (rightState) {
        ledState = HL_RIGHT;
      } else {
        ledState = HL;
      }
    }
}

// STEERING WHEEL TRIGGERS
void leftSignalTrigger() {
  Serial.println("Left signal pressed");
  leftState = !leftState;
  stateChanged = true;
}

void rightSignalTrigger() {
  Serial.println("Right signal pressed");
  rightState = !rightState;
  stateChanged = true;
}

void hornTrigger() {
  Serial.println("Horn pressed");
  hornState = !hornState;
  digitalWrite(hornRelayPin, !hornState);
}

void PTTTrigger() {
  Serial.println("PTT pressed");
}

void lapCounterTrigger() {
  Serial.println("Lap counter pressed");
}


// BUTTON CLUSTER TRIGGERS
void ignitionTrigger(){
  Serial.println("Ignition pressed");
  ignitionState = !ignitionState;
  digitalWrite(ignitionRelayPin, !ignitionState);
}

void ignitionReleaseTrigger() {
  Serial.println("Ignition released");
  digitalWrite(hornRelayPin, HIGH);
}

void hazardTrigger() {
  Serial.println("Hazard pressed");
  hazardState = !hazardState;
  stateChanged = true;
}

void wiperTrigger() {
  Serial.println("Wiper pressed");
  wiperState = !wiperState;
  digitalWrite(wiperRelayPin, !wiperState);
}

void headlightTrigger() {
  Serial.println("Headlight pressed");
  headlightState = !headlightState;
  stateChanged = true;
}


// LIMIT SWITCHES
void brakeTrigger() {
  Serial.println("Brake pressed");
  brakeState = !brakeState;
  stateChanged = true;
}

void clutchTrigger() {
  Serial.println("Clutch pressed");
  clutchState = !clutchState;
}
