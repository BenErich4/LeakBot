import RPi.GPIO as GPIO
import UltrasonicSensor

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
	sensorServo = UltrasonicSensor.SensorServo(90, 7, 11, 13)
	sensorServo.setup()
	sensorServo.fireSensor()
	print sensorServo._measuredDist
	
	print("yeah buddy")
	GPIO.cleanup();
main();
