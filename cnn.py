import cv2
from tensorflow import keras
import numpy as np

vidcap = cv2.VideoCapture("test_videos/pivideo2_cnn.avi")

frames = []
count = 0
ret = 1
while ret:
    ret, frame = vidcap.read()
    if ret == 0:
        break
    #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frames.append(frame)
    count += 1
print(count)
frames = np.array(frames)

model = keras.Sequential([
    keras.layers.Conv2D(32, (3, 3), padding='same', input_shape=(150, 150, 3)),
    keras.layers.Activation('relu'),
    keras.layers.MaxPooling2D((2, 2)),
    keras.layers.Conv2D(64, (3, 3), padding='same'),
    keras.layers.Activation('relu'),
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

annotations = [(2 * 24, 12), (3*24, 12), (19*24, 12), (27*24, 24), (50*24, 24)]
train_labels = np.zeros(len(frames))
for annotation in annotations:
    train_labels[annotation[0] - 1: annotation[0] + annotation[1] - 1] = 1

train_sample = 756
# cnnhistory = model.fit(np.expand_dims(frames[:656], axis=3),
#                        train_labels[:656],
#                        batch_size=8,
#                        epochs=1,
#                        validation_data=(
#                            np.expand_dims(frames[656:], axis=3),
#                            train_labels[656:]))
cnnhistory = model.fit(frames[:train_sample],
                       train_labels[:train_sample],
                       batch_size=8,
                       epochs=1,
                       validation_data=(
                           frames[train_sample:],
                           train_labels[train_sample:]))

model_json = model.to_json()
with open("model/model.json", "w") as json_file:
    json_file.write(model_json)
# serialize weights to HDF5
model.save_weights("model/model.h5")
print("Saved model to disk")
