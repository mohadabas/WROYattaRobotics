import R_LLoopControl
import SelClrCor
a=SelClrCor.ColorsCoordinations(60,'auto')
r=0
while r!=5:
    r=r+1
    print(a.getcoor(0,56,122,10,255,255))
    print(a.getcoor(114,86,122,120,255,255))
    xb,yb=a.getcoor(0,56,122,10,255,255)
    xo,yo=a.getcoor(114,86,122,120,255,255)
c=R_LLoopControl.forward_c(xb,yb,xo,yo)
R_LLoopControl.stop()
if c=='blue':
    R_LLoopControl.startL()
elif c=='orange':
    R_LLoopControl.startR()
