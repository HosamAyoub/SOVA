import RPi.GPIO as GPIO
import cv2
from sys import argv
from time import sleep

GPIO.setmode(GPIO.BOARD)
flashPIN = 31
GPIO.setup(flashPIN, GPIO.OUT)

name = argv[1] #replace with your name
cam = cv2.VideoCapture(5)

img_counter = 0

while True:
    # Take pictures every sec
    GPIO.output(flashPIN, GPIO.HIGH)
    ret, frame = cam.read()
    GPIO.output(flashPIN, GPIO.LOW)
    frame = imutils.resize(frame, width=720)
    frame = imutils.rotate(frame, 90)
    sleep(1)
    img_name = "FaceRecognition/dataset/"+ name +"/image_{}.jpg".format(img_counter)
    cv2.imwrite(img_name, frame)
    print("{} written!".format(img_name))
    img_counter += 1

cam.release()

cv2.destroyAllWindows()
