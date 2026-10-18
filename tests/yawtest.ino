#include <AccelStepper.h>

// FULL4WIRE takes the pins in coil order: IN1, IN3, IN2, IN4
AccelStepper yaw(AccelStepper::FULL4WIRE, 8, 10, 9, 11);

void setup() {
  yaw.setMaxSpeed(600);      // steps/s
  yaw.setAcceleration(150);
  yaw.moveTo(512);           // 90° right
}

void loop() {
  if (yaw.distanceToGo() == 0) {
    yaw.moveTo(-yaw.currentPosition());  // swing back the other way
  }
  yaw.run();
}