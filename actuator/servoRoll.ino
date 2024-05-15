#include <Servo.h>

Servo servoRoll;  // Create a servo object
Servo servoClaw;

// This will store the angle for the servo
int servoAngle = 0;  // Start at the midpoint, 90 degrees

void setup() {
  Serial.begin(9600);  
  servoRoll.attach(7);  // Attach servo on pin 12
  servoClaw.attach(6); 
}

void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n'); // Read the incoming data as string until newline
    servoAngle = command.toInt(); // Convert the string to integer
    servoRoll.write(servoAngle);  // Set the servo position
  }

  delay(15);  // Small delay to prevent overwhelming the servo
}