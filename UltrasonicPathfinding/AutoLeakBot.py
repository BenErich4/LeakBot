# This code is maintained by Benjamin Eric and Lachlan Clark
# This module interfaces an HC-SR04 (ultrasonic sensor) with a Raspberry Pi.
# @note: Add series external resistor to the ECHO pin as a safety precaution

import RPi.GPIO as GPIO
import time
import gpsReader as GPS
import math

# Constants
MIN_COLLISION_DISTANCE = 20 # Furthest distance (cm) the robot can be to an object before stopping
LEFT = 5 # Ultrasonic Servo Motor Position LEFT
CENTRE = 90 # Ultrasonic Servo Motor Position CENTRE
RIGHT = 175 # Ultrasonic Servo Motor Position RIGHT
DELAY = 0.1 # Delay between sensor readings (in seconds?)
TRIGGER_PIN = 7 # pin numberings can change
ECHO_PIN = 11
SERVO_PIN = 13
LEFT_MOTOR_PIN = 17 # more than 2 pins to control motors?
RIGHT_MOTOR_PIN = 18
LIGHT_PIN = 19
R_PIN = 20
G_PIN = 21
B_PIN = 22


class AutoLeakBot(object):

	def __init__(self):
		# just placeholders to be changed later 
		self.currentLat = 0
		self.currentLong = 0
		self.bearing = 0
		self.startLat = 0
		self.startLong = 0
		self.waterLat = 0
		self.waterLong = 0
		self.leftSensorDist = 0
		self.centreSensorDist = 0
		self.rightSensorDist = 0
		self.servoPWM = 0
		self.waterFound = False # has it found water?
		self.isMoving = False
	

	def setup(self):
		GPIO.setwarnings(False) #optional
		GPIO.cleanup()			#optional
		GPIO.setmode(BCM)
		GPIO.setup(SERVO_PIN, GPIO.OUT) #Sets the servo control pin as output
		GPIO.setup(ECHO_PIN, GPIO.IN)  # Sets the echo as an Input
		GPIO.setup(TRIGGER_PIN, GPIO.OUT) # Sets the trig as an Output
		GPIO.setup(LEFT_MOTOR_PIN, GPIO.OUT) # etc
		GPIO.setup(RIGHT_MOTOR_PIN, GPIO.OUT)
		GPIO.setup(LIGHT_PIN, GPIO.OUT)
		GPIO.setup(R_PIN, GPIO.OUT)
		GPIO.setup(G_PIN, GPIO.OUT)
		GPIO.setup(B_PIN, GPIO.OUT)
		#GPIO.setup(WATER_PIN, GPIO.IN) # need to add pull up/down?
		#GPIO.add_event_detect(WATER_PIN, GPIO.RISING, callback = waterDetected) # add interrupt to water pin, waterDetected set as ISR
		GPIO.output(TRIGGER_PIN, 0)
		self.readGPS('LatLong', 'intial')
		self.servoPWM = GPIO.PWM(SERVO_PIN, 50); # adds PWM functionality to servo control pin (50 Hz)
		self.setSensorAngle(CENTRE)	# make sensor point forward


	# readingType specifies latLong or bearing reading, callType specifies if taking current reading or reading for water or intial position coordinates	
	def readGPS(self, readingType, callType):
		# read gps until it gets valid data
		while True:
			gpsData = GPS.read()
			if gpsData['fix']:
				break
		
		# we will update the bearing independent of the coordinates on the assumption that the gps will read the 
		# coordinates more accurately while stationary, and the bearing more accurateley while moving
		if (readingType == 'LatLong'):
			if (callType == 'current'):
				self.currentLat = gpsData['latitude']
				self.currentLat = gpsData['longitude']
			elif (callType == 'intial'):
				self.startLat = gpsData['latitude']
				self.startLong = gpsData['longitude']
			elif (callType == 'water'):
				self.waterLat = gpsData['latitude']
				self.waterLong = gpsData['longitude']
		elif (readingType == 'bearing'):
			self.bearing == gpsData['bearing']
	

	def turnTowardsStart(self):
		# calculate the turn in degrees that the bot should make so it's facing its starting point
		# need to know its current bearing from last gps reading, its current gps coords and the 
		# starting gps coords

		startBearing = self.getBearingToStart()
		turnAngle = startBearing - self.currentBearing
		
		# if turning more than 180 anticlockwise, get equivalent clockwise turn
		if (turnAngle < -180):
			turnAngle = 360 - turnAngle

		self.turnByAngle(turnAngle)


	def getBearingToStart(self):
		# returns the compass bearing from current position to starting position

		self.readGPS('LatLong', 'current')
		
		if (self.startLat > self.currentLat):
			# bearing in first quadrant
			if (self.startLong > self.currentLong):
				theta = atan((self.startLat - self.currentLat) / (self.startLong - self.currentLong))
			# bearing in second quadrant
			elif (self.startLong < self.currentLong):
				theta = 180 - atan((self.startLat - self.currentLat) / (self.currentLong - self.startLong))
			# case that start is directly east of current position
			else:
				theta = 90
		elif (self.startLat < self.currentLat):
			# bearing in third quadrant
			if (self.startLong < self.currentLong):
				theta = 180 + atan((self.currentLat - self.startLat) / (self.currentLong - self.startLong))
			# bearing in forth quadrand
			elif (self.startLong > self.currentLong):
				theta = 360 - atan((self.currentLat - self.startLat) / (self.startLong - self.currentLong))
			# case that start is directly west of current position
			else:
				theta = 270
		# elif (self.startLat == self.currentLat)
		else:
			# case that start is directly north of current position
			if (self.startLong > self.currentLong):
				theta = 0
			# elif (self.startLong < self.currentLong)
			# case that start is directly south of current position
			else:
				theta = 180

		return theta


	def turnByAngle(self, bearing):
		# takes a number in degrees between -179 to 180 that the robot needs to turn
		# (the reference zero degrees point is the way it's now pointing, positive degrees = clockwise)
		# need to test motors to see the relationship between motor speed/time and degrees rotated
		# might be tricky to implement seeing as though motor power may be very dependent on its battery status


	# Set the angle of the ultra sonic sensor's servo motor
	def setSensorAngle(self, angle):
		duty = (angle / 18.6) + 2.5
		#GPIO.output(SERVO_PIN, True)
		self.servoPWM.start(duty)
		time.sleep(0.5)
		#GPIO.output(SERVO_PIN, False)
		self.servoPWM.stop()
		print angle

	def waterDetected(self):
		self.stopMovement()
		self.readGPS('LatLong', 'water')
		# take photo
		self.waterFound = True
		

	def changePath(self):
		self.stopMovement()
		self.scanSurroundings()

		# Scenario TURN-LEFT
		if (self.leftSensorDist > self.rightSensorDist):
			self.turnLeft()

		# Scenario TURN-RIGHT
		elif (self.rightSensorDist > self.leftSensorDist):
			self.turnRight()
			
		# Scenario REVERSE
		elif (self.rightSensorDist == self.leftSensorDist):
			self.reverse()


	# Scan to the LEFT, RIGHT and CENTRE of the robot to take measurements of its surroundings
	def scanSurroundings(self):
		# Turn the ultrasonic servo motor to LEFT RIGHT and CENTRE positions
		# Take a reading at each of these points and then return this data to the caller
		self.takeMeasurement(LEFT);
		time.sleep(DELAY)
		self.takeMeasurement(RIGHT);
		time.sleep(DELAY)
		self.setSensorAngle(CENTRE); # Re-centre the servo motor to face in front of the robot chassis to detect future head-on collisions
		# self.servoPWM.stop();


	def checkAhead(self):
		self.takeMeasurement(CENTRE)


	def isObstructed(self):
		return (self.centreSensorDist < MIN_COLLISION_DISTANCE)


	def takeMeasurement(self, position):
		self.setSensorAngle(position); # Rotate Servo to position to take distance measurement
		#distance = fireSensor();
		self.fireSensor(position)


	def fireSensor(self, position):
		# Release a TRIGGER_PINGER pulse from the ultrasonic sensor
		GPIO.output(TRIGGER_PIN, 1)
		time.sleep(0.00001)
		GPIO.output(TRIGGER_PIN, 0)

		# Time the return of the TRIGGER_PINGER pulse signal back to the ultrasonic sensor
		while GPIO.input(ECHO_PIN) == 0:
			pass
		start = time.time()
		while GPIO.input(ECHO_PIN) == 1:
			pass
		stop = time.time()

		measuredDist = round(((stop - start) * 17000), 3);
		
		if (position == LEFT):
			self.leftSensorDist = measuredDist
		elif (position == CENTRE):
			self.centreSensorDist = measuredDist
		elif (position == RIGHT):
			self.rightSensorDist = measuredDist	
		
		# @note: DEBUG ONLY
		# Display measurement and corresponding time
		#print("Distance:  " + str(measuredDistanceTemp) + " cm")
		# print("Time:      " + str(round((stop - start)*1000, 3)) + " ms")
	

	def isBackAtStart(self):
		# check if within 1.5 meters of start point using haversine formula

	# for motor control
	def moveforward(self):
		# moves forward indefinitley
		self.isMoving = True
		print('FORWARD')

		# should be a pwm.start() call that means it just keeps going


	def turnRight(self):
		print('RIGHT')	


	def turnLeft(self):
		print('LEFT')


	def reverse(self):
		print('REVERSE')


	def stopMovement(self)
		self.isMoving = False
		# lots of pwm.stop() calls
		