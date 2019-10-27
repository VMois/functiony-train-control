import cv2
import os
from tensorflow import keras
import numpy as np


train_images = []
train_labels = []

for filename in os.listdir('processed/'):
    frame = cv2.imread(f'processed/{filename}')
    label = int(filename.split('_')[1][0])
    train_images.append(frame)
    train_labels.append(label)

train_images = np.array(train_images)
train_labels = np.array(train_labels)

model = keras.Sequential([
    keras.layers.Conv2D(32, (3, 3), padding='same', input_shape=(200, 150, 3)),
    keras.layers.Activation('relu'),
    keras.layers.BatchNormalization(),
    keras.layers.MaxPooling2D((2, 2)),
    keras.layers.Conv2D(32, (3, 3), padding='same'),
    keras.layers.Activation('relu'),
    keras.layers.BatchNormalization(),
    keras.layers.Dropout(0.1),
    keras.layers.MaxPooling2D((2, 2)),
    keras.layers.Conv2D(64, (3, 3), padding='same'),
    keras.layers.Activation('relu'),
    keras.layers.BatchNormalization(),
    keras.layers.Flatten(),
    keras.layers.Dense(64, activation='relu'),
    keras.layers.BatchNormalization(),
    keras.layers.Dense(2, activation='softmax')
])

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

train_sample = 4500
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
