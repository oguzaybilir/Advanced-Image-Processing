import numpy as np  #gerekli kütüphaneleri import ettik
import cv2
from color_transfer import color_transfer
import argparse

from numpy.lib.utils import source



def show_image(title,image,width=300):  #show image adlı bir fonksiyon tanımladık ve içinde 
                                        #hem resmimizi  aspect:ratio oranına uygun şekilde resize ettik 
                                        #hem de resmimizi imshow ettirdik
    r = width/float(image.shape[1])
    dim =(width, int(image.shape[0]*r))
    resized = cv2.resize(image,dim,interpolation = cv2.INTER_AREA)

    cv2.imshow(title, resized)

def str2bool(v):                                    #str2bool adındanda anlaşılabileceği gibi string olabilecek değerleri alıp 
    if v.lower() in ('yes', 'true', 't','y','1'):   #boolean değerlerine (True, False) dönüştürüyoruz
        return True
    elif v.lower() in ('no', 'false',  'f','n','0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected')  #eğer alınan string değeri üsttekilere uymuyorsa direkt olarak Boolean değeri bekleniyor


ap = argparse.ArgumentParser()  #kullanıcıdan veri girişi almak için gerekli kodları yazdık
ap.add_argument("-s","--source", required=True, help="path tho the source image")
ap.add_argument("-t","--target", required=True, help="path to the target image")
ap.add_argument("-c","--clip", type=str2bool, default='t', help="should np.clip scale L*a*b* values before final conversation to BGR""Approptiate min-max scaling used if False.")
ap.add_argument("-p", "--preservePaper", type = str2bool, default = 't', help = "Should color transfer strictly follow methodology layed out in original paper?")
ap.add_argument("-o", "--output", help = "Path to the output image (optional)")
args = vars(ap.parse_args())



# source ve target değerlerini imread ettirdik
source = cv2.imread(args["source"])
target = cv2.imread(args["target"])

# source image  source tan target a değişim yapılıyor
transfer = color_transfer(source, target, clip=args["clip"], preserve_paper=args["preservePaper"])

# output yani çıktı resmi kaydedilsin diye zorla kaydettiriyoruz
if args["output"] is not None:
	cv2.imwrite(args["output"], transfer)


 # üstte yazdığımız show_image fonksiyonu ile resmi aspect:ratio ya göre resize ettirdik ve imshow ettirdik 
show_image("Source", source)
show_image("Target", target)
show_image("Transfer", transfer)
cv2.waitKey(0)

  #BURADA COLOR_TRANSFER fonksiyonunun mantığı anlatılmaktadır
"""
def color_transfer(source, target):
    source = cv2.cvtColor(source, cv2.COLOR_BGR2LAB).astype("float32")
    target = cv2.cvtColor(target, cv2.COLOR_BGR2LAB).astype("float32")

    (lMeanSrc, lStdSrc, aMeanSrc, aStdSrc, bMeanSrc, bStdSrc) = image_stats(source)
    (lMeanTar, lStdTar, aMeantar, aStdTar, bMeanTar, bStdTar) = image_stats(target)

    (l,a,b) = cv2.split(target)
    l -= lMeanTar
    a -= aMeantar
    b -= bMeanTar

    l = (lStdTar / lStdSrc) *l
    a = (aStdTar / aStdSrc) *a
    b = (bStdTar / bStdSrc) *b


    l += lMeanSrc
    a += aMeanSrc
    b += bMeanSrc


    l = np.clip(l, 0, 255)
    a = np.clip(a, 0, 255)
    b = np.clip(b, 0, 255)

    transfer = cv2.merge([l, a, b])
    transfer = cv2.cvtColor(transfer.astype("uint8"), cv2.COLOR_LAB2BGR)

    return transfer

def image_stats(image):

    (l,a,b) = cv2.split(image)
    (lMean, lStd) = (l.mean(), l.std())
    (aMean, aStd) = (a.mean(), a.std())
    (bMean, bStd) = (b.mean(), b.std())

    return (lMean, lStd, aMean, aStd, bMean, bStd)
"""