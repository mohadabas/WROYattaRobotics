#include <Servo.h>
int mspeed=100;
int servoval=100;
int dleft=200;
int dright=300;
int dfront=100;
int r1=0;
int r2=0;
int g1=0;
int g2=0;
int b1=0;
int b2=0;
int fval=35;
int rval=80;
int lval=0;

int m1=11;
int m2=12;
Servo myservo;  // create servo object to control a servo
void setup() {
  // put your setup code here, to run once:
    Serial.begin(9600);
    pinMode(m1, OUTPUT);
    pinMode(m2, OUTPUT);
    myservo.attach(2);  // attaches the servo on pin 9 to the servo object
    myservo.write(fval);

    
}
void conn()
{
  
    //String data = Serial.readStringUntil('\n');
    String data="a,"+String(dleft)+","+String(dright)+","+String(dfront)+"\n";
    Serial.print(data);

    String d = Serial.readStringUntil('\n');
    int len = d.length();
    if(len>10)
    {
        dleft=d.substring(len-3,len).toInt();
        if (dleft==0)
         {
          myservo.write(fval);
          analogWrite(m1, 200);
          analogWrite(m2, 0);         
         }
        else if(dleft==1)
          {
          myservo.write(fval);
          analogWrite(m1, 0);
          analogWrite(m2, 200);      
          }
         else if(dleft==2)
          {
          myservo.write(fval);
          analogWrite(m1, 0);
          analogWrite(m2, 255);      
          }
        else if(dleft==3)
          {
          myservo.write(fval);
          analogWrite(m1, 0);
          analogWrite(m2, 120); 
          }
          else if(dleft==4)
          {
          myservo.write(rval);
          delay(100);
          analogWrite(m1, 0);
          analogWrite(m2, 180); 
          }
          else if(dleft==5)
          {
          myservo.write(lval);
          delay(100);
          analogWrite(m1, 180);
          analogWrite(m2, 0); 
          }
          else if(dleft==6)
          {
          myservo.write(lval);
          analogWrite(m1, 0);
          analogWrite(m2, 250); 
          }
          else if(dleft==7)
          {
          myservo.write(rval);
          delay(100);
          analogWrite(m1, 180);
          analogWrite(m2, 0); 
          }
          else if(dleft==8)
          {
          myservo.write(lval);
          delay(100);
          analogWrite(m1, 0);
          analogWrite(m2, 180); 
          }
        else
          {
          analogWrite(m1, 0);
          analogWrite(m2, 0); 
              
          }
    }
    else
    {
        dleft=404;
    }
 
    

    
}


void loop() {
  // put your main code here, to run repeatedly:

  delay(10);
  
  conn();
 
}
