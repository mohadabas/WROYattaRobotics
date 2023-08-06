from gpiozero import Device, AngularServo
from gpiozero.pins.rpigpio import RPiGPIOFactory
from time import sleep

factory = RPiGPIOFactory()
servo =AngularServo(13, min_angle=0, max_angle=180, min_pulse_width=0.0005, max_pulse_width=0.0025, pin_factory=factory)

while (True):
    servo.angle = 10
    sleep(5)
    servo.angle = 30
    sleep(5)
    servo.angle = 60
    sleep(5)