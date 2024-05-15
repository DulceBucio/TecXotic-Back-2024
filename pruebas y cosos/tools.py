import pygame
from pygame.locals import *
import requests

# Constants
RANGE = 1000
NEUTRAL = 0
THROTTLE_RANGE = 500
NEUTRAL_THROTTLE = 500

# Initial values
throttle = 500
roll = 0
pitch = 0
yaw = 0
arm_disarm = True
mode = 'MANUAL'
safeZone = 0.012
power_limit_ref = 1

def calculate_potency(joystick, trigger):
    temp_power_limit = power_limit_ref if not trigger else 1.0
    return int(joystick * RANGE * temp_power_limit)

def calculate_throttle_potency(joystick, trigger):
    temp_power_limit = power_limit_ref if not trigger else 1.0
    return int((-joystick * THROTTLE_RANGE) * temp_power_limit + NEUTRAL_THROTTLE)

def post_actuator_data(commands):
    url_actuators = 'http://192.168.5.1:8080/actuators'
    try:
        response_actuators = requests.post(url_actuators, json=commands)
        print("Data sent to actuators. Status code:", response_actuators.status_code)
        if response_actuators.status_code != 200:
            print("Error from server:", response_actuators.text)
    except requests.exceptions.RequestException as e:
        print("Failed to send data to actuators:", e)

def handle_button_down(event):
    button_names = ["A", "B", "X", "Y", "LB", "RB", "LT", "RT", "Select", "Start"]
    if event.button < len(button_names):
        button_name = button_names[event.button]
        data = {'button_name': button_name, 'value': event.button}
        print(f"Button {button_name} pressed.")
        post_actuator_data({'actions': str(event.button)})
    else:
        print(f"Button {event.button} pressed.")

def handle_hat_motion(hat_value):
    if hat_value[0] == -1:  # Left roll
        post_actuator_data({'actions': 'LEFTROLL'})
        print("Rolling Left...")
    elif hat_value[0] == 1:  # Right roll
        post_actuator_data({'actions': 'RIGHTROLL'})
        print("Rolling Right...")
    elif hat_value[1] == 1:  # Up (adjust action if needed)
        post_actuator_data({'actions': 'UP'})  # Example: Adjust if you have 'UP' action
        print("Moving Up...")
    elif hat_value[1] == -1:  # Down (adjust action if needed)
        post_actuator_data({'actions': 'DOWN'})  # Example: Adjust if you have 'DOWN' action
        print("Moving Down...")

def main():
    pygame.init()
    pygame.joystick.init()
    
    if pygame.joystick.get_count() == 0:
        print("No joysticks detected.")
        return

    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    try:
        while True:
            for event in pygame.event.get():
                if event.type == JOYBUTTONDOWN:
                    handle_button_down(event)
                elif event.type == JOYHATMOTION:
                    handle_hat_motion(event.value)

    except KeyboardInterrupt:
        print("\nExiting the program.")
    finally:
        pygame.quit()

if __name__ == "__main__":
    print("Starting joystick control program.")
    main()
