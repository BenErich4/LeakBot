#!/usr/bin/env python
import time
import serial

gps = serial.Serial("/dev/ttyS0", baudrate = 9600)

while True:
    #read a serial line
    line = gps.readline()
    #get rid of unwanted prefix and suffix characters by decoding
    #and split the comma separated sentence into a list of strings
    data = line.decode().split(",")
    #look for the "RMC" Reccomended Minimum Navigation Info line
    if data[0] == "$GPRMC":
        #an 'A' here means data is valid
        if data[2] == "A":
            #get latitude, longitude from the list
            #the format of the GPS data sentences is specified
            #in the FGPMMOPA6H chip datasheet
            print("Latitude: %s %s" % (data[3], data[4]))
            print("Longitude: %s %s" % (data[5], data[6]))
            print("Direction: %s degrees" % data[8])
            print("********")