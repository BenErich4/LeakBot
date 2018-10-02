#!/usr/bin/python
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#define actuators GPIOs 
RGB_GREEN = 9 
RGB_RED = 11

# GPIO Setup
GPIO.setup(RGB_GREEN, GPIO.OUT)
GPIO.setup(RGB_RED, GPIO.OUT)

# Initialise low
GPIO.output(RGB_RED, GPIO.LOW)
GPIO.output(RGB_GREEN, GPIO.LOW)

while(1):
		for y in xrange(1, 10000, 1):
			GPIO.output(RGB_GREEN, 1)
			time.sleep(1)
			GPIO.output(RGB_GREEN, 0)
			time.sleep(0.1)
