import cv2
import numpy as np

img = cv2.imread("/home/oguzay/Downloads/coinss1.jpeg")

gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
blur = cv2.blur(gray,(5,5))
ret,threshold = cv2.threshold(blur,70,255,cv2.THRESH_BINARY)

contours,hierarchy = cv2.findContours(threshold,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

oncent = 0
bescent = 0

for cnt in contours:
    M = cv2.moments(cnt)
    if M['m00'] != 0:
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        cv2.drawContours(img,[cnt],-1,(0,255,0),4)
        cv2.circle(img,(cx,cy),2,(0,0,255),-1)
        area = cv2.contourArea(cnt)
        
        if area > 10000:
            cv2.putText(img,("10 cent"),(cx-20,cy-20),cv2.FONT_HERSHEY_SIMPLEX,1,cv2.LINE_AA)
            oncent += 10
        else:
            cv2.putText(img,("5 cent"),(cx-20,cy-20),cv2.FONT_HERSHEY_SIMPLEX,1,cv2.LINE_AA)
            bescent += 5
        toplam = bescent+oncent
        print("toplam para:"  , toplam)
        print(f"x: {cx}  y:{cy}")

cv2.imshow("img",img)
cv2.imshow("gray",gray)
cv2.imshow("threshold",threshold)

cv2.waitKey(0)
cv2.destroyAllWindows()

