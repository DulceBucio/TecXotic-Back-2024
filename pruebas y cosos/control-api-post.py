# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import requests  # Import the requests library

# Function to handle joystick axis motion
def handle_axis_motion(event, joystick):
    #print("Axis motion:", event.axis, "Value:", event.value)
    axis_names = {
        0: "JoyStick izquierdo",
        1: "JoyStick izquierdo",
        2: "JoyStick derecho",
        3: "JoyStick derecho", 
    }
    axis_name = axis_names.get(event.axis, "")
    if axis_name == "JoyStick izquierdo":
        value_x = joystick.get_axis(0)
        value_y = joystick.get_axis(1)
    elif axis_name == "JoyStick derecho":
        value_x = joystick.get_axis(2)
        value_y = joystick.get_axis(3)
        
    data = {'button_name': axis_name, 'value_x': value_x, 'value_y': value_y}
    post(data)


def post(data):
    print(data)
    '''
    try:
        response = requests.post('http://192.168.5.1:8080/postControlMovement', json=data)
        print("Data sent to API. Status code:", response.status_code)
    except Exception as e:
        print("Failed to send data to API:", e)
        '''


# The remaining functions and main loop remain unchanged
def handle_button_down(event):
    button_names = ["A", "B", "X", "Y", "LB", "RB"]
    button_name = button_names[event.button] if event.button < len(button_names) else str(event.button)
    data = {'button_name': button_name, 'value': event.button}
    post(data)

def handle_button_up(event):
    button_names = ["A", "B", "X", "Y", "LB", "RB"]
    button_name = button_names[event.button] if event.button < len(button_names) else str(event.button)
    data = {'button_name': button_name, 'value': event.button}
    post(data)

def handle_hat_motion(joystick):
    #print("JoyStick izquierdo manipulado. Valor: {}".format(joystick.get_hat(0)))
    data = {'button_name': "modo", 'value_x': joystick.get_hat(0)[0], 'value_y': joystick.get_hat(0)[1]}

    post(data)

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