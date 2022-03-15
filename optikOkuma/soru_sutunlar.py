import cv2
import numpy as np



def birinci_soru_sutun(kenar_siyahlar, image, x1_birinci_soru_sutun,x2_birinci_soru_sutun,birinci_soru_sutun_indis_1,birinci_soru_sutun_indis_2,birinci_soru_sutun_aralık):

    cevaplar_ilk_sutun = []
    i_soru = 1      
    for i,kenar_y in enumerate(kenar_siyahlar): 

        isaretli = 0 

        if birinci_soru_sutun_indis_2 > i > birinci_soru_sutun_indis_1:  

            roi_alan_kutucuk = image[

            kenar_y-birinci_soru_sutun_aralık:kenar_y+birinci_soru_sutun_aralık,
            x1_birinci_soru_sutun:x2_birinci_soru_sutun

            ]


            cv2.destroyAllWindows()  
            cv2.imshow("roi_alan_kutucuk",roi_alan_kutucuk)  
            cv2.waitKey(0)

            ###############################################

            en_siklar, boy_siklar ,kanal= roi_alan_kutucuk.shape 

            print("boy_siklar",roi_alan_kutucuk.shape) 
            boy_siklar_parca = int(boy_siklar/5)        
            print("boy_siklar_parca",boy_siklar_parca)

            

            y2_siklar = 0
            y1_siklar = boy_siklar
            x2_siklar = 0
            x1_siklar = boy_siklar_parca
    
            for i in range(0,5,1):  
                            
                roi_alan_siklar = roi_alan_kutucuk[y2_siklar:y1_siklar , x2_siklar:x1_siklar]   

                # ŞIK OLARAK İNCELEYEBİLMEMİZ İÇİN ONA GÖRE ROİ BELİRTİYORUZ
                # ŞIK ŞIK İLERLEMEK İÇİN ADDIM SAYIMIZ KADAR DEĞERLERE EKLEME YAPIYORUZ
                            
                x2_siklar +=  boy_siklar_parca
                x1_siklar += boy_siklar_parca

                # ROİ ALANINI GRAYE CERİYORUZ
                gray = cv2.cvtColor(roi_alan_siklar,cv2.COLOR_BGR2GRAY)
                theresh = cv2.threshold(gray,60,255,cv2.THRESH_BINARY_INV)[1]  
                erode = cv2.erode(theresh, np.ones((3,3), np.uint8), iterations=2)  
                dilate = cv2.dilate(erode, np.ones((3,3), np.uint8), iterations=2)  
                contours , _ = cv2.findContours(dilate,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)  

                # AŞAMALARI GÖREBİLMEK İÇİN İMSHOW EDİYORUZ
                cv2.imshow("roi_alan_siklar",roi_alan_siklar)
                cv2.imshow("theresh ",dilate)
                cv2.waitKey(0)

                # ŞIKLAR İÇERİSİNDE TEKRAR KONTUR ARATIP DOLULUK ORANLARINI  İNCELİYORUZ
                for c in contours:
                    area = cv2.contourArea(c)  # ALAN HESAPLAMA
                    print("area şık ",area)
                    
                    if area > 2500:  # BELİRLİ DOLULUGA ULAŞN DEĞERLERİ
                        cevap = i+1
                        isaretli += 1
                        
            
            if (isaretli == 0 and i==3) or isaretli > 1:
                cevaplar_ilk_sutun.append([i_soru , 0])
            else :
                cevaplar_ilk_sutun.append([i_soru ,cevap]) # ORTA NOKTASI BELİRLEME   
                                
            i_soru+=1 
    print("cevaplar",cevaplar_ilk_sutun)

    return cevaplar_ilk_sutun




########################################################################################


