import argparse
import cv2
import imutils
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("-i","--image", help = "path to the image file")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])


lower = np.array([0,0,0])
upper = np.array([15,15,15])
shapeMask = cv2.inRange(image, lower , upper)

cnts = cv2.findContours(shapeMask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
print = ("I found {} black shapes").format(len(cnts))
cv2.imshow("mask",shapeMask)


for c in cnts:
    cv2.drawContours(image, [c], -1 , (0,255,0), 2)
    cv2.imshow("iamge", image)

    cv2.waitKey(0)
    cv2.destroyAllWindows()