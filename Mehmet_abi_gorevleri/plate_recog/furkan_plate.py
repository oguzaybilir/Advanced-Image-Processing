import cv2
import numpy as np 
import matplotlib.pyplot as plt

img = cv2.imread("C:/KISISEL/pyhtonVs/goruntu_isleme/konvulasyon/abc.jpg")
img = cv2.resize(img,(960,600))
img = cv2.GaussianBlur(img,(5,5),3)

gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
gray = cv2.bitwise_not(gray)
kernel[0] = [1,1,0]
kernel[1] = [1,0,1]SFGHBSDFGHSDFGGHZDFGH
kernel[2] = [0,1,1]


kernelx = kernel.shape[0]
kernely = kernel.shape[1]

output_x = ( rows - kernel.shape[0] + 1)
output_y = ( cols - kernel.shape[1] + 1)

bos_ekran = np.zeros((output_x,output_y),np.uint8)


for x in range(output_x):
    for y in range(output_y):

        bos_ekran[x,y]= np.sum(gray[x: x+kernelx,y: y+kernely]*kernel)



plt.figure(1)
plt.imshow(bos_ekran)
plt.figure(2)
plt.imshow(gray)

plt.show()

cv2.destroyAllWindows()