import RPi.GPIO as GPIO
import ultralytics
from ultralytics import YOLO
import os 
import cv2
import numpy as np
from picamera2 import Picamera2
import time
from pygame import mixer, quit

GPIO.setmode(GPIO.BOARD)
flashPIN = 31
GPIO.setup(flashPIN, GPIO.OUT)

picam2 = Picamera2()
picam2.still_configuration.main.size = (720, 960)
#picam2.still_configuration.align()
picam2.configure("still")
#picam2.set_controls({"ExposureTime": 80000, "Saturation": 1.3})
picam2.start()
model = YOLO('WalletDetect/best.pt')
model.fuse()


def play_audio(audio_file):
    mixer.init()
    mixer.music.load(audio_file)
    mixer.music.play()
    while mixer.music.get_busy():
        continue
    quit()


def callImage():
    GPIO.output(flashPIN, GPIO.HIGH)
    picam2.capture_file("WalletDetect/test.jpg")
    GPIO.output(flashPIN, GPIO.LOW)
    image = cv2.imread('WalletDetect/test.jpg')
    rotated_image = np.rot90(image, k=1)
    cv2.imwrite("WalletDetect/test.jpg", rotated_image)
    img_path = "WalletDetect/test.jpg"
    img = cv2.imread(img_path)
    results = model(img, conf=0.7 , save=True)
    return results,img, img_path



def position():
    '''
    This function takes only the results of the Yolo custom model and 
    gives instructions on how to reach the desired object
     
    '''
    isIdeal = False
    results , img, path = callImage()
    # getting the location of box corners 
    try:
        xright =results[0].boxes.xyxy.cpu().numpy()[0][2] 
        xleft =results[0].boxes.xyxy.cpu().numpy()[0][0] 
        yright =results[0].boxes.xyxy.cpu().numpy()[0][3] 
        yleft =results[0].boxes.xyxy.cpu().numpy()[0][1] 
    except:
        print('No Wallets found')
        play_audio('WalletDetect/VoiceCommands/NoWallet.wav')
        return isIdeal,path
    #Locating the center of the box
    xc = (xright - xleft)/2 +xleft
    yc = (yright - yleft)/2 +yleft
    
    xideal,yideal = 0,0
    #calculating the location with respect to image width and height
    loc = np.divide((yc,xc),img.shape[:2])
    
    # if the image is a landscape (eitheer height or width is much higher than the other)
    if max(img.shape[:2])> 1.3*min(img.shape[:2]):
        #Height is higher
        if max(img.shape[:2]) == img.shape[:2][0]:
            if loc[1]< 0.25:
                play_audio('WalletDetect/VoiceCommands/LookLeft.wav')
            elif loc[1] > 0.75:
                play_audio('WalletDetect/VoiceCommands/LookRight.wav')
            else:
                xideal=1
                print('X axis is ok')
                    
            if loc[0] < 0.4:
                play_audio('WalletDetect/VoiceCommands/LookUp.wav')
            elif loc[0] > 0.6:
                play_audio('WalletDetect/VoiceCommands/LookDown.wav')
            else:  
                yideal=1  
                print('Y axis is ok')  
                
        # width is heigher        
        else:
            if loc[1]< 0.4 :
                play_audio('WalletDetect/VoiceCommands/LookLeft.wav')
            elif loc[1] > 0.6:
                play_audio('WalletDetect/VoiceCommands/LookRight.wav')
            else:
                xideal=1
                print('X axis is ok')
                
            if loc[0] < 0.25:
                play_audio('WalletDetect/VoiceCommands/LookUp.wav')
            elif loc[0] > 0.75:
                play_audio('WalletDetect/VoiceCommands/LookDown.wav')
            else: 
                yideal=1   
                print('Y axis is ok')    
                
    #image is close to a square                    
    else:
        if loc[1]< 0.4 :
            play_audio('WalletDetect/VoiceCommands/LookLeft.wav')
        elif loc[1] > 0.6:
            play_audio('WalletDetect/VoiceCommands/LookRight.wav')
        else:
            xideal=1
            print('X axis is ok')
            
        if loc[0] < 0.4:
            play_audio('WalletDetect/VoiceCommands/LookUp.wav')
        elif loc[0] > 0.6:
            play_audio('WalletDetect/VoiceCommands/LookDown.wav')
        else:
            yideal=1    
            print('Y axis is ok')  
    
    # Checking for the ideal prespective
    if xideal ==1 and yideal==1:
        play_audio('WalletDetect/VoiceCommands/InFront.wav')
        picam2.stop()
        isIdeal = True                          
    return isIdeal,path
               
    



isIdeal=False
while isIdeal== False:
    try :
        isIdeal,path = position()
        os.remove(path)
    except IndexError:
        print('No wallets infront of you')
        play_audio('WalletDetect/VoiceCommands/NoWallet.wav')
        os.remove(path)
        continue
    except FileNotFoundError:
        print('No such file, Process Terminated')
        picam2.stop()
        play_audio('WalletDetect/VoiceCommands/WalletTerminated.wav')
        break  