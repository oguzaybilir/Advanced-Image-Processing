from skimage.segmentation import clear_border       #   gerekli kütüphaneleri import ediyoruz
from imutils import contours
import numpy as np
import argparse
import imutils
import cv2

def extract_digits_and_symbols(image,charCnts,minW=5,minH=15):      #   digitleri ve sembolleri ayıracak olan fonksiyonu yazıyoruz
    charIter = charCnts.__iter__()  #   bir iterator yani yineleyici kullanarak listedeki objelerin kullanılmaya uygun olup olmadıklarını test ediyoruz
    rois = []   #   roileri ileride dolduracağımız boş bir listede tutuyoruz
    locs = []   #   lokasyonları ileride dolduracağımız boş bir listede tutuyoruz

    while True:     #   bir while döngüsü oluşturuyoruz
        try:    #   dene
            c = next(charIter)  
            (cX,cY,cW,cH) = cv2.boundingRect(c)
            roi = None

            if cW >= minW and cH >= minH:
                roi = image[cY:cY+cH, cX:cX+cW]

                rois.append(roi)
                locs.append(cX,cY,cX+cW,cY+cH)

            else:
                parts = [c,next(charIter),next(charIter)]
                (sXA,sYa,sXB,sYB) = (np.inf, np.inf, -np.inf, -np.inf )

                for p in parts:
                    (pX,pY,pW,pH) = cv2.boundingRect(p)
                    sXA = min(sXA,pX)
                    sYA = min(sYA,pY)
                    sXB = max(sXB,pX+pW)
                    sYB = max(sYB,pY+pH)

                roi = image[sYA:sYB, sXA:sXB]
                rois.append(roi)
                locs.append((sXA,sYA,sXB,sYB))
        except StopIteration:
            break

    return (rois,locs)


