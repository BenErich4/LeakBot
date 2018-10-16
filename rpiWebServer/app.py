import RPi.GPIO as GPIO
import subprocess, os, signal, time
import telemetry
import AutoLeakBot
import gpsReader as gps



from flask import Flask, render_template, Response, request, redirect, url_for, jsonify, send_from_directory

UPLOAD_FOLDER = '/home/pi/Documents/rpiWebServer'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpeg'])

app = Flask(__name__,template_folder = '/home/pi/Documents/rpiWebServer/templates')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Manual or Autonomous control variable
Manual = True

# set up the global telemetry list, containing gps data and if water has been detected,
# so can write this info to html page
#telemetry.init()

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
#define actuators GPIOs 
STDBY = 19
AIN1 = 13
AIN2 = 6
PWMA = 5
BIN1 = 26
BIN2 = 20
PWMB = 21

RGB_GREEN = 11
RGB_RED = 9
LIGHT_PIN = 10

# Define led pins as output
GPIO.setup(STDBY, GPIO.OUT)   
GPIO.setup(AIN1, GPIO.OUT) 
GPIO.setup(AIN2, GPIO.OUT) 
GPIO.setup(BIN1, GPIO.OUT)
GPIO.setup(BIN2, GPIO.OUT)
GPIO.setup(PWMA, GPIO.OUT)
GPIO.setup(PWMB, GPIO.OUT)
GPIO.setup(RGB_GREEN, GPIO.OUT)
GPIO.setup(RGB_RED, GPIO.OUT)
GPIO.setup(LIGHT_PIN, GPIO.OUT)
# turn leds OFF 
GPIO.output(STDBY, GPIO.LOW)
GPIO.output(AIN1, GPIO.LOW)
GPIO.output(AIN2, GPIO.LOW)
GPIO.output(BIN1, GPIO.LOW)
GPIO.output(BIN2, GPIO.LOW)
GPIO.output(PWMA, GPIO.LOW)
GPIO.output(PWMB, GPIO.LOW)
#GPIO.output(RGB_RED, GPIO.LOW)
#GPIO.output(RGB_GREEN, GPIO.LOW)
GPIO.output(LIGHT_PIN, GPIO.LOW)

def resetTelemFile():
	with open('stats.txt', 'r') as txt:
		# read a list of lines into data
		data = txt.readlines()
	txt.close()

	# now change the lines wishing to write to (see constants for defined line numbers)
	data[WATER_FOUND] = "False\n"
	gpsReading = gps.read()

	if gpsReading['fix']:
		data[CURRENT_LAT] = str(gpsReading['latitude'])+'\n'
		data[CURRENT_LONG] = str(gpsReading['longitude'])+'\n'
	else:
		data[CURRENT_LAT] = "No GPS Fix"
		data[CURRENT_LONG] = "No GPS Fix"
	date[WATER_LAT] = "Not Yet Found\n"
	data[WATER_LONG] = "Not Yet Found\n"

	# and write everything back
	with open('stats.txt', 'w') as file:
		txt.writelines(data)
	txt.close()

def check_kill_process(pstring):
	for line in os.popen("ps ax | grep " + pstring + " | grep -v grep"):
		fields = line.split()
		pid = fields[0]
		os.kill(int(pid), signal.SIGKILL)
		
@app.route("/")
def index():
	GPIO.output(RGB_GREEN, 0)
	GPIO.output(RGB_RED,   1)
	
	resetTelemFile()

	return render_template('index.html')
	
@app.route("/forwards")
def forwards():
	
	if Manual:
		print "works"
		check_kill_process("forwards.py")
		check_kill_process("backwards.py")
		check_kill_process("left.py")	
		check_kill_process("right.py")	
		pwm1 = subprocess.Popen("/home/pi/Documents/rpiWebServer/forwards.py", shell=True)

	return jsonify(False)
	
