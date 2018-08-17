# This code is maintained by Benjamin Erich

# This module interfaces an HC-SR04 (ultrasonic sensor) with a Raspberry Pi.
# Add series external resistor to the ECHO pin as a safety precaution

import RPi.GPIO as GPIO
import time

# GPIO pins used
TRIG = 7
ECHO = 11
    
def ultrasonicSensorSetup():
    GPIO.setwarnings(False)    # Disable console messages
    GPIO.setmode(GPIO.BOARD)   # Initialise GPIO pins 
    GPIO.setup(ECHO, GPIO.IN)  # Sets the echo as an Input
    GPIO.setup(TRIG, GPIO.OUT) # Sets the trig as an Output
    GPIO.output(TRIG, 0)
    print("Ultrasonic Sensor Successfully Initialised")

def takeUltrasonicMeasurement():
    print("Starting Measurement...")

    GPIO.output(TRIG, 1)
    time.sleep(0.00001)
    GPIO.output(TRIG, 0)

    # Time the signal
    while GPIO.input(ECHO) == 0:
        pass
    start = time.time()
    while GPIO.input(ECHO) == 1:
        pass
    stop = time.time()

    # Display measurement and corresponding time
    print("Distance: " + str(round(((stop - start) * 17000), 3)) + " cm")
    print("Time:      " + str(round((stop - start)*1000, 3)) + " ms")

print("*** Start Ultrasonic Test ***\n\n")
ultrasonicSensorSetup()
takeUltrasonicMeasurement()
GPIO.cleanup()
print("\n\n*** End Ultrasonic Test ***\n\n")
