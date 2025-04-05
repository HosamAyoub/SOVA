import RPi.GPIO as GPIO
import cv2
from picamera2 import Picamera2
from sys import argv
from time import sleep
import os
import imutils

GPIO.setmode(GPIO.BOARD)
flashPIN = 31
GPIO.setup(flashPIN, GPIO.OUT)

#print(os.getcwd())
name = argv[1] #replace with your name
#name = 'ahmed'

cam = Picamera2()
cam.still_configuration.main.size = (720, 960)
cam.still_configuration.main.format = "RGB888"
cam.still_configuration.controls.FrameRate = 10
cam.preview_configuration.align()
cam.configure("still")
    
img_counter = 0
fps = 0
cam.start()
sleep(2)
while True:
    GPIO.output(flashPIN, GPIO.HIGH)
    image = cam.capture_array()
    GPIO.output(flashPIN, GPIO.LOW)
    image = imutils.resize(image, width=720)
    image = imutils.rotate(image, 90)
    sleep(1)
    img_name = "FaceRecognition/dataset/"+ name +"/image_{}.jpg".format(img_counter)
    cv2.imwrite(img_name, image)
    print("{} written!".format(img_name))
    img_counter += 1

cam.stop()
cv2.destroyAllWindows()