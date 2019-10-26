import cv2
import os
from tensorflow import keras
import numpy as np

data = [
    'stream',
    'stream1',
    'stream3',
    'stream4',
    'videos',
]

w = 150
h = 200
#y = 480 - h
#x = int((640 - w) / 2)


def return_x_y(_frame):
    y = _frame.shape[0] - h
    x = int((frame.shape[1] - w) / 2)
    return x, y


train_images = []
train_labels = []

for entry in data:
    files = os.listdir(f'labeled/{entry}')
    for filename in files:
        frame = cv2.imread(f'labeled/{entry}/{filename}')
        label = int(filename.split('_')[1][0])
        x, y = return_x_y(frame)
        roi = frame[y:y + h, x:x + w]
        # cv2.imwrite('test_videos/roi.jpg', roi)
        # apply transformations
        # frame = cv2.Canny(frame, 100, 200)

        train_images.append(roi)
        train_labels.append(label)

train_images = np.array(train_images)
train_labels = np.array(train_labels)

model = keras.Sequential([
    keras.layers.Conv2D(32, (3, 3), padding='same', input_shape=(200, 150, 3)),
    keras.layers.Activation('relu'),
    keras.layers.MaxPooling2D((2, 2)),
    keras.layers.Conv2D(64, (3, 3), padding='same'),
    keras.layers.Activation('relu'),
    keras.layers.Dropout(0.1),
    keras.layers.MaxPooling2D((2, 2)),
    keras.layers.Conv2D(64, (3, 3), padding='same'),
    keras.layers.Activation('relu'),
    keras.layers.Flatten(),
    keras.layers.Dense(64, activation='relu'),
    keras.layers.Dense(2, activation='softmax')
])

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

train_sample = 4000
# cnnhistory = model.fit(np.expand_dims(frames[:train_sample], axis=3),
#                        train_labels[:train_sample],
#                        batch_size=8,
#                        epochs=1,
#                        validation_data=(
#                            np.expand_dims(frames[train_sample:], axis=3),
#                            train_labels[train_sample:]))
cnnhistory = model.fit(train_images[:train_sample],
                       train_labels[:train_sample],
                       batch_size=8,
                       epochs=1,
                       validation_data=(
                           train_images[train_sample:],
                           train_labels[train_sample:]))

model_json = model.to_json()
with open("model/model.json", "w") as json_file:
    json_file.write(model_json)
model.save_weights("model/model.h5")
print("Saved model to disk")
