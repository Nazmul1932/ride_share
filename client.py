import requests
import socketio
import time
import random
import json

sio_dh = socketio.Client()
sio_dh.connect('http://13.14.0.51:7070', namespaces=['/communication'])

sio_ca = socketio.Client()
sio_ca.connect('http://13.14.0.52:7070', namespaces=['/communication'])


def send_ratings(dr_name):
    ratings_data = random.randrange(1, 5)
    rating = {
        'driver_name': dr_name,
        'rating': ratings_data
    }
    r = requests.post("http://dhaka.server.com:80/rating", json=json.dumps(rating))


@sio_dh.event(namespace='/communication')
def message(data):
    fare = round(data[2], 2)
    print('..Dhaka..' + data[0] + ' is assigned to ' + data[1] + '.\n' +
          ' Total fare ' + str(fare) + ' Taka\n')

    send_ratings(data[1])


@sio_ca.event(namespace='/communication')
def message(data):
    fare = round(data[2], 2)
    print('..Comilla..' + data[0] + ' is assigned to ' + data[1] + '.\n' +
          ' Total fare ' + str(fare) + ' Taka\n')

    send_ratings(data[1])


id = 101

while True:
    x1 = random.randrange(2000)
    y1 = random.randrange(2000)
    x2 = random.randrange(2000)
    y2 = random.randrange(2000)

    x3 = random.randrange(2000)
    y3 = random.randrange(2000)
    carnum = random.randrange(10000000)

    if random.randint(1, 10) > 5:
        geotag = 13
    else:
        geotag = 14

    rider_data = {'name': 'r' + str(id),
                  'location': [x1, y1],
                  'desti': [x2, y2],
                  'division': geotag}

    driver_data = {'name': 'd' + str(id),
                   'car_number': carnum,
                   'location': [x3, y3],
                   'division': geotag}

    if geotag == 13:
        requests.post("http://dhaka.server.com:80/rider", json=json.dumps(rider_data))
        requests.post("http://dhaka.server.com:80/driver", json=json.dumps(driver_data))

    else:
        requests.post("http://comilla.server.com:80/rider", json=json.dumps(rider_data))
        requests.post("http://comilla.server.com:80/driver", json=json.dumps(driver_data))

    time.sleep(1)
    id += 1
