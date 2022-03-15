import cv2
import numpy as np




def ogrenci_no_sutun(

    kenar_siyahlar, image,x1_ogrenci_no_sutun,
    x2_ogrenci_no_sutun, ogrenci_no_indis_1, ogrenci_no_indis_2,ogrenci_no_aralik
     
    ):

    ogrenci_no_cevaplar = [] 
    i_ogrenci_no = 1    
    
    aralık = int((x2_ogrenci_no_sutun - x1_ogrenci_no_sutun) / 10 )

    y1_ogrenci_no_sutun = kenar_siyahlar[ogrenci_no_indis_1] - ogrenci_no_aralik
    y2_ogrenci_no_sutun = kenar_siyahlar[ogrenci_no_indis_2] + ogrenci_no_aralik

    x2_ogrenci_no_sutun = x1_ogrenci_no_sutun + aralık

    
    for j in range(0,10,1):

        ogrenci_no_roi = image[y1_ogrenci_no_sutun:y2_ogrenci_no_sutun, x1_ogrenci_no_sutun:x2_ogrenci_no_sutun]  
        ##############
        cv2.destroyAllWindows()
        cv2.imshow("ogrenci_no_roi",ogrenci_no_roi)   
        cv2.waitKey(0)
        #############

        for i in range(4,14,1):

            isaretli = 0 
            kenar_y = kenar_siyahlar[i] 
                                       
        
            roi_alan_kutucuk = image[

                kenar_y - ogrenci_no_aralik:kenar_y + ogrenci_no_aralik,
                x1_ogrenci_no_sutun:x2_ogrenci_no_sutun

                ]

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
                    isaretli += 1
                    
                
        if (isaretli == 0 and i==13) or isaretli > 1:
            ogrenci_no_cevaplar.append([i_ogrenci_no , 0])
        else :
            ogrenci_no_cevaplar.append([i_ogrenci_no ,cevap-4]) # ORTA NOKTASI BELİRLEME   
                    # 4 çıkarmamızın sebebi kenar indis 
                
        i_ogrenci_no+=1 
        
        print("ogrenci_no_cevaplar",ogrenci_no_cevaplar)
        
        
        
        x1_ogrenci_no_sutun = x1_ogrenci_no_sutun + aralık
        x2_ogrenci_no_sutun = x2_ogrenci_no_sutun + aralık




