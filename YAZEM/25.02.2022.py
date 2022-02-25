aranan = 7
pozisyon = -1
dizi = [3,4,9,7,3,1]

x = 0

for x in range(len(dizi)-1):
    if aranan == dizi[x]:
        pozisyon = x
    else:
        continue

print(pozisyon)