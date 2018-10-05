import RPi.GPIO as GPIO
import subprocess, os, signal, time

from flask import Flask, render_template, Response, request, redirect, url_for

UPLOAD_FOLDER = '/home/pi/Documents/rpiWebServer'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpeg'])

app = Flask(__name__,template_folder = '/home/pi/Documents/rpiWebServer/templates')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Manual or Autonomous control variable
Manual = False

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

RGB_GREEN = 9 
RGB_RED = 11

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
# turn leds OFF 
GPIO.output(STDBY, GPIO.LOW)
GPIO.output(AIN1, GPIO.LOW)
GPIO.output(AIN2, GPIO.LOW)
GPIO.output(BIN1, GPIO.LOW)
GPIO.output(BIN2, GPIO.LOW)
GPIO.output(PWMA, GPIO.LOW)
GPIO.output(PWMB, GPIO.LOW)
GPIO.output(RGB_RED, GPIO.LOW)
GPIO.output(RGB_GREEN, GPIO.LOW)

def check_kill_process(pstring):
	for line in os.popen("ps ax | grep " + pstring + " | grep -v grep"):
		fields = line.split()
		pid = fields[0]
		os.kill(int(pid), signal.SIGKILL)
		
@app.route("/")
def index():
	GPIO.output(RGB_GREEN, 0)
	GPIO.output(RGB_RED,   1)
	return render_template('index.html')
	
@app.route("/forwards")
def forwards():
	if Manual:
		check_kill_process("forwards.py")
		check_kill_process("backwards.py")
		check_kill_process("left.py")	
		check_kill_process("right.py")	
		pwm1 = subprocess.Popen("/home/pi/Documents/rpiWebServer/forwards.py", shell=True)

	return False;
	
@app.route("/backwards")
def backwards():
	if Manual:
		check_kill_process("forwards.py")
		check_kill_process("backwards.py")
		check_kill_process("left.py")	
		check_kill_process("right.py")	
		pwm2 = subprocess.Popen("/home/pi/Documents/rpiWebServer/backwards.py", shell=True)

	return False;
	
@app.route("/left")
def left():
	print Manual
	if Manual == True:
		check_kill_process("forwards.py")
		check_kill_process("backwards.py")
		check_kill_process("left.py")	
		check_kill_process("right.py")	
		pwm3 = subprocess.Popen("/home/pi/Documents/rpiWebServer/left.py", shell=True)
		
	else:
		pass
		
	return False;
	
@app.route("/right")
def right():
	if Manual:
		check_kill_process("forwards.py")
		check_kill_process("backwards.py")
		check_kill_process("left.py")	
		check_kill_process("right.py")	
		pwm4 = subprocess.Popen("/home/pi/Documents/rpiWebServer/right.py", shell=True)

	return False;

@app.route("/redled")
def redled():
	GPIO.output(RGB_GREEN, 0)
	GPIO.output(RGB_RED,   1)

	return False;
	
@app.route("/greenled")
def greenled():
	GPIO.output(RGB_RED,   0)
	GPIO.output(RGB_GREEN, 1)


	return False;
	
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

	return False;
	
@app.route("/manual")
def manual():
	global Manual
	Manual = True
	check_kill_process("pathfinder.py")
	check_kill_process("forwards.py")
	GPIO.output(PWMA, 0)
	GPIO.output(PWMB, 0)

	return False;
	
@app.route("/auto")
def auto():
	global Manual
	Manual = False
		
	auto = subprocess.Popen("/home/pi/Documents/rpiWebServer/pathfinder.py", shell=True)
	

	return False;
		
if __name__ == "__main__":
   app.run(host='192.168.43.127', port=80, debug=True)
