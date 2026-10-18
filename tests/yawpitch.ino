#include <AccelStepper.h>
#include <Servo.h>

// Yaw stepper on pins 8, 10, 9, 11 (IN1, IN3, IN2, IN4)
AccelStepper yaw(AccelStepper::FULL4WIRE, 8, 10, 9, 11);
Servo pitch;

const int PITCH_PIN   = 5;    // yellow wire on pin 5
const int NEUTRAL     = 90;   // level
const int PITCH_UP    = 95;   // +5°
const int PITCH_DOWN  = 85;   // -5°
const int PITCH_STEPS = 20;   // 90→95→85→90 at 1° per step
const int YAW_LIMIT   = 114;  // ±20° (2048 steps per revolution)

enum Phase { YAW, PITCH };
Phase phase = YAW;
int angle = NEUTRAL;
int dir = 1;
int steps = 0;
unsigned long last = 0;

void setup() {
  Serial.begin(9600);
  yaw.setMaxSpeed(600);
  yaw.setAcceleration(150);
  yaw.moveTo(YAW_LIMIT);      // first swing: +20°

  pitch.attach(PITCH_PIN);
  pitch.write(NEUTRAL);       // reset pitch to 90 on startup
  delay(1000);
  last = millis();
}

void loop() {
  if (phase == YAW) {
    yaw.run();
    if (yaw.distanceToGo() == 0) {
      yaw.disableOutputs();   // coils off while pitch moves
      Serial.println("yaw done");
      phase = PITCH;
      angle = NEUTRAL;
      dir = 1;
      steps = 0;
      last = millis();
    }
  } else {
    if (millis() - last >= 30) {   // 1° every 30 ms
      last = millis();
      angle += dir;
      pitch.write(angle);
      steps++;

      if (angle >= PITCH_UP)   dir = -1;
      if (angle <= PITCH_DOWN) dir = 1;

      if (steps >= PITCH_STEPS) {
        pitch.write(NEUTRAL);
        Serial.println("pitch done");
        phase = YAW;
        yaw.enableOutputs();
        yaw.moveTo(-yaw.currentPosition());  // swing to -20°
      }
    }
  }
}