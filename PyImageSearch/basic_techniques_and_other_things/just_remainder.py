import imutils #imutils resize gibi işlemleri daha kolay yapmamızı sağlar 
import cv2 #gerekli kütüphaneleri import ettik

image = cv2.imread("/home/oguzay/Downloads/faces.jpg")  #görseli aktardık
(h, w, d) = image.shape  # görselin en boy ve derinliğini verir
print("width{}, height{}, depth{}".format(w, h, d))

(B,G,R) = image[100,50]   # x = 50 ve y = 100 koordinatındaki pikselin b g r değerini verir
print("R={}, G={}, B={}".format(R, G, B))

roi = image[60:180, 320:420] # görselin y1:x1, y2:x2 arasındaki kısmını resimden ayırır ve işlem yapmak istediğimiz alanı küçülterek işimizi kolaylaştırır

resize = cv2.resize(image,(200,200)) # görseli yeniden boyutlandırdık

r = 300.0/w
dim = (300, int(h*r))
resize2 = cv2.resize(image,dim)

resize3 = imutils.resize(image,300)

center = (w//2, h//2)
M = cv2.getRotationMatrix2D(center, 45, 0)
rotated = cv2.warpAffine(image, M, (w,h))

rotated = imutils.rotate(image, -45)             #IMUTILS KUTUPHANESINDE BIR SIKINTI VAR, COZUNCE CALISACAK
cv2.imshow("Imutils Rotation", rotated)
cv2.waitKey(0)


blurred = cv2.GaussianBlur(image, (11, 11), 0) # 11x11 matrislik bir gaussian blur uyguladık

output = image.copy()
cv2.rectangle(output , (310,70),(440,240),(0,0,255),2)
cv2.circle(output, (340,160),20,(0,255,0),-1)
cv2.line(output, (60,20),(400,200),(255,0,0),5)
cv2.putText(output, "redhead",(10,25),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,255,0),2)

cv2.imshow("Imutils Resize", resize3)
cv2.imshow("resized",resize2)
cv2.imshow("resizeman",resize)
cv2.imshow("roi",roi)
cv2.imshow("image",image)
cv2.imshow("rotation",rotated)
cv2.imshow("Blurred", blurred)
cv2.imshow("rectangle",output)
cv2.waitKey(0)
cv2.destroyAllWindows()
