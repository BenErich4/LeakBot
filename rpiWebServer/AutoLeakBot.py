#!/usr/bin/python

# This code is maintained by Benjamin Eric and Lachlan Clark
# This module interfaces an HC-SR04 (ultrasonic sensor) with a Raspberry Pi.
# @note: Add series external resistor to the ECHO pin as a safety precaution

import RPi.GPIO as GPIO
import subprocess, os, signal, time
import gpsReader as GPS
import math
from time import sleep

# Constants
MIN_COLLISION_DISTANCE = 25 # Furthest distance (cm) the robot can be to an object before stopping
LEFT = 5 # Ultrasonic Servo Motor Position LEFT
CENTRE = 90 # Ultrasonic Servo Motor Position CENTRE
RIGHT = 175 # Ultrasonic Servo Motor Position RIGHT
DELAY = 1 # Delay between sensor readings (in seconds?)
TRIGGER_PIN = 3 # pin numberings can change
ECHO_PIN = 2
SERVO_PIN = 18
LIGHT_PIN = 10
WATER_PIN = 4
PWMA = 5
PWMB = 21

WATER_FOUND = 0
CURRENT_LAT = 1
CURRENT_LONG = 2
WATER_LAT = 3
WATER_LONG = 4

def check_kill_process(pstring):
		for line in os.popen("ps ax | grep " + pstring + " | grep -v grep"):
			fields = line.split()
			pid = fields[0]
			os.kill(int(pid), signal.SIGKILL)

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
		self.backAtStart = False # has it returned after finding water?
		self.isMoving = False
		
	#def isMoving(self):
		#return (self.isMoving)
	

	def setup(self):
		GPIO.setmode(GPIO.BCM)
		GPIO.setwarnings(False) #optional
		GPIO.setup(PWMA, GPIO.OUT)
		GPIO.setup(PWMB, GPIO.OUT)
		GPIO.output(PWMA, 0)
		GPIO.output(PWMB, 0)
		GPIO.setup(SERVO_PIN, GPIO.OUT) #Sets the servo control pin as output
		GPIO.setup(ECHO_PIN, GPIO.IN)  # Sets the echo as an Input
		GPIO.setup(TRIGGER_PIN, GPIO.OUT) # Sets the trig as an Output
		GPIO.setup(LIGHT_PIN, GPIO.OUT)
		#GPIO.setup(WATER_PIN, GPIO.IN) # need to add pull up/down?
		#GPIO.add_event_detect(WATER_PIN, GPIO.RISING, callback = waterDetected) # add interrupt to water pin, waterDetected set as ISR
		GPIO.output(TRIGGER_PIN, 0)
		#self.readGPS('LatLong', 'intial')
		#print "gps read"
		self.setSensorAngle(CENTRE)	# make sensor point forward


	# readingType specifies latLong or bearing reading, callType specifies if taking current reading or reading for water or intial position coordinates	
	def readGPS(self, readingType, callType):
		# read gps until it gets valid data
		#while True:
		gpsData = GPS.read()
			#if gpsData['fix']:
			#	break
		
		# we will update the bearing independent of the coordinates on the assumption that the gps will read the 
		# coordinates more accurately while stationary, and the bearing more accurateley while moving
		if (readingType == 'LatLong'):
			if (callType == 'current'):
				self.currentLat = gpsData['latitude']
				self.currentLat = gpsData['longitude']
				#telemetry.dataList['currentLat'] = gpsData['latitude']
				#telemetry.dataList['currentLong'] = gpsData['longitude']
			elif (callType == 'intial'):
				self.startLat = gpsData['latitude']
				self.startLong = gpsData['longitude']
				#telemetry.dataList['startLat'] = gpsData['latitude']
				#telemetry.dataList['startLong'] = gpsData['longitude']
			elif (callType == 'water'):
				self.waterLat = gpsData['latitude']
				self.waterLong = gpsData['longitude']
				#telemetry.dataList['waterLat'] = gpsData['latitude']
				#telemetry.dataList['waterLong'] = gpsData['longitude']
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


	#def turnByAngle(self, bearing):
		# takes a number in degrees between -179 to 180 that the robot needs to turn
		# (the reference zero degrees point is the way it's now pointing, positive degrees = clockwise)
		# need to test motors to see the relationship between motor speed/time and degrees rotated
		# might be tricky to implement seeing as though motor power may be very dependent on its battery status


	def waterDetected(self):
		self.stopMovement()
		filee = open("telemetry.txt", "w")
		filee.write("True")
		filee.close()
		#self.readGPS('LatLong', 'water')
		# take photo
		
		
	

	def changePath(self):
		self.stopMovement()
		self.scanSurroundings()

		# Scenario TURN-LEFT
		if (self.leftSensorDist > self.rightSensorDist):
			left = subprocess.Popen("/home/pi/Documents/rpiWebServer/left.py", shell=True)
			time.sleep(0.5)
			check_kill_process("left.py")
			print('Drive Left')

		# Scenario TURN-RIGHT
		elif (self.rightSensorDist > self.leftSensorDist):
			right = subprocess.Popen("/home/pi/Documents/rpiWebServer/right.py", shell=True)
			time.sleep(0.5)
			#heck_kill_process("right.py")
			print('Drive right')
			
		# Scenario REVERSE
		elif (self.rightSensorDist == self.leftSensorDist):
			backwards = subprocess.Popen("/home/pi/Documents/rpiWebServer/backwards.py", shell=True)
			time.sleep(0.5)
			check_kill_process("backwards.py")
			print('Drive reverse')


	# Scan to the LEFT, RIGHT and CENTRE of the robot to take measurements of its surroundings
	def scanSurroundings(self):
		# Turn the ultrasonic servo motor to LEFT RIGHT and CENTRE positions
		# Take a reading at each of these points and then return this data to the caller
		self.takeMeasurement(LEFT)
		time.sleep(DELAY)
		self.takeMeasurement(RIGHT)
		time.sleep(DELAY)
		self.setSensorAngle(CENTRE) # Re-centre the servo motor to face in front of the robot chassis to detect future head-on collisions
		#self.servoPWM.stop();


	def checkAhead(self):
		self.stopMovement()
		self.takeMeasurement(CENTRE)
		sleep(1)


	def isObstructed(self):
		return (self.centreSensorDist < MIN_COLLISION_DISTANCE)

	# Set the angle of the ultra sonic sensor's servo motor
	def setSensorAngle(self, angle):
		#duty = (angle / 18.6) + 2.5
		#GPIO.output(SERVO_PIN, True)
		if angle == CENTRE:
			cent = subprocess.Popen("/home/pi/Documents/rpiWebServer/ServoCentre.py", shell=True)
			time.sleep(0.5)
			print "centre"

		elif angle == LEFT:
			left = subprocess.Popen("/home/pi/Documents/rpiWebServer/ServoLeft.py", shell=True)
			time.sleep(0.5)
			print "left"

		elif angle == RIGHT:
			right = subprocess.Popen("/home/pi/Documents/rpiWebServer/ServoRight.py", shell=True)
			time.sleep(0.5)
			print "right"


		print angle

	def takeMeasurement(self, position):
		self.setSensorAngle(position) # Rotate Servo to position to take distance measurement
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

		measuredDist = round(((stop - start) * 17000), 3)
		
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
	

	# for motor control
	def moveforward(self):
		self.isMoving = True
		forward = subprocess.Popen("/home/pi/Documents/rpiWebServer/forwards.py", shell=True)
		print('Drive FORWARD')

		# should be a pwm.start() call that means it just keeps going


	def turnRight(self):
		print('RIGHT')	


	def turnLeft(self):
		print('LEFT')


	def reverse(self):
		print('REVERSE')


	def stopMovement(self):
		print "STOPPED"
		check_kill_process("forwards.py")
		GPIO.output(PWMA, 0)
		GPIO.output(PWMB, 0)
		self.isMoving = False
		# lots of pwm.stop() calls
		
	def writeToTelemetryFile(data, line_num):
		to_write = str(data)+'\n'
		
		with open('stats.txt', 'r') as txt:
		# read a list of lines into data
			data = txt.readlines()

		# now change the 2nd line, note that you have to add a newline
		data[line_num] = to_write

		# and write everything back
		with open('stats.txt', 'w') as file:
			file.writelines( data )
		
		
		
