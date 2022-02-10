import cv2
import numpy as np

cap = cv2.VideoCapture(0)

while True:
    ret,frame = cap.read()
    frame = cv2.flip(frame,1)
    if ret is False:
        break
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
# yeşil renk için renk değerleri
    lower_color = np.array([0,163,161])
    upper_color = np.array([92,255,255])

    rows,cols,_ = frame.shape
    
    mask = cv2.inRange(hsv,lower_color,upper_color)
    contours,ret = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    bitwise = cv2.bitwise_and(frame,frame,mask = mask)

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 100:
            (x,y,w,h) = cv2.boundingRect(cnt)
            cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),thickness=2)
            cv2.line(frame,(x+int(w/2),0),(x+int(w/2),rows),(0,255,0),2)
            cv2.line(frame,(0,y+int(h/2)),(cols,y+int(h/2)),(0,255,0),2)
            
    cv2.imshow("frame",frame)
    cv2.imshow("mask",mask)
    cv2.imshow("bitwise",bitwise)

    if cv2.waitKey(20) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()