
# This code is maintained by Benjamin Erich

# This module interfaces an HC-SR04 (ultrasonic sensor) with a Raspberry Pi.
# @note: Add series external resistor to the ECHO pin as a safety precaution

import RPi.GPIO as GPIO
import time

# GPIO pins used for the ultra sonic sensor's TRIGGER and ECHO pins 
TRIG = 7
ECHO = 11
LEFT   = 175 # Ultrasonic Servo Motor Position LEFT
CENTRE = 90  # Ultrasonic Servo Motor Position CENTRE
RIGHT  = 5   # Ultrasonic Servo Motor Position RIGHT

# Defined Constants
pinNumber = 2                   # Assigned GPIO pin to ultrasonic sensor's servo motor
#GPIO.setwarnings(False)        # Disable console messages

class SensorServo(object):

    MIN_COLLISION_PREVENTION_DISTANCE = 20

    def __init__(self, angle, trigPin, echoPin, controlPin):
        self._angle = angle
        self._trigPin = trigPin
        self._echoPin = echoPin
        self._controlPin = controlPin
        self._leftDist = 0
        self._centreDist = 0
        self._rightDist = 0
        self._decision = "FORWARD"
        self._pwm = GPIO.PWM(controlPin, 50); # adds PWM functionality to GPIO pin (50 Hz)

    def setup():
        GPIO.setmode(BOARD)
        GPIO.setup(_controlPin, GPIO.OUT) # Set assigned GPIO pin as output
        GPIO.setup(_echoPin, GPIO.IN)  # Sets the echo as an Input
        GPIO.setup(_trigPin, GPIO.OUT) # Sets the trig as an Output
        GPIO.output(_trigPin, 0)       # Set the trig pin LOW
        self.SetAngle(90)

    # Set the angle of the ultra sonic sensor's servo motor
    def SetAngle(angle):
      duty = (angle / 18) + 2
      GPIO.output(_controlPin, True)
      pwm.ChangeDutyCycle(duty)
      sleep(0.5)
      GPIO.output(_controlPin, False)
      pwm.ChangeDutyCycle(0)

    def LookForward():
        self.SetAngle(90)

    def MakeDecision():
        self.scanSurroundings()

         # Scenario TURN-LEFT
        if (_leftDist > _rightDist):
            _direction = "LEFT"

        # Scenario TURN-RIGHT
        elif (_rightDist > _leftDist):
            _direction = "RIGHT"
            
        # Scenario REVERSE
        #elif (_rightDist < ):
         #   _direction = "REVERSE"


    # Scan to the LEFT, RIGHT and CENTRE of the robot to take measurements of its surroundings
    def scanSurroundings():
        # Turn the ultrasonic servo motor to LEFT RIGHT and CENTRE positions
        # Take a reading at each of these points and then return this data to the caller
        _leftDist =  self.takeMeasurement(LEFT);
        sleep(DELAY)
        _centreDist = self.takeMeasurement(CENTRE);
        sleep(DELAY)
        _rightDist = self.takeMeasurement(RIGHT);
        sleep(DELAY)
        
        self.SetAngle(90); # Re-centre the servo motor to face in front of the robot chassis to detect future head-on collisions

    def takeMeasurement(positon):
      pwm.start(0);
      distance = 0;
      SetAngle(position); # Rotate Servo to position to take distance measurement
      distance = takeUltrasonicMeasurement();
      pwm.stop();
      return distance

    def takeUltrasonicMeasurement():
        measuredDistanceTemp = 0;

        # Release a TRIGGER pulse from the ultrasonic sensor
        GPIO.output(TRIG, 1)
        time.sleep(0.00001)
        GPIO.output(TRIG, 0)

        # Time the return of the TRIGGER pulse signal back to the ultrasonic sensor
        while GPIO.input(ECHO) == 0:
            pass
        start = time.time()
        while GPIO.input(ECHO) == 1:
            pass
        stop = time.time()

        measuredDistanceTemp = round(((stop - start) * 17000), 3);

        # @note: DEBUG ONLY
        # Display measurement and corresponding time
        # print("Distance:  " + str(measuredDistanceTemp) + " cm")
        # print("Time:      " + str(round((stop - start)*1000, 3)) + " ms")
        
        return measuredDistanceTemp;
