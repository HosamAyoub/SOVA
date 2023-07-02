import RPi.GPIO as GPIO
import pandas as pd
import numpy as np
import cv2
from picamera2 import Picamera2
from subprocess import call

GPIO.setmode(GPIO.BOARD)
flashPIN = 31
GPIO.setup(flashPIN, GPIO.OUT)

picam2 = Picamera2()
picam2.still_configuration.main.size = (2592, 1944)
picam2.still_configuration.align()
picam2.configure("still")
picam2.set_controls({"ExposureTime": 60000, "AnalogueGain": 15.0, "Saturation": 1.3})
picam2.start()
GPIO.output(flashPIN, GPIO.HIGH)
picam2.capture_file("ColorDetection/image_1.jpg")
GPIO.output(flashPIN, GPIO.LOW)
path = 'ColorDetection/image_1.jpg'
img = cv2.imread(path)
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
call(["./mimic1/mimic", "-t", f"The color is {color}."])