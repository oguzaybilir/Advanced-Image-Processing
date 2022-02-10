import transform
from skimage.filters import threshold_local
import numpy as np
import argparse
import cv2
import imutils

ap = argparse.ArgumentParser()
ap.add_argument("-i","--image",required="True",help="path to the input image")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])
ratio = image.shape[0]/500.0
orig = image.copy()
image = imutils.resize(image,height=500)

gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray,(5,5),0)
edged = cv2.Canny(gray,110,50)

print("ADIM 1: KENAR TESPITI")
cv2.imshow("Image",image)
cv2.imshow("Edged",edged)
cv2.waitKey(0)
cv2.destroyAllWindows()

cnts = cv2.findContours(edged.copy(),cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)

cnts = sorted(cnts, key = cv2.contourArea, reverse=True)[:5]

for c in cnts:

    perimeter = cv2.arcLength(c,True)

    approx = cv2.approxPolyDP(c,0.02*perimeter, True)

    (x,y,w,h) = cv2.boundingRect(c)
    
    (cx,cy),r = cv2.minEnclosingCircle(c)

    cv2.rectangle(orig,(int(x),int(y)),(int(x+w),int(x+h)),(255,0,0),2)
    cv2.imshow("points",orig)


    if len(approx) == 4:
        screenCnt = approx
        break

print("ADIM 2: KONTURLER CIZILDI")

cv2.drawContours(gray,[c],-1,(0,0,255),1)
cv2.imshow("outline",gray)
cv2.waitKey(0)
cv2.destroyAllWindows()

warped = transform.four_points_transform(orig,screenCnt.reshape(4,2)*ratio)

warped = cv2.cvtColor(warped,cv2.COLOR_BGR2GRAY)
T = threshold_local(warped,19,offset=10,method="gaussian")
warped = (warped > T).astype("uint8")*255

print("ADIM 3 : PERSPEKTIF DONUSUMUNU UYGULUYORUZ")
cv2.imshow("original", imutils.resize(orig,height=650))
cv2.imshow("Scanned",imutils.resize(warped,height=650))
cv2.waitKey(0)
cv2.destroyAllWindows()