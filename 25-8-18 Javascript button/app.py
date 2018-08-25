import RPi.GPIO as GPIO
import subprocess, os, signal

from flask import Flask, render_template, Response, request, redirect, url_for

UPLOAD_FOLDER = '/home/pi/Documents/rpiWebServer'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpeg'])

app = Flask(__name__,template_folder = '/home/pi/Documents/rpiWebServer/templates')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
#define actuators GPIOs
ledRed = 18
ledYlw = 19
ledGrn = 26
#initialize GPIO status variables
ledRedSts = 0
ledYlwSts = 0
ledGrnSts = 0
# Define led pins as output
GPIO.setup(ledRed, GPIO.OUT)   
GPIO.setup(ledYlw, GPIO.OUT) 
GPIO.setup(ledGrn, GPIO.OUT) 
# turn leds OFF 
GPIO.output(ledRed, GPIO.LOW)
GPIO.output(ledYlw, GPIO.LOW)
GPIO.output(ledGrn, GPIO.LOW)

def check_kill_process(pstring):
	for line in os.popen("ps ax | grep " + pstring + " | grep -v grep"):
		fields = line.split()
		pid = fields[0]
		os.kill(int(pid), signal.SIGKILL)
		
@app.route("/")
def index():

	return render_template('index.html')
	
@app.route("/forward")
def forward():
	pwm1 = subprocess.Popen("/home/pi/Documents/rpiWebServer/ledRed.py", shell=True)
	pwm2 = subprocess.Popen("/home/pi/Documents/rpiWebServer/ledYlw.py", shell=True)
	pwm3 = subprocess.Popen("/home/pi/Documents/rpiWebServer/ledGrn.py", shell=True)

	return False;
	
@app.route("/backward")
def backward():
	
	check_kill_process("ledYlw.py")
	check_kill_process("ledGrn.py")
	check_kill_process("ledRed.py")	

	return False;
		
if __name__ == "__main__":
   app.run(host='192.168.43.127', port=80, debug=True)
