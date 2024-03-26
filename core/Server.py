from flask import Flask, request, jsonify
import sys
from ConnectionPixhawk import Pixhawk
from threading import Thread



app = Flask(__name__)

# Initialize your Pixhawk and Serial connections here, similar to your WebSocket script
try:
    px = Pixhawk(direction='/dev/serial/by-id/usb-ArduPilot_Pixhawk1_380020000A51353338353732-if00')
except Exception as e:
    print("Initialization error:", str(e))
    # Handle initialization errors

@app.route('/control/movement', methods=['POST'])
def control_movement():
    data = request.json
    try:
        px.drive_manual(data['roll'], data['pitch'], data['yaw'], data['throttle'], 0)
        # You might need to adjust the key names based on what you're sending from the client
        return jsonify({"success": True, "message": "Movement command executed."})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})

@app.route('/control/mode', methods=['POST'])
def change_mode():
    mode = request.json.get('mode')
    try:
        px.change_mode(mode)
        return jsonify({"success": True, "message": f"Mode changed to {mode}."})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})

@app.route('/control/arming', methods=['POST'])
def control_arming():
    should_arm = request.json.get('arm', False)
    try:
        if should_arm:
            px.arm()
        else:
            px.disarm()
        return jsonify({"success": True, "message": "Arming status changed."})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})

if __name__ == '__main__':
        # Running the server that delivers video and the task, each request runs on diferent thread
    Thread(
            target=lambda: app.run(host='0.0.0.0', port=8080, debug=False, use_reloader=False, threaded=True)).start()
