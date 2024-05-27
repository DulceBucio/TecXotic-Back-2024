import os
import subprocess
from flask import Flask, Blueprint, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
photogammetry_blueprint = Blueprint('graph', __name__)
CORS(photogammetry_blueprint)

@photogammetry_blueprint.route('/upload', methods=['POST'])
def create_3d_model():
    data = request.get_json()
    image_folder = data.get('image_folder')
    output_folder = data.get('output_folder')

    if not image_folder or not output_folder:
        return jsonify({"error": "Missing image_folder or output_folder"}), 400

    # Verificar si la carpeta de salida existe, si no, crearla
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Ejecutar Meshroom mediante subprocess
    meshroom_cmd = [
        'C:\\Program Files\\Meshroom\\meshroom_batch',
        '--input', image_folder,
        '--output', output_folder
    ]
    result = subprocess.run(meshroom_cmd, capture_output=True, text=True)

    if result.returncode != 0:
        return jsonify({"error": result.stderr}), 500

    return jsonify({"message": "3D model created successfully"}), 200