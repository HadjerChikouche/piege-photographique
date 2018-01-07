from picamera import PiCamera
from time import sleep
import RPi.GPIO as IO
import time
from datetime import datetime

TRIG = 15
ECHO = 18
currentDistance = 0

def init_gpio():
    IO.setwarnings(False)
    IO.setmode(IO.BCM)

    IO.setup(2,IO.OUT) #GPIO 2 -> Red LED as output
    IO.setup(3,IO.OUT) #GPIO 3 -> Green LED as output
    IO.setup(14,IO.IN) #GPIO 14 -> IR sensor as input

    IO.setup(23,IO.OUT) #GPIO 23 -> Red LED as output
    IO.setup(24,IO.OUT) #GPIO 24 -> Green LED as output

    IO.setup(TRIG, IO.OUT)
    IO.setup(ECHO, IO.IN)


#program that take a pic after sleeping 5 sec
#and save it on /home/pi/Desktop/image.jpg
def take_picture():
	camera = PiCamera()
	camera.start_preview()
	sleep(5)
	camera.capture('/home/pi/Desktop/' + str(datetime.now().time()) + '.jpg')
	camera.stop_preview()

def calculate_distance():
    IO.output(TRIG, False)
    print ("Waiting For Sensor To Settle")
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
    return round(distance, 2)

def is_there_any_changement(newDistance):
    global currentDistance
    print("Distance: ", newDistance, " cm")
    if currentDistance != newDistance:
        currentDistance = newDistance
        return True
    return False

def main():
    while 1:
        init_gpio()
        newDistance = calculate_distance()
        if is_there_any_changement(newDistance) :
            take_picture()



main()
