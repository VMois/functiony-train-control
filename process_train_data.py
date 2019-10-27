import os
import cv2

data = [
    'stream',
    'stream1',
    'stream3',
    'stream4',
    'videos',
]

w = 150
h = 200


def return_x_y(_frame):
    y = _frame.shape[0] - h
    x = int((frame.shape[1] - w) / 2)
    return x, y


def increase_brightness(img, value=30):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)

    lim = 255 - value
    v[v > lim] = 255
    v[v <= lim] += value

    final_hsv = cv2.merge((h, s, v))
    img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
    return img


train_images = []
train_labels = []

index = 0
for entry in data:
    files = os.listdir(f'labeled/{entry}')
    for filename in files:
        frame = cv2.imread(f'labeled/{entry}/{filename}')
        label = int(filename.split('_')[1][0])
        x, y = return_x_y(frame)
        roi = frame[y:y + h, x:x + w]
        cv2.imwrite(f'processed/{index}_{label}.jpg', roi)
        index += 1
        # b_roi = increase_brightness(roi, 15)
        # cv2.imwrite(f'processed/{index}_{label}.jpg', b_roi)
        # index += 1
