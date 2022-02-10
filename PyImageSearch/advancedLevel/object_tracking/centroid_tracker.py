from lib2to3.pgen2.token import STAREQUAL
from pyparsing import Or
from scipy.spatial import distance as dst       #   gerekli kütüphaneleri import  ettik
from collections import OrderedDict
import numpy as np

class CentroidTracker():        #   merkezleri takip edecek olan classfonksiyonu yazıyoruz
    def __init__(self,maxDisappeared=50):   

        #bulunan objeleri bir sözlükte tutuyoruz bunun nedeni ise herbir obje ID sinin eşsiz olmasının istenmesi
        #örnek olarak bulunan objelerin etrafları farklı renklerle çizildiğinde
        # mavi bir kare nin etrafı yeşil ile çizilirse o kare ekrandan çıkarıldıpğında bile yeşil renkle çizilen başka bir
        #obje ekranda olmayacak
        self.nextObjectID = 0   
        self.objects = OrderedDict()
        self.disappeared = OrderedDict()

        self.maxDisappeared = maxDisappeared

    def register(self,centroid):
        # bir obje kayıtedildiğinde bir sayı ile numaralandırılacak ve ondan sonra gelen kayıt bir öncekinden 1 fazla olacak
        self.objects[self.nextObjectID] = centroid
        self.disappeared[self.nextObjectID] = 0
        self.nextObjectID += 1

    def deregister(self,objectID):

        del self.objects[objectID]
        del self.disappeared[objectID]


    def update(self,rects):

        if len(rects) == 0:

            for objectID in list(self.disappeared.keys()):
                self.disappeared[objectID] += 1


                if self.disappeared[objectID] > self.maxDisappeared:
                    self.deregister(objectID)

            return self.objects
        
        inputCentroids = np.zeros((len(rects),2),dtype="int")

        for (i,(startX,startY,endX,endY)) in enumerate(rects):

            cX = int((startX + endX)/2.0)
            cY = int((startY + endY)/2.0)
            inputCentroids = (cX,cY)
