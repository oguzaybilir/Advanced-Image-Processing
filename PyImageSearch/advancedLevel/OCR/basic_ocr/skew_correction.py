import cv2          #   gerekli kütüphaneleri ekledik
import numpy as np
import argparse

ap = argparse.ArgumentParser()      #   kullanıcıdan görseli aldık
ap.add_argument("-i","--image",required=True,help="path to input image")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])   #   görseli okuttuk

gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)   #   Görseli gri renk uzayına geçirdik
gray = cv2.bitwise_not(gray)        #   threshold yapacağımız için resmin arka planını siyah, textide beyaz yapıyoruz

cv2.imshow("gray",gray)
cv2.waitKey(0)

thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]   #   Resme thresold uyguluyoruz
cv2.imshow("thresh",thresh)
cv2.waitKey(0)


coords = np.column_stack(np.where(thresh>0))    #   0 dan büyük olan piksel değerlerini alıyoruz
angle = cv2.minAreaRect(coords)[-1]     #   tüm koordinatların  x,y değerlerinde dönüyoruz

#   cv2.minAreaRect fonksiyonu 90 dan 0 a kadar olan açı değerlerini döndürür bizde alınan o değerleri kullanıyoruz


if angle < -45:
    angle = -(90+angle)
else:
    angle = -angle


(h,w) = image.shape[:2]     #   
center = (w//2,h//2)

M = cv2.getRotationMatrix2D(center, angle, 1.0)
rotated = cv2.warpAffine(image, M, (w,h), flags = cv2.INTER_CUBIC, borderMode = cv2.BORDER_REPLICATE)

cv2.putText(rotated, "Angle: {:.2f} degrees".format(angle),(10,30),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)

print("[INFO] angle:  {:.3f}".format(angle))
cv2.imshow("input",image)
cv2.imshow("rotated",rotated)
cv2.waitKey(0)