# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *


#Aqui básicamente se define la función para poder manejar/manipular el eje por medio de sus movimientos:
def handle_axis_motion(event, joystick):
    #Aqui defino el nombre de los ejes de acuerdo a su respectivo número
    axis_names = {
        0: "boton movimiento",
        1: "boton movimiento",
        2: "JoyStick derecho",
        3: "JoyStick derecho",
        4: "Gatillo izquierdo",
        5: "Gatillo derecho"
    }
    #Aqui obtengo el nombre del eje
    axis_name = axis_names.get(event.axis, "")
    #Aqui se imprime el evento del movimiento del eje con su valor predefinido
    print("Eje {} manipulado. Valor: {}".format(axis_name, joystick.get_axis(event.axis)))

#Esta es la función para manjear los eventos de los botones presionados
def handle_button_down(event):
    #lista de los botonos que tiene el control
    button_names = ["A", "B", "X", "Y", "LB", "RB"]
    #obtenemos el nombre del boton seleccionado
    button_name = button_names[event.button] if event.button < len(button_names) else str(event.button)
    #se ejecuta el siguiente mensaje cuando se presiona el boton
    print("Boton {} presionado.".format(button_name))

#con esta función manejo el evento de cuando se deja de oprimir el boton, asi se puede agrega la funcion para interrumpir la señal al objeto
def handle_button_up(event):
    button_names = ["A", "B", "X", "Y", "LB", "RB"]
    button_name = button_names[event.button] if event.button < len(button_names) else str(event.button)
    #se ejecuta el siguiente mensaje en dado caso de soltar el boton
    print("Boton {} liberado. Valor: {}".format(button_name, event.button))

# lo mismo de las funciones de arriba pero ahora para el joystick
def handle_hat_motion(joystick):
    print("JoyStick izquierdo manipulado. Valor: {}".format(joystick.get_hat(0)))

def main():
    pygame.init()
    pygame.joystick.init()

    # Aqui solo válidamos que exista un mando conectado
    if pygame.joystick.get_count() == 0:
        print("No se detectaron controles de videojuegos.")
        return

    # Inicializamos nuestro controlador
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    try:
        while True:
            for event in pygame.event.get(): #este es nuestro loop/array para manejar los eventos por acción
                if event.type == JOYAXISMOTION:
                    handle_axis_motion(event, joystick)
                elif event.type == JOYBUTTONDOWN: #hacemos el callback de las funciones
                    handle_button_down(event)
                elif event.type == JOYBUTTONUP:  #hacemos el callback de las funciones
                    handle_button_up(event)
                elif event.type == JOYHATMOTION:  #hacemos el callback de las funciones
                    handle_hat_motion(joystick)
            

    except KeyboardInterrupt:
        #paramos el programa presionando Ctrl+C
        print("\nSaliendo del programa.")
        pygame.quit()



#se valida que se está ejecutando nuestra función main
if __name__ == "__main__":
    main()

