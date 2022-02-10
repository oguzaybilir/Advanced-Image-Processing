import seam_carving
from skimage import filters
import argparse
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-i","--image",required=True,help="path to input image")
ap.add_argument("-d","--direction",help="seam removal direction")
args = vars(ap.parse_args())


image = cv2.imread(args["image"])
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

mag = filters.sobel(gray.astype("float"))

cv2.imshow("original image",image)
cv2.waitKey(0)

for numSeams in range(20,140,20):
    carved = seam_carving.carve_seam(image,mag,args["direction"],numSeams)
    print(" [INFO] removing {} seams;   new size: ""w={}, h={}".format(numSeams, carved.shape[1],carved.shape[0]))

    cv2.imshow("Carved",carved)
    cv2.waitKey(0)

"""
kodlar çöp seam_carving skimageden kaldırılmış
"""
