import pygame
from pygame.locals import *
import requests

API_BASE_URL = 'http://192.168.5.1:8080'  # Base URL of your Flask API

# Function to send control signals for movement
def send_movement(roll, pitch, yaw, throttle):
    data = {
        'roll': roll,
        'pitch': pitch,
        'yaw': yaw,
        'throttle': throttle
    }
    response = requests.post(f'{API_BASE_URL}/control/movement', json=data)
    print("Movement command response:", response.json())

# Function to send control signals for mode change
def send_mode_change(mode):
    data = {'mode': mode}
    response = requests.post(f'{API_BASE_URL}/control/mode', json=data)
    print("Mode change response:", response.json())

# Function to send control signals for arming/disarming
def send_arm_disarm(arm):
    data = {'arm': arm}
    response = requests.post(f'{API_BASE_URL}/control/arming', json=data)
    print("Arming command response:", response.json())

# Modify your existing event handling functions to use these new functions
# Example for handling joystick axis motion
def handle_axis_motion(event, joystick):
    # Here, you would calculate your roll, pitch, yaw, throttle values based on the joystick input
    # Example values, replace with actual calculations
    roll, pitch, yaw, throttle = 0, 0, 0, 500
    send_movement(roll, pitch, yaw, throttle)

# Example for handling button press for mode change
def handle_button_down(event):
    # Determine the mode based on the button pressed
    # This is just an example, adjust according to your application logic
    mode = 'MANUAL'
    if event.button == 0:  # Assuming button 0 switches to MANUAL mode
        mode = 'MANUAL'
    send_mode_change(mode)

# Add similar handlers for arming/disarming and other controls

# Your main loop and joystick initialization remain largely unchanged
def main():
    pygame.init()
    pygame.joystick.init()

    if pygame.joystick.get_count() == 0:
        print("No se detectaron controles de videojuegos.")
        return

    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    try:
        while True:
            for event in pygame.event.get():
                if event.type == JOYAXISMOTION:
                    handle_axis_motion(event, joystick)
                elif event.type == JOYBUTTONDOWN:
                    handle_button_down(event)
                elif event.type == JOYBUTTONUP:
                    handle_button_up(event)
                elif event.type == JOYHATMOTION:
                    handle_hat_motion(joystick)

    except KeyboardInterrupt:
        print("\nSaliendo del programa.")
        pygame.quit()

if __name__ == "__main__":
    main()