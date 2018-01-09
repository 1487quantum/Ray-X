#include <Servo.h>
#define DEBUG 1
//Var
int alp = 80;             //Max Range
float amp = 0;            //Constrained max range
int f = 1;                //Frequency

bool k = 0;               //Motion Mode (0:straight, 1:inclined)
bool d = 0;               //Direction (0: Straight (1), 1: Backwards (-1))
float g = 0.00;           //Inclination coefficient

float out = 0;            //Servo output

float percentage;

//Servo
#define NUM_SERVOS 3
#define SMAX 80           //Maximum servo range

//Left
Servo servObj0;
Servo servObj1;
Servo servObj2;
//Right
Servo servObj3;
Servo servObj4;
Servo servObj5;

Servo servosL[] = {servObj0, servObj1, servObj2};
//Servo servosR[] = {servObj3, servObj4, servObj5};

//#define NUM_SERVOS (sizeof(servosL) / sizeof(Servo))


void setParams(int a, int frq, bool dir, bool m_mode, float inc) {
  alp = a > 0 ? a : 80;   //Amplitude: if a >0: set a, else default 80
  f = frq > 0 ? frq : 1;  //Freq: if frq >0: set frq, else default 1
  d = dir;
  k = m_mode;
  g = k ? inc : 1; //if k==1: incline, else straight
}

float calCAmp() {
  //Get constrained amplitude
  return constrain((float) alp / (1 + g * k), 0, SMAX);
}

float getPercent() {
  float t = micros() % 1000000;  // time
  return t / 1000000;   //Percent of sine
}

//Phase offet -> index k, sNum: NUM_SERVOS
float calPhi(int k, int sNum) {
  return 2 * PI * (k / (float) sNum);
}

//Calculate center offset -> j:index, dr:dir
float calCenter(int j, int dr) {
  return g * (alp / 2) * (1 - j) * (dr * k);
}

//pc->percentage, j->srv indx, dir->d
void servoOut(float pc, int j, int d) {
  out =  amp * sin( 2 * PI * (pc) * f + d*calPhi(j, NUM_SERVOS)) + calCenter(j, d);
  if (DEBUG) {
    Serial.print(out);
    if (j < NUM_SERVOS - 1)  Serial.print(",");
  }
  servosL[j].write((int)out + 90);  //Add 90 to output (Center is 90)
}

void setup() {
  setParams(25, 1, 0, 1, 1);
  //Initialise servos
  for (int j = 9; j < 12; j++) {
    servosL[j - 9].attach(j);
    servosL[j - 9].write(90);
    delay(1000);
  }
  delay(1000);  //Wait for 1s
  amp = calCAmp();
  if (DEBUG) {
    Serial.begin(115200);
  }
}

void loop() {
  percentage = getPercent();
  for (int i = 0; i < NUM_SERVOS; i++) {  //D bool -> dir int
    servoOut(percentage, i, (d == 0 ? 1 : -1));
  }
  if (DEBUG) {
    Serial.println(" ");
  }
  delay(1);
}
