import cv2
import numpy as np
import imutils
import pytesseract

#hsv degerleri  H (94, 115), S (90, 255), V (36,255) 


img = cv2.imread("bmw.jpg.jpg")
img = imutils.resize(img,width=500)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

cv2.imshow("original",img)
cv2.imshow("gray",gray)
cv2.waitKey(0)

bilateral = cv2.bilateralFilter(gray,11,17,17)
bilateral2 = cv2.bilateralFilter(img,11,17,17)
edged = cv2.Canny(bilateral,30,200)

lower = np.array([0,90,0])
upper = np.array([0,255,0])
hsv = cv2.cvtColor(bilateral2,cv2.COLOR_BGR2HSV)
mask = cv2.inRange(hsv,lower,upper)
bitwise = cv2.bitwise_and(img,img,mask=mask)

cv2.imshow("hsv",hsv)
cv2.imshow("mask",mask)
cv2.imshow("bitwise",bitwise)
cv2.waitKey(0)


cv2.imshow("bilateral",bilateral)
cv2.imshow("edged",edged)
cv2.waitKey(0)

contours = cv2.findContours(edged.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
contours = imutils.grab_contours(contours)
contours = sorted(contours, key = cv2.contourArea, reverse=True)[:10]

location = None
for contour in contours:
    approx = cv2.approxPolyDP(contour,10,True)
    if len(approx) == 4:
        location = approx
        break

print("aradıgimiz alanin konum bilgileri:   ",location)

mask = np.zeros(gray.shape,np.uint8)
new_image = cv2.drawContours(mask,[location],0,255,-1)
new_image = cv2.bitwise_and(img,img,mask=mask)

last_image = cv2.cvtColor(new_image,cv2.COLOR_BGR2RGB)

cv2.imshow("new image",last_image)
cv2.waitKey(0)

(x,y) = np.where(mask==255)
(x1,y1) = (np.min(x),np.min(y))
(x2,y2) = (np.max(x),np.max(y))
cropped = gray[x1:x2, y1:y2]
cropped = imutils.resize(cropped,width=600)

cropped_last = cv2.cvtColor(cropped,cv2.COLOR_BGR2RGB)

cv2.imshow("cropped",cropped_last)
cv2.waitKey(0)

dst = cv2.fastNlMeansDenoising(cropped, 31, 7, 21)

cv2.imshow("denoised image",dst)
cv2.waitKey(0)

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
text = pytesseract.image_to_string(cropped_last)
print(text)

font = cv2.FONT_HERSHEY_SIMPLEX
cv2.rectangle(img, tuple(approx[0][0]-3), tuple(approx[2][0]-1), (0,255,0),3)
cv2.putText(img,text=text,org=(approx[0][0][0]-300, approx[1][0][1]+110),fontFace=font,fontScale=1,color=(0,0,255),lineType=cv2.LINE_AA)

cv2.imshow("image",img)
cv2.waitKey(0)
cv2.destroyAllWindows()
