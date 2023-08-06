from gpiozero import Motor
import time

motor = Motor(18, 23)
motor.backward(1)
time.sleep(10)
motor.stop()