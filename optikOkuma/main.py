import cv2
import numpy as np
import kenar_algilama as kenar
import imutils
import ogrenci_numarasi as ogrenci_no
import  ogrenci_degerlendirme 
import soru_sutunlar as soru_sutun
import kitapcik_turu as kitapcik

class optik_okuma():



    def __init__(

        self,image,y1_hizalama,y2_hizalama,x1_hizalama,x2_hizalama,
        kenar_siyahlar,
        x1_ogrenci_no_sutun, x2_ogrenci_no_sutun, ogrenci_no_indis_1, ogrenci_no_indis_2, ogrenci_no_aralik,
        x1_ogrenci_degerlendirme, x2_ogrenci_degerlendirme, ogrenci_degerlendirme_indis_1, ogrenci_degerlendirme_indis_2, ogrenci_degerlendirme_aralık, 
        x1_birinci_soru_sutun, x2_birinci_soru_sutun, birinci_soru_sutun_indis_1, birinci_soru_sutun_indis_2, birinci_soru_sutun_aralık,
        x1_ikinci_soru_sutun, x2_ikinci_soru_sutun, ikinci_soru_sutun_indis_1, ikinci_soru_sutun_indis_2, ikinci_soru_sutun_aralık,
        x1_ucuncu_soru_sutun, x2_ucuncu_soru_sutun, ucuncu_soru_sutun_indis_1, ucuncu_soru_sutun_indis_2, ucuncu_soru_sutun_aralık,
        x1_kitapcik_turu,x2_kitapcik_turu,b_kitapcik_turu_indis_1,c_kitapcik_turu_indis_1,kitapcik_turu_aralık):

        self.image = image

        #-------HIZALAMA TANIMLAR-------#
        self.y1_hizalama = y1_hizalama
        self.y2_hizalama = y2_hizalama
        self.x1_hizalama = x1_hizalama
        self.x2_hizalama = x2_hizalama
        self.kenar_siyahlar = kenar_siyahlar

        #-------ÖĞRENCİ NO TANIMLAR ------------#
        self.x1_ogrenci_no_sutun = x1_ogrenci_no_sutun
        self.x2_ogrenci_no_sutun = x2_ogrenci_no_sutun
        self.ogrenci_no_indis_1 = ogrenci_no_indis_1
        self.ogrenci_no_indis_2 = ogrenci_no_indis_2
        self.ogrenci_no_aralik = ogrenci_no_aralik

        #--------  ÖĞRENCİ DEĞERLENDİRME TANINMLAR -----------#
        self.x1_ogrenci_degerlendirme = x1_ogrenci_degerlendirme       
        self.x2_ogrenci_degerlendirme = x2_ogrenci_degerlendirme
        self.ogrenci_degerlendirme_indis_1 = ogrenci_degerlendirme_indis_1 
        self.ogrenci_degerlendirme_indis_2 =  ogrenci_degerlendirme_indis_2 
        self.ogrenci_degerlendirme_aralık = ogrenci_degerlendirme_aralık


        #--------  BİRİNCİ SUTUN SORU TANIMLAR -----------#
        self.x1_birinci_soru_sutun = x1_birinci_soru_sutun   
        self.x2_birinci_soru_sutun = x2_birinci_soru_sutun 
        self.birinci_soru_sutun_indis_1 = birinci_soru_sutun_indis_1 
        self.birinci_soru_sutun_indis_2 = birinci_soru_sutun_indis_2 
        self.birinci_soru_sutun_aralık = birinci_soru_sutun_aralık 

        #--------  İKİNCİ SUTUN SORU TANIMLAR -----------#
        self.x1_ikinci_soru_sutun = x1_ikinci_soru_sutun   
        self.x2_ikinci_soru_sutun = x2_ikinci_soru_sutun 
        self.ikinci_soru_sutun_indis_1 = ikinci_soru_sutun_indis_1
        self.ikinci_soru_sutun_indis_2 = ikinci_soru_sutun_indis_2 
        self.ikinci_soru_sutun_aralık = ikinci_soru_sutun_aralık  

        #--------  ÜÇÜNCÜ SUTUN SORU TANIMLAR -----------#
        self.x1_ucuncu_soru_sutun = x1_ucuncu_soru_sutun      
        self.x2_ucuncu_soru_sutun = x2_ucuncu_soru_sutun 
        self.ucuncu_soru_sutun_indis_1 = ucuncu_soru_sutun_indis_1 
        self.ucuncu_soru_sutun_indis_2 = ucuncu_soru_sutun_indis_2 
        self.ucuncu_soru_sutun_aralık = ucuncu_soru_sutun_aralık 

        #--------  KİTAPCIK TÜRÜ TANIMLAR -----------#
        self.x1_kitapcik_turu = x1_kitapcik_turu  
        self.x2_kitapcik_turu = x2_kitapcik_turu
        self.b_kitapcik_turu_indis_1 = b_kitapcik_turu_indis_1  # B TİPİ DEĞERLENDİRME İNDİSİ
        self.c_kitapcik_turu_indis_1 = c_kitapcik_turu_indis_1  # C TİPİ DEĞERLENDİRME İNDİSİ
        self.kitapcik_turu_aralık = kitapcik_turu_aralık
        
        super().__init__()
        


    image = cv2.imread("C:/Users/oguza/OneDrive/Belgeler/GitHub/ileri_seviye_imageProcessing/advancedLevel/optikOkuma/hatali.jpg")


    #------------------- SORU TİPİNE GÖRE SORU ADETİ VE YÖNLENDİRME --------------------------------------#

    def b_tipi_soru(self):   # B TİPİ YÖNLENDİRME 

        soru_sayisi = int(input("SORU SAYISI: "))

        if soru_sayisi <= 40:
            #------- Hesaplama -------#
            fark = 40 - soru_sayisi
            self.birinci_soru_sutun_indis_2 = self.birinci_soru_sutun_indis_2 - fark
            #-------Foksiyonların çağrılması-------#
            cevap_1 = self.birinci_soru_sutun_start(self)
            #---- Cevapların Toplanması ----#
            print("cevap_1",cevap_1)
            cevap_final= cevap_1

        elif 80 >= soru_sayisi > 40 :
            #------- Hesaplama -------#
            fark = 80 - soru_sayisi
            self.ikinci_soru_sutun_indis_2 = self.ikinci_soru_sutun_indis_2 - fark
            #-------Foksiyonların çağrılması-------#
            cevap_1 = self.birinci_soru_sutun_start(self)
            cevap_2 = self.ikinci_soru_sutun_start(self)
            print("cevap1 ",cevap_1)
            print("cevap2 ",cevap_2)
            #---- Cevapların Toplanması ----#
            cevap_final = cevap_1.append(cevap_2)

        elif 120 >= soru_sayisi > 80 :
            #------- Hesaplama -------#
            fark = 120 - soru_sayisi
            self.ucuncu_soru_sutun_indis_2 = self.ucuncu_soru_sutun_indis_2 - fark
            #-------Foksiyonların çağrılması-------#
            cevap_1 = self.birinci_soru_sutun_start(self)
            cevap_2 = self.ikinci_soru_sutun_start(self)
            cevap_3 = self.ucuncu_soru_sutun_start(self)

            print("cevap1 ",cevap_1)
            print("cevap2 ",cevap_2)
            print("cevap3 ",cevap_3)

            #---- Cevapların Toplanması ----#
            
            cevap_1.append(cevap_2)
            cevap_1.append(cevap_3)
            cevap_final.append(cevap_1)
        
        else:
            print("SORU SAYISI HATALI LÜTFEN KONTROL EDİNİZ")

        return cevap_final
    

    #--------------------------------------------------------#

    def c_tipi_soru(self): # C TİPİ YÖNLENDİRME
           
        soru_sayisi = int(input("SORU SAYISI: "))
        self.ogrenci_no_start(self)

        if soru_sayisi <= 40:
            fark = 40 - soru_sayisi
            self.birinci_soru_sutun_indis_2 = self.birinci_soru_sutun_indis_2 - fark
            cevap_1 = self.birinci_soru_sutun_start(self)
            cevap_final = cevap_1
        else:
            print("Soru sayısı 40 den büyük olamaz")

        return cevap_final


    #------------------------------ KENAR ALGILAMA VE KONTROL --------------------------------------#

    #-------HIZALAMA AYARLAR-------#
    y1_hizalama = 0   
    y2_hizalama = image.shape[0]  
    x1_hizalama = 35         
    x2_hizalama = 255 

    def kenar_algılama_ve_kontrol(self):
   
        self.kenar_siyahlar = kenar.hizalama(self.image,self.y1_hizalama,self.y2_hizalama,self.x1_hizalama,self.x2_hizalama)

        for i in range(0,3,1):

            if len(self.kenar_siyahlar) == 62:
                print("elsedeyim")
                print("ikinci kontrol",len(self.kenar_siyahlar))
                self.kagit_tipi_secimi(self)

            #----------- KENAR KONTROLU ------------------#
            elif len(self.kenar_siyahlar) != 62:
                print("HATA: KENAR SİYAH SAYISI 62 DEĞİL")
                print("KENAR SİYAH SAYISI: ",self.kenar_siyahlar)
                print("RESİM 180 DERECE DÖNDÜRÜLÜP TEKRAR DENENİYOR")
                self.image = imutils.rotate(self.image, 180)
                self.kenar_siyahlar = kenar.hizalama(self.image,self.y1_hizalama,self.y2_hizalama,self.x1_hizalama,self.x2_hizalama)
            
            if i>=2:
                break

        else:
            print("KENARLARI KONTROL EDİNİZ KENAR CİZGİLERDE HATA VAR ")

        return self.kenar_siyahlar

   
    #------------------  KAĞIT TİPİNE GÖRE YÖNLENDİRME   ----------------------#

    def kagit_tipi_secimi(self):  # kagıt tipi ekle arguman olarak kagıt tipi alınacak

        kagit_tipi = input("KAGIT TİPİNİ SEÇİNİZ: ")
        kagit_tipi = kagit_tipi.upper()
                
        if kagit_tipi == "A":
            # test yok
            #sadecece hoca değerendirmesi
            ogrenci_no = self.ogrenci_no_start(self)

        if kagit_tipi == "B":
           
            ogrenci_no = self.ogrenci_no_start(self)
            soru_cevap = self.b_tipi_soru(self)  # b tipi sorularının adet kıyaslaması
            kitapcik_türü = self.b_tipi_kitapcik_turu_start(self)
            
        if kagit_tipi == "C":

            ogrenci_no = self.ogrenci_no_start(self)
            soru_cevap = self.c_tipi_soru(self)
            kitapcik_türü = self.c_tipi_kitapcik_turu_start(self)
 
        else:
            print("HATA: KAGIT TİPİ SEÇİMİ YANLIŞ")



