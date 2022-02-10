from matplotlib.animation import FuncAnimation
import serial as s
import time 
import matplotlib.pyplot as plt
import cv2


ser = s.Serial('/dev/ttyUSB0',9600,timeout=1)
time.sleep(2)

data = []
def plot_pot(data):
    plt.plot(data)
    plt.xlabel('time')
    plt.ylabel('Potentiometer Reading')
    plt.title('Potentiometer Reading vs Time')
    plt.savefig("grafik.png")

while True:
    line = ser.readline()
    if line:
        string = line.decode()
        num = int(string)
        print(num)
        data.append(num)
        plot_pot(data)
        a = cv2.imread("grafik.png")
    cv2.imshow("grafik.png",a)
    if cv2.waitKey(1) == ord('q'):
        break
cv2.destroyAllWindows()
    
