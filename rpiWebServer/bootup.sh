#!/bin/bash
sudo service motion start
sudo modprobe bcm2835-v4l2
sudo service motion restart
sudo /usr/bin/python /home/pi/Documents/rpiWebServer/templates/app.py
