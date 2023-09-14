import serial
import math
import threading
from jy901.device import JY901,DumbDevice
from jy901.frames import AngleFrame,AccelFrame
import multiprocessing
import jy901.json
import SelClrCor
a=SelClrCor.ColorsCoordinations(60,'auto')

from gpiozero import Device, AngularServo
from gpiozero.pins.rpigpio import RPiGPIOFactory
from time import sleep
from gpiozero import Motor
import ultraGPIO

sensF = ultraGPIO.ultra(4, 17)
sensL = ultraGPIO.ultra(25, 24)
sensR = ultraGPIO.ultra(22, 27)

ser = serial.Serial('/dev/ttyS0',115200)
jy901_dev = JY901(ser, "")
orig_dev = jy901_dev

sqha=[0,90,180,270,360]
Rsqha=[0,90,180,270,360]

start_F_Distance=140

factory = RPiGPIOFactory()
servo =AngularServo(13, min_angle=0, max_angle=180, min_pulse_width=0.0005, max_pulse_width=0.0025, pin_factory=factory)
motor = Motor(18, 23)

ser.close()

def readAngle():
    global ser
    global jy901_dev
    try:
        ser.open()
        f = jy901_dev.next_angle()
        ser.close()
        return int(f.yaw+180)


    except:
        ser = serial.Serial('/dev/ttyS0',115200)
        jy901_dev = JY901(ser, "")
        print("sErorr")
        pass
    
start_HA= readAngle()    
def nextLangel(ch):
    return (ch+90)%360

def nextRangel(ch):
    nxt=ch-90
    if(nxt>=0):
        return nxt
    else:
        return nxt+360
def calcLsqa(cangel):
    global sqha
    for i in range(len(sqha)):
        if i==0:
            sqha[i]=cangel
        else:
            sqha[i]=nextLangel(sqha[i-1])
def calcRsqa(cangel):
    global sqha
    for i in range(len(sqha)):
        if i==0:
            sqha[i]=cangel
        else:
            sqha[i]=nextRangel(sqha[i-1])         
def go_left():
    servo.angle = 5
    motor.forward(0.8)
def go_right():
    servo.angle = 60
    motor.forward(0.6)
def stop():
    servo.angle = 30

    motor.backward(1)
    sleep(0.01)
    motor.stop()

def forward_L(cur_angel):
    dth=0
    ath=0
    
    while int(sensF.Distance_test())>90 or (int(sensF.Distance_test())>50 and int(sensL.Distance_test()) < 120):
        dr=int(sensR.Distance_test())
        dl=int(sensL.Distance_test())
        print('dl=',dl)
        '''
        if dr>dl:
            dth=-5
            '''
        if dl<10:
            dth=6
        elif dr<15:
            dth=-6
            
        ath=(readAngle()-cur_angel)
        if ath>180:
            ath=-10
        elif ath<-180:
            ath=10
        serv_angle=30+dth+ath
        if(serv_angle>60):
            serv_angle=60
        elif(serv_angle<10):
            serv_angle=10

        servo.angle = serv_angle
        motor.forward(1)
def forward_c(xb,yb,xo,yo):
    dth=0
    ath=0
    cur_angel=start_HA
    while (xb==-1 and yb==-1 and xo==-1 and yo==-1) and (int(sensF.Distance_test())>90 or (int(sensF.Distance_test())>50 and int(sensL.Distance_test()) < 120 and int(sensR.Distance_test()) < 120)):
        dr=int(sensR.Distance_test())
        dl=int(sensL.Distance_test())
        print('dl=',dl)
        '''
        if dr>dl:
            dth=-5
            '''
        if dl<10:
            dth=6
        elif dr<15:
            dth=-6
            
        ath=(readAngle()-cur_angel)
        if ath>180:
            ath=-10
        elif ath<-180:
            ath=10
        serv_angle=30+dth+ath
        if(serv_angle>60):
            serv_angle=60
        elif(serv_angle<10):
            serv_angle=10

        servo.angle = serv_angle
        motor.forward(0.5)
        xb,yb=a.getcoor(0,0,0,10,255,255)
        xo,yo=a.getcoor(105,40,60,120,255,255)
    if(yb<yo):
        return("orange")
    elif(yb>yo):
        return("blue")
    elif(yb!=-1):
        print("tie")
    else:
        print("no color")

