import RPi.GPIO as GPIO
import AutoLeakBot
from time import sleep

# have to delcare this as global since cannot pass objects to ISR when water is detected
jim = AutoLeakBot()

# This is the main driver function for directing the robot
def main():
	GPIO.setmode(GPIO.BOARD);
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
		if !(jim.isMoving)
			jim.moveforward()
		# Robot may sense water during this sleep time
		# but it would be moving for max 1sec after first sensing water which should be ok
		sleep(1)

	jim.waterDetected()

	while !(jim.backAtStart):
		# go back to start


	print("yeah buddy")
	GPIO.cleanup();


main();
