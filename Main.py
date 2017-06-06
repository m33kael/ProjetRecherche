import numpy as np
import cv2
from Detect import *

glyphCoordinatesCamera = [0, 0]
markCoordinatesCamera = [0, 0]
markCoordinatesProjection = [500, 500]
lower_red = np.array([30, 30, 120], dtype="uint8")
upper_red = np.array([120, 120, 255], dtype="uint8")

cap = cv2.VideoCapture(1)
ret, frame = cap.read()
projector = cv2.imread('wallpaper.png')
red = cv2.imread('red.png')


glyphCoordinatesCamera = detect_glyph(frame)
while glyphCoordinatesCamera is None:
    ret, frame = cap.read()
    projector = cv2.imread('wallpaper.png')
    cv2.imshow('Frame', frame)
    cv2.imshow('Projector', projector)
    glyphCoordinatesCamera = detect_glyph(frame)
    print "Nope"


if glyphCoordinatesCamera is not None:
    print "Glyph found - X:" + str(glyphCoordinatesCamera[0]) + " Y:" + str(glyphCoordinatesCamera[1])
    x_align_ok = False
    y_align_ok = False
    while True:
        ret, frame = cap.read()
        projector = cv2.imread('wallpaper.png')
        #frame = cv2.flip(frame, 0)
        cv2.imshow('Frame', frame)

        mask = cv2.inRange(frame, lower_red, upper_red)
        mask = cv2.dilate(mask, None, iterations=2)
        contours = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        if len(contours) > 0:
            c = max(contours, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            markCoordinatesCamera[0] = int(x)
            markCoordinatesCamera[1] = int(y)
            cv2.imshow("mask", mask)
            if radius > 10:
                print "Red found - X:" + str(markCoordinatesCamera[0]) + " Y:" + str(markCoordinatesCamera[1])

                if glyphCoordinatesCamera[0] == markCoordinatesCamera[0] and glyphCoordinatesCamera[1] == markCoordinatesCamera[1]:
                    markOnGlyph = True
                    print "Success"
                else:
                    print glyphCoordinatesCamera
                    if x_align_ok is False:
                        if glyphCoordinatesCamera[0] - 10 > markCoordinatesCamera[0]:
                            markCoordinatesProjection[0] = markCoordinatesProjection[0] + 1
                        elif glyphCoordinatesCamera[0] + 10 < markCoordinatesCamera[0]:
                            markCoordinatesProjection[0] = markCoordinatesProjection[0] - 1
                        else:
                            x_align_ok = True

                    if y_align_ok is False:
                        if glyphCoordinatesCamera[1] - 10 > markCoordinatesCamera[1]:
                            markCoordinatesProjection[1] = markCoordinatesProjection[1] + 1
                        elif glyphCoordinatesCamera[1] + 10 < markCoordinatesCamera[1]:
                            markCoordinatesProjection[1] = markCoordinatesProjection[1] - 1
                        else:
                            y_align_ok = True

        x_offset_red = markCoordinatesProjection[0]
        y_offset_red = markCoordinatesProjection[1]
        projector[x_offset_red:x_offset_red + red.shape[0], y_offset_red:y_offset_red + red.shape[1]] = red

        cv2.imshow('Projector', projector)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
else:
    print "No Glyph detected"
cv2.destroyAllWindows()
