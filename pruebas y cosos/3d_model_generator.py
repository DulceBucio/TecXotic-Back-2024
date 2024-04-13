import os
import subprocess
from flask import Flask

app = Flask(__name__)
@app.route("/")

def create_3d_model(image_folder, output_folder):
    # Verificar si la carpeta de salida existe, si no, crearla
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Ejecutar Meshroom mediante subprocess
    meshroom_cmd = [
        #Configura la variable de entorno antes de ejecutar
        'C:\Program Files\Meshroom\meshroom_batch',
        '--input', image_folder,
        '--output', output_folder
    ]
    subprocess.run(meshroom_cmd)

if __name__ == "__main__":
    # Especifica la carpeta de entrada con las imágenes y la carpeta de salida para el modelo 3D
    image_folder = "ruta del directorio"
    output_folder = "ruta del directorio"

    # Llama a la función para crear el modelo 3D
    create_3d_model(image_folder, output_folder)
