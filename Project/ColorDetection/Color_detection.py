import RPi.GPIO as GPIO
import pandas as pd
import numpy as np
import cv2
#from picamera2 import Picamera2
from subprocess import call
from pygame import mixer , quit
import os

def play_audio(audio_file):
    mixer.init(devicename = "bcm2835 Headphones, bcm2835 Headphones")
    mixer.music.load(audio_file)
    mixer.music.play()
    while mixer.music.get_busy():
        continue
    quit()


GPIO.setmode(GPIO.BOARD)
flashPIN = 31
GPIO.setup(flashPIN, GPIO.OUT)

'''
picam2 = Picamera2()
picam2.still_configuration.main.size = (2592, 1944)
picam2.still_configuration.align()
picam2.configure("still")
picam2.set_controls({"ExposureTime": 60000, "AnalogueGain": 15.0, "Saturation": 1.3})
picam2.start()
'''
camera = cv2.VideoCapture(0 , cv2.CAP_V4L2 )
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
GPIO.output(flashPIN, GPIO.HIGH)
#picam2.capture_file("ColorDetection/image_1.jpg")
GPIO.output(flashPIN, GPIO.LOW)
#path = 'ColorDetection/image_1.jpg'
return_value, img = camera.read()
#img = cv2.imread(path)
# Reading csv file with pandas and giving names to each column
index = ["R", "G", "B","color_name"]
csv = pd.read_csv('ColorDetection/ral_standard.csv', names=index, header=None)

# function to calculate minimum distance from all colors and get the most matching color
def get_color_name(R, G, B):
    minimum = 10000
    for i in range(len(csv)):
        d = abs(R - int(csv.loc[i, "R"])) + abs(G - int(csv.loc[i, "G"])) + abs(B - int(csv.loc[i, "B"]))
        if d <= minimum:
            minimum = d
            cname = csv.loc[i, "color_name"]
    return cname


height,width,_ = img.shape
cx = int(width/2)
cy = int(height/2)
pixel_center = img[cy,cx]

color = get_color_name(pixel_center[2],pixel_center[1],pixel_center[0]).capitalize()
print(f"The color is {color}")
call(["mimic", "-t", f"The color is {color}.", "-o","Color.wav"])
play_audio("Color.wav")
os.remove ("Color.wav")