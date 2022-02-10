import argparse # gerekli kütüphaneleri, import ettik
import cv2
import numpy as np
import imutils

#bu ikisi bizim classlarımız ve bunları normal şekilde import ettiriyoruz
from ShapeDetector import ShapeDetector
from ColorLabeler import ColorLabeler

ap = argparse.ArgumentParser()  #   kullanıcıdan veri girişi aldık
ap.add_argument("-i","--image",required=True,help ="path to the input image")
args = vars(ap.parse_args())
image = cv2.imread(args["image"])   #   görseli okuttuk

resized = imutils.resize(image, width=300) #   görseli resize ettirdik
ratio = image.shape[0]/float(resized.shape[0])  #

blurred = cv2.GaussianBlur(resized,(5,5),0)    #   resmi blurluyoruz
gray = cv2.cvtColor(blurred,cv2.COLOR_BGR2GRAY)    #   resmi griye çevirdik
lab = cv2.cvtColor(blurred,cv2.COLOR_BGR2LAB)  #   görseli L*a*b* renk uzayına geçirdik
thresh = cv2.threshold(gray,60,255,cv2.THRESH_BINARY)[1]    #   görseli threshold ettik

cnts = cv2.findContours(thresh.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)    # görseldeki konturleri çizdirdik
cnts = imutils.grab_contours(cnts)  #   imutilsin kontur tutma fonksiyonunu kullandık

sd = ShapeDetector()    #PyImageSearch ün yazdığı class ı kullandık
cl = ColorLabeler()     #PyImageSearch ün yazdığı class ı kullandık

for c in cnts:

    M = cv2.moments(c)
    cX = int((M["m10"]/M["m00"])*ratio)
    cY = int((M["m01"]/M["m00"])*ratio)

    shape = sd.detect(c)
    color = cl.label(lab,c)

    c = c.astype("float")
    c *= ratio
    c = c.astype("int")

    text = "{} {}".format(color,shape)
    cv2.drawContours(image,[c],-1,(0,255,0),2)
    cv2.putText(image,text,(cX,cY),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255),2)


    cv2.imshow("image",image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()