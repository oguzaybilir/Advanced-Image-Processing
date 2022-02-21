from __future__ import print_function # __future__ kütüphanesi ilerleyen python sürümlerinde bile çalışacak bazı anlamsal işlemler yapar
from skimage.feature import peak_local_max # skimage kütüphanesi görüntü işleme üzerine çok yönlü işlemler yapabilen özel bir kütüphanedir 
from skimage.morphology import watershed 
from scipy  import ndimage #scipy numpy nin daha gelişmiş halidir.
import argparse #alıştığımız şeklin biraz daha kullanıcı dostu arayüzü oluşturmamızı sağlayan kütüphanedir
import imutils  #imutils kütüphanesi görseller üzerinde çalışırken kullanılan opencv ye yardımcı olan bir kütüphanedir yapay zekaya yatkın yerlerde kullanılır
import cv2 #görüntü işlemenin temelidir

ap = argparse.ArgumentParser() # terminale girile değeri almak için kullanılan fonksiyondur 
ap.add_argument("-i","--image",required=True, help="path to input image")   # dosya yolunun terminal üzerinden belirtmemizi sağlar
args=vars(ap.parse_args()) #girilen değerleri saklayan değişkendir                                             


image = cv2.imread(args["image"]) #args["image"] vars(ap.parse_args()) ın içinde sakladığı değeri işte burada kullandık
shifted = cv2.pyrMeanShiftFiltering(image,21,51) #pyramid mean shift filtresini uyguladık
gray = cv2.cvtColor(shifted,cv2.COLOR_BGR2GRAY) #klasik renk uzayı dönüşümü
thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]  #klasik threshold

contours = cv2.findContours(thresh.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE) #klasik olmayan kontur bulma, normalde cv2.RETR_TREE yazılırdı şimdi cv2.RETT_EXTERNAL yazdık
contours = imutils.grab_contours(contours) #imutils hiyerearşi yapısı olmadan konturleri sıralamada kullanılır
print("[INFO] {}  unique contours found".format(len(contours)))

for (i, c) in enumerate(contours):  # konturleri numaralandırdık
    ((x,y), _) = cv2.minEnclosingCircle(c)
    cv2.putText(image, "#{}".format(i+1), (int(x)-10, int(y)),cv2.FONT_HERSHEY_SIMPLEX,0.6,(0,0,255),2)
    cv2.drawContours(image, [c],-1,(0,255,0),2)

cv2.imshow("thresh",thresh)
cv2.imshow("input",image)

cv2.waitKey(0)
cv2.destroyAllWindows()
