import inputs
import time

while True:
    gamepad = inputs.get_gamepad()
    for event in gamepad:
        #print(event.code, event.state)
        # print(event.code, event.state)
    
        if event.code == "BTN_NORTH": print("y") #En vez de un print va una funcion
        if event.code == "BTN_EAST": print("b")
        if event.code == "BTN_SOUTH": print("a")
        if event.code == "BTN_WEST": print("x")

        # axes = gamepad.get_axes()

        # print(f"Joystick X: {axes[0]:.2f}, Joystick Y: {axes[1]:.2f}")

    time.sleep(0.1)

"""
BTN_NORTH	Y
BTN_EAST	B
BTN_SOUTH	A
BTN_WEST	X

BTN_TR		RB
BTN_TL		LB

Cruceta

ABS_HAT0X
ABS_HAT0Y

Joystick derecho

ABS_RY
ABS_RX

Joystick izquierdo

ABS_Y
ABS_X

Gatillo derecho

ABS_RZ

Gatillo izquierdo

ABS_Z"""