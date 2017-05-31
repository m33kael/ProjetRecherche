import numpy as np
import cv2
from Detect import *

cap = cv2.VideoCapture(0)
cv2.namedWindow('Projector', 0)
cv2.setWindowProperty('Projector', 0, cv2.cv.CV_WINDOW_FULLSCREEN)
ret, frame = cap.read()
frame_straight = frame
pic = np.zeros((len(frame_straight), len(frame_straight[0]), 3), np.uint8)


pic = cv2.imread('test.jpg', 0)



while (True):

    # Vanilla video capture
    ret, frame = cap.read()
    # Display the resulting frame
    frame = cv2.flip(frame, 1)
    cv2.imshow('frame', frame)

    # Bout a changer
    frame_straight = frame

    position_cross = detect_glyph(frame_straight)
    pic = np.zeros((len(frame_straight), len(frame_straight[0]), 3), np.uint8)
    if position_cross is not None:
        pic[position_cross[0], position_cross[1]] = (0, 0, 255)

    # Vanilla image to display
    cv2.imshow('Picture', pic)

    # Transformed image to project

    transform = pic
    # transform here
    cv2.namedWindow('Projector', 0)
    cv2.setWindowProperty('Projector', 0, cv2.cv.CV_WINDOW_FULLSCREEN)
    cv2.imshow('Projector', transform)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
