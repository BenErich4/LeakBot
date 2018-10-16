import RPi.GPIO as GPIO
import AutoLeakBot
from time import sleep

WATER_PIN = 23

# This is the main driver function for directing the robot
def main():
	jim = AutoLeakBot()
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(WATER_PIN, GPIO.IN) # need to add pull up/down?
	GPIO.add_event_detect(WATER_PIN, GPIO.RISING) # add 'interrupt' to water pin
	jim.setup()
	while True:
		#search for water
		jim.checkAhead()
		if (jim.isObstructed()):
			jim.changePath()
		# if found water
		if (GPIO.event_detected()):
			break  
		if not jim.isMoving():
			jim.moveforward()
		# Robot may sense water during this sleep time
		# but it would be moving for max 1sec after first sensing water which should be ok
		sleep(1)

	jim.waterDetected()

	while not jim.backAtStart():
		# go back to start


	GPIO.cleanup()


main()