from PIL import Image   #   Gerekli kütüphaneleri import ettik
import pytesseract
import cv2
import os
import argparse

ap = argparse.ArgumentParser()      #   kullanıcıdan okunacak resmi ve preprocess i aldık
ap.add_argument("-i","--image",required=True,help="path to input image")
ap.add_argument("-p","--preprocess",type=str, default="thresh",help="type of the preprocessing to be done")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])
gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

if args["preprocess"] == "thresh":
    gray = cv2.threshold(gray,0,255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

elif args["preprocess"] == "blur":
    gray = cv2.medianBlur(gray,3)

filename = "{}.png".format(os.getpid())
cv2.imwrite(filename,gray)

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
text = pytesseract.image_to_string(Image.open(filename))
os.remove(filename)
print(text)

cv2.imshow("ımage",image)
cv2.imshow("output",gray)
cv2.waitKey(0)
cv2.destroyAllWindows()



