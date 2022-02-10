import cv2
import numpy as np 
import serial 
import time

Serial = serial.Serial("/dev/ttyUSB0",9600)
time.sleep(2)
#print(Serial.readline())

cap = cv2.VideoCapture(0)

while True:
    ret,frame  = cap.read()
    frame = cv2.flip(frame,1)
    #gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    if ret is False:
        break
    
    lower_color = np.array([162,93,136])
    upper_color = np.array([179,255,255])

    rows,cols,_ = frame.shape

    mask = cv2.inRange(hsv,lower_color,upper_color)
    contours,ret = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    bitwise = cv2.bitwise_and(frame,frame,mask=mask)
    
    cv2.line(frame,(cols//2-10,rows//2),(cols//2+10,rows//2),(0,255,0),2)
    cv2.line(frame,(cols//2, rows//2-10),(cols//2,rows//2+10),(0,255,0),2)
    cv2.circle(frame,(cols//2, rows//2),3,(0,0,255),-1)

    for cnt in contours:
        area  = cv2.contourArea(cnt)
        if area > 500:
            (x,y,w,h)  = cv2.boundingRect(cnt)
            cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
            cv2.line(frame,(x+int(w/2),0),(x+int(w/2),rows),(0,255,0),2)
            cv2.line(frame,(0,y+int(h/2)),(cols,y+int(h/2)),(0,255,0),2)
            pos = x-cols//2
            pos = str((x*180)//cols)
            print("gönderilen derece:    ",pos)

            Serial.write(pos.encode())
            #time.sleep(4)
    cv2.imshow("frame", frame)

    if cv2.waitKey(30) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
