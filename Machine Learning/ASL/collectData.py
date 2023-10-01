import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np
import math
import time

#We Train the model in Teachable machine

offset = 20
imgSize = 300
counter = 0 

folder = "data/Z"

cap = cv2.VideoCapture(0)
detector = HandDetector(maxHands=1)
#continously run the camera
while True:
    success, img = cap.read()
    hands, img = detector.findHands(img)
    #Detects hand pressence
    if hands:
        #B/C the size of hand is modular, we need a set size param to fit it in
        #Thus the implmentation of imgWhite
        #Detects the x, y, width, and height
        hand = hands[0]
        x,y,w,h = hand['bbox']
        
        #Creates a white background
        imgWhite = np.ones((imgSize, imgSize, 3), np.uint8)*255
        imgCrop = img[y-offset:y+h+offset,x-offset:x+w+offset]
        
        #Overlay the White on Hand
        imgCropShape = imgCrop.shape
        
        #We need to stretch the boundries such that we leave no void space from overlay
        aspectRatio = h/w
        if aspectRatio > 1:
            k = imgSize/h
            wCal = math.ceil(k*w)
            imgResize = cv2.resize(imgCrop, (wCal, imgSize))
            imgResizeShape = imgResize.shape
            
            #We need to center it, we have a set width
            #so we need to shift w to be 300
            wGap = math.ceil((imgSize-wCal)/2)
            try:
                imgWhite[:, wGap:wCal+wGap] = imgResize
            except:
                print("minor error")
        
        else:
            k = imgSize/w
            hCal = math.ceil(k*w)
            imgResize = cv2.resize(imgCrop, (imgSize, hCal))
            imgResizeShape = imgResize.shape
            
            #We need to center it, we have a set height
            #so we need to shift h to be 300
            hGap = math.ceil((imgSize-hCal)/2)
            try:
                imgWhite[hGap:hCal+hGap, :] = imgResize
            except:
                print("minor error")
        
        cv2.imshow("ImageCrop",imgCrop)
        cv2.imshow("ImageWhite",imgWhite)
        
        
    cv2.imshow("Image",img)
    key = cv2.waitKey(1)
    if key == ord("s"):
        counter += 1
        cv2.imwrite(f'{folder}/Image_{time.time()}.jpg', imgWhite)
        print(counter)
    