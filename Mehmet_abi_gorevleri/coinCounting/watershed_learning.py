from time import thread_time
from skimage.feature import peak_local_max
from skimage.segmentation import watershed
from scipy import ndimage
import numpy as np
import argparse
import imutils
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-i","--image",required=True,help="path to input image")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])
image = cv2.resize(image,(480,640))
shifted = cv2.pyrMeanShiftFiltering(image,150,150)
cv2.imshow("shifted",shifted)

gray = cv2.cvtColor(shifted,cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, 0,255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
cv2.imshow("thresholded",thresh)

kernel = np.ones((3,3), np.uint8)
dilation = cv2.dilate(thresh, kernel, iterations = 3)
#dilation = cv2.GaussianBlur(dilation, (3, 3), 3)
#dilation = cv2.bilateralFilter(dilation,9,75,75)
cv2.imshow("dilation",dilation)


D = ndimage.distance_transform_edt(dilation) #oklid mesafe dönüşümü yapıyoruz
localMax =peak_local_max(D,indices=False,min_distance=5,labels=dilation)


markers = ndimage.label(localMax, structure = np.ones((3,3)))[0]
labels = watershed(-D, markers, mask=dilation)
print("[INFO] {} unique segments found".format(len(np.unique(labels))-1))

for label in np.unique(labels): 
    if label == 0:
        continue

    mask = np.zeros(gray.shape, dtype="uint8")
    mask[labels == label] = 255

    contours = cv2.findContours(mask.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    c = max(contours, key=cv2.contourArea)

    ((x,y),r) = cv2.minEnclosingCircle(c)
    
    cv2.circle(image,(int(x), int(y)),int(r), (0,255,0), 2)
    cv2.putText(image, "#{}".format(label), (int(x)-10, int(y)), cv2.FONT_HERSHEY_SIMPLEX,0.6,(0,0,255),2)
    
cv2.imshow("output",image)

cv2.waitKey(0)
cv2.destroyAllWindows()