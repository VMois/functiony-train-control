import cv2
import numpy as np
import urllib.request

out = cv2.VideoWriter('test_videos/stream.avi',
                      cv2.VideoWriter_fourcc('M','J','P','G'), 24, (320, 240))

stream = urllib.request.urlopen('http://192.168.0.190:8080/stream/video.mjpeg')

bytes = b''

index = 0
while True:
    bytes += stream.read(1024)
    a = bytes.find(b'\xff\xd8') # JPEG start
    b = bytes.find(b'\xff\xd9') # JPEG end
    if a != -1 and b != -1:
        jpg = bytes[a:b+2]  # actual image
        bytes = bytes[b+2:]  # other informations

        img = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
        out.write(img)
    index += 1

out.release()
