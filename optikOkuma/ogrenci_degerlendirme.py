import cv2
import numpy as np




def ogrenci_degerlendirme_sutun(

    kenar_siyahlar, image, ogrenci_degerlendirme_aralık, x1_ogrenci_degerlendirme, x2_ogrenci_degerlendirme,
    ogrenci_degerlendirme_indis_1, ogrenci_degerlendirme_indis_2):

    ogrenci_degerlendirme_cevaplar = [] 
    i_ogrenci_degerlendirme = 1    
    
    aralık = int((x2_ogrenci_degerlendirme - x1_ogrenci_degerlendirme) / 21 )

    y1_degerlendirme_sutun = kenar_siyahlar[ogrenci_degerlendirme_indis_1] - ogrenci_degerlendirme_aralık
    y2_degerlendirme_sutun = kenar_siyahlar[ogrenci_degerlendirme_indis_2] + ogrenci_degerlendirme_aralık

    x2_ogrenci_degerlendirme = x1_ogrenci_degerlendirme + aralık

    
    for j in range(0,21,1):

        ogrenci_degerlendirme_roi = image[y1_degerlendirme_sutun:y2_degerlendirme_sutun, x1_ogrenci_degerlendirme:x2_ogrenci_degerlendirme]  
        ##############
        cv2.destroyAllWindows()
        cv2.imshow("ogrenci_degerlendirme_roi",ogrenci_degerlendirme_roi)   
        cv2.waitKey(0)
        #############
        for i in range(3,14):  

            isaretli = 0 
            kenar_y= kenar_siyahlar[i]
                      
        
            roi_alan_kutucuk = image[
                kenar_y - ogrenci_degerlendirme_aralık:kenar_y + ogrenci_degerlendirme_aralık,
                x1_ogrenci_degerlendirme:x2_ogrenci_degerlendirme]
                
            cv2.imshow("roi_alan_kutucuk",roi_alan_kutucuk)
            
            gray = cv2.cvtColor(roi_alan_kutucuk,cv2.COLOR_BGR2GRAY)
            theresh = cv2.threshold(gray,60,255,cv2.THRESH_BINARY_INV)[1]  
            erode = cv2.erode(theresh, np.ones((3,3), np.uint8), iterations=2)  
            dilate = cv2.dilate(erode, np.ones((3,3), np.uint8), iterations=2)  
            contours , _ = cv2.findContours(dilate,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE) 

            cv2.imshow("roi_alan_kutucuk",roi_alan_kutucuk)
            cv2.imshow("theresh ",dilate)
            cv2.waitKey(0)

            
            for c in contours:
                area = cv2.contourArea(c)  
                print("area şık ",area)

                if area > 2500:
                        
                    cevap = i+1
                    isaretli = isaretli + 1
                        
        print("isaretli",isaretli)
        print("i",i)      

        if (isaretli == 0 and i==14) or isaretli > 1:
            ogrenci_degerlendirme_cevaplar.append([i_ogrenci_degerlendirme , 0])

        else :
            ogrenci_degerlendirme_cevaplar.append([i_ogrenci_degerlendirme ,cevap-4]) 
                    # 4 çıkarmamızın sebebi kenar indis 
                
        i_ogrenci_degerlendirme+=1 
    
        print("ogrenci_degerlendirme_cevaplar",ogrenci_degerlendirme_cevaplar)


        x1_ogrenci_degerlendirme = x1_ogrenci_degerlendirme + aralık
        x2_ogrenci_degerlendirme = x2_ogrenci_degerlendirme + aralık


       





