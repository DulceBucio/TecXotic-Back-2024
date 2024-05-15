#include <Servo.h>

Servo servoRoll;  // Create a servo object to control a servo

const int LEFTROLL = 1;
const int RIGHTROLL = 2;
const int STOP = 0;  // Command to stop the movement

int currentCommand = STOP;  // Current command being executed

void setup() {
  Serial.begin(9600);  // Start serial communication at 9600 baud
  servoRoll.attach(12);  // Attaches the servo on pin 12 to the servo object
}

void loop() {
  if (Serial.available() > 0) {
    // Read the next command from serial input
    int command = Serial.parseInt();
    // If a new command is received, update the current command
    if (command == LEFTROLL || command == RIGHTROLL || command == STOP) {
      currentCommand = command;
    }
  }

  // Execute the current command
  switch (currentCommand) {
    case LEFTROLL:
      servoRoll.writeMicroseconds(1300); // Rotate left, adjust as needed for your servo
      break;
    case RIGHTROLL:
      servoRoll.writeMicroseconds(1700); // Rotate right, adjust as needed for your servo
      break;
    case STOP:
      servoRoll.writeMicroseconds(1500); // Stop rotation
      break;
  }
}
