from imutils import build_montages #gerekli kütüphaneleri import ediyoruz
from imutils import paths 
import argparse
import random
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-i","--image",required=True, help = "path to input directory of images")
ap.add_argument("-s","--sample",required=True, type=int, default=21, help=" #of images to make")
args = vars(ap.parse_args())

imagepaths = list(paths.list_images(args["image"]))  #imutilsin içindeki list_images fonksiyonunu çağırdık
random.shuffle(imagepaths)
imagepaths = imagepaths[:args["sample"]]

images = []   # görselleri koyacağımız bir liste oluşturduk

for imagepath in imagepaths: # resim dosya yollarının içinde dönen bir döngü oluşturduk
    image = cv2.imread(imagepath)   # görselleri yükledik ve görsel listesini güncelledik
    images.append(image)

# görseller için montagesleri kurduk
montages = build_montages(images, (128,196), (7,3))

for montage in montages:
    cv2.imshow("montage",montage)
    cv2.waitKey(0)

