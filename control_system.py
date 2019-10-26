import json
import time
import urllib.request

train_base_address = 'http://192.168.0.180'
track_base_address = 'http://192.168.0.100:5000'


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
    with urllib.request.urlopen(f'{track_base_address}/rest/items') as response:
        response_text = response.read()
        return json.loads(response_text, encoding='utf-8')


def find_train_position(sensors):
    sensors_activated = []
    for id, value in sensors.items():
        if value['state'] == 0:
            sensors_activated.append(int(id))
    return sensors_activated


def suggest_speed_on_position(train_position_sensor):
    print(train_position_sensor)
    if train_position_sensor in [33, 25]:
        print('max speed')
        return int(default_speed * 1.2)
    elif train_position_sensor in [34, 35, 11]:
        print('min speed')
        return int(default_speed)
    elif train_position_sensor in [31]:
        print('stop 32')
        set_speed(0)
        time.sleep(2)
        return int(default_speed)
    else:
        print('default speed')
        return default_speed


default_speed = 700
current_speed = default_speed
prev_speed = default_speed

paths = []

while True:
    track_data = get_track_data()
    positions = find_train_position(track_data['track']['rail_sections'])
    print(positions)
    current_speed = suggest_speed_on_position(positions[0])
    set_speed(current_speed)
    time.sleep(0.3)
# 800 on turns
# 700 on
#set_speed(700)
#time.sleep(20)
set_speed(0)
