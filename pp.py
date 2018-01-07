from picamera import PiCamera
from time import sleep
import RPi.GPIO as IO
import time
from datetime import datetime

TRIG = 15
ECHO = 18

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

def init_camera():
    camera = PiCamera()
    camera.start_preview()
    sleep(5)
    return camera

def stop_camera(camera):
    camera.stop_preview()

def take_picture(camera):
	camera.capture('/home/pi/Desktop/' + str(datetime.now().time()) + '.jpg')

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
    return int(round(distance, 1))

def main():
    print ("Lancement du piege photographique en cours ... ")
    print ("Initialisation de la Camera ... ")
    camera = init_camera()
    print ("Initialisation des variables GPIO ... ")
    init_gpio()

    currentDistance = 0

    while 1:
        newDistance = calculate_distance()
        print("newDistance : ", newDistance, "!=", currentDistance, "currentDistance")
        if newDistance != currentDistance :
            currentDistance = newDistance
            print("prise de photo en cours ... ")
            take_picture(camera)

main()
