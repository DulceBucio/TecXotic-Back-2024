import pygame
from pygame.locals import *
import requests

# Constants for servo control
SERVO_MIN = 0
SERVO_MAX = 180
SERVO_MID = 90
servo_position = SERVO_MID  # Start at the midpoint

# Define the step size for each joystick movement
STEP_SIZE = 90  # Adjust this value to control the movement speed

# Function to send servo position to the Arduino
def post_servo_position(position):
    url = 'http://192.168.5.1:8080/actuators'
    try:
        # Ensure the position is sent as a string
        response = requests.post(url, json={"actions": str(position)})
        print("Data sent to actuators. Status code:", response.status_code)
        if response.status_code != 200:
            print("Error from server:", response.text)
    except requests.exceptions.RequestException as e:
        print("Failed to send data to actuators:", e)

def handle_hat_motion(hat_value):
    global servo_position
    
    if hat_value[0] == -1:  # Left roll
        servo_position -= STEP_SIZE
        if servo_position < SERVO_MIN:
            servo_position = SERVO_MAX - (SERVO_MIN - servo_position - 1) % (SERVO_MAX + 1)
        post_servo_position(servo_position)
        print(f"Rolling Left to {servo_position}...")
        
    elif hat_value[0] == 1:  # Right roll
        servo_position += STEP_SIZE
        if servo_position > SERVO_MAX:
            servo_position = SERVO_MIN + (servo_position - SERVO_MAX - 1) % (SERVO_MAX + 1)
        post_servo_position(servo_position)
        print(f"Rolling Right to {servo_position}...")

def main():
    pygame.init()
    pygame.joystick.init()
    
    # Check if there are any joysticks connected
    if pygame.joystick.get_count() == 0:
        print("No joysticks detected.")
        return

    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    try:
        while True:
            pygame.event.pump()
            for event in pygame.event.get():
                if event.type == JOYBUTTONDOWN:
                    # Check for Select button; adjust '6' if needed based on your controller
                    if event.button == 6:  # Often the 'Select' button
                        print("Select button pressed - Resetting servo position")
                        servo_position = SERVO_MID
                        post_servo_position(servo_position)
                    else:
                        print(f"Button {event.button} pressed")
                
                elif event.type == JOYHATMOTION:
                    handle_hat_motion(event.value)

            pygame.time.wait(100)

    except KeyboardInterrupt:
        print("\nExiting the program.")
    finally:
        pygame.quit()

if __name__ == "__main__":
    print("Starting joystick control program.")
    main()
