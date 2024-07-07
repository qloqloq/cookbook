#pip install influxdb
from influxdb import InfluxDBClient
from datetime import datetime


if __name__ == '__main__':
    # Setup database
    client = InfluxDBClient('localhost', 8086, 'admin', 'Password1', 'mydb')
    client.create_database('mydb')
    client.get_list_database()
    client.switch_database('mydb')

    # Write
    json_payload = []
    data = {
        "measurement": "home",
        "tags": {
            "ticker": "bedroom"
            },
        "time": datetime.now(),
        "fields": {
            'temperature': 22,
            'hum': 35.5
        }
    }
    json_payload.append(data)
    client.write_points(json_payload)

    # Read
    print(client.get_list_measurements())
    print(client.query('select * from home'))
