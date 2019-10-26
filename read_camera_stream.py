import cv2
from tensorflow import keras
import numpy as np
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


json_file = open('model/model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = keras.models.model_from_json(loaded_model_json)
# load weights into new model
loaded_model.load_weights("model/model.h5")
print("Loaded model from disk")
out = cv2.VideoWriter('test_videos/stream.avi',
                      cv2.VideoWriter_fourcc('M','J','P','G'), 24, (640, 480))

#stream = urllib.request.urlopen('http://192.168.0.190:8080/stream/video.mjpeg')

bytes = b''

w = 150
h = 150
y = 480 - h
x = int((640 - w) / 2)
vcap = cv2.VideoCapture("http://192.168.0.190:8080/stream/video.mjpeg")
index = 0
while vcap.isOpened():
    #bytes += stream.read(1024)
    #a = bytes.find(b'\xff\xd8') # JPEG start
    #b = bytes.find(b'\xff\xd9') # JPEG end
    ret, frame = vcap.read()
    #out.write(frame)
    cv2.imwrite(f'stream4/{index}.jpg', frame)
    if ret == 0:
        continue
    #if a != -1 and b != -1:
    #    jpg = bytes[a:b+2]  # actual image
    #    bytes = bytes[b+2:]  # other informations

        # frame = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
        # print(frame.shape)
    y = 480 - h
    x = int((640 - w) / 2)
    roi = frame[y:y + h, x:x + w]
    #roi = cv2.Canny(roi, 100, 200)
    #prediction = loaded_model.predict(np.array([roi]))
    #print(prediction[0])
    #if prediction[0][0] < 0.6:
    #    print('Collision')
    #    #set_speed(0)
    #    time.sleep(0.5)
    #    continue
    #
    set_speed(700)
    index += 1
    time.sleep(0.5)
    #time.sleep(0.1)

out.release()