import cv2
import numpy as np


x1_kitapcik_turu = 1408    
x2_kitapcik_turu = 2608
kitapcik_turu_indis_1 = 4
kitapcik_turu_aralık = 44


def kitapcik_turu(
    kenar_siyahlar, image, x1_kitapcik_turu,x2_kitapcik_turu, kitapcik_turu_indis_1, kitapcik_turu_aralık):

    kitapcik_no_cevaplar = []
 
    aralık = int((x2_kitapcik_turu - x1_kitapcik_turu) / 4 )

    y1_kitapcik_sutun = kenar_siyahlar[kitapcik_turu_indis_1] - kitapcik_turu_aralık
    y2_kitapcik_sutun = kenar_siyahlar[kitapcik_turu_indis_1] + kitapcik_turu_aralık


    for j in range(0,4,1):

        i_soru = 1

        ogrenci_no_roi = image[y1_kitapcik_sutun:y2_kitapcik_sutun, x1_kitapcik_turu:x2_kitapcik_turu]  
        cv2.destroyAllWindows()
        cv2.imshow("ogrenci_no_roi",ogrenci_no_roi)   
        cv2.waitKey(0)

        for i,kenar_y in enumerate(kenar_siyahlar):  

            isaretli = 0 

            x2_kitapcik_turu = x1_kitapcik_turu + aralık
                           
            if  i == kitapcik_turu_indis_1 :

                roi_alan_kutucuk = image[
                    
                kenar_y - kitapcik_turu_aralık:kenar_y + kitapcik_turu_aralık, 
                x1_kitapcik_turu:x2_kitapcik_turu]

                cv2.imshow("roi_alan_kutucuk",roi_alan_kutucuk)
                
                gray = cv2.cvtColor(roi_alan_kutucuk,cv2.COLOR_BGR2GRAY)
                theresh = cv2.threshold(gray,60,255,cv2.THRESH_BINARY_INV)[1]  # THERESH UYGULUYORUZ
                erode = cv2.erode(theresh, np.ones((3,3), np.uint8), iterations=2)  # ERODE İŞLEMİ
                dilate = cv2.dilate(erode, np.ones((3,3), np.uint8), iterations=2)  # DİLATE İŞLEMİ
                contours , _ = cv2.findContours(dilate,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)  # CONTUR BULMA 

                # AŞAMALARI GÖREBİLMEK İÇİN İMSHOW EDİYORUZ
                cv2.imshow("roi_alan_kutucuk",roi_alan_kutucuk)
                cv2.imshow("theresh ",dilate)
                cv2.waitKey(0)
  
                # ŞIKLAR İÇERİSİNDE TEKRAR KONTUR ARATIP DOLULUK ORANLARINI  İNCELİYORUZ
                for c in contours:
                    area = cv2.contourArea(c)  # ALAN HESAPLAMA
                    print("area şık ",area)
                    if area > 2500:  # BELİRLİ DOLULUGA ULAŞN DEĞERLERİ
                        cevap = i+1
                        isaretli += 1

                x1_kitapcik_turu = x1_kitapcik_turu + aralık
                x2_kitapcik_turu = x1_kitapcik_turu + aralık
               

    if (isaretli == 0 and i==4) or isaretli > 1:
        kitapcik_no_cevaplar.append([i_soru , 0])
        
    else :
        kitapcik_no_cevaplar.append([i_soru ,cevap-3])

    i_soru+=1 
    print("cevaplar",kitapcik_no_cevaplar)

    return kitapcik_no_cevaplar

  