import serial as s
import time 

serial = s.Serial("/dev/ttyUSB0",9600)
time.sleep(2)

while True:
    print("gönderilen derece: ",pos)
        
        pos = 80
        serial.write(pos.encode())
        serial.write(pos.encode())