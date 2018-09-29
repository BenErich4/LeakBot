# This code is maintained by Benjamin Eric and Lachlan Clark
# This module interfaces an HC-SR04 (ultrasonic sensor) with a Raspberry Pi.
# @note: Add series external resistor to the ECHO pin as a safety precaution

import RPi.GPIO as GPIO
import time
import gpsReader.py as GPS

# Constants
MIN_COLLISION_PREVENTION_DISTANCE = 20
LEFT = 5 # Ultrasonic Servo Motor Position LEFT
CENTRE = 90 # Ultrasonic Servo Motor Position CENTRE
RIGHT = 175 # Ultrasonic Servo Motor Position RIGHT
DELAY = 0.1

class LeakBot(object)

	def __init__(self, leftTrackControlPin, rightTrackControlPin, lightPin, rPin, gPin, bPin, waterPin)
		self.leftTrackControlPin = leftControlPin
		self.rightTrackControlPin = rightTrackControlPin
		self.lightPin = lightPin
		self.rPin = rPin
		self.gPin = gPin
		self.bPin = bPin
		# rest are just placeholders to be changed later 
		self.currentLat = 0
		self.currentLong = 0
		self.currentBearing = 0
		self.startLat = 0
		self.startLong = 0
		self.waterLat = 0
		self.waterLong = 0
		self.sensorServo = 0
		
		
	def readGPS(self, readingType)
		# read gps until it gets valid data
		while True:
			gpsData = GPS.read()
			if gpsData['fix']:
				break
		
		# we will update the bearing independent of the coordinates on the assumption that the gps will read the 
		# coordinates more accurately while stationary, and the bearing more accurateley while moving
		if (readingType == 'LatLong')
			self.latitude = gpsData['latitude']
			self.longitude = gpsData['longitude']
		elif (readingType == 'bearing')
			self.bearing == gpsData['bearing']
			
	def turnByXYZDegrees(self, bearing)
		# takes a number in degrees between -179 to 180 that the robot needs to turn
		# (the reference zero degrees point is the way it's now pointing, positive degrees = clockwise)
		# need to test motors to see the relationship between motor speed/time and degrees rotated
		# might be tricky to implement seeing as though motor power may be very dependent on its battery status
			
	def turnToward  

class SensorServo(object):

	def __init__(self, angle, trigPin, echoPin, controlPin):
		self.trigPin = trigPin
		self.echoPin = echoPin
		self.controlPin = controlPin
		self.leftDist = 0
		self.centreDist = 0
		self.rightDist = 0
		self.decision = "FORWARD"
		self.pwm = 0

	# Set the angle of the ultra sonic sensor's servo motor
	def SetAngle(self, angle):
		duty = (angle / 18.6) + 2.5
		GPIO.output(self.controlPin, True)
		self.pwm.ChangeDutyCycle(duty)
		time.sleep(0.5)
		GPIO.output(self.controlPin, False)
		self.pwm.ChangeDutyCycle(0)
		print angle
	
	def setup(self):
		GPIO.setwarnings(False)
		GPIO.cleanup()
		GPIO.setup(self.controlPin, GPIO.OUT)
		GPIO.setup(self.echoPin, GPIO.IN)  # Sets the echo as an Input
		GPIO.setup(self.trigPin, GPIO.OUT) # Sets the trig as an Output
		GPIO.output(self.trigPin, 0)       # Set the trig pin LOW
		self.pwm = GPIO.PWM(self.controlPin, 50); # adds PWM functionality to GPIO pin (50 Hz)
		self.pwm.start(0)
		self.SetAngle(CENTRE)

	def MakeDecision(self):
		self.scanSurroundings()

		# Scenario TURN-LEFT
		if (self.leftDist > self.rightDist):
			self.direction = "LEFT"

		# Scenario TURN-RIGHT
		elif (self.rightDist > self.leftDist):
			self.direction = "RIGHT"
			
		# Scenario REVERSE
		elif (self.rightDist < ):
			self.direction = "REVERSE"


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
		# Release a trigPinGER pulse from the ultrasonic sensor
		GPIO.output(self.trigPin, 1)
		time.sleep(0.00001)
		GPIO.output(self.trigPin, 0)

		# Time the return of the trigPinGER pulse signal back to the ultrasonic sensor
		while GPIO.input(self.echoPin) == 0:
			pass
		start = time.time()
		while GPIO.input(self.echoPin) == 1:
			pass
		stop = time.time()

		measuredDistanceTemp = round(((stop - start) * 17000), 3);
		
		if (position == LEFT):
			self.leftDist = measuredDistanceTemp
		elif (position == CENTRE):
			self.centreDist = measuredDistanceTemp
		elif (position == RIGHT):
			self.rightDist = measuredDistanceTemp
			self.SetAngle(CENTRE); # Re-centre the servo motor to face in front of the robot chassis to detect future head-on collisions
			self.pwm.stop();
			
		
		# @note: DEBUG ONLY
		# Display measurement and corresponding time
		#print("Distance:  " + str(measuredDistanceTemp) + " cm")
		# print("Time:      " + str(round((stop - start)*1000, 3)) + " ms")
		
