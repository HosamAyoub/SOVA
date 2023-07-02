import RPi.GPIO as GPIO
import cv2
#from picamera2 import Picamera2
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
 
#picam2 = Picamera2()
#still_config = picam2.create_still_configuration({'size':(1280, 720), 'format':'RGB888'})
#picam2.configure(still_config)
#picam2.still_configuration.main.format = "RGB888"
#picam2.still_configuration.align()
#picam2.configure("still")
#picam2.set_controls({"ExposureTime": 150000, "AnalogueGain": 15.0, "Saturation": 1.3})
#picam2.start()
camera = cv2.VideoCapture(0 , cv2.CAP_V4L2 )
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
GPIO.output(flashPIN, GPIO.HIGH)
#picam2.capture_file("OCR/NewOCR/New.jpg")
GPIO.output(flashPIN, GPIO.LOW)
return_value, img_source = camera.read()
#img_source = cv2.imread("OCR/NewOCR/New.jpg")
#picam2.stop()
 
def get_grayscale(image):
     return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
 
 
def thresholding(image):
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

 
 
gray = get_grayscale(img_source)
thresh = thresholding(gray)
# opening = opening(gray)

 


ExtractedText= pytesseract.image_to_string(thresh,lang='eng')

if ExtractedText != "":
    print(ExtractedText)
    call(["./mimic1/mimic", "-t", ExtractedText])
    """speech = gTTS(text = ExtractedText, lang = 'en')
    file1 = str("hello.mp3")
    speech.save(file1)
    mixer.init()

    #Load audio file
    mixer.music.load(file1)

    print("music started playing....")

    #Set preferred volume
    mixer.music.set_volume(0.2)
    
    #Play the music
    mixer.music.play()

    while True:
        print("------------------------------------------------------------------------------------")
        print("Press 'p' to pause the music")
        print("Press 'r' to resume the music")
        print("Press 'e' to exit the program")
    
        #take user input
        userInput = input(" ")
    
        if userInput == 'p':
            # Pause the music
            mixer.music.pause()
            print("music is paused....")
            
        elif userInput == 'r':
            # Resume the music
            mixer.music.unpause()
            print("music is resumed....")
            
        elif userInput == 'e':
            # Stop the music playback
            mixer.music.stop()
            print("music is stopped....")
            break
    
    os.remove(file1)"""
else:
    call(["./mimic1/mimic", "-t", "Sorry, I couldn't detect any text."])
    print(">>>>> No Text <<<<<")
