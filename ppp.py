from picamera import PiCamera
from time import sleep
import RPi.GPIO as IO
import time
from datetime import datetime

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

TRIG = 15
ECHO = 18

def init_gpio():
    IO.setwarnings(False)
    IO.setmode(IO.BCM)

    IO.setup(2,IO.OUT) #GPIO 2 -> Red LED as output
    IO.setup(3,IO.OUT) #GPIO 3 -> Green LED as output
    IO.setup(14,IO.IN) #GPIO 14 -> light sensor as input


    IO.setup(23,IO.OUT) #GPIO 23 -> Red LED as output
    IO.setup(24,IO.OUT) #GPIO 24 -> Green LED as output

    IO.setup(TRIG, IO.OUT)
    IO.setup(ECHO, IO.IN)

def init_camera():
    camera = PiCamera()
    camera.start_preview()
    sleep(5)
    return camera

def stop_camera(camera):
    camera.stop_preview()

def take_picture(camera):
	camera.capture('/home/pi/Documents/' + 'image' + '.jpg')

def send_email():
	imgFileName = 'image' + '.jpg'
	server = 'smtp.gmail.com'
	port = 587
	img_data = open(imgFileName, 'rb').read()
	msg = MIMEMultipart()
	msg['Subject'] = 'Image'
	msg['From'] = 'piege.photographique1@gmail.com'
	msg['To'] = 'chikouche.hadjer@gmail.com'

	text = MIMEText("This is My Image ... :) ")
	msg.attach(text)
	image = MIMEImage(img_data, name=os.path.basename(imgFileName))
	msg.attach(image)


	s = smtplib.SMTP(server, port)
	s.ehlo()
	s.starttls()
	s.ehlo()

	s.login('piege.photographique1@gmail.com', 'azertyuiop1')
	s.sendmail('piege.photographique1@gmail.com', 'chikouche.hadjer@gmail.com', msg.as_string())
	s.quit()

def light():
	if(IO.input(14)==True): #
        	IO.output(2,True) #Green led Off
        	IO.output(3,False) # Red led On	
    
    	if(IO.input(14)==False): #
		
		IO.output(2,False) #Red led OFF
        	IO.output(3,True) # Green led ON

def calculate_distance():
    IO.output(TRIG, False)
    time.sleep(2)

    IO.output(TRIG, True)
    time.sleep(0.00001)
    IO.output(TRIG, False)

    while IO.input(ECHO) == 0:
        pulse_start = time.time()

    while IO.input(ECHO) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    return round(distance, 1)

def main():
    print ("Lancement du piege photographique en cours ... ")
    print ("Initialisation de la Camera ... ")
    camera = init_camera()
    print ("Initialisation des variables GPIO ... ")
    init_gpio()

    currentDistance = 30

    while 1:
        newDistance = calculate_distance()
        if currentDistance - 5 > newDistance and newDistance < currentDistance + 5 or currentDistance - 5 < newDistance and newDistance > currentDistance + 5:
            currentDistance = newDistance
            print("prise de photo en cours ... ")
	    light()
            take_picture(camera)
	    send_email()

main()
#str(datetime.now().time())
