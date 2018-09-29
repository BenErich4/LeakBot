import RPi.GPIO as GPIO
import AutoLeakBot
from time import sleep

# This is the main driver function for directing the robot
def main():
	GPIO.setmode(GPIO.BOARD);
	jim = AutoLeakBot()
	jim.setup()
	while !(jim.waterFound):
		#search for water

	while !(jim.done):
		#go back to start

	print("yeah buddy")
	GPIO.cleanup();
main();
