import os,sys
folder = "C:/Users/oguza/OneDrive/Belgeler/GitHub/ileri_seviye_imageProcessing/advancedLevel/optikOkuma2/images"
#folder değişkenine, değiştirmek istediğiniz dosyaların bulunduğu klasör yolunu kopyalayın
for filename in os.listdir(folder):
    infilename = os.path.join(folder,filename)
    if not os.path.isfile(infilename):
        continue
    oldbase = os.path.splitext(filename)
    newname = infilename.replace('.png', '.jpeg')
    output = os.rename(infilename, newname)