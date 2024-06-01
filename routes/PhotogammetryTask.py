import os
import subprocess
from flask import Blueprint, request, jsonify
from flask_cors import CORS

photogammetry_blueprint = Blueprint('photogammetry', __name__)
CORS(photogammetry_blueprint)

@photogammetry_blueprint.route('/upload', methods=['POST'])
def create_3d_model():
    try:
        if request.is_json:
            data = request.get_json()
            image_folder = os.path.join(os.getcwd(), data.get('image_folder'))
            output_folder = data.get('output_folder')

            if image_folder:
                print("Image folder: ", image_folder)

            if not image_folder or not output_folder:
                return jsonify({"error": "Missing image_folder or output_folder"}), 400

            # Verify if the output folder exists, if not, create it
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)

            # Execute Meshroom via subprocess
            meshroom_cmd = [
                'C:\\Program Files\\Meshroom\\meshroom_batch.exe',
                '--input', image_folder,
                '--output', output_folder
            ]
            result = subprocess.run(meshroom_cmd, capture_output=True, text=True)

            if result.returncode != 0:
                print(f"Meshroom error: {result.stderr}")
                return jsonify({"error": result.stderr}), 500

            return jsonify({"message": "3D model created successfully"}), 200
        else:
            print("Request is not JSON")
            return jsonify({"error": "Request must be JSON"}), 400
    except Exception as e:
        print(f"Exception occurred: {str(e)}")
        return jsonify({"error": str(e)}), 500
