#include <Servo.h>
#include "param.h"

//Linux upload: chmod 666 to port

//Initialization
void setParams(char aLow, char aHigh , float frq, bool dir) {
  //Incase order is wrong
  if(aLow>aHigh){
    char tmp = aLow;
    aLow = aHigh;
    aHigh = tmp;
  }
  for (int i = 0; i < 2; i++) {
    aSt[i] = aSt[i] > 0 ? (i == 0 ? aLow : aHigh) : aSt[i]; //Amplitude: if a >0: set a, else default val
  }
  f = frq > 0 ? frq : 1;  //Freq: if frq >0: set frq, else default 1
  d = dir;
}

float getPercent() {
  float t = micros() % 1000000;   // 1s -> 1000000 microsecond
  return t / 1000000;             //Percent of sine in 1Hz
}

//Phase offet -> index k, sNum: NUM_SERVOS
float calPhi(int k, int sNum) {
  return 2 * PI * (k / (float) sNum);
}
//pc->percentage, ai->amplitude index (0->Low, 1-> high) , j->srv indx, dir->d
void servoOut(float pc, char ai, char j, char d) {
  out =  aSt[ai] * sin( 2 * PI * (pc) * f + d * calPhi(j, NUM_SERVOS));
  acp = aSt[ai] * (1 - WCLIP);
  out = constrain(out, -acp, acp);
  if (DEBUG) {
    Serial.print((int)out);
    if (j < NUM_SERVOS - 1)  Serial.print(",");
  }
  servosL[j].write((int)out + 90);        //Add 90 to output (Center is 90)
}

void setup() {
  setParams(10, 20, 1, 1);
  //Initialise servos
  for (int j = 9; j < 12; j++) {
    servosL[j - 9].attach(j);
    servosL[j - 9].write(90);
    delay(100);
  }
  delay(1000);  //Wait for 1s
  if (DEBUG) {
    Serial.begin(115200);
  }
}

void loop() {
  percentage = getPercent();
  for (int i = 0; i < NUM_SERVOS; i++) {  //D bool -> dir int
    servoOut(percentage, 1, i, (d == 0 ? 1 : -1));
  }
  if (DEBUG) {
    Serial.println(" ");
  }
  delay(1);
}
