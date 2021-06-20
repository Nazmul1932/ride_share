from flask import Flask, request
from flask_socketio import SocketIO
import json

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


@app.route('/match', methods=['POST'])
def rider():
    data = request.json
    rider_data = json.loads(data)
    communicate(rider_data)
    return data


@socketio.on('message')
def communicate(d):
    data = [d['rider'], d['driver'], d['fare']]
    socketio.emit('message', data, namespace='/communication')


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=7070)
