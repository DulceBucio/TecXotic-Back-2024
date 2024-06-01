from threading import Thread
from flask import Flask, request, jsonify, Response, send_from_directory
from flask_cors import CORS

from routes.PhotogammetryTask import photogammetry_blueprint

app = Flask(__name__)
CORS(app)

app.register_blueprint(photogammetry_blueprint, url_prefix='/photogammetry')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False, use_reloader=False, threaded=True)