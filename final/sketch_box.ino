#include <Servo.h>
#include <MD_Parola.h>
#include <MD_MAX72xx.h>
#include <SPI.h>
#include <ezButton.h>

#define HARDWARE_TYPE MD_MAX72XX::FC16_HW
// #define HARDWARE_TYPE MD_MAX72XX::GENERIC_HW

#define MAX_DEVICES 4
#define CS_PIN 10

int servo_pin = 4;
int outside = 0;
int charge = 0;
int rotate = 0;
ezButton limitSwitch(7);
Servo first_servo;
MD_Parola myDisplay = MD_Parola(HARDWARE_TYPE, CS_PIN, MAX_DEVICES);

void setup() {
  Serial.begin(9600);
  limitSwitch.setDebounceTime(50);
  first_servo.attach(servo_pin);
  myDisplay.begin();
  myDisplay.setIntensity(4);
  myDisplay.displayClear();
}

void openGates(){
  first_servo.write(135);
}

void closeGates(){
  first_servo.write(0);
}


void loop() {
  limitSwitch.loop();
  if (charge == 1) {
    first_servo.write(130);
    delay(1000);
    first_servo.write(0);
    delay(1000);
    Serial.println(first_servo.read());
    myDisplay.print("I&C");
    // При нажатии будет гореть Inside после 5 секунд загорается Charge
  }
  if (outside == 0){
    Serial.println("Open");
    // first_servo.write(0);
    myDisplay.setTextAlignment(PA_LEFT);
    myDisplay.print("Open");
  }


  if(limitSwitch.isPressed()) {
    Serial.println("Inside");
    Serial.println("Charging");
    outside = 1;
    charge = 1;
  }

  if(limitSwitch.isReleased()) {
    Serial.println("Inside");
    charge = 0;
    outside = 0;
  }
  if (myDisplay.displayAnimate()) {
    myDisplay.displayReset();
  }
}
