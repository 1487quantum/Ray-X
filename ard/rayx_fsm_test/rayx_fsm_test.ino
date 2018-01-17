//Ray X Finite State Machine Test

bool hlt = false;         //Halt program, turn on LED pin 13
int sts = 0;              //Initial state is idle
int led = 13;

void setup() {
  pinMode(led, OUTPUT);
  Serial.begin(9600);

  for (int i = 3; i < 9; i++) {
    pinMode(i, OUTPUT);
  }
}

void state(int s) {
  switch (s) {
    case 1: //FWD
      for (int i = 3; i < 9; i++) {
        digitalWrite(i, i == 4 ? 1 : 0);

      }
      break;
    case 2: //BWD
      for (int i = 3; i < 9; i++) {
        digitalWrite(i, i == 5 ? 1 : 0);
      }
      break;
    case 3: //LFT
      for (int i = 3; i < 9; i++) {
        digitalWrite(i, i == 6 ? 1 : 0);

      }
      break;
    case 4: //RGT
      for (int i = 3; i < 9; i++) {
        digitalWrite(i, i == 7 ? 1 : 0);
      }
      break;
    case 5: //HLT
      for (int i = 3; i < 9; i++) {
        digitalWrite(i, i == 8 ? 1 : 0);
      }
      hlt = true;
      break;
    /*
      case 6: //RST
      hlt = false;
      sts = 0;
      break;
    */
    case 0: //STP/IDLE
    default:
      for (int i = 3; i < 9; i++) {
        digitalWrite(i, i == 3 ? 1 : 0);
      }
      break;
  }
}

void halt() {
  digitalWrite(led, HIGH);
  for (int i = 3; i < 8; i++) {
    digitalWrite(i, LOW);
  }
}

int dt = 0;
void loop() {
  while (Serial.available())
  {
    dt = Serial.read() - '0';
    sts = dt;
    Serial.println(dt);
  }
  if (!hlt) {
    digitalWrite(led, 0);
    state(sts);
  } else {
    halt();
  }
  delay(1);
}
