from skimage.segmentation import clear_border       #   gerekli kütüphaneleri import ediyoruz
from imutils import contours
import numpy as np
import argparse
import imutils
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-i","--image",required=True,help="path to input image")
ap.add_argument("-r","--reference",required=True,help="path to reference")
args = vars(ap.parse_args())

charNames = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0",
	"T", "U", "A", "D"]

ref = cv2.imread(args["reference"])
ref = cv2.cvtColor(ref,cv2.COLOR_BGR2GRAY)
ref = imutils.resize(ref,width=400)
ref = cv2.threshold(ref,0,255,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]


refCnts = cv2.findContours(ref.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
refCnts = imutils.grab_contours(refCnts)
refCnts = contours.sort_contours(refCnts, method="left-to-right")[0]

clone = np.dstack([ref.copy()] * 3)

for c in refCnts:
	(x, y, w, h) = cv2.boundingRect(c)
	cv2.rectangle(clone, (x, y), (x + w, y + h), (0, 255, 0), 2)

cv2.imshow("Simple Method", clone)
cv2.waitKey(0)