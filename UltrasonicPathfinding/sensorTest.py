# /user/bin/python ????????

import AutoLeakBot
from time import sleep

CENTRE = 90
LEFT = 5
RIGHT = 175

def main():
	test = AutoLeakBot()
	while True:
		test.setSensorAngle(CENTRE)
		sleep(2)
		test.setSensorAngle(LEFT)
		sleep(2)
		test.setSensorAngle(RIGHT)
		sleep(2)
		