import numpy as np
import argparse
import imutils
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-i","--image", required=True, help="path to the image file")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])

for angle in np.arange(0,360,15):  #GÖRSEL BÜTÜNLÜĞÜNÜ KORUYAMAYAN ŞEKİLDE GÖRSELİ DÖNDÜRÜYORUZ 
    rotated = imutils.rotate(image,angle)   #yanlış olan bir rotate işlemi
    cv2.imshow("rotated (problemli)", rotated)  
    cv2.waitKey(0)

for angle in np.arange(0,360,15):   #GÖRSEL BÜTÜNLÜĞÜNÜ KORUYAN VE GÖRSELİ KESMEK YERİNE PENCEREYİ YENİDEN BOYUTLANDIRAN SİSTEM
    rotated = imutils.rotate_bound(image,angle) #doğru bir rotate işlemi
    cv2.imshow("rotated (dogru)", rotated)
    cv2.waitKey(0)

# cv2.cv2.getRotationMatrix2D fonksiyonun çalışma mantığı https://pyimagesearch.com/wp-content/uploads/2016/12/opencv_rotate_matrix.png





#imutilsin içindeki rotate_bound fonksiyonunun çalışma mantığı
"""""
def rotate_bound(image,angle):
    (h,w) = image.shape[:2]
    (cX, cY) = (w//2, h//2)

    M = cv2.getRotationMatrix2D((cX,cY),-angle,1.0)
    cos = np.abs(M[0,0])
    sin = np.abs(M[0,1])

    nW = int((h*sin),+(w*cos))
    nH = int((h*cos)+(w*sin))

    M[0,2] += (nW /2) - cY
    M[1,2] += (nH /2) - cX

    return cv2.warpAffine(image, M, (nH,nW))
"""""