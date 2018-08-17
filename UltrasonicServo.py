# This code is maintained by Benjamin Erich

# This module controls the servo motor for the ultrasonic sensor

import RPi.GPIO as GPIO
from time import sleep

# Defined Constants
LEFT   = 175
CENTRE = 90
RIGHT  = 5
DELAY  = 0.01

pinNumber = 7                   # Assigned GPIO pin
GPIO.setwarnings(False)         # Disable console messages
GPIO.setmode(GPIO.BOARD)        # Initialise GPIO pins


def UltrasonicServoSetup():
  GPIO.setup(pinNumber, GPIO.OUT) # Set assigned GPIO pin as output

def SetAngle(angle):
  duty = (angle / 18) + 2
	GPIO.output(pinNumber, True)
	pwm.ChangeDutyCycle(duty)
	sleep(0.5)
	GPIO.output(pinNumber, False)
	pwm.ChangeDutyCycle(0)
	
# Check the robot's current line of sight
def CheckLOS():
  SetAngle(LEFT)   # Check Left
  sleep(DELAY)
  SetAngle(CENTRE) # Check Centre
  sleep(DELAY)
  SetAngle(RIGHT)  # Check Right
  sleep(DELAY)
  SetAngle(CENTRE) # Return to centre


print("Start Motor Test")
UltrasonicServoSetup()
pwm=GPIO.PWM(pinNumber, 50)     # adds PWM functionality to GPIO pin (50 Hz)
pwm.start(0)
CheckLOS()
pwm.stop()
GPIO.cleanup()
print("End Motor Test")
