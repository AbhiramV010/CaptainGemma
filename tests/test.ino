#include <Servo.h>

Servo pitch;

void setup() {
  Serial.begin(115200);
  pitch.attach(6);
  pitch.write(90);
  delay(1000);
  Serial.println("Pitch sweep start");
}

void loop() {
  for (int a = 30; a <= 150; a++) { pitch.write(a); delay(15); }
  for (int a = 150; a >= 30; a--) { pitch.write(a); delay(15); }
}