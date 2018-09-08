import RPi.GPIO as GPIO
import subprocess, os, signal, time

from flask import Flask, render_template, Response, request, redirect, url_for

UPLOAD_FOLDER = '/home/pi/Documents/rpiWebServer'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpeg'])

app = Flask(__name__,template_folder = '/home/pi/Documents/rpiWebServer/templates')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
#define actuators GPIOs
STDBY = 6

AIN1 = 21
AIN2 = 13
PWMA = 26

BIN1 = 20
BIN2 = 16
PWMB = 19

# Define led pins as output
GPIO.setup(STDBY, GPIO.OUT)   
GPIO.setup(AIN1, GPIO.OUT) 
GPIO.setup(AIN2, GPIO.OUT) 
GPIO.setup(BIN1, GPIO.OUT)
GPIO.setup(BIN2, GPIO.OUT)
GPIO.setup(PWMA, GPIO.OUT)
GPIO.setup(PWMB, GPIO.OUT)
# turn leds OFF 
GPIO.output(STDBY, GPIO.LOW)
GPIO.output(AIN1, GPIO.LOW)
GPIO.output(AIN2, GPIO.LOW)
GPIO.output(BIN1, GPIO.LOW)
GPIO.output(BIN2, GPIO.LOW)
GPIO.output(PWMA, GPIO.LOW)
GPIO.output(PWMB, GPIO.LOW)

def check_kill_process(pstring):
	for line in os.popen("ps ax | grep " + pstring + " | grep -v grep"):
		fields = line.split()
		pid = fields[0]
		os.kill(int(pid), signal.SIGKILL)
		
@app.route("/")
def index():

	return render_template('index.html')
	
@app.route("/forwards")
def forwards():
	check_kill_process("forwards.py")
	check_kill_process("backwards.py")
	check_kill_process("left.py")	
	check_kill_process("right.py")	
	pwm1 = subprocess.Popen("/home/pi/Documents/rpiWebServer/forwards.py", shell=True)

	return False;
	
@app.route("/backwards")
def backwards():
	check_kill_process("forwards.py")
	check_kill_process("backwards.py")
	check_kill_process("left.py")	
	check_kill_process("right.py")	
	pwm2 = subprocess.Popen("/home/pi/Documents/rpiWebServer/backwards.py", shell=True)

	return False;
	
@app.route("/left")
def left():
	check_kill_process("forwards.py")
	check_kill_process("backwards.py")
	check_kill_process("left.py")	
	check_kill_process("right.py")	
	pwm3 = subprocess.Popen("/home/pi/Documents/rpiWebServer/left.py", shell=True)

	return False;
	
@app.route("/right")
def right():
	check_kill_process("forwards.py")
	check_kill_process("backwards.py")
	check_kill_process("left.py")	
	check_kill_process("right.py")	
	pwm4 = subprocess.Popen("/home/pi/Documents/rpiWebServer/right.py", shell=True)

	return False;

@app.route("/autonomous")
def right():
	check_kill_process("forwards.py")
	check_kill_process("backwards.py")
	check_kill_process("left.py")	
	check_kill_process("right.py")	
	pwm4 = subprocess.Popen("/home/pi/Documents/rpiWebServer/right.py", shell=True)

	return False;
	
@app.route("/stop")
def stop():
	GPIO.output(STDBY, 0)
	check_kill_process("forwards.py")
	check_kill_process("backwards.py")
	check_kill_process("left.py")	
	check_kill_process("right.py")	

	GPIO.output(STDBY, 0)

	return False;
		
if __name__ == "__main__":
   app.run(host='0.0.0.0', debug=True)
