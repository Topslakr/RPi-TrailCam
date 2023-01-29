#!/bin/python3

#Import Modules
import time
from datetime import datetime
from pathlib import Path
from gpiozero import MotionSensor
import os

#Script Variables
movement = '/home/topslakr/movement'
#Define Pin used for PIR Detection
pir = MotionSensor(23)


#Actions to take when PIR detects motion
def MotionDetect():
  pir.wait_for_motion()
  #Current Time for logging
  dt = datetime.now()
  #Start Script logic and Logging
  print('There was a movement!', dt)
  print('Will Write imovement file')
  #Create File for Capture Process to Use
  Path("/home/topslakr/movement").touch()

#Core loop of Script.
#Checks to see if Cap process is triggered.
#If not, begins to wait for motion
try:
    while True:
        print('Check for Existing Movement Trigger')
        file_check = os.path.exists(movement)
        print('Does the Movement file Exist?', file_check)
        if file_check == False:
            #Current Time for logging
            dt = datetime.now()
            print('No Movement File. Check PIR!', dt)
            #Triggers motion detection loop
            MotionDetect()
        else:
            #If the Capture process is running, just wait until it's not
            print('Waiting 10 Seconds')
            time.sleep(10)

except KeyboardInterrupt:
    print ("Finish...")
