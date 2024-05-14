import json
from flask import Flask, request, Blueprint
from flask_cors import CORS
import serial

buttons_functionality = Blueprint('buttons_functionality', __name__)
CORS(buttons_functionality)

try:
    arduino = serial.Serial(port='/dev/ttyTHS1', baudrate=9600)
except Exception as e:
    print("ERROR in ButtonsFunctionality.py, serial route not founded: " + str(e))

if(arduino):
    print("Arduino connected")
else:
    print("Arduino not connected")

def send(message):
    try:
        arduino.write(bytes(message, 'utf-8'))
    except Exception as e:
        print("ERROR in ButtonsFunctionality.py, arduino.write failed: " + str(e))
        arduino.close()

@buttons_functionality.route('/actuators', methods=['POST'])
def send_actions():
    json = request.get_json()
    print('json_respone: ', str(json["actions"]))
    send(str(json["actions"]))
    return ""
