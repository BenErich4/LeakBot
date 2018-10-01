import RPi.GPIO as GPIO
import AutoLeakBot
from time import sleep

# have to delcare this as global since cannot pass objects to ISR when water is detected
jim = AutoLeakBot()

# This is the main driver function for directing the robot
def main():
	GPIO.setmode(GPIO.BOARD);
	GPIO.setup(WATER_PIN, GPIO.IN) # need to add pull up/down?
	GPIO.add_event_detect(WATER_PIN, GPIO.RISING) # add interrupt to water pin
	jim.setup()
	while !(jim.waterFound):
		#search for water
		jim.checkAhead()
		if (jim.isObstructed()):
			jim.makeDecision()
		jim.moveforward()
		sleep(500)

	# could set ISR directly here for water detection?
	# does the robot actually have to stop right at the instant it detects water? Probably not
	# just needs to get GPS location of water & take photo - can be done in threaded callback interrupt
	while !(jim.backAtStart):
		# go back to start


	print("yeah buddy")
	GPIO.cleanup();


main();
