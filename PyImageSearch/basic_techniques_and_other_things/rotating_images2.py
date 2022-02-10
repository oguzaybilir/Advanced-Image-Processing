import argparse  #gerekli kütüphaneleri import ettik
import cv2
import imutils
import numpy as np

    # komut satırı argümanlarını almak için kodları yazıyoruz
ap = argparse.ArgumentParser()
ap.add_argument("-i","--image", required = True, help = "path to the image file")
args = vars(ap.parse_args())


img = cv2.imread(args["image"])
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray,(3,3), 0)
edged = cv2.Canny(gray, 20, 100)
cv2.imshow("edged", edged)


cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  #edge li resimde kontur çıkarıyoruz
cnts = imutils.grab_contours(cnts) 



if len(cnts) > 0:    #en az bir konturun var olduğundan emin olmalıyız

    c = max(cnts, key = cv2.contourArea)   # en büyük konturu alıyoruz
    mask = np.zeros(gray.shape, dtype = "uint8")    # maskeleme yapıyoruz
    cv2.drawContours(mask, [c], -1, 255, 1)


    #hapın sınırlarına teğet bir kare çiziliyor ve bu karenin olduğu değerlerden roi uygulanıyor
    (x,y,w,h) = cv2.boundingRect(c)
    roi = img[y :y +h , x:x +w]
    roimask = mask[y:y+h, x:x+w]    
    roi = cv2.bitwise_and(roi, roi, mask=roimask)   #   bitwise işleçlleri kullanarak renkli bir görüntüye sahip olduk

    cv2.imshow("mask",roimask)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


