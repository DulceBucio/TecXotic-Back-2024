from flask import Flask, request
from threading import Thread

app = Flask(__name__)

@app.route('/post', methods=['POST'])
def handle_post():
    data = request.get_json()  # Recibir datos JSON del cuerpo del mensaje POST
    # Hacer algo con los datos recibidos
    print("Datos recibidos:", data)
    return "Datos recibidos correctamente", 200

if __name__ == '__main__':
    # Ejecutar la aplicación Flask en la dirección IP de la red local y en el puerto 5000
    Thread(
            target=lambda: app.run(host='0.0.0.0', port=8080, debug=False, use_reloader=False, threaded=True)).start()