#------------------------------------------ OGRENCİ NO ------------------------------------------------# 
 
    #---ÖĞRENCİ NO DEĞERLER---#
    x1_ogrenci_no_sutun = 294
    x2_ogrenci_no_sutun= 1294
    ogrenci_no_indis_1 = 4
    ogrenci_no_indis_2 = 13
    ogrenci_no_aralik = 44
      
    def ogrenci_no_start(self):

        cevap = ogrenci_no.ogrenci_no_sutun(

            self.kenar_siyahlar, self.image, self.x1_ogrenci_no_sutun, self.x2_ogrenci_no_sutun,
            self.ogrenci_no_indis_1, self.ogrenci_no_indis_2, self.ogrenci_no_aralik

            )
        return cevap

        
#-------------------------------------------- HOCA DEĞERLENDİRME -------------------------------------------------------#
        
    #--- ÖĞRENCİ DEĞENDİRME DEĞERLER ----#
    x1_ogrenci_degerlendirme = 2493    
    x2_ogrenci_degerlendirme= 4590
    ogrenci_degerlendirme_indis_1 = 4
    ogrenci_degerlendirme_indis_2 = 13
    ogrenci_degerlendirme_aralık = 44

    def ogrenci_degerlendirme_start(self):

        cevap = ogrenci_degerlendirme.ogrenci_degerlendirme_sutun(
            self.kenar_siyahlar, self.image, self.ogrenci_degerlendirme_aralık, self.x1_ogrenci_degerlendirme, self.x2_ogrenci_degerlendirme,
            self.ogrenci_degerlendirme_indis_1, self.ogrenci_degerlendirme_indis_2)
        return cevap




