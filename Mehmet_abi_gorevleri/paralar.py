import cv2
import numpy as np

img = cv2.imread("C:/Users/oguza/Desktop/opencvresimler/paralar.jpg")

gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
ret,thresh = cv2.threshold(gray,127,255,cv2.THRESH_BINARY)

contours,ret = cv2.findContours(img,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)




for cnt in contours:
   area = cv2.contourArea(cnt)

cv2.imshow("thresh",thresh)

cv2.imshow("img",img)
cv2.waitKey(0)
cv2.destroyAllWindows()
    



