import cv2
import json
import time
from tensorflow import keras
import urllib.request

MAX_SPEED = 1023
DEFAULT_SPEED = 800
MINIMAL_SPEED = 750

train_base_address = 'http://192.168.0.180'
track_base_address = 'http://192.168.0.100:5000'

scap = cv2.VideoCapture('http://192.168.0.190:8080/stream/video.mjpeg')

json_file = open('model/model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()

loaded_model = keras.models.model_from_json(loaded_model_json)
loaded_model.load_weights('model/model.h5')
print('Loaded model from disk')


def crop_frame(frame):
    pass


def set_speed(speed: int):
    train_speed_url = f'{train_base_address}/motor'
    params = {
        'x': str(speed),
    }
    query_string = urllib.parse.urlencode(params)

    train_speed_url = train_speed_url + '?' + query_string
    urllib.request.urlopen(train_speed_url)


def get_track_data():
    with urllib.request.urlopen(f'{track_base_address}/rest/items') as response:
        return json.loads(response.read(), encoding='utf-8')


def find_activated_sensors(sensors):
    sensors_activated = []
    for sensor_id, value in sensors.items():
        if value['state'] == 0:
            sensors_activated.append(int(sensor_id))
    return sensors_activated


def get_leading_position(sensors_activated, prev_sensors):
    result = list(set(sensors_activated) - set(prev_sensors))
    if len(result):
        return result[0]
    return None


def position_to_speed(position):
    if position in [33, 25, 12, 26]:
        return MAX_SPEED
    elif position in [31, 34, 13, 11, 24, 32, 27, 23]:
        return DEFAULT_SPEED
    elif position in [21]:
        return MINIMAL_SPEED
    else:
        return MINIMAL_SPEED


def should_camera_be_activate(position):
    return position in [32, 21, 13, 11, 24, 23, 22]


prev_activated_sensors = []

while True:
    track_data = get_track_data()
    activated_sensors = find_activated_sensors(track_data['track']['rail_sections'])
    #if len(activated_sensors) != 0:
    #    print(activated_sensors)
    new_leading_position = get_leading_position(activated_sensors, prev_activated_sensors)
    if new_leading_position:
        if should_camera_be_activate(new_leading_position):
            pass
        print(new_leading_position)
        speed = position_to_speed(new_leading_position)
        print(speed)
    #set_speed(current_speed)
    prev_activated_sensors = activated_sensors
    time.sleep(0.1)
# 800 on turns
# 700 on
#set_speed(700)
#time.sleep(20)

