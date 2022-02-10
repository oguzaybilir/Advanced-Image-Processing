import serial as s
import time



Serial = s.Serial("/dev/ttyUSB0",9600)
time.sleep(2) # sistemin hazır hale gelmesi için bir süre bekletiyoruz
print(Serial.readline())

while True:
    var = int(input("press 1 or 0 "))
    print("girilen deger", var)

    if var == 1:
        Serial.write(b'1')
    if var == 0:
        Serial.write(b'0')