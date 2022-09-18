import numpy as np
import cv2

def order_points(pts):  #noktaları bulan fonksiyonu yazıyoruz

    rect = np.zeros((4,2),dtype = "float32")    

    s = pts.sum(axis=1) #rectin içinde saklı olan sol üst yer bizim min degerimiz ve en dip sagdaki degerimiz ise max degerimiz (bu durumu analitik düzlemde düşün)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    


    diff = np.diff(pts,axis=1)  #türevini aldık

    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]

    return rect #düzenli koordinatları döndürüyoruz 

def four_points_transform(image,pts):   #pts değişkeni, roi alacağımız piksel değerlerini saklar
                                        #image değişkeni perspektif dönüşümü uygulayacağımız resmi saklar

    rect = order_points(pts)    #order points fonksiyonun çağırdık
                                #rect, roi alınacak 4 degeri saklar
    (tl,tr,br,bl) = rect    #order fonksiyonun bulduğu değerleri t,tr,br,bl degerlerine eşitledik

    widthA = np.sqrt(((br[0]-bl[1])**2)+((br[1]-bl[1])**2))     #analitik geometrideki 2 nokta arasındaki mesafe formulüyle 
    widthB = np.sqrt(((tr[0]-tl[0])**2)+((tr[1]-tl[1])**2))     #yeni resmin genişliğini buluyoruz 
    maxWidth = max(int(widthA), int(widthB))

    heightA = np.sqrt(((tr[0]-br[0])**2)+((br[1]-bl[1])**2))    #analitik geometrideki 2 nokta arası uzaklık formulüyle
    heightB = np.sqrt(((tr[0]-tl[0])**2)+((tr[1]-bl[1])**2))    #yeni resmin yüksekliğini buluyoruz
    maxHeight = max(int(heightA),int(heightB))

    #   şuanda elimizde resmin yeni boyutları var
    #   resmin kuş bakısı görüntüsünü çıkararak yine sol tepe, sağ tepe, sağ al, sol alt degerlerini buluyoruz

    dst = np.array([[0,0],[maxWidth-1,0],[maxWidth-1,maxHeight-1],[0,maxHeight-1]],dtype="float32")
    #dst, dönüştürülmüş roi degerlerini saklar

    M = cv2.getPerspectiveTransform(rect,dst)   #perspektif dönüşümü hesabını yapıyor
                                                #cv2.getPerspetiveTransform fonksiyonu rect ve dst değerlerini kullanır 
    warped = cv2.warpPerspective(image,M,(maxWidth,maxHeight))  #ve uyguluyoruz

    return warped