#!/usr/bin/python
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
#define actuators GPIOs
ledRed = 18
ledYlw = 19
ledGrn = 26
#initialize GPIO status variables
ledRedSts = 0
ledYlwSts = 0
ledGrnSts = 0
# Define led pins as output
GPIO.setup(ledRed, GPIO.OUT)   
GPIO.setup(ledYlw, GPIO.OUT) 
GPIO.setup(ledGrn, GPIO.OUT) 
# turn leds OFF 
GPIO.output(ledRed, GPIO.LOW)
GPIO.output(ledYlw, GPIO.LOW)
GPIO.output(ledGrn, GPIO.LOW)

p = GPIO.PWM(

