from typing_extensions import Required
from imutils.video import VideoStream
import argparse
import datetime
import imutils
import cv2

ap = argparse.ArgumentParser()  #argparse ile kullanicidan video yolunu ve takip edilecek objenin minimum alanın aldık
ap.add_argument("-v", "--video",help="path to the video file")
ap.add_argument("-a","--min-area",type=int, default=3000, help="minimum area size")
args = vars(ap.parse_args())

#print("bize ne veriyor",args["video"])

if args["video"] == None: #eğer video argümanı None ise (yoksa), webcami açıyoruz
    cap = cv2.VideoCapture(0)
    
else:
    cap = cv2.VideoCapture(args["video"])    #aksi halde ir video dosyasından alıyoruz


firstFrame = None   #Video akışından ilk frame'i alıyoruz
# ilk karede direkt obje olmayacağı için None olarak başlatıyoruz


while True: #framelerin içinde dönüyoruz

    ret, frame = cap.read()   #ilk frame i al ve dolu mu boş mu diye bak 
    text = "Unoccupied"

    if ret == False:   #   frame None ise
        break   #programı kapat

    frame = imutils.resize(frame, width=500)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0) #   görseldeki gürültüleri engellemek için GaussianBlur uyguluyoruz

    if firstFrame is None:  #   eğer firstFrame None ise
        firstFrame = gray   #   firstframe = gray al ve 
        continue            #   devam et

    frameDelta = cv2.absdiff(firstFrame, gray)  # frameDelta diye bir değişkene arkaplan temizleme uyguladığımız görseli atadık
    thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]   #frameDeltaya threshold uyguluyoruz

    thresh = cv2.dilate(thresh, None, iterations=5) #   threshold uyguladığımız görseli dilate ediyoruz
    cnts = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)   #   görseldeki konturleri bulduruyoruz
    cnts = imutils.grab_contours(cnts)  #   konturleri tutturuyoruz

    for c in cnts:  #   konturlerin içinde dolanıyoruz

        if cv2.contourArea(c) > args["min_area"]:   #   eğer konturlerin alanı bizim belirlediğimiz alandan küçükse devam et
            
            (x,y,w,h) = cv2.boundingRect(c) #   konturlerin x y koordinatlarını ve w h (genişlik uzunluk) değerlerini alıyoruz
            cv2.rectangle(frame,(x,y),(x+w, y+h),(0,255,0),2)   #   aldığımız x,y,w,h lar ile objenin etrafına bir dikdörtgen çizdiriyoruz
            text = "Occupied"

    cv2.putText(frame,"Room Status: {}".format(text),(10,20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255),2),

    cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),(10,frame.shape[0]-10),cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0,0,255),1)


    cv2.imshow("Security Feed",frame)
    #cv2.imshow("Thresh",thresh)
    cv2.imshow("Frame Delta",frameDelta)
    
    key = cv2.waitKey(1)

    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()