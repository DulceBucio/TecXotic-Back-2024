import json
from flask import Flask, request, Blueprint, jsonify
from flask_cors import CORS
import serial
import time

# Initialize the Flask blueprint
buttons_functionality = Blueprint('buttons_functionality', __name__)
CORS(buttons_functionality)

# Initialize serial connection
def init_serial_connection(port='/dev/ttyUSB0', baudrate=9600):
    try:
        arduino = serial.Serial(port, baudrate=baudrate, timeout=1)
        time.sleep(2)  # Give time for Arduino's reset and bootloader
        print("Arduino connected")
        return arduino
    except Exception as e:
        print("ERROR in ButtonsFunctionality.py, serial route not founded: " + str(e))
        return None

# Get the Arduino connection
arduino = init_serial_connection()

def send(message):
    try:
        # Ensure the message is a string and ends with a newline
        message_str = f"{message}\n"
        arduino.write(message_str.encode('utf-8'))
        time.sleep(0.5)  # Give time for Arduino to process the command
    except Exception as e:
        print("ERROR in ButtonsFunctionality.py, arduino.write failed: " + str(e))
        if arduino:
            arduino.close()

@buttons_functionality.route('/actuators', methods=['POST'])
def send_actions():
    if not arduino:
        return "Arduino not connected", 500
    data = request.get_json()
    print('json_response: ', str(data["actions"]))

    # Map commands to integers
    command_map = {
        "LEFTROLL": 1,
        "RIGHTROLL": 2,
        "STOP": 0
    }

    command = command_map.get(data["actions"], None)

    if command is not None:
        send(str(command))  # Convert command to string
        return jsonify({"message": "Command sent", "status": "success"})
    else:
        return jsonify({"message": "Invalid command", "status": "error"}), 400

                                                                                                  