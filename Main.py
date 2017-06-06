import numpy as np
import cv2
import time
from Detect import *

WIDTH = 1024
HEIGHT = 768

start = time.time()

cap = cv2.VideoCapture(1)
cap.set(3,WIDTH)
cap.set(4,HEIGHT)

"""
Situation
Projecteur fixe perpendiculaire à un mur
Caméra mobile filmant le cadre exact de la projection
"""

#Projetter une image témoin centré
fond = cv2.imread('fond.png')
face = cv2.imread('face.png')
x_offset = int(WIDTH/2 - 50)
y_offset = int(HEIGHT/2 - 87)
fond[y_offset:y_offset+face.shape[0], x_offset:x_offset+face.shape[1]] = face
cv2.imshow('render',fond)

#chargement du facecascad
faceCascade = cv2.CascadeClassifier("C:\Python27\Lib\site-packages\opencv\sources\data\haarcascades\haarcascade_frontalface_default.xml")

#Set abs et ordo à none
xv = None
yv = None
vv = None
wv = None

"""Récupération des coordonnées vidéos du témoin pour en trouver le décalage"""
while (True):
    print("Recup temoin")
    """Récupérer les coordonnées virtuelles vv,wv de la face témoin"""
    ret, frame = cap.read()
    position_face = detect_face(frame)
    if position_face is not None:
        print("Trump detected")
        # Abs haute de la face
        x = position_face[0]
        # Ordo haute de la face
        y = position_face[1]
        #Largeur de la face
        w = position_face[2]
        #Longueur de la face
        h = position_face[3]
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 0), 2)
        cv2.imwrite("facedetection.jpg", frame)
        #Changement de plan pour avoir les coordonées
        vv = x + (w/2)
        wv = y + (h/2)
        #Calcul du shift de calibration
        xshift = vv - WIDTH/2
        yshift = wv - HEIGHT/2
        print("Shifting")
        print(xshift, yshift)
        print(time.time() - start)
        print("Coordos virtuelles de la face")
        print(vv, wv)
        break

while (True):

    #Capture vidéo en continue
    ret, frame = cap.read()
    """Récupérer les coordonnées virtuel xv,yv du glyphe"""
    position_cross = detect_glyph(frame)
    if position_cross is not None:
        print("Glyph detected")
        #Abs du glyph
        xv = position_cross[0]
        #Ordo du glyph
        yv = position_cross[1]
        cv2.circle(frame, (int(xv), int(yv)), 10, (0, 0, 255), -1)
        print("Coordos vidéos du glyph")
        print(xv, yv)
        """Calculer les coordonnées réels xr/yr du glyphe grâce à la transformation subie par le témoin """
        xr = xv + (vv - WIDTH/2)
        yr = yv + (wv - HEIGHT/2)
        print("Coordos reels du glyph")
        print(xr,yr)
        """Projetter l'image en xr, yr, elle sera bien sur le glyph"""
        x_offset = int(xr - 50)
        y_offset = int(yr - 87)
        fond2 = cv2.imread('fond.png')
        fond2[y_offset:y_offset + face.shape[0], x_offset:x_offset + face.shape[1]] = face
        cv2.imshow('render', fond2)
        """On enrgistre l'image projetté et le moment ou le point de l'image où est detecté le glyph pour vérifier"""
        cv2.imwrite("render.jpg", fond2)
        cv2.imwrite("screen.jpg", frame)

    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
