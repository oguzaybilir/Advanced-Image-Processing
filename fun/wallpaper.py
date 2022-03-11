import cv2
import argparse
import imutils


ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path to the image")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])

image1 = cv2.resize(image,(1920,1080))
image2 = imutils.resize(image,width = 1080)

cv2.imwrite("wallpaper1.jpg",image1)
cv2.imwrite("wallpaper2.jpg",image2)

cv2.waitKey(0)
cv2.destroyAllWindows()