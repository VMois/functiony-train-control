import cv2
import numpy as np

videos_to_transfer = [
    'pivideo2.mp4',
    'pivideo3.mp4',
    'nokiachallenge-1026-01.mp4',
    'nokiachallenge-1026-02.mp4',
    'nokiachallenge-1026-03.mp4',
    'nokiachallenge-1026-04.mp4',
    'nokiachallenge-1026-05.mp4',
    'nokiachallenge-1026-06.mp4',
    'nokiachallenge-1026-07.mp4',
    # 'nokiachallenge-1026-08.mp4',
]

annotations = [
    [],
    [(2 * 24, 20), (19*24, 8), (27*24, 24), (50*24, 24)],
    [],
    [(8 * 25, 12), (10 * 25, 12), (20 * 25, 25 * 2 + 25)],
    [(19 * 25, 25+12)],
    [(10*25, 25)],
    [(20*25 + 12, 12)],
    [(12 * 25 + 12, 25)],
    [(20*25 + 12, 12+25)],
]

file_index = 0

for index, video in enumerate(videos_to_transfer):
    vcap = cv2.VideoCapture(f'original/{video}')
    length = int(vcap.get(cv2.CAP_PROP_FRAME_COUNT))

    train_labels = np.zeros(length)
    for annotation in annotations[index]:
        train_labels[annotation[0] - 1: annotation[0] + annotation[1] - 1] = 1

    ret = 1
    inner_index = 0
    while ret == 1:
        ret, frame = vcap.read()
        if ret == 0:
            break
        label = int(train_labels[inner_index])
        cv2.imwrite(f'labeled/videos/{file_index}_{label}.jpg', frame)
        file_index += 1
        inner_index += 1

    vcap.release()
