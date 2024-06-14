from flask import Flask, jsonify
from flask_cors import CORS
import serial

app = Flask(__name__)
CORS(app)

# Sirve con el puerto, falta la dirección IP para que funcione inalámbricamente
SERIAL_PORT = '/dev/tty.usbserial-56A40600321'
BAUDRATE = 115200
ser = serial.Serial()

@app.route('/heartbeat', methods=['GET'])
def get_heartbeat():
    try:
        if ser.is_open:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').rstrip()
                try:
                    value = int(line)
                    return jsonify({'heartbeat': value})
                except ValueError:
                    return jsonify({'error': 'Invalid data'}), 500
        return jsonify({'error': 'No data available'}), 500
    except serial.SerialException as e:
        return jsonify({'error': f'Serial port error: {e}'}), 500

if __name__ == '__main__':
    try:
        ser = serial.Serial(SERIAL_PORT, BAUDRATE)
        print(f"Serial port opened: {SERIAL_PORT}")
        app.run(debug=True)
    except serial.SerialException as e:
        print(f"Error opening serial port: {e}")
