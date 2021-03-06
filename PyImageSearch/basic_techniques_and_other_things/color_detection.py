import numpy as np      
import argparse
import cv2

ap=argparse.ArgumentParser()
ap.add_argument("-i","--image",help = "path to image")
args = vars(ap.parse_args())

img = cv2.imread(args["image"])

boundaries = [
	([17, 15, 100], [50, 56, 200]),
	([86, 31, 4], [220, 88, 50]),
	([25, 146, 190], [62, 174, 250]),
	([103, 86, 65], [145, 133, 128])]

for (lower,upper) in boundaries:
    lower = np.array(lower, dtype = "uint8")
    upper = np.array(lower, dtype = "uint8")

    mask = cv2.inRange(img,lower, upper)
    output = cv2.bitwise_and(img, img, mask = mask)

cv2.imshow("images", np.hstack([img,output]))
cv2.waitKey(0)