# This code is maintained by Benjamin Erich

# This module interfaces an HC-SR04 (ultrasonic sensor) with a Raspberry Pi.
# @note: Add series external resistor to the ECHO pin as a safety precaution

import RPi.GPIO as GPIO
import time

# GPIO pins used for the ultra sonic sensor's TRIGGER and ECHO pins 
TRIG = 7
ECHO = 11
    
def ultrasonicSensorSetup():
    #GPIO.setwarnings(False)    # Disable console messages
    GPIO.setup(ECHO, GPIO.IN)  # Sets the echo as an Input
    GPIO.setup(TRIG, GPIO.OUT) # Sets the trig as an Output
    GPIO.output(TRIG, 0)       # Set the trig pin LOW
    print("Ultrasonic Sensor Successfully Initialised")

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
