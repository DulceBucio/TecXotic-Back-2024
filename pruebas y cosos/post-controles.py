# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import requests  # Import the requests library

RANGE = 1000
NEUTRAL = 0
THROTTLE_RANGE = 500
NEUTRAL_THROTTLE = 500


counter = 0


arduino = 0
throttle = 500,
roll = 0
pitch = 0
yaw = 0
arm_disarm = True

mode = 'MANUAL'

safeZone = 0.012

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
    return data


def post(commands):
    #response = requests.post('http://192.168.5.1:8080/postControlMovement', json=commands)
    print(commands)


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
    return data

def handle_hat_motion(joystick):
    print("JoyStick izquierdo manipulado. Valor: {}".format(joystick.get_hat(0)))
    value_x = joystick.get_hat(0)[0]
    value_y = joystick.get_hat(0)[1]
    data = {'button_name': "modo", 'value_x': value_x, 'value_y': value_y}
    return data

def main():
    pygame.init()
    pygame.joystick.init()
    if pygame.joystick.get_count() == 0:
        print("No se detectaron controles de videojuegos.")
        return
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    mode = 'MANUAL' #Inicializa el modo de vuelo en MANUAL
    try:
        while True:
            commands = { #Cada while se reinicia el diccionario de comandos
                'throttle': 500,
                'roll': 0,
                'pitch': 0,
                'yaw': 0,
                'arm_disarm': True,
                'mode': mode,
                'arduino': 0,
            }                   
            for event in pygame.event.get(): #Cada que se detecta un evento en el control modificamos los comandos
                if event.type == JOYAXISMOTION:
                    data = handle_axis_motion(event, joystick)
                    if data['button_name'] == "JoyStick izquierdo": 
                        lx = data['value_x']
                        ly = data['value_y']
                        #commands['pitch'] = 1 #calculate_potency(-ly, trigger, power_limit_ref) if ly > safeZone or ly < -safeZone else NEUTRAL
                        #commands['roll'] = 1 #calculate_potency(lx, trigger, power_limit_ref) if lx > safeZone or lx < -safeZone else NEUTRAL

                    elif data['button_name'] == "JoyStick derecho":
                        rx = data['value_x']
                        ry = data['value_y']
                        commands['arduino'] = 5            
    
                    '''    
                    elif event.type == JOYBUTTONDOWN:
                        handle_button_down(event)
                    '''


                elif event.type == JOYBUTTONUP:
                    data = handle_button_up(event)
                    if(data['button_name'] == "A"):
                        commands['arduino'] = 1
                    elif(data['button_name'] == "B"):
                        commands['arduino'] = 4
                    elif(data['button_name'] == "X"):
                        commands['arduino'] = 3
                    elif(data['button_name'] == "Y"):
                        commands['arduino'] = 2
                    

                    
                elif event.type == JOYHATMOTION:
                    data = handle_hat_motion(joystick)
                    if(data['value_x'] == 1 and data['value_y'] == 0):
                        mode = 'MANUAL'
                    elif(data['value_x'] == 0 and data['value_y'] == 1):
                        mode = 'STABILIZE'
                    elif(data['value_x'] == 0 and data['value_y'] == -1):
                        mode = 'ACRO'

                
                post(commands)


    except KeyboardInterrupt:
        print("\nSaliendo del programa.")
        pygame.quit()

if __name__ == "__main__":
    if counter == 0:
        commands = { #Cada while se reinicia el diccionario de comandos
            'throttle': 500,
            'roll': 0,
            'pitch': 0,
            'yaw': 0,
            'arm_disarm': True,
            'mode': mode,
            'arduino': 0,
        }   
        print("Iniciando programa.")
        print(commands )
        post(commands)
        counter += 1
    main()