@app.route("/backwards")
def backwards():
	if Manual:
		check_kill_process("forwards.py")
		check_kill_process("backwards.py")
		check_kill_process("left.py")	
		check_kill_process("right.py")	
		pwm2 = subprocess.Popen("/home/pi/Documents/rpiWebServer/backwards.py", shell=True)

	return jsonify(False)
	
@app.route("/left")
def left():
	if Manual == True:
		check_kill_process("forwards.py")
		check_kill_process("backwards.py")
		check_kill_process("left.py")	
		check_kill_process("right.py")	
		pwm3 = subprocess.Popen("/home/pi/Documents/rpiWebServer/left.py", shell=True)
		
	else:
		pass
		
	return jsonify(False)
	
@app.route("/right")
def right():
	if Manual:
		check_kill_process("forwards.py")
		check_kill_process("backwards.py")
		check_kill_process("left.py")	
		check_kill_process("right.py")	
		pwm4 = subprocess.Popen("/home/pi/Documents/rpiWebServer/right.py", shell=True)

	return jsonify(False)

@app.route("/redled")
def redled():
	GPIO.output(RGB_GREEN, 0)
	GPIO.output(RGB_RED,   1)

	return jsonify(False)
	
@app.route("/greenled")
def greenled():
	GPIO.output(RGB_RED,   0)
	GPIO.output(RGB_GREEN, 1)


	return jsonify(False)
	
@app.route("/stop")
def stop():
	GPIO.output(STDBY, 0)
	check_kill_process("forwards.py")
	check_kill_process("backwards.py")
	check_kill_process("left.py")	
	check_kill_process("right.py")
	GPIO.output(RGB_RED, GPIO.LOW)
	GPIO.output(RGB_GREEN, GPIO.LOW)

	GPIO.output(STDBY, 0)

	return jsonify(False)
	
@app.route("/manual")
def manual():
	global Manual
	Manual = True
	check_kill_process("pathfinder.py")
	check_kill_process("forwards.py")
	check_kill_process("right.py")
	check_kill_process("left.py")
	check_kill_process("backwards.py")
	GPIO.output(PWMA, 0)
	GPIO.output(PWMB, 0)
	
	return jsonify(False)
	
@app.route("/auto")
def auto():
	global Manual
	Manual = False
	resetTelemFile()	
	auto = subprocess.Popen("/home/pi/Documents/rpiWebServer/pathfinder.py", shell=True)

	return jsonify(False)

@app.route("/update_telemetry", methods=['POST'])
def update_telemetry():
	global Manual
	telemetry_data = {}
	
	with open('telemetry.txt', 'r') as telemFile:
		# read a list of lines into data
		telemList = telemFile.readlines()
	filo.close()
	
	telemetry_data['waterFound'] = telemList(WATER_FOUND)
	telemetry_data['currentLat'] = telemList(CURRENT_LAT)
	telemetry_data['currentLong'] = telemList(CURRENT_LONG)
	telemetry_data['waterLat'] = telemList(WATER_LAT)
	telemetry_data['waterLong'] = telemList(WATER_LONG)
	
	foundWater = False

	if (telemetry_data['waterFound'] == "True"):
		Manual = True
		foundWater = True
		GPIO.output(RGB_RED,   0)
		GPIO.output(RGB_GREEN, 1)
	
	result = [{'data': render_template('response.html', telemetry_data=telemetry_data), 'waterFound': foundWater}]


	print ("Manual ="+str(Manual))

	return jsonify(result)
	
@app.route("/lightOn")
def lightOn():
	GPIO.output(LIGHT_PIN, GPIO.HIGH)
	print "Lights On"
	return ("LightsOn")
	
@app.route("/lightOff")
def lightOff():
	GPIO.output(LIGHT_PIN, GPIO.LOW)
	print "Lights Off"
	return ("LightsOff")
	
		
if __name__ == "__main__":
   app.run(host='192.168.137.154', debug=True)
