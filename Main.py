import numpy as np
import cv2
from Detect import *
from getPerspectiveTransform import *
import time
time_start = time.time()

cap = cv2.VideoCapture(0)
cv2.namedWindow('Projector', 0)
cv2.setWindowProperty('Projector', 0, cv2.cv.CV_WINDOW_FULLSCREEN)
ret, frame = cap.read()
frame_straight = frame
pic = np.zeros((len(frame_straight), len(frame_straight[0]), 3), np.uint8)
red = cv2.imread('red.png')

calibrated = False

while calibrated == False:
    ret, frame = cap.read()

    cv2.imshow('frame', frame)

    frame_straight = frame

    pic = np.zeros((len(frame_straight), len(frame_straight[0]), 3), np.uint8)
    pic[:,:,0]=255

    transform = pic
    cv2.namedWindow('Projector', 0)
    cv2.setWindowProperty('Projector', 0, cv2.cv.CV_WINDOW_FULLSCREEN)

    ret, frame = cap.read()

    #frame = cv2.flip(frame, 1)
    cv2.imshow('frame', frame)

    cv2.imshow('Projector', pic)
    time.sleep(1)
    try:
        points_corner = points_detection(frame)
        print "ok"
        calibrated = True
        print time.time() - time_start
    except Exception:
        print "fail"

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

while True:

    # Vanilla video capture
    ret, frame = cap.read()
    # Display the resulting frame
    cv2.imshow('frame', frame)

    frame_straight = four_point_transform(frame, points_corner)
    cv2.imshow('frameStraight', frame_straight)
    position_cross = detect_glyph(frame_straight)

    pic = np.zeros((len(frame_straight), len(frame_straight[0]), 3), np.uint8)
    if position_cross is not None:
        print "point display"
        x_offset_red = position_cross[0]
        y_offset_red = position_cross[1]
        pic[x_offset_red:x_offset_red + red.shape[0], y_offset_red:y_offset_red + red.shape[1]] = red


    cv2.imshow('Picture', pic)

    transform = pic

    cv2.namedWindow('Projector', 0)
    cv2.setWindowProperty('Projector', 0, cv2.cv.CV_WINDOW_FULLSCREEN)
    cv2.imshow('Projector', transform)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
