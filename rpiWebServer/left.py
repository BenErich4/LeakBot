#!/usr/bin/python

# 28/9: Pins updated for shield, while loop replacing PWM function.

import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#define actuators GPIOs 
STDBY = 19
AIN1 = 13
AIN2 = 6
PWMA = 5
BIN1 = 26
BIN2 = 20
PWMB = 21

# Define led pins as output
GPIO.setup(STDBY, GPIO.OUT)   
GPIO.setup(AIN1, GPIO.OUT) 
GPIO.setup(AIN2, GPIO.OUT) 
GPIO.setup(BIN1, GPIO.OUT)
GPIO.setup(BIN2, GPIO.OUT)
GPIO.setup(PWMA, GPIO.OUT)
GPIO.setup(PWMB, GPIO.OUT)


# Run PWM
GPIO.output(AIN1, 1)
GPIO.output(AIN2, 0)
GPIO.output(BIN1, 1)
GPIO.output(BIN2, 0)
GPIO.output(STDBY, 1)


#Default 50% Duty Cycle, Tweak for appropriate speed
while(1):
	GPIO.output(PWMA, 1)
	GPIO.output(PWMB, 1)
	#time.sleep(0.005)
	#GPIO.output(PWMA, 0)
	#GPIO.output(PWMB, 0)
	#time.sleep(0.005)
