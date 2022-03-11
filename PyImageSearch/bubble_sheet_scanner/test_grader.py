import transform    #gerekli kütüphaneleri ve class ları import ettik
import argparse
import imutils
import cv2
from imutils import contours
import numpy as np


ap = argparse.ArgumentParser()  #   kullanıcıdan dosya yolunu aldık    
ap.add_argument("-i","--image",required="True",help="path to the input image")
args = vars(ap.parse_args())

answerKey = {0: 1, 1: 4, 2: 0, 3: 3, 4: 1}
 
image = cv2.imread(args["image"])   #görüntüyü aldık
cv2.imshow("image",image)
cv2.waitKey(0)

gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)   #görüntüyü griye çevirdik, tek kanal görüntü
blur = cv2.GaussianBlur(gray,(5,5),0)   #görüntüdeki gürültüyü azaltmak için blur uyguladık
edged = cv2.Canny(blur,75,200) #görüntüdeki kenarları saptamak için Canny fonksiyonunu kullandık

cv2.imshow("canny edged",edged)
cv2.waitKey(0)


cnts = cv2.findContours(edged.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)    #görseldeli konturleri çizdirdik
cnts = imutils.grab_contours(cnts)  #imutilsin grab_contours fonksiyonu ile konturleri tutturduk
docCnt = None   #docCnt diye bir değişken oluşturduk ve None ' a eşitledik

if len (cnts) > 0:  #eğer cnts ' nin uzunluğu 0 dan büyükse
    cnts = sorted(cnts,key=cv2.contourArea,reverse=True)  #grab_contoursla tutturduğun konturleri alanlarına göre sıraal

    for c in cnts:  #   c'yi cnts içinde döndür

        perimeter = cv2.arcLength(c, True)   #çevreyi hesaplatıyoruz
        approx = cv2.approxPolyDP(c,0.02*perimeter, True)   #şeklin konturü sıkıntılı çıkarsa diye ortalama bir kontur çizdirebilmek için bu fonksiyonu kullanıyoruz

        if len(approx) == 4:    #eğer konturun uzunluğu 4 ise docCnt yi approx a eşitle ve döngüden çık

            docCnt = approx  
            break

paper = transform.four_points_transform(image,docCnt.reshape(4,2))  #orijinal resme four_points_transform uyguladık 
warped = transform.four_points_transform(gray, docCnt.reshape(4,2)) #griye dönüştürülmüş resme kuş bakışı dönüşüm yani four_points_transform dönüşümü yaptık
cv2.imshow("transformed",paper)
cv2.waitKey(0)

thresh  =cv2.threshold(warped, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]  #OTSUNUN THRESHOLİNG İNİ UYGULADIK

cv2.imshow("threshold",thresh)
cv2.waitKey(0)

cnts = cv2.findContours(thresh.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)    #threshold edilmiş görüntüdeki konturleri buldurduk
cnts = imutils.grab_contours(cnts)  #grab_contours ile kontuleri tuttuk
questionCnts = []   #   boş bir questionCnts dizisi oluşturduk


paper_copy = paper.copy()

for c in cnts:  #   c değerinin içinde dönüyoruz

    (x,y,w,h) = cv2.boundingRect(c) #   konturlerin konumlarının değerlerini alıyoruz
    ar  = w / float(h)  #   ar = AspectRatio demektir yani dimensions

    print(x,y,w,h)
    
    area = cv2.contourArea(c)   #bubble lar yeteri kadar geniş ve uzun olmalıdır 
    print("alan:    ",      area)
    
    if area > 900:

        cv2.rectangle(paper_copy, (int(x),int(y)),((int(x)+int(w)),(int(y)+int(h))), (0,0,255),2)
                                                                                                #bubble ların aspectRatio oranı ortalama 1 olmalıdır
        questionCnts.append(c)
        (cx,cy),r = cv2.minEnclosingCircle(c)

        cv2.circle(paper_copy,(int(cx),int(cy)),int(r),(255,0,0),2)                            #bu şartları sağlarsa questionCnts dizisine ekliyoruz
                                                        #questioningCnts belirli bir alanı bubble ları listeler ve bubble olarak listeye ekler
cv2.imshow("circles",paper_copy)
cv2.waitKey(0)

questionCnts = contours.sort_contours(questionCnts,method="top-to-bottom")[0]   #konturleri üstten-alta sıralar
correct = 0         #ve toplam doğru cevap sayısını paraflar

for (q,i) in enumerate(np.arange(0,len(questionCnts),5)):    #her sorunun 5 muhtemel cevabı var, bu 5 li cevap yığının içinde dönüyoruz

    cnts = contours.sort_contours(questionCnts[i:i+5])[0]   #konturleri soldan sağa doğru sırala ve işaretli şıkkın indisini ver
    bubbled = None


    for (j,c) in enumerate(cnts):   #sıralanmış konturlerin içinde dönüyoruz

        mask = np.zeros(thresh.shape,dtype = "uint8")  #sadece işaretlenmiş bubble ları göstersin diye bir mask uyguluyoruz
        cv2.drawContours(mask,[c] ,-1,255,-1)    

        mask = cv2.bitwise_and(thresh, thresh, mask=mask)   #maskeyi threshold edilmiş resme uyguluyoruz
        total = cv2.countNonZero(mask)  #işaretlenmiş alandaki 0 olmayan (siyah-beyaz renk düzeyi, 0 = siyah) yerleri say

        cv2.imshow("siklar",mask)
        cv2.waitKey(0)
        if bubbled is None or total > bubbled[0]:   #eğer total, siyah olmayan yerlerden daha fazlaysa cevap odur diyebiliriz
            bubbled = (total, j)

    color = (0,0,255)   #kontur rengini ayarlıyoruz
    k  = answerKey[q]   #ve doğru cevabın indisini alıyoruz

    if k == bubbled[1]: #işaretlenmiş şıkkın doğru olup olmadığını onaylıyoruz
        color = (0,255,0)
        correct += 1

    cv2.drawContours(paper,[cnts[k]],-1,color,3)    #   doğru olan şıkkın dışına bir kontur çizdiriyoruz
    cv2.imshow("Exam",paper)
    cv2.waitKey(0)

mark = (correct / 5.0)*100
print("[INFO] mark: {: .2f}%".format(mark))
cv2.putText(paper,"{: .2f}%".format(mark),(10,30),cv2.FONT_HERSHEY_SIMPLEX,0.9,(0,0,255),2)

#cv2.imshow("Original",image)
cv2.imshow("Exam",paper)
cv2.waitKey(0)