#-------------------------------------------- SORU KONTROL  -------------------------------------------------------#

#------------------------------------------------#
    #---SORU SUTUN BİR DEĞERLER---#
    x1_birinci_soru_sutun  = 496  
    x2_birinci_soru_sutun = 1023
    birinci_soru_sutun_indis_1 = 16
    birinci_soru_sutun_indis_2 = 57
    birinci_soru_sutun_aralık = 43

    def birinci_soru_sutun_start(self):

        deger_1 = soru_sutun.birinci_soru_sutun(
        self.kenar_siyahlar, self.image, self.x1_birinci_soru_sutun,self.x2_birinci_soru_sutun,
        self.birinci_soru_sutun_indis_1,self.birinci_soru_sutun_indis_2,self.birinci_soru_sutun_aralık)
        return deger_1



#-----------------------------------------------#

    #---SORU SUTUN İKİ DEĞERLER---#
    x1_ikinci_soru_sutun  = 1400   
    x2_ikinci_soru_sutun = 1904
    ikinci_soru_sutun_indis_1 = 16
    ikinci_soru_sutun_indis_2 = 57
    ikinci_soru_sutun_aralık = 43

    def ikinci_soru_sutun_start(self):
        deger_2 = soru_sutun.ikinci_soru_sutun(
        self.kenar_siyahlar, self.image, self.x1_ikinci_soru_sutun, self.x2_ikinci_soru_sutun, 
    self.ikinci_soru_sutun_indis_1, self.ikinci_soru_sutun_indis_2, self.ikinci_soru_sutun_aralık)    
        return deger_2


