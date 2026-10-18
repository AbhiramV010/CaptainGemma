#include <AccelStepper.h>
#include <Servo.h>

// Yaw stepper on pins 8, 10, 9, 11 (IN1, IN3, IN2, IN4)
AccelStepper yaw(AccelStepper::FULL4WIRE, 8, 10, 9, 11);
Servo pitchS, rollS;

const int PITCH_PIN     = 5;
const int ROLL_PIN      = 6;
const int BUZZER_PIN    = 12;    // crash alarm: beeps twice on a "C" line
const bool BUZZER_PASSIVE = false; // true for a passive buzzer (needs tone), false for active / plain signal
const int BEEP_MS       = 150;   // length of each beep and each gap
const int PITCH_NEUTRAL = 100;   // level under load, measured
const int ROLL_NEUTRAL  = 90;    // change after measuring under load
const int LIMIT         = 20;    // ±20° on every axis
const float STEPS_PER_DEG = 2048.0 / 360.0;

int pitchTarget = 0, rollTarget = 0;   // offsets in degrees from neutral
int pitchCur = 0, rollCur = 0;
long yawTargetSteps = 0;
unsigned long lastServo = 0;
String buf = "";

// Buzzer: non-blocking so the stepper keeps running. Phases 0..3 = on, off, on, off.
int beepPhase = -1;
unsigned long beepT = 0;

void buzz(bool on) {
  if (BUZZER_PASSIVE) { if (on) tone(BUZZER_PIN, 2000); else noTone(BUZZER_PIN); }
  else digitalWrite(BUZZER_PIN, on ? HIGH : LOW);
}

void startBeep() { beepPhase = 0; beepT = millis(); buzz(true); }

void updateBeep() {
  if (beepPhase < 0 || millis() - beepT < (unsigned long)BEEP_MS) return;
  beepT = millis();
  beepPhase++;
  if (beepPhase >= 4) { beepPhase = -1; buzz(false); return; }
  buzz(beepPhase % 2 == 0);
}

void parse(const String &line) {
  if (line == "C") { startBeep(); return; }   // crash: beep twice
  if (line.length() < 2) return;
  char axis = line.charAt(0);
  int v = constrain(line.substring(1).toInt(), -LIMIT, LIMIT);
  if (axis == 'Y') yawTargetSteps = lround(v * STEPS_PER_DEG);
  else if (axis == 'P') pitchTarget = v;
  else if (axis == 'R') rollTarget = v;
}

void readSerial() {
  while (Serial.available()) {
    char c = Serial.read();
    if (c == '\n') { parse(buf); buf = ""; }
    else if (c != '\r') buf += c;
  }
}

void setup() {
  Serial.begin(9600);
  yaw.setMaxSpeed(600);
  yaw.setAcceleration(150);
  yaw.setCurrentPosition(0);
  pitchS.attach(PITCH_PIN);
  rollS.attach(ROLL_PIN);
  pitchS.write(PITCH_NEUTRAL);
  rollS.write(ROLL_NEUTRAL);
  pinMode(BUZZER_PIN, OUTPUT);
  buzz(false);
  Serial.println("READY");
}

void loop() {
  readSerial();
  updateBeep();

  if (yaw.targetPosition() != yawTargetSteps) yaw.moveTo(yawTargetSteps);

  if (yaw.distanceToGo() != 0) {
    // Yaw moving: servos hold still so the 5 V rail isn't loaded twice
    yaw.enableOutputs();
    yaw.run();
  } else {
    yaw.disableOutputs();
    // Yaw idle: step the servos 1° every 15 ms toward their targets
    if (millis() - lastServo >= 15) {
      lastServo = millis();
      if (pitchCur < pitchTarget) pitchCur++;
      else if (pitchCur > pitchTarget) pitchCur--;
      if (rollCur < rollTarget) rollCur++;
      else if (rollCur > rollTarget) rollCur--;
      pitchS.write(PITCH_NEUTRAL + pitchCur);
      rollS.write(ROLL_NEUTRAL + rollCur);
    }
  }
}