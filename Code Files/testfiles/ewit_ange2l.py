from jy901.device import JY901,DumbDevice
from jy901.frames import AngleFrame,AccelFrame
import serial
from time import sleep
import jy901.json

ser = serial.Serial('/dev/ttyS0',115200)
jy901_dev = JY901(ser, "")
orig_dev = jy901_dev
#while True:
ser.close()

def readAngle():
    global ser
    global jy901_dev
    try:
        ser.open()
        f = jy901_dev.next_angle()
        ser.close()
        return int(f.yaw)


    except:
        ser = serial.Serial('/dev/ttyS0',115200)
        jy901_dev = JY901(ser, "")
        print("sErorr")
        pass
    
while True:
        a=input("direction is:")
        print(readAngle())


