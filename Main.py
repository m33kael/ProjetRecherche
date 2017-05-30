
import numpy as np
import cv2

cap = cv2.VideoCapture(0)
pic = cv2.imread('test.jpg', 0)
while(True):

    #Vanilla video capture
    ret, frame = cap.read()
    # Display the resulting frame
    cv2.imshow('frame', frame)


    #Vanilla image to display
    cv2.imshow('Picture', pic)


    #Transformed image to project

    transform = pic
    #transform here
    cv2.namedWindow('Projector', 0)
    cv2.setWindowProperty('Projector',  0, cv2.cv.CV_WINDOW_FULLSCREEN)
    cv2.imshow('Projector', transform)



    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()