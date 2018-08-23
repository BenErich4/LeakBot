import RPi.GPIO as GPIO
import subprocess, os, signal
from flask import Flask, render_template, request
app = Flask(__name__,template_folder = '/home/pi/Documents/rpiWebServer/templates')
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
	# Read Sensors Status
	ledRedSts = GPIO.input(ledRed)
	ledYlwSts = GPIO.input(ledYlw)
	ledGrnSts = GPIO.input(ledGrn)
	templateData = {
              'title' : 'GPIO output Status!',
              'ledRed'  : ledRedSts,
              'ledYlw'  : ledYlwSts,
              'ledGrn'  : ledGrnSts,
        }
	return render_template('index.html', **templateData)
	
@app.route("/<deviceName>/<action>")
def action(deviceName, action):
	
	
	if deviceName == 'ledRed' and action == "on":
		pwm1 = subprocess.Popen("/home/pi/Documents/rpiWebServer/ledRed.py", shell=True)
	
	if deviceName == 'ledYlw' and action == "on":
		pwm2 = subprocess.Popen("/home/pi/Documents/rpiWebServer/ledYlw.py", shell=True)
	
	if deviceName == 'ledGrn' and action == "on":
		pwm3 = subprocess.Popen("/home/pi/Documents/rpiWebServer/ledGrn.py", shell=True)


	if deviceName == 'ledRed' and action == "off":
		check_kill_process("ledRed.py")	
		
	if deviceName == 'ledYlw' and action == "off":
		check_kill_process("ledYlw.py")
	
	if deviceName == 'ledGrn' and action == "off":
		check_kill_process("ledGrn.py")

		
		     
	ledRedSts = GPIO.input(ledRed)
	ledYlwSts = GPIO.input(ledYlw)
	ledGrnSts = GPIO.input(ledGrn)
   
	templateData = {
              'ledRed'  : ledRedSts,
              'ledYlw'  : ledYlwSts,
              'ledGrn'  : ledGrnSts,
	}
	return render_template('index.html', **templateData)
if __name__ == "__main__":
   app.run(host='192.168.43.127', port=80, debug=True)
