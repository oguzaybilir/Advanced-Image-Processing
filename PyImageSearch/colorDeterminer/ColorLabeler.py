# import the necessary packages
from scipy.spatial import distance as dist
from collections import OrderedDict
import numpy as np
import cv2
class ColorLabeler:
    def __init__(self):
        colors = OrderedDict({"red": (255, 0, 0),"green": (0, 255, 0),"blue": (0, 0, 255),"yellow":(255,255,0),"orange":(255,165,0)})
        #renk isimlerini ve değerlerini bir sözlük içine yazdık, bir renk sözlüğü oluşturduk

        self.lab = np.zeros((len(colors), 1, 3), dtype="uint8") #L*a*b* dönüşümü için bir tuval oluşturuyoruz
        self.colorNames = []    #L*a*b* dönüşümü için bir hafıza gerek, bir liste oluşturuyoruz

        for (i, (name, rgb)) in enumerate(colors.items()):  #renk sözlüğünün içinde dönüyoruz
            self.lab[i] = rgb   #L*a*b* dönüşümü için ayırdığımız hafızaya yani array e verileri ekliyoruz
            self.colorNames.append(name)

        self.lab = cv2.cvtColor(self.lab, cv2.COLOR_RGB2LAB)    #L*a*b* array i içindeki verileri RGB uzayından L*a*b* uzayına çeviriyoruz ve renk uzayı dönüşüm işlemini tamamlıyoruz
    
    def label(self, image, c):  #   konturleri maskeleyerek maskelenmiş alanın ortalama L*a*b* değerini bulan bir fonksiyon yazıyoruz
       
        mask = np.zeros(image.shape[:2], dtype="uint8")
        cv2.drawContours(mask, [c], -1, 255, -1)
        mask = cv2.erode(mask, None, iterations=2)
        mean = cv2.mean(image, mask=mask)[:3]   #maskelenmiş alanın ortalama değerini alır

        minDist = (np.inf, None)    #şimdiye kadar bulduğumuz minimum mesafeden başlıyoruz

        for (i, row) in enumerate(self.lab):    #dönüştürdüğümüz L*a*b* değerlerinin içinde dönüyoruz

            d = dist.euclidean(row[0], mean)    #meanle bulduğumuz değerle L*a*b* değeri arasındaki farkı hesaplıyor

            if d < minDist[0]:
                minDist = (d, i)

        return self.colorNames[minDist[1]]  #en küçük farkla renkleri isimlendiriyor


