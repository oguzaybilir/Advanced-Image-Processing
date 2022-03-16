import glob
import os

metin_belgesi = open("C:/Users/oguza/OneDrive/Belgeler/GitHub/ileri_seviye_imageProcessing/advancedLevel/optikOkuma2/klasorden_dosya_alma.txt", "x")

metin_dosyalari = glob.glob("C:/Users/oguza/OneDrive/Belgeler/GitHub/ileri_seviye_imageProcessing/advancedLevel/optikOkuma2/images/*.jpeg")

liste = []

for dosya in metin_dosyalari:

    basename = os.path.basename(dosya)
    #basename = str(basename)
    liste.append(str(basename))

print(sorted(liste))