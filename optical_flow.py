import cv2
vidcap = cv2.VideoCapture("test_videos/pivideo4.mp4")

w = 150
h = 150
out = cv2.VideoWriter('test_videos/pivideo4_cropped.avi', cv2.VideoWriter_fourcc('M','J','P','G'), 24, (w, h))

ret = 1
y = 480 - h
x = int((640 - w) / 2)
index = 0
while ret:
    ret, frame = vidcap.read()
    if ret == 0:
        break
    roi = frame[y:y+h, x:x+w]
    #cv2.imwrite(f'test_videos/3/{index}.jpg')
    #edges = cv2.Canny(roi, 50, 100)
    #roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    #roi = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
    out.write(roi)
    index += 1

out.release()
vidcap.release()
