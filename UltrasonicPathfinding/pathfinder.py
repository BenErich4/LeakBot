# Created by Lachlan Clark and Benjamin Eric
# This module controls the movement/pathfinding of the robot

import GPIO

# Global Constants
MIN_COLLISION_PREVENTION_DISTANCE = 20; # Closest distance (cm) the robot can be to an object before stopping
MOTOR_ONE_CONTROL_PIN = 7;  # Defines which GPIO connects to the control signal of MOTOR 1
MOTOR_TWO_CONTROL_PIN = 11; # Defines which GPIO connects to the control signal of MOTOR 2

# Instruct the motors to turn the chassis LEFT
def turnLeft():
    pass;

# Instruct the motors to turn the chassis RIGHT
def turnRight():
    pass;
    
# Instruct the motors to REVERSE the chassis
def reverse():
    # Reverse for a brief perior of time and then halt
    halt();
    pass;

# Instruct the motors to HALT the chassis 
def halt():
    pass;

# Scan to the LEFT, RIGHT and CENTRE of the robot to take measurements of its surroundings
def scanSurroundings(distanceLeft, distanceRight, distanceInFront):
    # Turn the ultrasonic servo motor to LEFT RIGHT and CENTRE positions
    # Take a reading at each of these points and then return this data to the caller
    return (distanceLeft, distanceRight, distanceInFront)

# Determines what is the best path to take, given the surroundings
# This module needs lots of tweaking - this is barebones at this moment 
def makeDecision(distanceLeft, distanceRight, distanceInFront):
    # Scenario TURN-LEFT
    if (distanceLeft > distanceRight & distanceLeft > distanceInFront):
        turnLeft();

    # Scenario TURN-RIGHT
    elif (distanceRight > distanceLeft & distanceRight > distanceInFront):
        turnRight();
        
    # Scenario REVERSE
    # This scenario needs fixing. Under certain circumstances the robot will not work as desired
    # e.g. the probe is at a dead-end where the sides are greater in width to MIN_COLLISION_PREVENTION_DISTANCE
    elif (distanceRight <= MIN_COLLISION_PREVENTION_DISTANCE & distanceRight <= MIN_COLLISION_PREVENTION_DISTANCE & distanceInFront <= MIN_COLLISION_PREVENTION_DISTANCE):
        reverse();  
    
# movementMonitor() is the main function in this program that continuously directs the robot
def movementMonitor():
    current_state = [FORWARD, REVERSE, IDLE] # Current state the robot is in
    distanceInFront = 0; # Recorded distance (returned value from scanSurroundings()) to the closest object in front of the robot
    distanceRight   = 0; # Recorded distance (returned value from scanSurroundings()) to the closest object on the RIGHT side of the robot 
    distanceLeft    = 0; # Recorded distance (returned value from scanSurroundings()) to the closest object on the LEFT side of the robot

    # Determine an initial path
    scanSurroundings(distanceLeft, distanceRight, distanceInFront);
    makeDecision(distanceLeft, distanceRight, distanceInFront);
    
    # Infinite Loop, main body of this program
    while True:
        
        # Note: This 'if' statement could be replaced by an ISR, might reduce the processor load if checking was controlled by a timer.
        # Continuously check the distance in front of the robot when driving FORWARD
        if (current_state == FORWARD):
            if (distanceInFront <= MIN_COLLISION_PREVENTION_DISTANCE):
                halt();
                current_state = IDLE;
            
        # Scan the surroundings and make a decision when IDLE
        elif (current_state == IDLE):
            scanSurroundings(distanceLeft, distanceRight, distanceInFront);
            makeDecision(distanceLeft, distanceRight, distanceInFront);

        # Reverse robot and then determine a new path
        elif (current_state == REVERSE):
            reverse();
            current_state = IDLE;
