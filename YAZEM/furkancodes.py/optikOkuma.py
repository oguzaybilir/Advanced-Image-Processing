import cv2
import numpy as np
import argparse

from sympy import apart

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to input image")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])  # Dosya yolu 


#=====  KENAR SİYAHLARI ALGILAMAK İÇİN ROİ ALANI DEĞERLERİ  ======#

y1_hizalama = 0   # Y EKSENİNDE TAMAMINI ALMAK İÇİN BAŞLANGİC NOKTASINI RESMİN BAŞLANGICI YANİ 0 OLARAK VERİYORUZ
y2_hizalama = image.shape[0]  # FOTOĞRAFIN SHAPENİN Y DEĞERİNİN YANİ KAĞIDIN UZUNLUĞUNU ALMAK İÇİN KULLANILIR 
x1_hizalama = 35         # DIŞARDAN QR KOD  BİLGİSİ İLE VERİLECEK DEĞERLER (ÖZELLEŞTİRİLMİŞ) 
x2_hizalama = 255         # DIŞARDAN QR KOD  BİLGİSİ İLE VERİLECEK DEĞERLER (ÖZELLEŞTİRİLMİŞ) 

kenar_siyahlar = []       # KAĞIDIN KENAR UZUNLUĞUNU ALDIKTAN SONRA BİR DEĞİŞKENDE DEPOLAMAK İÇİN BOŞ BİR DİZİ TAANIMLIYORUZ


def hizalama(y1_hizalama,y2_hizalama,x1_hizalama,x2_hizalama):     # KENARDAKİ SİYAH DĞERLERİ ALGILAIP DİZİ İÇİNDE TUTMAK İÇİN FONKSİYON

    roi_alan_hizalama = image[y1_hizalama:y2_hizalama, x1_hizalama:x2_hizalama]  # YUKARDA VERİLEN DEĞERLERİ VERİP ROİ BELİRTİYORUZ
    roi_alan_parca_dilate = cv2.dilate(roi_alan_hizalama, np.ones((3,3), np.uint8), iterations=4)  # GÖRÜNTÜYÜ DİLATE EDİP GEREKESİZ PİKSELLERİ TEMİZLİYORUZ 
    roi_alan_parca_gray = cv2.cvtColor(roi_alan_parca_dilate, cv2.COLOR_BGR2GRAY)  # GRAYA CEVİRME  
    ret, roi_alan_parca_threshold = cv2.threshold(roi_alan_parca_gray,60,255,cv2.THRESH_BINARY_INV)  # THERESH YAPMA
    contourss , _ = cv2.findContours(roi_alan_parca_threshold,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)  # CONTUR BULMA 

    cv2.imshow("roi_alan_hizalama",roi_alan_hizalama)     # AŞAMAYI  GÖRMEK İÇİN EKRANA VERİYORUZ
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


x1_birinci_soru_sutun  = 494    # DIŞARDAN QR KOD  BİLGİSİ İLE VERİLECEK DEĞERLER (ÖZELLEŞTİRİLMİŞ) 
x2_birinci_soru_sutun = 1005     # DIŞARDAN QR KOD  BİLGİSİ İLE VERİLECEK DEĞERLER (ÖZELLEŞTİRİLMİŞ) 


def birinci_soru_sütün(x1_birinci_soru_sutun,x2_birinci_soru_sutun):

    cevaplar = []   # CEVAPLARI TUTMAK İÇİN DİZİ TANIMLIYORUZ
    i_soru = 1      # SORU SAYISI 

    for i,kenar_y in enumerate(kenar_siyahlar):  # KENARDAN ALDIMIZ Y DEĞERLERİ İÇİNDE  DÖNÜORUZ

        isaretli = 0 

        if 59 > i > 18:  # İSTEDİĞİMİZ ŞARTLARDA DÖNMESİNİ SAĞLIYORUZ

            roi_alan_kutucuk = image[kenar_y-43:kenar_y+43, x1_birinci_soru_sutun:x2_birinci_soru_sutun]
            # Y DEĞERİ MERKEZ OLDUĞĞU  İÇİN -43  -43  YAPTIK
            # 43 DEĞERİ TAMAMEN HESAPLAMA ÜZERİNE 

            cv2.destroyAllWindows()   # TÜM PENCERLERİ KAPAT
            cv2.imshow("roi_alan_kutucuk",roi_alan_kutucuk)  # AŞAMALARI GÖRMEK İÇİN EKRANA VER 
            cv2.waitKey(0)

            ###############################################

            en_siklar, boy_siklar ,kanal= roi_alan_kutucuk.shape # ALDIĞIMIZ SORU KUTUCUĞUNUN SHAPİNİ ALIP KULLANIYORUZ 

            print("boy_siklar",roi_alan_kutucuk.shape) 
            boy_siklar_parca = int(boy_siklar/5)        # HER KUTUCUKTA 5 SORU OLDUĞU İÇİN ALINAN X DEĞERİNİ 5 E BÖLÜYORUZ
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
                    area = cv2.contourArea(c)  # ALAN HESAPLAMA
                    print("area şık ",area)
                    
                    if area > 2500:  # BELİRLİ DOLULUGA ULAŞN DEĞERLERİ
                        cevap = i+1
                        isaretli += 1
                        
            if (isaretli == 0 and i==4) or isaretli > 1:
                cevaplar.append([i_soru , 0])
            else :
                cevaplar.append([i_soru ,cevap]) # ORTA NOKTASI BELİRLEME   
                        
            i_soru+=1 
            print("cevaplar",cevaplar)


hizalama(y1_hizalama,y2_hizalama,x1_hizalama,x2_hizalama)
birinci_soru_sütün(x1_birinci_soru_sutun,x2_birinci_soru_sutun)
