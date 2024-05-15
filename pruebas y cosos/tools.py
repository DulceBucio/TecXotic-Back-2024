import pygame
from pygame.locals import *
import requests

# Constants for servo control
SERVO_MIN = 0
SERVO_MAX = 180
SERVO_MID = 90

# Initial positions
servo_roll_position = SERVO_MID  # Start at the midpoint for the roll servo
servo_claw_position = SERVO_MID  # Start at the midpoint for the claw servo

# Define the step size for finer movements of the claw
CLAW_STEP_SIZE = 5
ROLL_STEP_SIZE = 90

# Function to send servo position to the Arduino
def post_servo_position(roll_position, claw_position):
    url = 'http://192.168.5.1:8080/actuators'
    try:
        # Ensure the positions are sent as strings
        response = requests.post(url, json={"roll": str(roll_position), "claw": str(claw_position)})
        print("Data sent to actuators. Status code:", response.status_code)
        if response.status_code != 200:
            print("Error from server:", response.text)
    except requests.exceptions.RequestException as e:
        print("Failed to send data to actuators:", e)

def handle_hat_motion(hat_value):
    global servo_roll_position, servo_claw_position
    
    # Handle left/right for roll servo
    if hat_value[0] == -1:  # Left roll
        if servo_roll_position == SERVO_MIN:
            servo_roll_position = SERVO_MAX
        elif servo_roll_position == SERVO_MID:
            servo_roll_position = SERVO_MIN
        elif servo_roll_position == SERVO_MAX:
            servo_roll_position = SERVO_MID
    elif hat_value[0] == 1:  # Right roll
        if servo_roll_position == SERVO_MIN:
            servo_roll_position = SERVO_MID
        elif servo_roll_position == SERVO_MID:
            servo_roll_position = SERVO_MAX
        elif servo_roll_position == SERVO_MAX:
            servo_roll_position = SERVO_MIN
    
    # Handle up/down for claw servo
    if hat_value[1] == 1:  # Up
        servo_claw_position += CLAW_STEP_SIZE
        if servo_claw_position > SERVO_MAX:
            servo_claw_position = SERVO_MAX
    elif hat_value[1] == -1:  # Down
        servo_claw_position -= CLAW_STEP_SIZE
        if servo_claw_position < SERVO_MIN:
            servo_claw_position = SERVO_MIN

    post_servo_position(servo_roll_position, servo_claw_position)
    print(f"Roll Position: {servo_roll_position}, Claw Position: {servo_claw_position}...")

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
                        print("Select button pressed - Resetting positions")
                        servo_roll_position = SERVO_MID
                        servo_claw_position = SERVO_MID
                        post_servo_position(servo_roll_position, servo_claw_position)
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
