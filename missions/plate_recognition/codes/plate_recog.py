from calendar import c
import numpy as np
import cv2
import argparse
import imutils
from sympy import re

ap = argparse.ArgumentParser()
ap.add_argument("-i","--image",required=True,help="path to input image")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])
image = imutils.resize(image,width=700)
blur = cv2.GaussianBlur(image,(5,5),1)
gray = cv2.cvtColor(blur,cv2.COLOR_BGR2GRAY)

edges = cv2.Canny(gray,30,100)

#sobelx = cv2.Sobel(gray, ddepth=cv2.CV_64F, dx=1, dy=0, ksize=5) 
sobelx = cv2.Sobel(gray, ddepth=cv2.CV_64F, dx=0, dy=1, ksize=5) 
#sobelxy = cv2.Sobel(gray, ddepth=cv2.CV_64F, dx=1, dy=1, ksize=5) 

thresh = cv2.adaptiveThreshold(edges,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,11,2)
#dilation = cv2.dilate(thresh,(5,5))
#closing = cv2.morphologyEx(thresh,cv2.MORPH_CLOSE,(7,7))
contours, _ = cv2.findContours(thresh.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)

for c in contours:
    if contours:
        area = cv2.contourArea(c)
        (x,y,w,h) = cv2.boundingRect(c)
        cv2.drawContours(image,[c],-1,(0,0,255),2)
        cv2.imshow("contours",image)
        cv2.waitKey(0)


#cv2.imshow("sobel x",sobelx)
cv2.imshow("sobel y",sobely)
#cv2.imshow("sobel xy",sobelxy)
#cv2.imshow("closing",closing)
#cv2.imshow("dilation",dilation)
#cv2.imshow("original",image)
#cv2.imshow("blur",blur)
#cv2.imshow("gray",gray)
cv2.imshow("edges",edges)
cv2.imshow("threshold",thresh)
cv2.waitKey(0)