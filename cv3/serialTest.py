import serial
import time

ser = serial.Serial(
    port='/dev/ttyACM0',
    baudrate=9600,
    parity=serial.PARITY_ODD,
    stopbits=serial.STOPBITS_TWO,
    bytesize=serial.SEVENBITS
)
ser.isOpen()
d = []
while True:
    for i in range(0,9):
        print(bytes([i]))
        ser.write(bytes([i]))
        time.sleep(.5) #0.5 s delay
        out = ''
        while ser.inWaiting() > 0:
            print(ser.read(1))
            #out += string(ser.read(1))
        if out != '':
            print(">>" + out)
        if(i==8):
            i=0
        else:
            i+=1
        

