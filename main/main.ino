#include <Stepper.h>

const int STPRVLUTN = 2038;  // change this to fit the number of steps per revolution
// for your motor

long int waitS = 24*60*60*1000 //One day
long int startT; 

// initialize the stepper library on pins 8 through 11:
Stepper myStepper(STPRVLUTN, 8, 9, 10, 11);

void setup() {
  // set the speed at 60 rpm:
  myStepper.setSpeed(6);

  startT = millis();
}

void loop() {
  // Start timer
  if (millis() - startT >= (wait){
    myStepper.step(degreesToSteps(160));

    digitalWrite(8, LOW);
    digitalWrite(9, LOW);
    digitalWrite(10, LOW);
    digitalWrite(11, LOW);

    startT = millis();
  }
}

long int degreesToSteps(int degree){
  return (long int) STPRVLUTN*degree/360;
}