#-----------------------------------------------#

    #---SORU SUTUN ÜÇ DEĞERLER---#
    x1_ucuncu_soru_sutun  = 2297   
    x2_ucuncu_soru_sutun = 2805
    ucuncu_soru_sutun_indis_1 = 16
    ucuncu_soru_sutun_indis_2 = 57
    ucuncu_soru_sutun_aralık = 43  

    def ucuncu_soru_sutun_start(self):
        deger_3 = soru_sutun.ucuncu_soru_sutun(
        self.kenar_siyahlar, self.image, self.x1_ucuncu_soru_sutun, self.x2_ucuncu_soru_sutun,
        self.ucuncu_soru_sutun_indis_1, self.ucuncu_soru_sutun_indis_2, self.ucuncu_soru_sutun_aralık)
        return deger_3


#------------------------------------------ KİTAPCIK TURU ----------------------------------------------------#

    #---KİTAPCİK TÜRÜ DEĞERLER---#
    x1_kitapcik_turu = 1408    
    x2_kitapcik_turu = 2608
    b_kitapcik_turu_indis_1 = 4
    c_kitapcik_turu_indis_1 = 3
    kitapcik_turu_aralık = 44

    def b_tipi_kitapcik_turu_start(self):
        kitapcik_turu = kitapcik.kitapcik_turu(
        self.kenar_siyahlar, self.image, self.x1_kitapcik_turu,self.x2_kitapcik_turu,
        self.b_kitapcik_turu_indis_1, self.kitapcik_turu_aralık)
        return kitapcik_turu

    def c_tipi_kitapcik_turu_start(self):
        kitapcik_turu = kitapcik.kitapcik_turu(
        self.kenar_siyahlar, self.image, self.x1_kitapcik_turu,self.x2_kitapcik_turu,
        self.c_kitapcik_turu_indis_1, self.kitapcik_turu_aralık)
        return kitapcik_turu











  

