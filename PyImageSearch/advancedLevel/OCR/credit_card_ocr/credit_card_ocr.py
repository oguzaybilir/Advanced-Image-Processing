from imutils import contours    #gerekli kütüphaneleri ekledik
import numpy as np
import argparse
import imutils
import cv2

ap = argparse.ArgumentParser()  #kullanıcıdan sayılara referans olacak görselle, kredi kartının görselini aldık
ap.add_argument("-i","--image",required=True,help="path to input image")
ap.add_argument("-r","--reference",required=True,help="path to reference OCR-A image")
args = vars(ap.parse_args())

FIRST_NUMBER = {    #   kartlara özgü başlangıç sayılarını bir sözlüğün içine yazdık
	"3": "American Express",
	"4": "Visa",
	"5": "MasterCard",
	"6": "Discover Card"
}

ref = cv2.imread(args["reference"]) #   referans görselimizi ekledik
cv2.imshow("reference",ref)
cv2.waitKey(0)

ref = cv2.cvtColor(ref,cv2.COLOR_BGR2GRAY)  #   referans görseline gri renk uzayına çevirme işlemini uyguladık
cv2.imshow("gray",ref)
cv2.waitKey(0)

ref = cv2.threshold(ref,10,255,cv2.THRESH_BINARY_INV)[1]    #   referans görseline temel işlemlerden olan threshold işlemini uyguladık
cv2.imshow("thresholded ref",ref)
cv2.waitKey(0)

refCnts = cv2.findContours(ref.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)    #   referans görselindeki sayıların konturlerini buldurduk
refCnts = imutils.grab_contours(refCnts)    #   imutils kütüphanesinin grab_contours fonksiyonu ile konturlerimizi tutturduk
refCnts = contours.sort_contours(refCnts, method="left-to-right")[0]    #   buldurduğumuz konturleri soldan sağa doğru sıraladık 
digits = {}    #   bulunan sayılar dijital olarak yazıldıkları için, bu sayıların hangi sayı olduğunu anlayabilmek adına digits diye bir sözlük oluşturduk

for (i,c) in enumerate(refCnts):    #   buldurduğumuz konturleri numaralandırıp içlerinde i ve c yi döndürüyoruz

    (x,y,w,h) = cv2.boundingRect(c) #   bulunan konturlerin x,y,w,h değerlerini buluyoruz
    roi = ref[y:y+h, x:x+w]     #   işlem uygulayacağımız alan belli olduğu için o alanı alıyouz, geri kalan görselle işimiz yok
    roi = cv2.resize(roi, (57,88))  #   roi'yi yeniden boyutlandırdık
    cv2.imshow("roi",roi)   #   roi'yi gösterdik
    cv2.waitKey(0)

    digits[i] = roi     #   digits arrayinin içine döndürdüğümüz i değerini girip roi ye eşitliyoruz

rectKernel = cv2.getStructuringElement(cv2.MORPH_RECT,(9,3))   
sqKernel = cv2.getStructuringElement(cv2.MORPH_RECT,(5,5))

image = cv2.imread(args["image"])   #   şimdi kredi kartı görselimizi alıyoruz
image = imutils.resize(image,width=300)     #   yeniden boyutlandırıyoruz
cv2.imshow("credit-card",image)
cv2.waitKey(0)

gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)   #   görselimizi gri renk uzayına çeviriyoruz
cv2.imshow("credit-card",gray)
cv2.waitKey(0)

tophat = cv2.morphologyEx(gray,cv2.MORPH_TOPHAT,rectKernel)     #   
cv2.imshow("tophat - credit-card",tophat)
cv2.waitKey(0)

gradX = cv2.Sobel(tophat,ddepth=cv2.CV_32F,dx=1,dy=0,ksize=1)

cv2.imshow("gradX sobel",gradX)
cv2.waitKey(0)

gradX = np.absolute(gradX)
cv2.imshow("absolute-gradX",gradX)
cv2.waitKey(0)

(minval,maxval) = (np.min(gradX),np.max(gradX))
gradX = (255*((gradX-minval)/(maxval-minval)))
gradX = gradX.astype("uint8")

gradX = cv2.morphologyEx(gradX,cv2.MORPH_CLOSE, rectKernel)
cv2.imshow("morphed gradX",gradX)
cv2.waitKey(0)

thresh = cv2.threshold(gradX,0,255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
cv2.imshow("thresholded gradX",thresh)
cv2.waitKey(0)

thresh = cv2.morphologyEx(thresh,cv2.MORPH_CLOSE,sqKernel)
cv2.imshow("morphed thresh",thresh)
cv2.waitKey(0)

cnts = cv2.findContours(thresh.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)


locs = []

for (i,c) in enumerate(cnts):
    (x,y,w,h) = cv2.boundingRect(c)
    ar = w/float(h)


    area = cv2.contourArea(c)
    if area > 500 and area < 600:
        locs.append((x,y,w,h))

locs = sorted(locs,key=lambda x:x[0])
print("bunlar locationlar:  ",locs)

output = []


for (i, (gX,gY,gW,gH)) in enumerate(locs):

    groupOutput = []
    group = gray[gY-5:gY+gH+5, gX-5:gX+gW+5]
    group = cv2.threshold(group,0,255,cv2.THRESH_BINARY|cv2.THRESH_OTSU)[1]
    cv2.imshow("group threshold",group)
    cv2.waitKey(0)

    digitCnts = cv2.findContours(group.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    print("conturler burada kirve")

    digitCnts = imutils.grab_contours(digitCnts)
    digitCnts = contours.sort_contours(digitCnts,method="left-to-right")[0]
    
    for c in digitCnts:
        (x,y,w,h) = cv2.boundingRect(c)
        roi = group[y:y+h, x:x+w]
        roi = cv2.resize(roi, (57,88))
        cv2.imshow("resized group roi",roi)
        cv2.waitKey(0)
        scores = []

        for (digit, digitROI) in digits.items():

            result = cv2.matchTemplate(roi, digitROI,cv2.TM_CCOEFF)
            result = imutils.resize(result,width=300)

            (_,score,_,_) = cv2.minMaxLoc(result)
            scores.append(score)
            print("scores:  ",score)

        groupOutput.append(str(np.argmax(scores)))
        print("gropuOutputs:    ",groupOutput)
    
    cv2.rectangle(image,(gX-5,gY-5),(gX+gW+5,gY+gH+5),(0,0,255),2)
    cv2.putText(image, "".join(groupOutput),(gX,gY-15),cv2.FONT_HERSHEY_SIMPLEX,0.65,(0,0,255),2)

    output.extend(groupOutput)
    print("output2:     ",output)

print("Credit Card Type:    {}".format(FIRST_NUMBER[output[0]]))
print("Credit Card #:   {}".format("".join(output)))

cv2.imshow("image",image)
cv2.waitKey(0)
cv2.destroyAllWindows()