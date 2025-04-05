import RPi.GPIO as GPIO
import cv2
from picamera2 import Picamera2
import pytesseract
import numpy as np
from pytesseract import Output
from gtts import gTTS
import os
import time
import sys
from pygame import mixer
from subprocess import call
 
GPIO.setmode(GPIO.BOARD)
flashPIN = 31
GPIO.setup(flashPIN, GPIO.OUT) 
 
picam2 = Picamera2()
picam2.still_configuration.main.size = (1944, 2592)
picam2.still_configuration.align()
picam2.configure("still")
picam2.start()
GPIO.output(flashPIN, GPIO.HIGH)
picam2.capture_file("OCR/NewOCR/New.jpg")
GPIO.output(flashPIN, GPIO.LOW)
image = cv2.imread("OCR/NewOCR/New.jpg")
rotated_image = np.rot90(image, k=1)
cv2.imwrite("OCR/NewOCR/New.jpg", rotated_image)
img_source = cv2.imread("OCR/NewOCR/New.jpg")
picam2.stop()
 
def get_grayscale(image):
     return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
 
 
def thresholding(image):
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

 
 
gray = get_grayscale(img_source)
thresh = thresholding(gray)

 


ExtractedText= pytesseract.image_to_string(thresh,lang='eng')

if ExtractedText != "":
    print(ExtractedText)
    call(["./mimic1/mimic", "-t", ExtractedText])
else:
    call(["./mimic1/mimic", "-t", "Sorry, I couldn't detect any text."])
    print(">>>>> No Text <<<<<")
