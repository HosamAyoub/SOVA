import pandas as pd
import numpy as np
import cv2

path = '1.jpg'
img = cv2.imread(path)
# Reading csv file with pandas and giving names to each column
index = ["R", "G", "B","color_name"]
csv = pd.read_csv('ral_standard.csv', names=index, header=None)

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

color = get_color_name(pixel_center[2],pixel_center[1],pixel_center[0])
print(color)