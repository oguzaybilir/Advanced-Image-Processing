import argparse
import numpy as np
import cv2
import imutils
from stitch_class import Stitcher

ap  = argparse.ArgumentParser()
ap.add_argument("-f","--firstimage",required=True,help="path to the first image")
ap.add_argument("-s","--secondimage",required=True,help="path to the second image")
args = vars(ap.parse_args())


imageA = cv2.imread(args["firstimage"])
imageB = cv2.imread(args["secondimage"])

imageA = imutils.resize(imageA,width=400)
imageB = imutils.resize(imageB,width=400)

stitcher = Stitcher()
(result,vis) = stitcher.stitch([imageA, imageB],showMatches=True)
print(result)
print(vis)

cv2.imshow("image A",imageA)
cv2.imshow("image B", imageB)
cv2.imshow("keypoint matches", vis)
cv2.imshow("result",result)

cv2.waitKey(0)
cv2.destroyAllWindows()