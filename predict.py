import cv2
import numpy as np
from tensorflow import keras

vidcap = cv2.VideoCapture("test_videos/pivideo2_cnn.avi")
json_file = open('model/model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = keras.models.model_from_json(loaded_model_json)
# load weights into new model
loaded_model.load_weights("model/model.h5")
print("Loaded model from disk")

w = 150
h = 150
out = cv2.VideoWriter('test_videos/cnn_test.avi',
                      cv2.VideoWriter_fourcc('M','J','P','G'), 24, (w, h))
ret = 1
y = 480 - h
x = int((640 - w) / 2)
index = 0
while ret:
    ret, roi = vidcap.read()
    if ret == 0:
        break
    #roi = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #prediction = loaded_model.predict(np.expand_dims(np.array([roi]), axis=3))
    prediction = loaded_model.predict(np.array([roi]))
    #print(prediction[0])
    if prediction[0][0] < 0.9:
        print('Collision: ', index / 24)
    index += 1
