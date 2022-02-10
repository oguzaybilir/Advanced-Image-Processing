from PyQt5.QtWidgets import*
from ana_ekran_python import Ui_MainWindow
import os
import json


#    C:\Users\90551\venv\Scripts\pyuic5.exe -x untitled.ui -o untitled_python.py

class ana_ekran_python(QMainWindow):

    

    def __init__(self):

        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("OPTİK OKUMA")
        self.sayac = 0
        self.cevaplar= {}
        self.cevap_liste= []
        

        #------ BUTONLARI KAPATIYOR--------#
        self.ui.dosya_yolu_duzenle_buton.setEnabled(False)  # butonu kapatıyor
        self.ui.ekle_butonu.setEnabled(False)
        self.ui.bitir_butonu.setEnabled(False)
        self.ui.temizle_butonu.setEnabled(False)
        self.ui.cevap.setReadOnly(True)
        self.ui.bitir_butonu.setEnabled(False)
        self.ui.temizle_butonu.setEnabled(False)
        

    def dosya_yolu_buton(self,index):

        
        self.ui.dosya_yolu_buton.setEnabled(False)
        self.ui.dosya_yolu.setReadOnly(True)        # KUTUCUĞU SADECE OKUNABİLİR HALE GETİYOR
        self.dosya_yolu = self.ui.dosya_yolu.text() # DOSYA YOLUNU ÇEKİYOR

        print(self.dosya_yolu)

        if os.path.exists(self.dosya_yolu):    # dosya dizini kontrol ediyor
            
            #  self.ui.dosya_yolu_bilgi.setStyle()
            self.ui.dosya_yolu_bilgi.setText("Dosya Bulundu")  # bilgi veriyor
            self.ui.dosya_yolu_duzenle_buton.setEnabled(True)  # düzenle butonu aktif hale geliyor 
            self.ui.ekle_butonu.setEnabled(True)
            self.ui.cevap.setReadOnly(False)
            self.ui.bitir_butonu.setEnabled(True)
            self.ui.temizle_butonu.setEnabled(True)

        else:

            self.ui.dosya_yolu_bilgi.clear()                      # bilgiyi temizliyor
            self.ui.dosya_yolu_bilgi.setText("Dosya Bulunamadı")  # bilgi veriyor
            self.ui.dosya_yolu_buton.setEnabled(True)             # butonu aç
            self.ui.dosya_yolu.setReadOnly(False)                 # düzenlemeyi aç
            
    
    def dosya_yolu_duzenle_buton(self):

        self.ui.dosya_yolu_bilgi.clear()   # bilgiyi temizliyor
        self.ui.dosya_yolu.setReadOnly(False)  # yazı yerini aç 
        self.ui.dosya_yolu_buton.setEnabled(True)
        self.ui.dosya_yolu_duzenle_buton.setEnabled(False)
        self.dosya_yolu = None
        
    def cevap_ekle(self):
        
        cevap = self.ui.cevap.text()  # harfi cekiyoruz
        cevap = cevap.upper()
        self.ui.bilgi_optik_sag.clear()


        if cevap == "A" or cevap == "B" or cevap == "C" or cevap == "D" or cevap == "E" :   
            # gelen harfleri kontrol ediyor

            cevap = cevap.upper()   # hepsini büyük harf yapıyoruz
            soru_indis = {"A":"0",  # sözlüğümüz
                         "B":"1",
                         "C":"2",
                         "D":"3",
                         "E":"4"}
            
            cevap_indis = soru_indis[cevap] # harfleri indise ceviriyoruz
            
            
            self.cevaplar[self.sayac] = cevap_indis # sözlüğe ekleme

            self.sayac = self.sayac + 1
        
            self.ui.cevap.clear()
            self.ui.bilgi_optik_sol.clear()
            self.ui.bilgi_optik_sol.setText("Cevap Eklendi. Son eklenen: {} . Cevap Adedi: {} ".format(cevap,self.sayac))
        
            self.cevap_liste.append(cevap) # cevapalrı harf olarak yeni bir listeye ekliyoruz
            print(self.cevap_liste)      
            result = json.dumps(self.cevap_liste) # sözlüğü dönüştürüyor
            self.ui.cevap_liste.setText(result)  #liseye yazdırıyor
   



        else :          # geçersiz girişteki durumlar 

            self.ui.cevap.clear()  # kutuyu temizle
            self.ui.bilgi_optik_sol.clear()   # yazıyı temizle
            self.ui.bilgi_optik_sol.setText("Geçersiz Karakter. Tekrar Deneyiniz")

        


    def bitir_butonu(self):

        self.ui.ekle_butonu.setEnabled(False)
        self.ui.cevap.setReadOnly(True)
        self.ui.bilgi_optik_sag.clear()
        self.ui.bilgi_optik_sag.setText("KAYIT EDİLDİ")

    def temizle_butonu(self):

        #---- listeleri temızle ---#
        self.cevaplar= {}
        self.cevap_liste= []
        self.sayac = 0

        #---  cevapları temizle ---#
        self.ui.cevap.clear()
        self.ui.cevap_liste.clear()
        self.ui.bitir_butonu.setEnabled(True)
        self.ui.temizle_butonu.setEnabled(True)
        self.ui.cevap.setReadOnly(False)
        self.ui.bilgi_optik_sol.clear()
        self.ui.bilgi_optik_sag.clear()
        self.ui.bilgi_optik_sag.setText("Temizlendi")
        self.ui.ekle_butonu.setEnabled(True)


def arayuz_ac():

    uygulama = QApplication([])
    pencere = ana_ekran_python()
    pencere.show()
    uygulama.exec_()

arayuz_ac()