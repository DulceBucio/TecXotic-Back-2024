from flask import Flask, request, jsonify
from ConnectionPixhawk import Pixhawk
from threading import Thread

app = Flask(__name__)

# Initialize Pixhawk and Serial connections
try:
    px = Pixhawk(direction='/dev/serial/by-id/usb-ArduPilot_Pixhawk1_380020000A51353338353732-if00')
except Exception as e:
    print(f"Initialization error: {e}")

# Handle commands
@app.route('/postControlMovement', methods=['POST'])
def post_control_movement():
    commands = request.json
    
    # Manual Control Commands
    if all(k in commands for k in ('roll', 'pitch', 'yaw', 'throttle')):
        px.drive_manual(commands['roll'], commands['pitch'], commands['yaw'], commands['throttle'], 0)
    
    # Mode Change Command
    if 'mode' in commands:
        current_mode = px.get_pix_info()['mode']
        if commands['mode'] != current_mode:
            px.change_mode(commands['mode'])
    
    # Arm/Disarm Command
    if 'arm_disarm' in commands:
        current_arm_state = px.get_pix_info()['is_armed']
        if commands['arm_disarm'] != current_arm_state:
            if commands['arm_disarm']:
                px.arm()
            else:
                px.disarm()


    imuVal = px.get_msg('AHRS2', timeout=0.5) if 'imu' in commands else {}
    response = {
        "message_received": True,
        "imu": {
            "roll": imuVal.get('roll', 0),
            "yaw": imuVal.get('yaw', 0),
            "pitch": imuVal.get('pitch', 0)
        } if imuVal else {},
        "pix_info": px.get_pix_info()
    }

    return jsonify(response)

if __name__ == '__main__':
    Thread(
            target=lambda: app.run(host='0.0.0.0', port=8080, debug=False, use_reloader=False, threaded=True)).start()
