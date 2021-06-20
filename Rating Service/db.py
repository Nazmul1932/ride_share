from flask import Flask, request
import json
import mysql.connector

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'


def insertVariableIntoTable(driver_name, rating):
    connection = mysql.connector.connect(user='admin', host='13.14.0.100', database='nhdb', password='admin')
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
    insertVariableIntoTable(dr_name, str(rat))
    return data


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=7000)
