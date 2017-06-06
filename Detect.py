import cv2
from glyphfunctions import *

QUADRILATERAL_POINTS = 4
SHAPE_RESIZE = 100.0
BLACK_THRESHOLD = 100
WHITE_THRESHOLD = 155
GLYPH_PATTERN = [1, 0, 1, 0, 1, 0, 1, 0, 1]

#chargement du facecascad
faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

def detect_face(picture):
    gray = cv2.cvtColor(picture, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )
    face_found = False
    for (x, y, w, h) in faces:
        face_found = True
    if face_found == True:
        center = [x, y, w, h]
        return center
    else:
        return None

def detect_glyph (picture):

    gray = cv2.cvtColor(picture, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(gray, 100, 200)
    _, contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

    for contour in contours:
        perimeter = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.01 * perimeter, True)

        if len(approx) == QUADRILATERAL_POINTS:
            topdown_quad = get_topdown_quad(gray, approx.reshape(4, 2))
            resized_shape = resize_image(topdown_quad, SHAPE_RESIZE)

            if resized_shape[5, 5] > BLACK_THRESHOLD:
            #if resized_shape[(resized_shape.shape[0]/100)*5, (resized_shape.shape[1]/100)*5] > BLACK_THRESHOLD:
                continue
            glyph_found = False


            for i in range(4):
                glyph_pattern = get_glyph_pattern(resized_shape, BLACK_THRESHOLD, WHITE_THRESHOLD)

                if glyph_pattern == GLYPH_PATTERN:
                    glyph_found = True
                    break

                resized_shape = rotate_image(resized_shape, 90)

            if glyph_found:

                coord = approx.reshape(4, 2)
                mid_x = (coord[2][1] + coord[0][1])/2
                mid_y = (coord[2][0] + coord[0][0])/2

                center = [mid_x, mid_y]
                return center
