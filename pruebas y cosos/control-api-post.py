# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import requests  # Import the requests library

# Function to handle joystick axis motion
def handle_axis_motion(event, joystick):
    axis_names = {
        0: "boton movimiento",
        1: "boton movimiento",
        2: "JoyStick derecho",
        3: "JoyStick derecho",
        4: "Gatillo izquierdo",
        5: "Gatillo derecho"
    }
    axis_name = axis_names.get(event.axis, "")
    value = joystick.get_axis(event.axis)
    print("Eje {} manipulado. Valor: {}".format(axis_name, value))

    # Construct the data to be sent
    data = {'axis_name': axis_name, 'value': value}

    # Send a POST request to the Flask API
    try:
        response = requests.post('http://192.168.5.1:5000/postControlMovement', json=data)
        print("Data sent to API. Status code:", response.status_code)
    except Exception as e:
        print("Failed to send data to API:", e)

# The remaining functions and main loop remain unchanged
def handle_button_down(event):
    button_names = ["A", "B", "X", "Y", "LB", "RB"]
    button_name = button_names[event.button] if event.button < len(button_names) else str(event.button)
    print("Boton {} presionado.".format(button_name))

def handle_button_up(event):
    button_names = ["A", "B", "X", "Y", "LB", "RB"]
    button_name = button_names[event.button] if event.button < len(button_names) else str(event.button)
    print("Boton {} liberado. Valor: {}".format(button_name, event.button))

def handle_hat_motion(joystick):
    print("JoyStick izquierdo manipulado. Valor: {}".format(joystick.get_hat(0)))

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
