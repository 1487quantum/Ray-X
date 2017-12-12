#include <Servo.h>

//Var
int alp = 80;           //Max Range
float amp = 0;            //Final max range
int f = 1;             //Frequency
float phi = 0;       //Phase offet
float t = 0;              //Time t

float b = 0;              //Center offset
bool k = 0;             //Motion Mode (0:straight, 1:inclined)
bool d = 0;             //Direction (0: Straight (1), 1: Backwards (-1))
float g = 0.00;         //Inclination coefficient

float out = 0;            //Servo output

//Servo
const int sMax = 80;    //Maximum servo range
Servo servObj0;  // create servo object to control a servo
Servo servObj1;  // create servo object to control a servo
Servo servObj2;  // create servo object to control a servo

Servo servosL[] = {servObj0, servObj1, servObj2};
#define NUM_SERVOS (sizeof(servosL) / sizeof(Servo))

int pos = 0;    // variable to store the servo position

void setup() {
  alp = 25;
  f=1;
  k = 0;
  if (k) {
    //Only used when in incline mode
    g = 1;
    d = 0;
  }
  //Initialise servo
  for (int j = 9; j < 12; j++) {
    servosL[j - 9].attach(j);
    servosL[j - 9].write(90);
    delay(1000);
  }
  delay(1000);  //Wait for 1s
  //Get final amplitude
  amp = (float) alp / (1 + g * k);
  amp = constrain(amp, 0, sMax);  //Constrain final amplitude
  Serial.begin(115200);
}

void loop() {
  t = micros() % 1000000;
  float percentage = t / 1000000;   //Percent of sine

  for (int i = 0; i < NUM_SERVOS; i++) {
    phi =  2 * PI * (i / (float)NUM_SERVOS);
    // Serial.print(phi);
    b = g * (alp / 2) * (1 - i) * ((d == 0 ? 1 : -1) * k) ;
    // Serial.print(b);
    out = amp * sin( 2 * PI * (percentage) * f + phi) + b;
    Serial.print(out);

    if (i < NUM_SERVOS - 1)  Serial.print(",");

    //Add 90 to output
    servosL[i].write((int)out + 90);

    /*
      float time = micros() % 1000000;
      float percentage = time / 1000000;
      float templitude = sin(((percentage) * freq) * 2 * PI);
     * */

  }
  Serial.println(" ");
  delay(1);
}

