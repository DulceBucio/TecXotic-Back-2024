from flask import Flask, request, jsonify
import sys
from ConnectionPixhawk import Pixhawk
from threading import Thread



app = Flask(__name__)

# Initialize your Pixhawk and Serial connections here, similar to your WebSocket script
# try:
#     px = Pixhawk(direction='/dev/serial/by-id/usb-ArduPilot_Pixhawk1_380020000A51353338353732-if00')
# except Exception as e:
#     print("Initialization error:", str(e))
#     # Handle initialization errors

@app.route('/postControlMovement', methods=['POST'])
def postControlMovement():
    data = request.json
    print(data)
    px.drive_manual(data['throttle'], data['roll'], data['pitch'], data['yaw'])
    return jsonify(data)

if __name__ == '__main__':
        # Running the server that delivers video and the task, each request runs on diferent thread
    Thread(
            target=lambda: app.run(host='0.0.0.0', port=8080, debug=False, use_reloader=False, threaded=True)).start()