def ikinci_soru_sutun(

    kenar_siyahlar, image, x1_ikinci_soru_sutun, x2_ikinci_soru_sutun, 
    ikinci_soru_sutun_indis_1, ikinci_soru_sutun_indis_2, ikinci_soru_sutun_aralık):

    cevaplar_ikinci_sütün = []  
    i_soru = 41   
    for i,kenar_y in enumerate(kenar_siyahlar):  

        isaretli = 0 

        if ikinci_soru_sutun_indis_2 > i > ikinci_soru_sutun_indis_1:  

            roi_alan_kutucuk = image[

            kenar_y - ikinci_soru_sutun_aralık:kenar_y + ikinci_soru_sutun_aralık,
            x1_ikinci_soru_sutun:x2_ikinci_soru_sutun
            ]


            cv2.destroyAllWindows()   # TÜM PENCERLERİ KAPAT
            cv2.imshow("roi_alan_kutucuk",roi_alan_kutucuk)  # AŞAMALARI GÖRMEK İÇİN EKRANA VER 
            cv2.waitKey(0)

            ###############################################

            en_siklar, boy_siklar ,kanal= roi_alan_kutucuk.shape 

            print("boy_siklar",roi_alan_kutucuk.shape) 
            boy_siklar_parca = int(boy_siklar/5)        
            print("boy_siklar_parca",boy_siklar_parca)

            # TÜM KUTUCUĞU BELİRTMEK İÇİN ROİ İLE İLGİLİ AYARLAMALAR 

            y2_siklar = 0
            y1_siklar = boy_siklar
            x2_siklar = 0
            x1_siklar = boy_siklar_parca
        
            for i in range(0,5,1):  # HER ŞIK İÇİN FOR DÖNECEK 
                            
                roi_alan_siklar = roi_alan_kutucuk[y2_siklar:y1_siklar , x2_siklar:x1_siklar]   

                # ŞIK OLARAK İNCELEYEBİLMEMİZ İÇİN ONA GÖRE ROİ BELİRTİYORUZ
                # ŞIK ŞIK İLERLEMEK İÇİN ADDIM SAYIMIZ KADAR DEĞERLERE EKLEME YAPIYORUZ
                            
                x2_siklar +=  boy_siklar_parca
                x1_siklar += boy_siklar_parca

                # ROİ ALANINI GRAYE CERİYORUZ
                gray = cv2.cvtColor(roi_alan_siklar,cv2.COLOR_BGR2GRAY)
                theresh = cv2.threshold(gray,60,255,cv2.THRESH_BINARY_INV)[1]  # THERESH UYGULUYORUZ
                erode = cv2.erode(theresh, np.ones((3,3), np.uint8), iterations=2)  # ERODE İŞLEMİ
                dilate = cv2.dilate(erode, np.ones((3,3), np.uint8), iterations=2)  # DİLATE İŞLEMİ
                contours , _ = cv2.findContours(dilate,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)  # CONTUR BULMA 

                # AŞAMALARI GÖREBİLMEK İÇİN İMSHOW EDİYORUZ
                cv2.imshow("roi_alan_siklar",roi_alan_siklar)
                cv2.imshow("theresh ",dilate)
                cv2.waitKey(0)

                # ŞIKLAR İÇERİSİNDE TEKRAR KONTUR ARATIP DOLULUK ORANLARINI  İNCELİYORUZ
                for c in contours:
                    area = cv2.contourArea(c)  
                    print("area şık ",area)
                    
                    if area > 2500: 
                        cevap = i+1
                        isaretli += 1
                        
            
            if (isaretli == 0 and i==4) or isaretli > 1:
                cevaplar_ikinci_sütün.append([i_soru , 0])
            else :
                cevaplar_ikinci_sütün.append([i_soru ,cevap]) 
                        
                    
            i_soru+=1 
    print("cevaplar",cevaplar_ikinci_sütün)

    return cevaplar_ikinci_sütün


###################################################################################################################




def ucuncu_soru_sutun(

    kenar_siyahlar, image, x1_ücüncü_soru_sutun,x2_ücüncü_soru_sutun,
    ücüncü_soru_sutun_indis_1,ücüncü_soru_sutun_indis_2,ücüncü_soru_sutun_aralık):


    cevaplar_ücüncü_sütün = []   # CEVAPLARI TUTMAK İÇİN DİZİ TANIMLIYORUZ
    i_soru = 81  # SORU SAYISI 

    for i,kenar_y in enumerate(kenar_siyahlar):  # KENARDAN ALDIMIZ Y DEĞERLERİ İÇİNDE  DÖNÜORUZ

        isaretli = 0 

        if ücüncü_soru_sutun_indis_2 > i > ücüncü_soru_sutun_indis_1:  # İSTEDİĞİMİZ ŞARTLARDA DÖNMESİNİ SAĞLIYORUZ

            roi_alan_kutucuk = image[
            kenar_y - ücüncü_soru_sutun_aralık:kenar_y + ücüncü_soru_sutun_aralık,
            x1_ücüncü_soru_sutun:x2_ücüncü_soru_sutun]



            cv2.destroyAllWindows() 
            cv2.imshow("roi_alan_kutucuk",roi_alan_kutucuk) 

            ###############################################

            en_siklar, boy_siklar ,kanal= roi_alan_kutucuk.shape 

            print("boy_siklar",roi_alan_kutucuk.shape) 
            boy_siklar_parca = int(boy_siklar/5)        
            print("boy_siklar_parca",boy_siklar_parca)

        
            y2_siklar = 0
            y1_siklar = boy_siklar
            x2_siklar = 0
            x1_siklar = boy_siklar_parca
        
            for i in range(0,5,1):  
                            
                roi_alan_siklar = roi_alan_kutucuk[y2_siklar:y1_siklar , x2_siklar:x1_siklar]   

                
                            
                x2_siklar +=  boy_siklar_parca
                x1_siklar += boy_siklar_parca

                
                gray = cv2.cvtColor(roi_alan_siklar,cv2.COLOR_BGR2GRAY)
                theresh = cv2.threshold(gray,60,255,cv2.THRESH_BINARY_INV)[1]  
                erode = cv2.erode(theresh, np.ones((3,3), np.uint8), iterations=2)  
                dilate = cv2.dilate(erode, np.ones((3,3), np.uint8), iterations=2)
                contours , _ = cv2.findContours(dilate,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE) 

                # AŞAMALARI GÖREBİLMEK İÇİN İMSHOW EDİYORUZ
                cv2.imshow("roi_alan_siklar",roi_alan_siklar)
                cv2.imshow("theresh ",dilate)
                cv2.waitKey(0)

                # ŞIKLAR İÇERİSİNDE TEKRAR KONTUR ARATIP DOLULUK ORANLARINI  İNCELİYORUZ
                for c in contours:
                    area = cv2.contourArea(c)  # ALAN HESAPLAMA
                    print("area şık ",area)
                    
                    if area > 2500:  # BELİRLİ DOLULUGA ULAŞN DEĞERLERİ
                        cevap = i+1
                        isaretli += 1
                        
            
            if (isaretli == 0 and i==4) or isaretli > 1:
                cevaplar_ücüncü_sütün.append([i_soru , 0])
            else :
                cevaplar_ücüncü_sütün.append([i_soru ,cevap]) # ORTA NOKTASI BELİRLEME   
                        
                    
            i_soru+=1 
    print("cevaplar",cevaplar_ücüncü_sütün)

    return cevaplar_ücüncü_sütün
