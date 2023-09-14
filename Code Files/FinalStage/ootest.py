import R_LLoopControl
import SelClrCor
a=SelClrCor.ColorsCoordinations(60,'auto')
r=0
df=100
x,y,w,h=a.getcoor2(160, 50, 77,179, 255, 255,0, 112, 74,10, 255, 195)
x1,y1,w1,h1=a.getcoor(40, 55, 80,80, 255, 210)
while True:
    if df<20:
        R_LLoopControl.stop()
        break 
    if(x!=-1 and x1!=-1):
        if y+h > y1+h1:
            df=R_LLoopControl.forward_cR(x,0,1008,True)
        else:
            df=R_LLoopControl.forward_cG(x1,0,1008,False)
    elif x!=-1:
        df=R_LLoopControl.forward_cR(x,0,1008,True)
    elif x1!=-1:
        df=R_LLoopControl.forward_cG(x1,0,1008,False)
    elif df>20:
        df=R_LLoopControl.forward_one(self.start_HA)
    else:
        R_LLoopControl.stop()
        break

    
print(x)

