from picamera import PiCamera
from time import sleep
import RPi.GPIO as IO
import time



IO.setwarnings(False)
IO.setmode(IO.BCM)

IO.setup(2,IO.OUT) #GPIO 2 -> Red LED as output
IO.setup(3,IO.OUT) #GPIO 3 -> Green LED as output
IO.setup(14,IO.IN) #GPIO 14 -> IR sensor as input

TRIG = 15
ECHO = 18

IO.setup(23,IO.OUT) #GPIO 23 -> Red LED as output
IO.setup(24,IO.OUT) #GPIO 24 -> Green LED as output




print("Distance Measurement In Progress")

IO.setup(TRIG, IO.OUT)
IO.setup(ECHO, IO.IN)
currentDistance=0

while 1:
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

    distance = round(distance, 2)
    print("Distance: ", distance, " cm")
    if currentDistance != distance:
	#program that take a pic after sleeping 5 sec
	#and save it on /home/pi/Desktop/image.jpg
	
	camera = PiCamera()

	camera.start_preview()
	sleep(5)
	camera.capture('/home/pi/Desktop/' + str(pulse_end) + '.jpg')
	camera.stop_preview()
	
    currentDistance = distance
	
    

#while 1:
 #   if(IO.input(14)==True): #object is far away
  #      IO.output(2,True) #Red led ON
   #     IO.output(3,False) # Green led OFF
    
    #if(IO.input(14)==False): #object is near
     #   IO.output(3,True) #Green led ON
      #  IO.output(2,False) # Red led OFF
    



