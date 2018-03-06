#include <Adafruit_NeoPixel.h>
#include <SoftwareSerial.h>
#include <Adafruit_GPS.h>

//test
int s_counter=0;
int s_counter_m=0;

//GPS
#define GPSECHO  false
// this keeps track of whether we're using the interrupt
// off by default!
#define SPEED 83 //speed S
boolean usingInterrupt = false;

uint32_t timer = millis();
//   Connect the GPS TX (transmit) pin to Digital 3
//   Connect the GPS RX (receive) pin to Digital 2
// If using software serial, keep this line enabled
// (you can change the pin numbers to match your wiring):
SoftwareSerial mySerial(3, 2);
Adafruit_GPS GPS(&mySerial);

//LED CONFIG
#define PINF_L 7//output pin to front
#define PINF_R 6 //output pin to front  
#define PINR 5 //output pin to rear
#define PIN_S 4 //output pin to starter
#define OFF 0// 
#define HEADLIGHTS 1//
#define HAZARD 2//
#define LEFT 3//
#define RIGHT 4//
#define BRAKE 5//
#define STARTER 6//
#define HEADLIGHTS_OFF 65//A
#define HEADLIGHTS_ON 66//B
#define HAZARD_OFF 67//C
#define HAZARD_ON 68//D
#define LEFT_OFF 69//E
#define LEFT_ON 70//F
#define RIGHT_OFF 71//G
#define RIGHT_ON 72//H
#define STARTER_OFF 73//I
#define STARTER_ON 74//J
#define BRAKE_OFF 75//K
#define BRAKE_ON 76//L
#define CONVERT 48//

#define NUM_LEDS_F 31
#define NUM_LEDS_R 132
#define NUM_LEDS_S 36
Adafruit_NeoPixel strip_s= Adafruit_NeoPixel(NUM_LEDS_S,PIN_S, NEO_GRB + NEO_KHZ800);
Adafruit_NeoPixel strip_f_l = Adafruit_NeoPixel(NUM_LEDS_F, PINF_L, NEO_GRB + NEO_KHZ800);
Adafruit_NeoPixel strip_f_r = Adafruit_NeoPixel(NUM_LEDS_F, PINF_R, NEO_GRB + NEO_KHZ800);
Adafruit_NeoPixel strip_r = Adafruit_NeoPixel(NUM_LEDS_R, PINR, NEO_GRB + NEO_KHZ800);

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


//COLOUR PALLETE
uint32_t amber = strip_r.Color(255, 51, 0);
uint32_t halfred = strip_r.Color(50, 0, 0);
uint32_t fullred = strip_r.Color(255, 0, 0);
uint32_t fullwhite= strip_r.Color(255,255,255);
uint32_t halfwhite=strip_r.Color(127,127,127);

//TRUE FALSE FOR LIGHTS
int L = 0;
int R = 0;
int HL = 0;
int HZ=0;
int B=0;
int B_LAST=0;
int S=0;
//PRIORITY TRACKER & LAST LIGHT STATE
int PRIORITY=0;
int LAST_STATE=0;
int whitecheck=0;

//TURNING/HAZARD LED CONTROL TRACKER
int lstate=0;

