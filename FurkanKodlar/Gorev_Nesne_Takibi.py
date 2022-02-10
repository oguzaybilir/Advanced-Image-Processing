import cv2
import numpy as np



cap = cv2.VideoCapture(0)




while(1):
    # Görüntü frame'i al
    _, frame = cap.read()
    # HSV uzayina donustur
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # Mavi rengin HSV uzayindaki araligi
    lower_blue = np.array([110,50,50])
    upper_blue = np.array([130,255,255])
    # HSV icindeki mavi rengi tespit edebilmek icin threshold
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    kernel = np.ones((3,3),np.uint8)
    mask = cv2.dilate(mask,kernel,iterations=1)
    mask = cv2.erode(mask,kernel,iterations=2)
    mask = cv2.medianBlur(mask,15)
    # Bitwise-AND islemi ve mask uygulaniyor
    img = cv2.bitwise_and(frame,frame, mask= mask)
    
    contours,_ = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    rows,cols,_ = frame.shape
    
    for cnt in contours:
        area = cv2.contourArea(cnt)

        if area > 1000:

            x,y,w,h = cv2.boundingRect(cnt)
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)
            cv2.line(frame,(x+int(w/2),0),(x+int(w/2),rows),(0,255,0),2)
            cv2.line(frame,(0,y+int(h/2)),(cols,y+int(h/2)),(0,255,0),2)
        


    cv2.imshow('frame',frame)
    cv2.imshow('mask',mask)
    cv2.imshow('img',img)
    if cv2.waitKey(20) & 0xFF==ord('q'):
        break
cv2.destroyAllWindows()