def lastforward_L(dist,cur_angel):
    dth=0
    ath=0
    
    while int(sensF.Distance_test())>dist:
        dr=int(sensR.Distance_test())
        dl=int(sensL.Distance_test())
        '''
        if dr>dl:
            dth=-5
            '''
        if dl<10:
            dth=8
            
        ath=(readAngle()-cur_angel)
        if ath>180:
            ath=-10
        elif ath<-180:
            ath=10
        serv_angle=30+dth+ath
        if(serv_angle>60):
            serv_angle=60
        elif(serv_angle<10):
            serv_angle=10

        servo.angle = serv_angle
        motor.forward(1)
def turn90dL(x):
    go_left()
    
    while(abs(readAngle()-x)>5):
        print(readAngle(),',',x)
    stop()
    sleep(0.1)        


def forward(cur_angel):
    dth=0
    ath=0
    dr=int(sensR.Distance_test())
    dl=int(sensL.Distance_test())
    df=int(sensF.Distance_test())
    while int(df>90 or  dr < 200 and df>50):

        '''
        if dr>dl:
            dth=-5
            '''
        if dr<10:
            dth=-8
        elif dl<10:
            dth=8
            
        ath=(readAngle()-cur_angel)
        if ath>180:
            ath=-10
        elif ath<-180:
            ath=10
        serv_angle=30+dth+ath
        if(serv_angle>60):
            serv_angle=60
        elif(serv_angle<10):
            serv_angle=10

        servo.angle = serv_angle
        motor.forward(1)
        dr=int(sensR.Distance_test())
        dl=int(sensL.Distance_test())
        sleep(0.05)
        df=int(sensF.Distance_test())
        print(df ,',',dr)

def lastforward(dist,cur_angel):
    dth=0
    ath=0
    
    while int(sensF.Distance_test())>dist+10:
        dr=int(sensR.Distance_test())
        dl=int(sensL.Distance_test())
        
        if dr<10:
            dth=-8
        elif dl<10:
            dth=8
            
        ath=(readAngle()-cur_angel)
        if ath>180:
            ath=-10
        elif ath<-180:
            ath=10
        serv_angle=30+dth+ath
        if(serv_angle>60):
            serv_angle=60
        elif(serv_angle<10):
            serv_angle=10

        servo.angle = serv_angle
        motor.forward(1)
def turn90dR(x):
    go_right()
    
    while(abs(readAngle()-x)>5):
        print(readAngle(),',',x)
    stop()
    sleep(0.1)        



def startR():
    sleep(1)
    print(start_HA)
    calcRsqa(start_HA)
    start_F_Distance=int(sensF.Distance_test())
    print(sqha)
    a=0
    while (a!=3):
        a=a+1
        sleep(0.1)
        forward(sqha[0])
        turn90dR(sqha[1])
        forward(sqha[1])
        turn90dR(sqha[2])
        forward(sqha[2])
        turn90dR(sqha[3])
        forward(sqha[3])
        turn90dR(sqha[0])
        stop()
    lastforward(140,sqha[0])
        
    stop()
def startL():
    sleep(1)
    print(start_HA)
    calcLsqa(start_HA)
    start_F_Distance=int(sensF.Distance_test())
    print(sqha)
    a=0
    while (a!=3):
        a=a+1
        sleep(0.1)
        forward_L(sqha[0])
        turn90dL(sqha[1])
        forward_L(sqha[1])
        turn90dL(sqha[2])
        forward_L(sqha[2])
        turn90dL(sqha[3])
        forward_L(sqha[3])
        turn90dL(sqha[0])
        stop()
    lastforward_L(140,sqha[0])
        
    stop()

'''
go_left()

while(abs(heading[1]-sqha[1])>5):
    print(heading[1],',',sqha[1])
stop()
sleep(5)

go_left()
while(abs(heading[1]-sqha[2])>5):
    print(heading[1],',',sqha[2])
stop()
sleep(5)

go_left()
while(abs(heading[1]-sqha[3])>5):
    print(heading[1],',',sqha[3])
stop()
sleep(5)
go_left()
while(abs(heading[1]-sqha[4])>5):
    print(heading[1],',',sqha[4])
stop()
sleep(5)

servo.angle = 30
motor.backward(1)
sleep(5)
servo.angle = 60
motor.forward(1)
sleep(5)

'''


