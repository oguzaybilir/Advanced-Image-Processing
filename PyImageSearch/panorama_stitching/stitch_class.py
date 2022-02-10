import numpy as np  #gerekli kütüphaneleri import ettik
import imutils
import cv2

class Stitcher:     #Stitcher classını oluşturduk
    def __init__(self): 
        self.isv3  = imutils.is_cv3(or_better=True) #kullandığımız opencv sürümünü kontrol ediyoruz, çünkü sürümden sürüme fark ediyor

    def stitch(self,images,ratio=0.75,reprojThresh=4.0,showMatches=False):  # iki görsel arasındaki ortak noktaları bulan fonksiyonumuzu yazıyoruz
        (imageA,imageB) = images
        (kpsA,featuresA) = self.detectAndDescribe(imageA)   #   A görselinin kilit noktalarını ve özelliklerini bulduruyoruz
        (kpsB,featuresB) = self.detectAndDescribe(imageB)   #   B görselinin kilit noktalarını ve özelliklerini bulduruyoruz

        M = self.matchKeypoints(kpsA,kpsB,featuresA,featuresB,ratio,reprojThresh)   #   2 görsel arasındaki anahtar noktalar ve özellikleri eşleştiriyoruz

        if M == None:  #   Eğer anahtar noktalar arasında bir eşleşme olmazsa None döndürüyoruz
            print("M degeri None'dir") 
            return None

        (matches, H, status) = M    #   eşleşmeler, H , durum değişkenlerini içinde tutan bir M değeri atıyoruz
        result = cv2.warpPerspective(imageA,H,(imageA.shape[1]+imageB.shape[1], imageA.shape[0]))   #   görüntüye perspektif dönüşümü uyguluyoruz
        result[0:imageB.shape[0], 0:imageB.shape[1]] = imageB

        if showMatches: #   eğer kilit nokta eşleşmeleri gösterilebiliyorsa
            vis = self.drawMatches(imageA, imageB, kpsA, kpsB, matches, status) #   göster

            return (result,vis) #   sonucu ve kilit noktaları göster

        return result   #   sonucu döndür

    def detectAndDescribe(self, image): #   anahtar noktaları bulup özellikleri açıklayacak olan fonksiyonu yazıyoruz

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  #   görüntüyü gri renk uzayina ceviriyoruz

        if self.isv3:   #   eğer opencv sürümünüz 3 ten büyükse bu işlemleri yap    
            descriptor = cv2.xfeatures2d.SIFT_create()      #   SIFT = Scale-invariant feature transform OZELLIK DONUSUM YONTEMIDIR
            (kps,features) = descriptor.detectAndCompute(image,None)    #   SIFT donusum yontemi ile sakladigimiz anahtar noktalari ve özellikleri tespit edip hesapliyoruz

        else:   # opencv sürümü 3 ten küçükse bu islemleri yapiyoruz
            detector = cv2.FastFeatureDetector_create("SIFT")   #   detector degiskenine SIFT fonksiyonunu koyuyoruz
            kps = detector.detect(gray)     #   gri renk  uzayina cevirdigimiz resime SIFT donusumu uyguluyoruz


            extractor = cv2.DescriptorExtractor_create("SIFT")  #   
            (kps,features) = extractor.compute(gray,kps)    #   SIFT donusum yontemiyle sakladigimiz anahtar noktalari ve özellikleri tespit edip hesaplatiyoruz

        kps = np.float32([kp.pt for kp in kps]) #   anahtar noktalari bir array icine aliyoruz

        return (kps, features)  # anahtar noktalari ve ozellikleri döndür


    def matchKeypoints(self,kpsA,kpsB,featuresA,featuresB,ratio,reprojThresh):  #   2  görsel arasindaki anahtar noktalari eşletirecek olan fonksiyonu yaziyoruz
        
        matcher = cv2.DescriptorMatcher_create("BruteForce")    #   BruteForce yöntemiyle anahtar noktalari eşleştiriyoruz
        rawMatches = matcher.knnMatch(featuresA,featuresB,2)    #   ham eşleşmeleri k-nn eşleşme yöntemi ile bulduruyoruz
        matches = []    #   eşleşen noktaların tutulacağı bir array oluşturuyoruz

        for m in rawMatches:    #   ham eşleşmelerin içinde dönüyoruz

            if len(m) == 2 and m[0].distance < m[1].distance*ratio:  #   eğer ham eşleşmeler 2 ye eşitse ve Lowe'un ölçü testine göre arada belirli bir mesafe olması lazım, bu şartıda sağlıyorsa if 'in altındaki işlemleri yapacak
                matches.append((m[0].trainIdx, m[0].queryIdx))   #eşleşen noktaları saklayacağımız array'in içine noktaları ekliyoruz

            if len(matches) > 4:    #   eğer eşleşmelerin sayısı 4 ten fazla ise alttaki işlemleri yap
                ptsA = np.float32([kpsA[1] for (_,i) in matches])   #   A noktalarının içinde dönüyor ve array içine koyuyor
                ptsB = np.float32([kpsB[1] for (i,_) in matches])   #   B noktalarının içinde dönüyor ve array içine koyuyor

                (H, status) = cv2.findHomography(ptsA,ptsB,cv2.RANSAC,reprojThresh) #   RANSAC yöntemine göre Homografi işlemini uyguluyoruz

                return (matches, H, status) #   eşleşmeleri, H 'ı ve durumu döndürüyor

            return None #   None döndürüyoruz

    def drawMatches(self,imageA,imageB,kpsA,kpsB,matches,status):   #   Eşleşmeleri çizen fonksiyonu yazıyoruz

        (hA,wA) = imageA.shape[:2]  #   A görseline ait yükseklik ve genişlik değerlerini alıyoruz
        (hB,wB) = imageB.shape[:2]  #   B görseline ait yükseklik ve genişlik değerlerini alıyoruz
        vis = np.zeros((max(hA,hB),wA+wB,3),dtype="uint8")  #   vis adında, A ve B yüksekliklerinden en büyük olanı yükseklik, A ve B görsellerinin genişliklerinin toplamını da genişlik kabul eden bir tuval oluşturuyoruz(siyah bir tuval)
        vis[0:hA, 0:wA] = imageA    #   vis'e ait olan en ve boyu A görseline ait yapıyoruz(resize ediyoruz)
        vis[0:hB, wA:] = imageB     #   vis'e ait olan en ve boyu B görseline ait yapıyoruz(resize ediyoruz)

        for ((trainIdx, queryIdx),s) in zip(matches, status):   # eşleşmeleri ve durumları zipliyor ve trainIdx ile queryIdx değişkenlerinini ziplenmiş şeyin içinde dönderiyoruz

            if s == 1:  #   s burada status(durum) içinde dönecek ve sadece line çekilebiliryorsa yani durum 1 ise işlem devam edecek
                ptA = (int(kpsA[queryIdx][0]),int(kpsA[queryIdx][1]))   #   A görseli üzerinde line çekilecek noktalardan birincisi
                ptB = (int(kpsB[trainIdx][0])+wA, int(kpsB[trainIdx][1]))   #   B görseli üzerindeki line çekilecek noktalardan birincisi

                cv2.line(vis, ptA, ptB, (0,255,0), 1)   #   ptA ve ptB noktalarını kullanarak vis üzerinde bir line çekiyoruz

        return vis  #   anahtar noktaların olduğu ve line çizilmiş olan görseli dönder
            