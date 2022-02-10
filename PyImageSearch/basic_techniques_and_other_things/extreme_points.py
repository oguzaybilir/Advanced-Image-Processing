import argparse     #gerekli kütüphaneleri import ediyoruz
import numpy as np
import imutils
import cv2


ap = argparse.ArgumentParser()      #kullanıcıdan veri girişi alıyoruz
ap.add_argument("-i","--image", required=True, help="path to the image file")
args = vars(ap.parse_args())
image = cv2.imread(args["image"])

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)      #resmi griye dönüştürüyoruz
gray = cv2.GaussianBlur(gray,(5,5),0)   #resimdeki gürültüleri yok etmek için blur uyguladık

threshold = cv2.threshold(gray,65,255,cv2.THRESH_BINARY)[1]     #resmi binary sisteme geçirmek için threshold uyguladık
threshold = cv2.erode(threshold, None, iterations=2)    #resimdeki beyaz yerleri (yani istediğimiz nesneyi) erozyona uğratarak tıraşladık
threshold = cv2.dilate(threshold, None, iterations=2)   #resimdeki beyaz yerleri (yani istediğimiz nesneyi) kalınlaştırıyoruz yani 1 leri arttırıyoruz

cnts = cv2.findContours(threshold.copy(),cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)    #thresholda uğrattığımız resmin konturunu bulduruyoruz
cnts = imutils.grab_contours(cnts)  #buldurduğumuz konturleri hiyerarşi sırasına uygun olmadan sıralıyoruz
c = max(cnts, key=cv2.contourArea)  #konturlerin alanlarına göre büyükten küçüğe bir sıralama yapıyoruz

extLeft = tuple(c[c[:, :, 0].argmin()][0])  #en soldaki bulunan konturu alıyoruz
extRight = tuple(c[c[:, :, 0].argmax()][0]) #en sağdaki bulunan konturu alıyoruz
extTop = tuple(c[c[:, :, 1].argmax()][0])   #en üstteki bulunan konturu alıyoruz   
extBot = tuple(c[c[:, :, 1].argmin()][0])   #en alttaki bulunan konturu alıyoruz

cv2.drawContours(image, [c],-1,(0,255,0),2) #üst satırlardaki sisteme göre buldurduğumuz kontürleri çizdiriyoruz

cv2.circle(image, extLeft, 8, (0,0,255),-1) #en sol noktaya circle çizdiriyoruz
cv2.circle(image, extRight, 8, (0,255,0), -1)   #en sağ noktaya circle çizdiriyoruz
cv2.circle(image, extTop, 8, (255,0,0),-1)  #en tepe noktaya circle çizdiriyoruz
cv2.circle(image, extBot, 8, (255,255,0),-1)    #en alt noktaya circle çizdiriyoruz

cv2.imshow("thresh",threshold)  #threshold edilmiş resmi imshow ettirdik    
cv2.imshow("image",image)   #konturleri bulunmuş ve circle çizilmiş resmi imshow ettirdik
cv2.waitKey(0)  #resmin ekranda görüntülenme süresini belirler
cv2.destroyAllWindows() #açılan pencerenin rahatça kapatılmasını sağlıyoruz