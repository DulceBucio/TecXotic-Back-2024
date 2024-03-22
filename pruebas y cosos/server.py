import websockets
import asyncio
from flask import Response, request, abort
from flask_cors import CORS

def run():
    start_server = websockets.serve(echo, '0.0.0.0', 55000)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()

app = Flask(__name__)
CORS(app)


app.route('/postControlMovement', methods=['POST'])
def postControlMovement():
    if request.method == 'POST':
        data = request.get_json()
        print(data)
        return Response(status=200)
    else:
        abort(400)

        