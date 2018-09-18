#!/usr/bin/python
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#define actuators GPIOs
STDBY = 6
AIN1 = 21
AIN2 = 13
PWMA = 18
BIN1 = 20
BIN2 = 16
PWMB = 19

# Define led pins as output
GPIO.setup(STDBY, GPIO.OUT)   
GPIO.setup(AIN1, GPIO.OUT) 
GPIO.setup(AIN2, GPIO.OUT) 
GPIO.setup(BIN1, GPIO.OUT)
GPIO.setup(BIN2, GPIO.OUT)
GPIO.setup(PWMA, GPIO.OUT)
GPIO.setup(PWMB, GPIO.OUT)


# Run PWM
GPIO.output(AIN1, 0)
GPIO.output(AIN2, 1)
GPIO.output(BIN1, 0)
GPIO.output(BIN2, 1)
GPIO.output(STDBY, 1)

LEFT_MOTOR = GPIO.PWM(PWMA, 50)

LEFT_MOTOR.start(70)
time.sleep(100)
LEFT_MOTOR.stop()
GPIO.cleanup()
