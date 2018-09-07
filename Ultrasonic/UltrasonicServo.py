# This code is maintained by Benjamin Erich

# This module controls the servo motor for the ultrasonic sensor

import RPi.GPIO as GPIO
from time import sleep
from UltrasonicSensor.py import takeUltrasonicMeasurement

# Defined Constants
pinNumber = 7                   # Assigned GPIO pin to ultrasonic sensor's servo motor 
#GPIO.setwarnings(False)        # Disable console messages

def ultrasonicServoSetup():
  GPIO.setup(pinNumber, GPIO.OUT) # Set assigned GPIO pin as output

# Set the angle of the ultra sonic sensor's servo motor
def SetAngle(angle):
  duty = (angle / 18) + 2
  GPIO.output(pinNumber, True)
  pwm.ChangeDutyCycle(duty)
  sleep(0.5)
  GPIO.output(pinNumber, False)
  pwm.ChangeDutyCycle(0)
	
# Check the robot's current line of sight
def fireSensor(position):
  distanceMeasuredTemp = 0;
  SetAngle(position); # Rotate Servo to position to take distance measurement
  distanceMeasuredTemp = takeUltrasonicMeasurement();  
  return (distanceMeasuredTemp);

def CheckLOS(positon):
  pwm=GPIO.PWM(pinNumber, 50); # adds PWM functionality to GPIO pin (50 Hz)
  pwm.start(0);
  fireSensor(position);
  pwm.stop();
