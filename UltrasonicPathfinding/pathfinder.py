import RPi.GPIO as GPIO
import UltrasonicSensor
from time import sleep

#Constants
MIN_COLLISION_PREVENTION_DISTANCE = 20
LEFT = 0 # Ultrasonic Servo Motor Position LEFT
CENTRE = 90 # Ultrasonic Servo Motor Position CENTRE
RIGHT = 180 # Ultrasonic Servo Motor Position RIGHT

TRIGGER_PIN =7
ECHO_PIN = 11
CONTROL_PIN = 13
# Global Constants

MAX_COLLISION_PREVENTION_DISTANCE = 20; # Furthest distance (cm) the robot can be to an object before stopping
MOTOR_ONE_CONTROL_PIN = 7;  # Defines which GPIO connects to the control signal of MOTOR 1
MOTOR_TWO_CONTROL_PIN = 11; # Defines which GPIO connects to the control signal of MOTR 2
DELAY  = 0.01 # Delay time (seconds) between ultrasonic sensor readings
LEFT_ARRAY_ELEMENT   = 0; # Data in the array that represents the reading from the LEFT   side of the chassis
RIGHT_ARRAY_ELEMENT  = 1; # Data in the array that represents the reading from the RIGHT  side of the chassis
CENTRE_ARRAY_ELEMENT = 2; # Data in the array that represents the reading from the CENTRE side of the chassis

# This is the main procedure in this program that continuously directs the robot
def main():
	GPIO.setmode(GPIO.BOARD);
	sensorServo = UltrasonicSensor.SensorServo(CENTRE, TRIGGER_PIN, ECHO_PIN, CONTROL_PIN)
	sensorServo.setup()
	sensorServo.scanSurroundings()
		
	print sensorServo.leftDist
	print sensorServo.centreDist
	print sensorServo.rightDist
	sleep(3)
	
	print("yeah buddy")
	GPIO.cleanup();
main();
