import pygame
import requests  # Add this import at the beginning of your Pygame script

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
    response = requests.post('http://192.168.5.1/postControlMovement', json=data)
    print(response.text)
