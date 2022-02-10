import cv2
import argparse
from datetime import datetime

#ap = argparse.ArgumentParser()
#ap.add_argument("-i","--image",required=True,help="path to the input image")
#ap.add_argument("-x","--xml",required=True,help="path to the input image")

#args = vars(ap.parse_args())

#img = cv2.imread(args["image"])
cap = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier("/home/oguzay/Documents/GitHub/HAARCASCADE/haarCascadeImagesXml/frontal_face.xml.xml")

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame,1)
    copy_frame = frame.copy()

    if ret is True:

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(frame,1.1,8) #yüz bulunacak yer, ölçeklendirme oranı, yüz arayacak kare sayısı

        for (x,y,w,h) in faces:
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),3)
        try:

            roi = copy_frame[y:y+h, x:x+w]

            if cv2.waitKey(20) == ord('s'):

                tarih = datetime.now().strftime("%H_%M_%S")
                cv2.imwrite(f'/home/oguzay/Documents/GitHub/HAARCASCADE/negative/oguzay{tarih}.png',roi) 
                print("resim kaydedildi")
        except:
            print("yüz bulamadi")


        if cv2.waitKey(20) == ord('q'):
            break

        cv2.imshow("frame",frame)
        cv2.imshow("roi",roi)
    
  

cap.release()
cv2.destroyAllWindows()