//TIMINGS
//unsigned long l_interval=50; //hazard & turn light interval
unsigned long l_previousMillis=0; // track for light interval
unsigned long s_previousMillis=0; //track for starter
void setup() {
  //SERIAL SETUP FOR RASPI COMMS
  Serial.begin(115200);

  //GPS SETUP
  // 9600 NMEA is the default baud rate for Adafruit MTK GPS's- some use 4800
  GPS.begin(9600);
  GPS.sendCommand(PMTK_SET_NMEA_OUTPUT_RMCGGA);
  GPS.sendCommand(PMTK_SET_NMEA_UPDATE_1HZ);
  GPS.sendCommand(PGCMD_ANTENNA);

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
  // put your main code here, to run repeatedly:
  unsigned long currentMillis= millis();
  serialParse();
  if ((unsigned long)(currentMillis-timer)>=1){
    char c=GPS.read();
      if (GPS.newNMEAreceived()) {
    // a tricky thing here is if we print the NMEA sentence, or data
    // we end up not listening and catching other sentences! 
    // so be very wary if using OUTPUT_ALLDATA and trytng to print out data
    //Serial.println(GPS.lastNMEA());   // this also sets the newNMEAreceived() flag to false
  
    if (!GPS.parse(GPS.lastNMEA()))   // this also sets the newNMEAreceived() flag to false
      return;  // we can fail to parse a sentence in which case we should just wait for another
    }
  }
//  if (currentMillis - timer >1000){
//    float x=1.852*GPS.speed;
//    Serial.print(10);
//    Serial.print('\n');
//    timer=millis();
//  }
  if (S==1){
    lightLogic(STARTER,currentMillis);
  }
  else if(S==0){
    starterOff();
  }
  if (HZ==1){
    lightLogic(2,currentMillis);
    PRIORITY=1;
    }
  else if (HZ==0){
    if (PRIORITY==1){
      PRIORITY=0;
      lightLogic(LAST_STATE,currentMillis);
    }
    else{
      if (B==1 && B_LAST==0){
        lightLogic(BRAKE,currentMillis);
        B_LAST++;
      }
      else if(B==0 && B_LAST ==1){
        lightLogic(LAST_STATE,currentMillis);
        B_LAST--;
      }
      if (HL==1 && LAST_STATE != 3 && LAST_STATE != 4 && B_LAST != 1){
        lightLogic(HEADLIGHTS,currentMillis);
        LAST_STATE=1;
        }
      if (HL==0 && LAST_STATE==1){
        lightLogic(OFF,currentMillis);
        LAST_STATE=0; 
        }
      if (L==1){
        lightLogic(LEFT,currentMillis);
        LAST_STATE=3;
        }
      if (L==0 && LAST_STATE==3){
        //returnLights(ind_f, ind_R_L1, ind_R_L2);
        lstate=0;
        whitecheck=0;
        if (HL==1){ 
          LAST_STATE=1;
          lightLogic(LAST_STATE,currentMillis);      
          }
        else{
          LAST_STATE=0;
          lightLogic(LAST_STATE,currentMillis);
          }
        }
      if (R==1){
        lightLogic(RIGHT,currentMillis);
        LAST_STATE=4;
        }
      if (R==0 && LAST_STATE==4){
        //returnLights(ind_f, ind_R_R1, ind_R_R2);
        lstate=0;
        whitecheck=0;
        if (HL==1){
          LAST_STATE=1;
          lightLogic(LAST_STATE,currentMillis);      
          }
        else{
          LAST_STATE=0;
          lightLogic(LAST_STATE,currentMillis);
          }
        }
      }
  }
}

//LOGIK
void serialParse(){
  int sig;
//  int sig2;
//  byte sig[1];
  if(Serial.available() > 0){
    unsigned long t=millis();
    sig=Serial.read();
//    Serial.print("SIG A ");
//    Serial.println(sig);
//    Serial.print("SIG B ");
//    Serial.println(sig2);
//    Serial.print("READ DONE");
    t=millis();
//    Serial.println(t);
    if (sig==SPEED){
      pingSpeed();
    }
    if (sig==HAZARD_ON && HZ==0){
      HZ=1;
      }
    else if(sig==HAZARD_OFF && HZ==1){
      HZ=0;
      }
    if (HZ!=1){
      if (sig==LEFT_ON && L==0 && R!=1){
        L=1;
        }
      else if(sig==LEFT_OFF && L==1){
        L=0;
        }
      if (sig==(RIGHT_ON) && R==0 && L!=1){
        R=1;
        }
      else if(sig==(RIGHT_OFF)){
        R=0;
        }
      if (sig==(HEADLIGHTS_ON) && HL==0){
        HL=1;
        }
      else if(sig==(HEADLIGHTS_OFF) && HL==1){
        HL=0;
        }
      if (sig==(BRAKE_ON) && B==0){
        B=1;
        }
      else if(sig==(BRAKE_OFF) && B==1){
        B=0;
        }
      }
//      Serial.print("BREAK");
//      Serial.println(HL);
//      Serial.println(L);
//      Serial.println(R);
//      Serial.println(HZ);
//      Serial.println(B);
//      Serial.print("BREAK");
    }

}

