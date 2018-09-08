# This code is maintained by Benjamin Eric and Lachlan Clark
# This module interfaces an HC-SR04 (ultrasonic sensor) with a Raspberry Pi.
# @note: Add series external resistor to the ECHO pin as a safety precaution

import RPi.GPIO as GPIO
import time

# Constants
MIN_COLLISION_PREVENTION_DISTANCE = 20
LEFT = 5 # Ultrasonic Servo Motor Position LEFT
CENTRE = 90 # Ultrasonic Servo Motor Position CENTRE
RIGHT = 175 # Ultrasonic Servo Motor Position RIGHT
DELAY = 0.1

class SensorServo(object):

	def __init__(self, angle, trigPin, echoPin, controlPin):
		self._trigPin = trigPin
		self._echoPin = echoPin
		self._controlPin = controlPin
		self._leftDist = 0
		self._centreDist = 0
		self._rightDist = 0
		self._decision = "FORWARD"
		self._pwm = 0

	def setup(self):
		GPIO.setwarnings(False)
		GPIO.cleanup()
		GPIO.setup(self._controlPin, GPIO.OUT)
		GPIO.setup(self._echoPin, GPIO.IN)  # Sets the echo as an Input
		GPIO.setup(self._trigPin, GPIO.OUT) # Sets the trig as an Output
		GPIO.output(self._trigPin, 0)       # Set the trig pin LOW
		self._pwm = GPIO.PWM(self._controlPin, 50); # adds PWM functionality to GPIO pin (50 Hz)
		self._pwm.start(0)
		#self.SetAngle(CENTRE)

	# Set the angle of the ultra sonic sensor's servo motor
	def SetAngle(self, angle):
		duty = (angle / 18.6) + 2.5
		GPIO.output(self._controlPin, True)
		self._pwm.ChangeDutyCycle(duty)
		time.sleep(0.5)
		GPIO.output(self._controlPin, False)
		self._pwm.ChangeDutyCycle(0)
		print angle
		
	def LookForward(self):
		self.SetAngle(CENTRE)

	def MakeDecision(self):
		self.scanSurroundings()

		# Scenario TURN-LEFT
		if (self._leftDist > self._rightDist):
			self._direction = "LEFT"

		# Scenario TURN-RIGHT
		elif (self._rightDist > self._leftDist):
			self._direction = "RIGHT"
			
		# Scenario REVERSE
		elif (self._rightDist < ):
			_direction = "REVERSE"


	# Scan to the LEFT, RIGHT and CENTRE of the robot to take measurements of its surroundings
	def scanSurroundings(self):
		# Turn the ultrasonic servo motor to LEFT RIGHT and CENTRE positions
		# Take a reading at each of these points and then return this data to the caller
		self.takeMeasurement(LEFT);
		time.sleep(DELAY)
		self.takeMeasurement(CENTRE);
		time.sleep(DELAY)
		self.takeMeasurement(RIGHT);
		time.sleep(DELAY)

	def takeMeasurement(self, position):
		self.SetAngle(position); # Rotate Servo to position to take distance measurement
		#distance = fireSensor();
		self.fireSensor(position)

	def fireSensor(self, position):
		# Release a _trigPinGER pulse from the ultrasonic sensor
		GPIO.output(self._trigPin, 1)
		time.sleep(0.00001)
		GPIO.output(self._trigPin, 0)

		# Time the return of the _trigPinGER pulse signal back to the ultrasonic sensor
		while GPIO.input(self._echoPin) == 0:
			pass
		start = time.time()
		while GPIO.input(self._echoPin) == 1:
			pass
		stop = time.time()

		measuredDistanceTemp = round(((stop - start) * 17000), 3);
		
		if (position == LEFT):
			self._leftDist = measuredDistanceTemp
		elif (position == CENTRE):
			self._centreDist = measuredDistanceTemp
		elif (position == RIGHT):
			self._rightDist = measuredDistanceTemp
			self.SetAngle(CENTRE); # Re-centre the servo motor to face in front of the robot chassis to detect future head-on collisions
			self._pwm.stop();
			
		
		# @note: DEBUG ONLY
		# Display measurement and corresponding time
		#print("Distance:  " + str(measuredDistanceTemp) + " cm")
		# print("Time:      " + str(round((stop - start)*1000, 3)) + " ms")
		
