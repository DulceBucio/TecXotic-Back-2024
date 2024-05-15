import pygame
from pygame.locals import *
import requests

# Constants for servo control
SERVO_MIN = 0
SERVO_MAX = 180
SERVO_MID = (SERVO_MAX + SERVO_MIN) // 2  # Correct midpoint calculation
servo_position = SERVO_MID  # Start at the midpoint

# Define the step size for each joystick movement
STEP_SIZE = 45  # Adjust this value to control the movement speed

# Function to send servo position to the Arduino
def post_actuator_data(position):
    url = 'http://192.168.5.1:8080/actuators'
    try:
        # Ensure the position is sent as a string or as a dictionary directly
        data = {"actions": position} if isinstance(position, str) else {"actions": str(position)}
        response = requests.post(url, json=data)
        print("Data sent to actuators. Status code:", response.status_code)
        if response.status_code != 200:
            print("Error from server:", response.text)
    except requests.exceptions.RequestException as e:
        print("Failed to send data to actuators:", e)

# Function to handle hat motion events and send roll commands
def handle_hat_motion(joystick):
    value_x, value_y = joystick.get_hat(0)
    data = {'button_name': "DPad", 'value_x': value_x, 'value_y': value_y}

    # Define commands for left and right rolls
    if value_x == -1:  # Left roll
        post_actuator_data('LEFTROLL')
    elif value_x == 1:  # Right roll
        post_actuator_data('RIGHTROLL')
    elif value_y == -1 and value_x == 0:
        post_actuator_data('CLAW_OPEN')
    elif value_y == 1 and value_x == 0:
        post_actuator_data('CLAW_MIDOPEN')

    return data

def main():
    global servo_position

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
                    if event.button == 6:  # 'Select' button
                        print("Select button pressed - Resetting servo position")
                        servo_position = 0
                        post_actuator_data(servo_position)
                    elif event.button == 7:  # 'Start' button
                        print("Start button pressed - Resetting servo position")
                        servo_position = 180
                        post_actuator_data('CLAW_CLOSE')
                    else:
                        print(f"Button {event.button} pressed")
                
                elif event.type == JOYHATMOTION:
                    handle_hat_motion(joystick)  # Pass joystick, not event.value

            pygame.time.wait(100)

    except KeyboardInterrupt:
        print("\nExiting the program.")
    finally:
        pygame.quit()

if __name__ == "__main__":
    post_actuator_data(servo_position)
    print("Starting joystick control program.")
    main()
