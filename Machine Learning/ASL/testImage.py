import cv2
from cvzone.HandTrackingModule import HandDetector
from cvzone.ClassificationModule import Classifier
import numpy as np
import math
import sys
import tensorflow as tf

#Followed this video tutorial
#https://www.youtube.com/watch?v=wa2ARoUUdU8
#We Train the model in Teachable machine

def signLang(file):
    offset = 20
    imgSize = 300
    labels = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
    k = cv2.waitKey(0)
    detector = HandDetector(maxHands=1)
    classifier = Classifier("Model/keras_model.h5", "Model/labels.txt")

    #Reads the image from the adjacent file to testImage.py
    img = cv2.imread((file))
    if img is None:
        sys.exit("Image not Found")

    imgOutput = img.copy()
    hands, img = detector.findHands(img)
    #Detects hand pressence
    if hands:
        try:
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
                imgWhite[:, wGap:wCal+wGap] = imgResize
                    
                #Send our image to our model, it well classify img
                prediction, index = classifier.getPrediction(imgWhite, draw=False)
                print(prediction, index)
                
            else:
                k = imgSize/w
                hCal = math.ceil(k*w)
                imgResize = cv2.resize(imgCrop, (imgSize, hCal))
                imgResizeShape = imgResize.shape
                    
                #We need to center it, we have a set height
                #so we need to shift h to be 300
                hGap = math.ceil((imgSize-hCal)/2)
                imgWhite[hGap:hCal+hGap, :] = imgResize
                #Send our image to our model, it well classify img
                prediction, index = classifier.getPrediction(imgWhite, draw=False)
                print(prediction, index)
                
            cv2.putText(imgOutput, labels[index],(x,y-offset), cv2.FONT_HERSHEY_COMPLEX, 2, (255,0,255), 2,)
            cv2.rectangle(imgOutput, (x-offset,y-offset), (x+w+offset, y+h+-offset), (255,0,255), 2)
        except:
            #Hand may sometimes be inside or outside the boundaries
            sys.exit("Hands out of Bounds Error")
        cv2.imshow("Image",imgOutput)
        key = cv2.waitKey(0)
    else:
        print("No hands detected Bozo")
        
    return labels[index]