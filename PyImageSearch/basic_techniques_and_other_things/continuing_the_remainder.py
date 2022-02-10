import argparse #gerekli kütüphaneleri import ettik
import imutils
import cv2
from imutils import contours

ap = argparse.ArgumentParser() # argümanları tutan boş listemizi oluştduk
ap.add_argument("-i","--image",required=True, help="path to input image") # bir üst satırdaki boş listeyi dolduracak olan argümanı tutacak
args = vars(ap.parse_args())  #argümanı çözümlüyoruz

img = cv2.imread(args["image"]) # görseli aktardık
cv2.imshow("Image",img) # görselin ham halini görmek için imshow ettirdik
 
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # çoğu işlem için görselimizi griye ve/veya siyah beyaza çevirmemiz gereklidir, burada da griye çevirdik
cv2.imshow("gray",gray)

edge = cv2.Canny(gray,30,150)  #kenarları saptamak için özel bir fonksiyon kullandık, 30 ve 150 kafamıza göre verdiğimiz threshold değerleri
cv2.imshow("edged",edge)

thresh = cv2.threshold(gray, 225,255, cv2.THRESH_BINARY_INV)[1]  #resmi threshold ettik 
cv2.imshow("thresh",thresh)

mask = thresh.copy()    
mask = cv2.erode(mask,None,iterations=5)
cv2.imshow("eroded",mask)

mask = cv2.dilate(mask,None,iterations=5)
cv2.imshow("dilated",mask)

mask = thresh.copy()
output = cv2.bitwise_and(img, img, mask=mask)
cv2.imshow("output",output)

cnt = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # konturleri buluyoruz
cnt = imutils.grab_contours(cnt) # buldurduğumuz konturleri piksel sırasına göre sıralıyor
output = img.copy() #elimizdeki görselin kopyasını kullanıyoruz

count = 0
findcnt = contours.sort_contours(cnt, method="top-to-bottom")[0]
for c in findcnt: # bulduğumuz konturlerin içerisinde c değerini döndürüyoruz  
    cv2.drawContours(output,[c],-1,(240,0,159),3) # konturleri çizdiriyoruz
    (x,y,w,h) = cv2.boundingRect(c)
    M = cv2.moments(c)
    x = int(M['m10']/M['m00'])
    y = int(M['m01']/M['m00'])
    print(x,y)
    count += 1
    cv2.putText(output,f"{count}",(x-50,y), cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,0),1)
    cv2.putText(output,f"{x},{y}",(x,y), cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
    cv2.circle(output,(x,y),3,(0,255,0),-1)
    cv2.imshow("cnts",output) # imshow ettiriyoruz



cv2.waitKey(0)
cv2.destroyAllWindows()


