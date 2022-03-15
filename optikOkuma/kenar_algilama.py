import cv2
import numpy as np



def hizalama(image,y1_hizalama,y2_hizalama,x1_hizalama,x2_hizalama):     
    
    kenar_siyahlar = []  

    roi_alan_hizalama = image[y1_hizalama:y2_hizalama, x1_hizalama:x2_hizalama] 
    roi_alan_parca_dilate = cv2.dilate(roi_alan_hizalama, np.ones((3,3), np.uint8), iterations=4)  
    roi_alan_parca_gray = cv2.cvtColor(roi_alan_parca_dilate, cv2.COLOR_BGR2GRAY)  
    ret, roi_alan_parca_threshold = cv2.threshold(roi_alan_parca_gray,60,255,cv2.THRESH_BINARY_INV) 
    contourss , _ = cv2.findContours(roi_alan_parca_threshold,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE) 

    cv2.imshow("roi_alan_hizalama",roi_alan_hizalama)    
    cv2.waitKey(0)       

    #===== ALGILANAN KONTURLERİN DEĞERLENDİRMESİ VE LİSTEYE EKLEME======#

    for c in contourss:
        area = cv2.contourArea(c)  # GELEN KONTURLERİN ALANINI  HESAPLIYORUZ
        (x,y,w,h) = cv2.boundingRect(c)   # KONTURUN BOUNDING RECT İLE DEĞERLERİ ÇEKİYORUZ

        if area > 1150:                # ALAN SINIRI VERİP  LİSTEYE EKLENEN CONTURLERİ SINIRLIYORUZ
           kenar_siyahlar.append(int(y+(h/2)))

            # PARCALANAN DEĞERİN Y VE H DEĞERLERİ KULLLANARAK HESAPALAMA YAPTIRIYORUZ 
           # VE ALGILANAN KUTUCUKLARIN MERKEZ DEĞERİNİN Y DEĞERİNİ LİSTEYE EKLİYORUZ 

    kenar_siyahlar.sort()  # Y DEĞERLERİNİ SIRALAMA
  
    return kenar_siyahlar