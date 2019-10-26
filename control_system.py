import json
import time
import urllib.request

train_base_address = '192.168.0.180'
track_base_address = '192.168.0.100:5000'


def set_speed(speed: int):
    train_speed_url = f'{train_base_address}/motor'
    params = {
        'x': str(speed),
    }
    query_string = urllib.parse.urlencode(params)

    train_speed_url = train_speed_url + '?' + query_string
    with urllib.request.urlopen(train_speed_url) as response:
        response_text = response.read()
    return speed


def get_gyroscope_data():
    pass


def get_track_data():
    with urllib.request.urlopen(f'http://{track_base_address}/rest/items') as response:
        response_text = response.read()
        return json.loads(response_text, encoding='utf-8')


def find_train_position(sensors):
    sensors_activated = []
    for id, value in sensors.items():
        if value.state == 1:
            sensors_activated.append(int(id))
    return sensors_activated


def suggest_speed_on_position(train_position_sensor):
    if train_position_sensor in [33, 25]:
        return default_speed * 2
    elif train_position_sensor in [34, 35, 31, 11]:
        return int(default_speed / 2)
    else:
        return default_speed


default_speed = 511
current_speed = default_speed
prev_speed = default_speed

paths = []

while True:
    track_data = get_track_data()
    positions = find_train_position(track_data['rail_sections'])
    current_speed = suggest_speed_on_position(positions)
    if current_speed != prev_speed:
        current_speed = set_speed(default_speed)
    time.sleep(0.2)
