#include <Servo.h>

Servo servoRoll;  // Servo para el roll
Servo servoClaw;  // Servo para la garra
int servoAngle = 90;

void setup() {
  Serial.begin(9600);
  servoRoll.attach(7);  // Pin 9 para el servoRoll
  servoClaw.attach(6); // Pin 10 para el servoClaw
}

void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n'); // Read the incoming data as string until newline
    int commandInt = command.toInt(); // Convert the string to integer

    switch (commandInt) {
      case 1:
        servoRoll.write(180); // Mover el servo a 180 grados
        break;
      case 2:
        servoRoll.write(0); // Mover el servo a 0 grados
        break;
      case 3:
        servoClaw.write(15); // dpad up
        break;
      case 4:
        servoClaw.write(23); // dpad down (open)
        break;
      case 5:
        servoClaw.write(0);
      default:
        break;
    }
  }
}