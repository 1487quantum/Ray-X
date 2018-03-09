
#define DEBUG 1                 //Enable debug log msgs

#define NUM_SERVOS 3
#define SMAX 80                //Max servo range
#define WCLIP 0.20             //How much % to clip wave (0.0~0.8)
#define ANGLES_LENGTH 60       //

//Var
char aSt[2] = {40, 80};         //Default preset amplitude value if none define, Index: 0->low, 1 -> high
char amp = 0;                   //Output amplitude (angle)
float f = 1.4;                  //Frequency
bool d = 0;                     //Direction (0: Straight (1), 1: Backwards (-1))

//Used char instead of int as it's smaller & range is within -128<->127
char out = 0;                    //Servo output
char acp = 0;                  //Amp clipping

float percentage;               //For wave generation timing

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

