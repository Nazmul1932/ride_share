from flask import Flask, request, g
from flask_apscheduler import APScheduler
from flask_socketio import SocketIO, emit
import json
import mysql.connector

app = Flask(__name__)


scheduler = APScheduler()
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

riders = []
drivers = []


@app.route('/driver', methods=['POST'])
def driver():
    data = request.json
    x = json.loads(data)
    drivers.append(x)
    return data


@app.route('/rider', methods=['POST'])
def rider():
    data = request.json
    x = json.loads(data)
    riders.append(x)
    return data


def insertVariableIntoTable(driver_name, rating):
    connection = mysql.connector.connect(user='root', host='127.0.0.1', database='DS')
    cursor = connection.cursor()
    cursor.execute('''INSERT INTO Ratings(driver_name,rating) VALUES (%s,%s)''', (driver_name, rating))
    connection.commit()
    print("Record inserted........")

    connection.close()


@app.route('/rating', methods=['POST'])
def ratings():
    data = request.json
    x = json.loads(data)
    dr_name = x['driver_name']
    rat = x['rating']
    insertVariableIntoTable(dr_name, rat)
    return data


@socketio.on('message')
def match_rider_driver():
    mini = 1e10
    for rider in riders:
        driverr = {}
        r1 = rider['location'][0]
        r2 = rider['location'][1]
        r3 = rider['desti'][0]
        r4 = rider['desti'][1]

        for driver in drivers:
            d1 = driver['location'][0]
            d2 = driver['location'][1]

            distance = ((r1 - d1) ** 2 + (r2 - d2) ** 2) ** .5
            if distance < mini:
                driverr = driver

        r_name = rider['name']
        d_name = driverr['name']
        fare = (((r1 - r3) ** 2 + (r2 - r4) ** 2) ** .5) * 2

        assign = [r_name, d_name, fare]

        socketio.emit('message', assign, namespace='/communication')

        drivers.remove(driverr)
        riders.remove(rider)


if __name__ == '__main__':
    scheduler.add_job(id='Schedule task', func=match_rider_driver, trigger='interval', seconds=5)
    scheduler.start()
    # app.run()
    socketio.run(app, port=8000)
