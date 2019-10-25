import logging

import tensorflow as tf
logging.info("TF version: " + tf.__version__)
import tensorflow_hub as hub
# import tempfile
# from six.moves.urllib.request import urlopen
# from six import BytesIO

# For measuring the inference time.
import time
import cv2


module_handle = "https://tfhub.dev/google/openimages_v4/ssd/mobilenet_v2/1"
#["https://tfhub.dev/google/openimages_v4/ssd/mobilenet_v2/1",
# "https://tfhub.dev/google/faster_rcnn/openimages_v4/inception_resnet_v2/1"]

detector = hub.load(module_handle).signatures['default']


def run_detector(detector, frame):
    img = frame
    converted_img = tf.image.convert_image_dtype(img, tf.float32)[tf.newaxis, ...]
    start_time = time.time()
    result = detector(converted_img)
    end_time = time.time()

    result = {key:value.numpy() for key,value in result.items()}

    print("Found %d objects." % len(result["detection_scores"]))
    print("Inference time: ", end_time-start_time)


vidcap = cv2.VideoCapture('test_videos/pivideo2.mp4')
success, image = vidcap.read()
read_amount = 1
while success:
    # cv2.imwrite("test_videos/1/frame%d.jpg" % count, image)
    #  save frame as JPEG file

    success, image = vidcap.read()
    run_detector(detector, image)
    read_amount += 1
    if read_amount > 1:
        break
