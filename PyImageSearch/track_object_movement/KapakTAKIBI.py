import cv2
from cv2 import COLOR_HSV2BGR
from cv2 import COLOR_BGR2HSV
import numpy as np  #kütüphaneleri import ettik

cap= cv2.VideoCapture(0)  #şuan görüntü olarak kamerayı kullanacağımızı belli ettik. 

#şimdi de bir trackbar oluşturmamız gerekiyor.

def nothing(x):
    pass

cv2.namedWindow("Trackbar") #pencereye isim verdik.
cv2.resizeWindow("Trackbar",500,500) #burada trackbar boyutlarını oluşturdum.

cv2.createTrackbar("Lower-H","Trackbar",0,180,nothing) #ilk baştaki trackbar'da hangi isimle görüneceği olacak.
cv2.createTrackbar("Lower-S","Trackbar",0,255,nothing) #ilk baştaki trackbar'da hangi isimle görüneceği olacak.
cv2.createTrackbar("Lower-V","Trackbar",0,255,nothing) #ilk baştaki trackbar'da hangi isimle görüneceği olacak.
#şimdi gördüğünüz gibi alt değerleri oluşturduk şimdi Upper H-S-V oluşturma zamanı.

cv2.createTrackbar("Upper-H","Trackbar",0,180,nothing) #ilk baştaki trackbar'da hangi isimle görüneceği olacak.
cv2.createTrackbar("Upper-S","Trackbar",0,255,nothing) #ilk baştaki trackbar'da hangi isimle görüneceği olacak.
cv2.createTrackbar("Upper-V","Trackbar",0,255,nothing)

#en son değerlerimin 0'dan başlaması mantıksız ona bir çözüm bulmak amacıyla

cv2.setTrackbarPos("Upper-H","Trackbar",180)
cv2.setTrackbarPos("Upper-S","Trackbar",255)
cv2.setTrackbarPos("Upper-V","Trackbar",255)

#şimdi trackbar'ımı tam anlamıyla oluşturdum.
#şimdi de kameradan görüntüdeki kontrol etmek için while döngüsü oluşturuyorum.
while True:
    ret,frame = cap.read()
    frame= cv2.flip(frame,1) #buna takla attırmam lazım. y eksenine göre takla attıyoruz. aynadaki gibi görmemiz için.
    
    frameHsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

    lowerH = cv2.getTrackbarPos("Lower-H","Trackbar")
    lowerS = cv2.getTrackbarPos("Lower-S","Trackbar")
    lowerV = cv2.getTrackbarPos("Lower-V","Trackbar")


    upperH = cv2.getTrackbarPos("Upper-H","Trackbar")
    upperS = cv2.getTrackbarPos("Upper-S","Trackbar") #burada en üst değerlerimizi bir değişkene atadık.
    upperV = cv2.getTrackbarPos("Upper-V","Trackbar")

    yellow1=np.array([0,137,162])
    yellow2=np.array([180,255,251])  #sarı rengin trackbar'dan bulup şimdi sadeece takip etmesini sağlayabilirim.

    mask= cv2.inRange(frame,yellow1,yellow2) #maskelemek için 3 tane değişkenimi girdim.

    bitAnd = cv2.bitwise_and(frameHsv,frame,mask)
    #bitRGB = cv2.cvtColor(bitAnd, cv2.COLOR_BGR2RGB)

     
    #cv2.imshow("bitwise", bitRGB)
    cv2.imshow("orijinal", frame)
    cv2.imshow("masked1", mask)

    if cv2.waitKey(30) & 0xFF== ord('q'):
        break

cap.release() #görüntüyü serbest bırakmamız için yazdığımız kodlar.
cv2.destroyAllWindows