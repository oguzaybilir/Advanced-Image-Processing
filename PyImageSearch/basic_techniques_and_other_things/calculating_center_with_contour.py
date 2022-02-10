import argparse #GEREKLI KUTUPHANELERI IMPORT ETTIK
import imutils
import cv2

ap = argparse.ArgumentParser()  #KULLANICIDAN RESMI ALDIK
ap.add_argument("-i","--image", required = True, help = "path to the input image")
args = vars(ap.parse_args())
img = cv2.imread(args["image"])  #RESME KLASIK GRAY, BLUR VE THRESHOLD TEKNİKLERİNİ UYGULADIK

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)    #RESMI GRI RENK UZAYINA CEVIRDIK
blur = cv2.GaussianBlur(gray,(5,5),0)   #RESIMDEKI GURULTULERI ENGELLEMEK ICIN BLUR UYGULADIK
thresh = cv2.threshold(blur, 80,150,cv2.THRESH_BINARY)[1]   #BLURLANMIS RESME THRESHOLD UYGULADIK
cv2.imshow("thresh",thresh) #THRESHOLD UYGULADIGIMIZ RESMI IMSHOW ETTIRECEGIZ

cnts = cv2.findContours(thresh.copy(),cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)   #KONTURLERI BULDURUYORUZ
cnts = imutils.grab_contours(cnts)  #CONTURLERI HIYERARSI SISTEMINE UYGUN OLMAYAN SEKILDE SIRALIYORUZ

for c in cnts:  #cnts ICINDE  c yi DONDURUYORUZ
    M = cv2.moments(c)  #BULUNAN KONTURLERIN MERKEZLERINI  BULDUK
    cX = int(M["m10"]/M["m00"]) #MERKEZIN X DEGERİ
    cY = int(M["m01"]/M["m00"]) #MERKEZIN Y DEGERİ

    cv2.drawContours(img, [c],-1, (0,255,0), 2) #BULDURDUGUMUZ KONTURLERI CIZDIRIYORUZ
    cv2.circle(img, (cX,cY), 7 , (255,255,255), -1) #MERKEZE BIR CIRCLE CIZDIRIYORUZ
    cv2.putText(img, "center", (cX-20, cY-20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 2)    #MERKEZI BELIRTEN BIR YAZI YAZDIRIYORUZ

    cv2.imshow("img",img)   #SON OLARAK KONTURLERIN CIZILMIS OLDUGU RESIMLERI IMSHOW ETTIRILDI
    cv2.waitKey(0)  #PENCERENIN EKRANDA KALMA SURESINI AYARLADIK
    cv2.destroyAllWindows() #ACILAN PENCERELERIN RAHATCA KAPATILMASINI SAGLADIK




