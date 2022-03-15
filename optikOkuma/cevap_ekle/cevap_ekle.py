import numpy as np

cevaplar_ogrenci = [[1, 1], [2, 1], [3, 1], [4, 8], [5, 8], [6, 4], [7, 4], [8, 3], [9, 3], [10, 7], [11, 7], [12, 10], [13, 10], [14, 8], [15, 8], 
[16, 8], [17, 8], [18, 8], [19, 8], [20, 8], [21, 8]]

np.array(cevaplar_ogrenci)
print(len(cevaplar_ogrenci))

sozluge_gidecekler = {}

for i, j in np.array(cevaplar_ogrenci):

    i = 0
    j = 0

    if j == 0:
        j = None
        sozluge_gidecekler[i] = j
    
    j = 1

    i += 1
    j += 1

    sozluge_gidecekler[i] = j
    print(sozluge_gidecekler)

print(sozluge_gidecekler)  