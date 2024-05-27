from threading import Thread
from flask import Flask, request, jsonify, Response, send_from_directory
from flask_cors import CORS

from core.Serverr import pwm
from routes.CamServer import camServer
from routes.graph.GraphTask import graph_blueprint
from routes.ButtonsFunctionality import buttons_functionality
from routes.PhotogammetryTask import photogammetry_blueprint



app = Flask(__name__)
CORS(app)

app.register_blueprint(graph_blueprint, url_prefix='/graph')
app.register_blueprint(camServer)
app.register_blueprint(pwm)
app.register_blueprint(buttons_functionality)
app.register_blueprint(photogammetry_blueprint, url_prefix='/photogammetry')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False, use_reloader=False, threaded=True)