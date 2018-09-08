import time
import serial

def read():	
	#open the GPIO pins' serial port where the GPS is plugged in
	gps = serial.Serial("/dev/ttyS0", baudrate = 9600)
	
	#construct an empty dictionary
	gpsData = {}
	
	while True:
		#read a serial line
		line = gps.readline()
		#split the comma separated sentence into a list of strings
		data = line.split(",")
		#look for the "RMC" Reccomended Minimum Navigation Info line
		if data[0] == "$GPRMC":
			#an 'A' here means the GPS has a connection, aka a fix
			if data[2] == "A":
				#get latitude, longitude from the list and store it a dictionary
				#dictionaries are like arrays but indexed by a specified 'key' string, eg 'latitude'
				#(the format of the GPS data sentences is specified
				#in the FGPMMOPA6H chip datasheet)
				gpsData['latitude'] = data[3]
				gpsData['longitude'] = data[5]
				gpsData['fix'] = True
				return gpsData
			else:
				gpsData['fix'] = False
				return gpsData
		else:
			#the GPS spits out other lines with info about satelites etc that we don't need
			#therefore we skip over the lines that aren't tagged '$GPRMC'
			continue

def test():
	return "test"