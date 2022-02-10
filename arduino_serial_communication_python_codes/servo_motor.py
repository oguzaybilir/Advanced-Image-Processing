import serial as s
import time 

Serial = s.Serial("/dev/ttyUSB0",9600)
time.sleep(2)

while True:
    pos = input("0 ile 180 arasında bir deger giriniz")
    print("girilen deger",  pos)
    Serial.write(pos.encode()) # pos degerini arduinonun anlayacağı şekilde yeniden kodladık