void lightLogic(int check, unsigned long currentMillis){
  unsigned long s_interval=5;
  unsigned long l_interval=50;
  switch(check){
    case 0://OFF
           noLights();
           break;
    case 1://HEADLIGHTS
//          Serial.print("HL");
           headlights();
           break;
    case 2://HAZARD
//          Serial.print("HZ");
           if ((unsigned long)(currentMillis-l_previousMillis)>=l_interval){
//              Serial.print("HAZARD");
              hazard();
              l_previousMillis=currentMillis;
            }
            break;
    case 3://LEFT
          if ((unsigned long)(currentMillis-l_previousMillis)>=l_interval){
//              Serial.print("LEFT");
              turn("L", ind_f, ind_R_L1, ind_R_L2,amber);
              l_previousMillis=currentMillis;
            }
            break;
    case 4://RIGHT 
          if ((unsigned long)(currentMillis-l_previousMillis)>=l_interval){
//              Serial.print("RIGHT");
              turn("R", ind_f, ind_R_R1, ind_R_R2,amber);
              l_previousMillis=currentMillis;
            }
            break;
    case 5://BRAKE
           brakeLights();
           break;
    case 6://STARTER
           if ((unsigned long)(currentMillis-s_previousMillis)>=s_interval){
            starterLights();
            s_previousMillis=currentMillis;   
           }
  }
}

//LIGHT FUNCS

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
 
void turn(String dir, int front[],int rear1[],int rear2[], uint32_t c){

  if (dir=="L"){
    if (whitecheck != 1 && HL==1){
      whitecheck = 1;
      for (int i=0; i<ELEMENTS(const_f); i++){
        strip_f_l.setPixelColor(const_f[i],halfwhite);
      }
    }
    if (lstate<ELEMENTS(ind_f)){
      uint32_t check = strip_f_l.getPixelColor(front[lstate]);
      if (check != c){
        strip_f_l.setPixelColor(front[lstate],c);
        strip_r.setPixelColor(rear1[lstate],c);
        strip_r.setPixelColor(rear2[lstate],c);                 
        }
    lstate++;
    }
    else{
      lstate=0;
      for(int i=0; i<ELEMENTS(ind_f); i++){
        strip_f_l.setPixelColor(front[i], 0, 0, 0);
        }
      for(int i=0; i<ELEMENTS(ind_f); i++){
        strip_r.setPixelColor(rear1[i], 0, 0, 0);
        strip_r.setPixelColor(rear2[i], 0, 0, 0);
        }    
    }
  strip_f_l.show();
  strip_r.show();
  }

  if(dir=="R"){
    if (whitecheck != 1 && HL == 1){
      whitecheck = 1;
      for (int i=0; i<ELEMENTS(const_f); i++){
        strip_f_r.setPixelColor(const_f[i],halfwhite);
      }
    }    
    if (lstate<ELEMENTS(ind_f)){
      uint32_t check = strip_f_r.getPixelColor(front[lstate]);
      if (check != c){
        strip_f_r.setPixelColor(front[lstate],c);
        strip_r.setPixelColor(rear1[lstate],c);
        strip_r.setPixelColor(rear2[lstate],c);                 
        }
    lstate++;
    }
    else{
      lstate=0;
      for(int i=0; i<ELEMENTS(ind_f); i++){
        strip_f_r.setPixelColor(front[i], 0, 0, 0);
        }
      for(int i=0; i<ELEMENTS(ind_f); i++){
        strip_r.setPixelColor(rear1[i], 0, 0, 0);
        strip_r.setPixelColor(rear2[i], 0, 0, 0);
        }    
    }
  strip_f_r.show();
  strip_r.show();    
  }
}

