import cv2
import numpy as np
import serial as s
import time

Serial = s.Serial("/dev/ttyUSB0",9600)
time.sleep(2)

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

    cv2.line(frame, (int(cols/2),0), (int(cols/2),rows), (80,12,255),3)
    cv2.putText(frame,"led yanar", (20,50),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),cv2.LINE_4)
    cv2.putText(frame,"led yanmaz", (int(cols/2)+30, 50), cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),cv2.LINE_4)

    for cnt in contours:
        area =  cv2.contourArea(cnt)
        if area > 100:
            (x,y,w,h) = cv2.boundingRect(cnt)
            cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),thickness=2)
            cv2.line(frame,(x+int(w/2),0),(x+int(w/2),rows),(0,255,0),2)
            cv2.line(frame,(0,y+int(h/2)),(cols,y+int(h/2)),(0,255,0),2)
            #cv2.putText(frame,"led kapanır",())
            if x < int(cols/2):
                Serial.write(b'1')
                print("led yandi")
            else:
                Serial.write(b'0')
                print("led kapatildi")

            
    cv2.imshow("frame",frame)
    #cv2.imshow("mask",mask)
    #v2.imshow("bitwise",bitwise)

    if cv2.waitKey(20) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()