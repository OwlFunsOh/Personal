#sign language :D
import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np
import math
from cvzone.ClassificationModule import Classifier

#Setting up webcam. 0 is id number of webcam
captureObject = cv2.VideoCapture(0)

#Set up Hand detector
detector = HandDetector(maxHands = 1)
classifier = Classifier("Machine Learning\ASL\Model\keras_model.h5", "Machine Learning\ASL\Model\labels.txt")

#increasing the boundary of the hand detection box
offset = 20

#defining image size
imgSize = 300

labels = ["A", "B", "C"]

while True:
    try:
        #will capture image from webcam
        success, image = captureObject.read()

        #create a copy of the image
        imgOutput = image.copy()

        #hand detector will find hands in the image
        hands, image = detector.findHands(image)

        #cropping image
        #if there are hands
        if hands:
            #only have one hand so hands = 0
            hand = hands[0]

            #dimensions are x, y, width, and height
            x, y, w, h = hand['bbox']

            #Creating a fixed image
            #defining image size + add color
            #np.uint8 means integer values are from 0 to 255
            imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255 #multiply values by 255 to make white

            #y = starting height. h = height
            #x = starting width. w = width
            imgCrop = image[y - offset: y + h + offset, x - offset: x + w + offset]

            imgCropShape = imgCrop.shape


            #if height is bigger value
            aspectRatio = h/w

            #if value is above 1, then hieght is greather
            if aspectRatio > 1:
                #constant to stretch width
                k = imgSize / h
                #width calculated
                wCal = math.ceil(k*w)

                imgResize = cv2.resize(imgCrop, (wCal, imgSize))
                imgResizeShape = imgResize.shape

                #centering the image
                wGap = math.ceil((300 - wCal) / 2)

                #obtain height and width of imgCrop
                imgWhite[:, wGap:imgResizeShape[1] + wGap] = imgResize

                #gives prediction and index
                prediction, index = classifier.getPrediction(imgWhite)
                print(prediction, index)
            else:
                k = imgSize / w
                hCal = math.ceil(k * h)
                imgResize = cv2.resize(imgCrop, (imgSize, hCal))
                imgResizeShape = imgResize.shape
                hGap = math.ceil((imgSize - hCal) / 2)
                imgWhite[hGap:hCal + hGap, :] = imgResize

                #gives prediction and index
                prediction, index = classifier.getPrediction(imgWhite)
                print(prediction, index)

            #cv2.imshow("ImageCrop", imgCrop)
            #cv2.imshow("ImageWhite", imgWhite)
            cv2.putText(imgOutput, labels[index], (x, y - 20), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 0, 255), 2)
    except:
        print("Minor error")

    cv2.imshow("Image", imgOutput)
    key = cv2.waitKey(1)