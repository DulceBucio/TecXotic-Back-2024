import pygame
from pygame.locals import *
import requests

# Constants
RANGE = 1000
NEUTRAL = 0
THROTTLE_RANGE = 500
NEUTRAL_THROTTLE = 500

# Initial values
counter = 0
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
    except requests.exceptions.RequestException as e:
        print("Failed to send data to actuators:", e)

def handle_axis_motion(event, joystick):
    axis_names = {
        0: "JoyStick izquierdo",
        1: "JoyStick izquierdo",
        2: "JoyStick derecho",
        3: "JoyStick derecho", 
    }
    axis_name = axis_names.get(event.axis, "")
    value_x = joystick.get_axis(0 if axis_name == "JoyStick izquierdo" else 2)
    value_y = joystick.get_axis(1 if axis_name == "JoyStick izquierdo" else 3)
    
    data = {'button_name': axis_name, 'value_x': value_x, 'value_y': value_y}
    return data

def handle_button_down(event):
    button_names = ["A", "B", "X", "Y", "LB", "RB"]
    button_name = button_names[event.button] if event.button < len(button_names) else str(event.button)
    data = {'button_name': button_name, 'value': event.button}
    post_actuator_data(data)

def handle_button_up(event):
    button_names = ["A", "B", "X", "Y", "LB", "RB"]
    button_name = button_names[event.button] if event.button < len(button_names) else str(event.button)
    data = {'button_name': button_name, 'value': event.button}
    return data

def handle_hat_motion(joystick):
    value_x = joystick.get_hat(0)[0]
    value_y = joystick.get_hat(0)[1]

    if value_x == -1:  # Left roll
        post_actuator_data({'actions': 'LEFTROLL'})
    elif value_x == 1:  # Right roll
        post_actuator_data({'actions': 'RIGHTROLL'})

def main():
    pygame.init()
    pygame.joystick.init()
    
    if pygame.joystick.get_count() == 0:
        print("No se detectaron controles de videojuegos.")
        return

    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    mode = 'MANUAL'  # Initialize the flight mode in MANUAL
    trigger = False

    try:
        while True:
            commands = {
                'throttle': 500,
                'roll': 0,
                'pitch': 0,
                'yaw': 0,
                'arm_disarm': True,
                'mode': mode,
                'arduino': 0,
            }
            for event in pygame.event.get():
                if event.type == JOYAXISMOTION:
                    data = handle_axis_motion(event, joystick)
                    lx, ly, rx, ry = 0, 0, 0, 0
                    if data['button_name'].startswith("JoyStick izquierdo"):
                        lx, ly = data['value_x'], data['value_y']
                    elif data['button_name'].startswith("JoyStick derecho"):
                        rx, ry = data['value_x'], data['value_y']

                    commands['pitch'] = calculate_potency(-ly, trigger) if abs(ly) > safeZone else NEUTRAL
                    commands['roll'] = calculate_potency(lx, trigger) if abs(lx) > safeZone else NEUTRAL
                    commands['yaw'] = calculate_potency(rx, trigger) if abs(rx) > safeZone else NEUTRAL
                    if abs(ry) > safeZone:
                        commands['throttle'] = calculate_throttle_potency(ry, trigger)

                elif event.type == JOYBUTTONUP:
                    handle_button_up(event)

                elif event.type == JOYBUTTONDOWN:
                    handle_button_down(event)

                elif event.type == JOYHATMOTION:
                    handle_hat_motion(joystick)

    except KeyboardInterrupt:
        print("\nSaliendo del programa.")
        pygame.quit()

if __name__ == "__main__":
    if counter == 0:
        commands = {
            'throttle': 500,
            'roll': 0,
            'pitch': 0,
            'yaw': 0,
            'arm_disarm': True,
            'mode': mode,
            'arduino': 0,
            'imu': True
        }
        print("Iniciando programa.")
        print(commands)
        counter += 1
    main()
