"""import cv2
path = "/home/oguzay/Downloads/imutils.jpg"
image = cv2.imread(path)

gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
print(image.shape)

cv2.imshow("image",image)"""

# BU KODUN AMACI BİZE NONETYPE ERROR ALMAYI/ALMAMAYI ÖĞRETMEKTİR AMA KODLARIN DOĞRUSUNU YAZDIĞIM İÇİN ÇALIŞIYORLAR

# videolar için dosya yolu string veya kameradan görüntü almak için integer olur

import argparse
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-i","--image",required = True, help = "path to the image file")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])
(h,w,d) = image.shape
print("w: {}, h:{}, d:{}".format(w,h,d))

cv2.imshow("image",image)
cv2.waitKey(0)
cv2.destroyAllWindows()