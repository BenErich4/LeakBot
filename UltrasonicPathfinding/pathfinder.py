# Created by Lachlan Clark and Benjamin Eric
# This module controls the movement/pathfinding of the robot

import RPi.GPIO as GPIO
import UltrasonicSensor

# Global Constants
MAX_COLLISION_PREVENTION_DISTANCE = 20; # Furthest distance (cm) the robot can be to an object before stopping
MOTOR_ONE_CONTROL_PIN = 7;  # Defines which GPIO connects to the control signal of MOTOR 1
MOTOR_TWO_CONTROL_PIN = 11; # Defines which GPIO connects to the control signal of MOTOR 2
DELAY  = 0.01 # Delay time (seconds) between ultrasonic sensor readings
LEFT_ARRAY_ELEMENT   = 0; # Data in the array that represents the reading from the LEFT   side of the chassis
RIGHT_ARRAY_ELEMENT  = 1; # Data in the array that represents the reading from the RIGHT  side of the chassis
CENTRE_ARRAY_ELEMENT = 2; # Data in the array that represents the reading from the CENTRE side of the chassis

# Instruct the motors to turn the chassis LEFT
# @parameter: Time in ms that the motors will drive for (100 ms is default for manual control mode)
def turnLeft(autonomousDriveTime, manualDriveTime=100):
    # Drive Motor 1 High
    # Drive Motor 2 Low
    # Halt
    # Return to caller
    pass;

# Instruct the motors to turn the chassis RIGHT
# @parameter: Time in ms that the motors will drive for (100 ms is default for manual control mode)
def turnRight(autonomousDriveTime, manualDriveTime=100):
    # Drive Motor 2 High
    # Drive Motor 1 Low
    # Halt
    # Return to caller
    pass;
    
# Instruct the motors to REVERSE the chassis
# @parameter: Time in ms that the motors will drive for (100 ms is default for manual control mode)
def reverse(autonomousDriveTime, manualDriveTime=100):
    # Reverse for a brief period of time and then
    # Halt
    # Return to caller
    pass;

# Instruct the motors to move the chassis FORWARD (100 ms is default for manual control mode)
# @parameter: Time in ms that the motors will drive for
def forward(autonomousDriveTime, manualDriveTime=100):
    # Drive Forward
    pass;

# Instruct the motors to HALT the chassis 
def halt():
    # Drive Motor 1 IDLE
    # Drive Motor 2 IDLE
    # Return to caller
    pass;


# Determines what is the best path to take, given the surroundings
def makeDecision(distanceArrayTemp):
   
        
# Allows the user to manually control the robot
# @parameter: User instruction e.g. turnLeft, turnRight, reverse, forward, halt
def driveManually(userInstruction):
    # Need to somehow get the button presses from the webpage to here to instruct the motors accordingly

# This is the main procedure in this program that continuously directs the robot
def main():

    sensorServo = UltrasonicSensor.SensorServo(90, 7, 11, 2)
    
    # Record the current state the robot is in
    # @note Type: enumeration
   #class current_state(Enum):
    #    FORWARD = 1;
    #   REVERSE = 2;
     #   IDLE    = 3;
        
    # Recorded distance to the closest object on the LEFT, RIGHT and CENTRE sides of the robot
    #distanceArrayTemp = [0, 0, 0]; # [LEFT, RIGHT, CENTRE]
    
    # Initialise the robot
    #GPIO.setmode(GPIO.BOARD)   # Initialise GPIO pins
    #ultrasonicServoSetup();
    #ultrasonicSensorSetup();
    #current_state = IDLE;
    
    # Infinite Loop, main body of this program
    while True:



        # Add variables to receive an external command for manual instruction by user
        
        # Note: This 'if' statement could be replaced by an ISR, might reduce the processor load if checking was controlled by a timer.
        # Continuously check the distance in front of the robot when driving FORWARD
        # if (current_state == FORWARD):
        #     if (distanceInFront <= MIN_COLLISION_PREVENTION_DISTANCE):
        #         halt();
        #         current_state = IDLE;
            
        # # Scan the surroundings and make a decision when IDLE
        # # The robot ONLY scans when IDLE
        # elif (current_state == IDLE):
        #     distanceArrayTemp = scanSurroundings();
        #     makeDecision(distanceArrayTemp);
        #     current_state = FORWARD;

        # # Reverse robot and then determine a new path
        # elif (current_state == REVERSE):
        #     reverse();
        #     current_state = IDLE;
        
        # # User operates the robot manually    
        # elif (current_state == MANUAL):
        #     driveManually();

main();
