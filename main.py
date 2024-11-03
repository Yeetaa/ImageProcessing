import cv2
import numpy as np
from picamera2 import Picamera2

picam2 = Picamera2()
config = picam2.create_preview_configuration(main={"size": (640, 480)})
picam2.configure(config)
picam2.start()

#Blau im HSV-Farbraum
lower_color = np.array([110,50,50], dtype=np.uint8) #Untergrenze in HSV
upper_color = np.array([130,255,255], dtype=np.uint8) #Obergrenze in HSV


while True:
    frame = picam2.capture_array()

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) #Farbraumwechsel; bei Auskommentierung werden B und R gewechselt
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) #wechelst BGR-Frabraum zu HSV-Farbraum

    maske = cv2.inRange(hsv, lower_color, upper_color) #Erstellt Maske

    maske = cv2.erode(maske, None, iterations=2) # Minimiert Störung
    maske = cv2.dilate(maske, None, iterations=2) # Minimiert Störung

    contours, _ = cv2.findContours(maske, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) #Konturen; _ = ungenutzte Hierachie

    if contours:
        largest_contour = max(contours, key=cv2.contourArea) #Findet größte Contour

        x, y, w, h =cv2.boundingRect(largest_contour)

        cv2.rectangle(frame, (x, y), (x +w, y+ h), (0,255,0), 2) #Berechnet Rechteck um Farbe

    cv2.imshow('Frame', frame) #Zeichnet Frame
    #cv2.imshow('Maske', maske)

    if cv2.waitKey(1) & 0xFF == ord('q'): #Abbruch Bedingung
        break #Verlässt die While-True Schleife

picam2.stop()
cv2.destroyAllWindows
