#!/usr/bin/env python3
import picamera
import datetime
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
SHUTTER_SWITCH = 4  # Physical pin 26, switch to GND
MODE_SWITCH = 17
GPIO.setup(SHUTTER_SWITCH,GPIO.IN,pull_up_down = GPIO.PUD_UP)
GPIO.setup(MODE_SWITCH,GPIO.IN,pull_up_down = GPIO.PUD_UP)

print ("Press Ctrl & C to Quit")

mode = "None"

while True:
    try:
        while mode == "None":
            if GPIO.input(MODE_SWITCH) == 0:
                print("Switched to Picture")
                mode = "Picture"
                time.sleep(0.5)
                
    except KeyboardInterrupt:
        print("Quit")
        GPIO.cleanup()

    try:
        while mode == "Picture":
            with picamera.PiCamera() as camera:
                camera.resolution = (1280, 720)
                now = datetime.datetime.now()
                timestamp = now.strftime("%y-%m-%d_%H-%M-%S")
                camera.start_preview()
                if GPIO.input(SHUTTER_SWITCH) == 0:
                    print("Snap")
                    camera.capture("/mnt/extra/" + str(timestamp) + '.jpeg')
                    time.sleep(.5)
                if GPIO.input(MODE_SWITCH) == 0:
                    print("Switched to Video")
                    mode = "Video"
                    time.sleep(0.5)

    except KeyboardInterrupt:
        print ("Quit")
        GPIO.cleanup()

    Record = 0

    try:
        while mode == "Video":
            with picamera.PiCamera() as camera:
                camera.resolution = (1280, 720)
                camera.framerate = 60
                if GPIO.input(MODE_SWITCH) == 0:
                   print("Switched to None")
                   mode = "None"
                   time.sleep(0.5)
                elif GPIO.input(SHUTTER_SWITCH) == 0:
                    Record = 1
                    print ("Recording")
                    now = datetime.datetime.now()
                    timestamp = now.strftime("%y-%m-%d_%H-%M-%S")
                    camera.start_preview()
                    camera.start_recording("/mnt/extra/" + str(timestamp) + '.h264')
                    time.sleep(.5)
                    while Record == 1:
                        if GPIO.input(SHUTTER_SWITCH) == 0:
                            print ("Stopped")
                            camera.stop_recording()
                            Record = 0
                            while GPIO.input(SHUTTER_SWITCH) == 0:
                                time.sleep(0.1)
                            time.sleep(.5)
                        elif GPIO.input(MODE_SWITCH) == 0 and Record == 1:
                            camera.stop_recording()
                            Record = 0
                            print("Switched to None")
                            mode = "None"
                            time.sleep(0.5)

    except KeyboardInterrupt:
        print ("Quit")
        GPIO.cleanup()