void hazard(){

    for (int i=0; i<ELEMENTS(const_f); i++){
      strip_f_l.setPixelColor(const_f[i],fullwhite);
      strip_f_r.setPixelColor(const_f[i],fullwhite);
      }
    for (int i=0; i<ELEMENTS(const_r); i++){
      strip_r.setPixelColor(const_r[i],fullred);
      }  
    if (lstate<ELEMENTS(ind_f)){
      uint32_t check = strip_f_r.getPixelColor(ind_f[lstate]);
      if (check != amber){
        strip_f_l.setPixelColor(ind_f[lstate],amber);
        strip_r.setPixelColor(ind_R_L1[lstate],amber);
        strip_r.setPixelColor(ind_R_L2[lstate],amber);
        strip_f_r.setPixelColor(ind_f[lstate],amber);
        strip_r.setPixelColor(ind_R_R1[lstate],amber);
        strip_r.setPixelColor(ind_R_R2[lstate],amber);                      
        }
    lstate++;
    }
   else{
    lstate=0;
    for(int i=0; i<ELEMENTS(ind_f); i++){
      strip_f_l.setPixelColor(ind_f[i], 0, 0, 0);
      strip_f_r.setPixelColor(ind_f[i], 0, 0, 0);
      }
    for(int i=0; i<ELEMENTS(ind_f); i++){
      strip_r.setPixelColor(ind_R_L1[i], 0, 0, 0);
      strip_r.setPixelColor(ind_R_L2[i], 0, 0, 0);
      strip_r.setPixelColor(ind_R_R1[i], 0, 0, 0);
      strip_r.setPixelColor(ind_R_R2[i], 0, 0, 0);
      }    
   }
  strip_f_l.show();
  strip_f_r.show();
  strip_r.show();  
}
void returnLights(int front[], int rear1[], int rear2[]){
  uint32_t ret_f =strip_f_r.getPixelColor(10);
  uint32_t ret_r =strip_r.getPixelColor(38);
//  Serial.print("RESETTING");
  for(int i=0; i<ELEMENTS(ind_f); i++){
    strip_f_l.setPixelColor(front[i], ret_f);
    strip_f_r.setPixelColor(front[i],ret_f);
    strip_r.setPixelColor(rear1[i], ret_r);
    strip_r.setPixelColor(rear2[i], ret_r);
  }
  strip_f_l.show();
  strip_f_l.show();
  strip_r.show();
}

void brakeLights(){
  if (HZ ==1){
    return;
  }
  if (L == 1 || R == 1){
    for(int i=0; i<ELEMENTS(const_r); i++){
      strip_r.setPixelColor(const_r[i], fullred);
    }
  strip_r.show();  
  }
  else{
    for(int i=0; i<ELEMENTS(const_r); i++){
      strip_r.setPixelColor(const_r[i], fullred);  
    }
    for(int i=0; i<ELEMENTS(ind_f); i++){
        strip_r.setPixelColor(ind_R_L1[i], fullred);
        strip_r.setPixelColor(ind_R_L2[i], fullred);
        strip_r.setPixelColor(ind_R_R1[i], fullred);
        strip_r.setPixelColor(ind_R_R2[i], fullred);        
    }
  strip_r.show();
  }
}
void starterOff(){
  int starter_F[]={0,1,2,3,4,5,6,7,8,9,10,19,18,17,16,15,14,13,20,21,22,23,24,11,12,35,34,33,32,31,30,29,28,27,26,25};
    for (int i=0; i<ELEMENTS(starter_F); i++){
      strip_s.setPixelColor(starter_F[i],0,0,0);
    }
  strip_s.show();  
}
void starterLights(){
  int starter_F[]={0,1,2,3,4,5,6,7,8,9,10,19,18,17,16,15,14,13,20,21,22,23,24,11,12,35,34,33,32,31,30,29,28,27,26,25};
//  starter_R[]={0,1,2,3,4,5,6,7,8,9,10};
//  starter_M_R[]={19,18,17,16,15,14,13};
//  starter_M_L[]={20,21,22,23,24,11,12};
//  starter_L[]={35,34,33,32,31,30,29,28,27,26,25}
  //RESET TO BLANK
  if (strip_s.getPixelColor(25)){
    for (int i=0; i<ELEMENTS(starter_F); i++){
      strip_s.setPixelColor(starter_F[i],0,0,0);
    }
  }
  else{
  //SCROLL FUNC
    if (s_counter==0){
      strip_s.setPixelColor(starter_F[0], fullred);
      strip_s.setPixelColor(starter_F[11], fullred);
      strip_s.setPixelColor(starter_F[18], fullred);
      strip_s.setPixelColor(starter_F[25], fullred);
      
    }
    if ( (s_counter< 12) && (s_counter%3) == 0){
      if (s_counter==11){
         strip_s.setPixelColor(starter_F[s_counter], fullred);
         strip_s.setPixelColor(starter_F[s_counter+10], fullred);
         s_counter=0;
         s_counter_m=0;
      }
      else {
        strip_s.setPixelColor(starter_F[s_counter], fullred);
        strip_s.setPixelColor(starter_F[s_counter_m+11], fullred);
        strip_s.setPixelColor(starter_F[s_counter_m+18], fullred);
        strip_s.setPixelColor(starter_F[s_counter+25], fullred);
        s_counter++;
        s_counter_m++;
        }
  
    }
  }
  strip_s.show();
}   

//GPS FUNC
void pingSpeed(){
    float x=1.852*GPS.speed;
    
    Serial.print(int(x));

    Serial.print('\n');
}


