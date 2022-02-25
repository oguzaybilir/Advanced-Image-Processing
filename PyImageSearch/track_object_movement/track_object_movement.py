from collections import deque
import numpy as np
import argparse
import cv2
import imutils
import time

ap = argparse.ArgumentParser()  # kullanıcıdanm veri girisi aldık
ap.add_argument("-v","--video",help="path to the video file")
ap.add_argument("-b","--buffer", type=int, default=32, help="max buffer size")
args = vars (ap.parse_args())

greenLower = (0,137,162)   #yeşil rengin hsv kodlarini girdik
greenUpper = (180,255,251)

pts = deque(maxlen=args["buffer"])  #noktaları deque ile sıraya dizdik
counter = 0
(dX, dY) = (0,0)    
direction = ''

if args["video"] == None:
    cap = cv2.VideoCapture(0)
else:
    cap = cv2.VideoCapture(args["video"]) 

time.sleep(2)

while True:
    ret,frame = cap.read()
    frame = cv2.flip(frame,1)

    if ret == False:
        break
    frame = imutils.resize(frame, width = 600)
    blur = cv2.GaussianBlur(frame, (11,11),0)
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, greenLower, greenUpper)
    mask = cv2.erode(mask, None, iterations=1)
    mask = cv2.dilate(mask, None, iterations=2)

    cnts = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    center = None

    rows,cols,_ = frame.shape

    if len(cnts) > 0:
        c = max(cnts, key=cv2.contourArea)
        ((x,y),radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = int((M["m10"]/M["m00"])),int((M["m01"]/M["m00"]))

        if radius > 10:
            (cx,cy,w,h) = cv2.boundingRect(c)
            cv2.circle(frame, (int(x),int(y)),int(radius),(0,255,255),2)
            cv2.circle(frame,center,5,(0,0,255),-1)
            cv2.rectangle(frame,(cx,cy),(cx+w,cy+h),(255,0,0),2)
            cv2.line(frame,(cx+int(w/2),0),(cx+int(w/2),rows),(0,255,0),2)
            cv2.line(frame,(0,cy+int(h/2)),(cols,cy+int(h/2)),(0,255,0),2)
            pts.appendleft(center) 

    if len(pts) > 11:

        for i in np.arange(1, len(pts)):
            
            if pts[i - 1] is None or pts[i] is None:
                continue
            if counter >= 200 and i == 1 and pts[-20] is not None:
                dX = pts[-10][0] - pts[i][0]
                dY = pts[-10][1] - pts[i][1]
                (dirX, dirY) = ("", "")
                if np.abs(dX) > 20: 
                    dirX = "East" if np.sign(dX) == 1 else "West"
                if np.abs(dY) > 20:
                    dirY = "North" if np.sign(dY) == 1 else "South"
                if dirX != "" and dirY != "":
                    direction = "{}-{}".format(dirY,dirX)
                else:
                    direction = dirX if dirX != "" else dirY
            thickness = int(np.sqrt(args["buffer"]/float(i +1))*2.5)
            cv2.line(frame, pts[i - 1], pts[i], (0,0,255), thickness)
        cv2.putText(frame, direction, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,0.65, (0, 0, 255), 3)
        cv2.putText(frame, "dx: {}, dy: {}".format(dX, dY),(10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,0.35, (0, 0, 255), 1)
    counter += 1
    cv2.imshow("frame",frame)
    key = cv2.waitKey(1)
    if key == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()