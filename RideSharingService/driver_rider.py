from flask import Flask, request
from flask_apscheduler import APScheduler
import json
import requests

# from client import rider_data

app = Flask(__name__)

scheduler = APScheduler()
app.config['SECRET_KEY'] = 'secret!'

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

        assign_driver_rider = {
            'driver': d_name,
            'rider': r_name,
            'fare': fare
        }

        if rider['division'] == 13:
            requests.post("http://communication-service-dhaka:7070/match", json=json.dumps(assign_driver_rider))
        else:
            requests.post("http://communication-service-comilla:7070/match", json=json.dumps(assign_driver_rider))

        drivers.remove(driverr)
        riders.remove(rider)


if __name__ == '__main__':
    scheduler.add_job(id='Schedule task', func=match_rider_driver, trigger='interval', seconds=3)
    scheduler.start()
    app.run(debug=True, host='0.0.0.0', port=6001)
