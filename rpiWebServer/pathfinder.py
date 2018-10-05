#!/usr/bin/python


import RPi.GPIO as GPIO
import AutoLeakBot
from time import sleep
from AutoLeakBot import AutoLeakBot

WATER_PIN = 4


# This is the main driver function for directing the robot
def main():
	jim = AutoLeakBot()
	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)
	GPIO.setup(WATER_PIN, GPIO.IN) 
	GPIO.add_event_detect(WATER_PIN, GPIO.RISING) # add 'interrupt' to water pin
	jim.setup()
	while True:
		#search for water
		jim.checkAhead()
		if (jim.isObstructed()):
			jim.changePath()
		# if found water
		#if (GPIO.event_detected()):
			#break
		if not jim.isMoving:
			jim.moveforward()
		# Robot may sense water during this sleep time
		# but it would be moving for max 1sec after first sensing water which should be ok
		sleep(1)

	jim.waterDetected()

	#while not jim.backAtStart():
		# go back to start

	#GPIO.cleanup()


main()
