#include <AccelStepper.h>
#include <Servo.h>

// Stepper on pins 8, 10, 9, 11 (IN1, IN3, IN2, IN4)
AccelStepper yaw(AccelStepper::FULL4WIRE, 8, 10, 9, 11);
Servo pitch;

const int PITCH_PIN = 5;
const int PITCH_MIN = 60;    // nose down limit
const int PITCH_MAX = 120;   // nose up limit
const int PITCH_NEUTRAL = 90;

enum Phase { YAW_MOVE, PITCH_MOVE };
Phase phase = YAW_MOVE;
int pitchAngle = PITCH_NEUTRAL;
int pitchDir = 1;
unsigned long lastPitchStep = 0;

void setup() {
  Serial.begin(115200);
  yaw.setMaxSpeed(600);
  yaw.setAcceleration(150);
  pitch.attach(PITCH_PIN);
  pitch.write(PITCH_NEUTRAL);
  yaw.moveTo(512);            // start with a 90° right swing
}

void loop() {
  if (phase == YAW_MOVE) {
    yaw.run();
    if (yaw.distanceToGo() == 0) {
      yaw.disableOutputs();   // coils off while the pitch servo moves
      Serial.println("yaw done, pitch next");
      phase = PITCH_MOVE;
      pitchAngle = PITCH_NEUTRAL;
      lastPitchStep = millis();
    }
  } else {
    if (millis() - lastPitchStep >= 15) {
      lastPitchStep = millis();
      pitchAngle += pitchDir;
      pitch.write(pitchAngle);
      if (pitchAngle >= PITCH_MAX) pitchDir = -1;
      if (pitchAngle <= PITCH_MIN) {
        pitchDir = 1;
        // one full up/down pass done, swing yaw the other way
        yaw.enableOutputs();
        yaw.moveTo(-yaw.currentPosition());
        phase = YAW_MOVE;
      }
    }
  }
}