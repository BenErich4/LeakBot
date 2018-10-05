#!/usr/bin/python
import RPi.GPIO as GPIO
import subprocess, os, signal, time
import gpsReader as GPS
import math
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#define actuators GPIOs 
SERVO_PIN = 18

def main():
	GPIO.setup(SERVO_PIN, GPIO.OUT)
	print "cent"
	servoPWM = GPIO.PWM(SERVO_PIN, 50)
	servoPWM.start(7.5)
	time.sleep(0.5)
	servoPWM.stop()
	
main()
