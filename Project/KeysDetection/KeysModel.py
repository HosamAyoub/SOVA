import RPi.GPIO as GPIO
import ultralytics
from ultralytics import YOLO
import os 
import cv2
import numpy as np
#from picamera2 import Picamera2
from time import sleep
from subprocess import call
from pygame import mixer, quit

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

def callImage():
    GPIO.output(flashPIN, GPIO.HIGH)
    #picam2.capture_file("KeysDetection/test.jpg")
    GPIO.output(flashPIN, GPIO.LOW)
    #img_path = "KeysDetection/test.jpg"
    return_value, img = camera.read()
    #img = cv2.imread(img_path)
    results = model(img, conf=0.6 , save=True)
    return results,img



def position():
    '''
    This function takes only the results of the Yolo custom model and 
    gives instructions on how to reach the desired object
     
    '''
    isIdeal = False
    results , img = callImage()
    # getting the location of box corners 
    try:
        xright =results[0].boxes.xyxy.cpu().numpy()[0][2] 
        xleft =results[0].boxes.xyxy.cpu().numpy()[0][0] 
        yright =results[0].boxes.xyxy.cpu().numpy()[0][3] 
        yleft =results[0].boxes.xyxy.cpu().numpy()[0][1] 
    except:
        print('No Keys found')
        play_audio('KeysDetection/VoiceCommands/NoKeys.wav')
        return isIdeal
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
            if loc[1]< 0.25 :
                play_audio('KeysDetection/VoiceCommands/LookLeft.wav')
            elif loc[1] > 0.75:
                play_audio('KeysDetection/VoiceCommands/LookRight.wav')
            else:
                xideal=1
                print('X axis is ok')
                    
            if loc[0] < 0.4:
                play_audio('KeysDetection/VoiceCommands/LookUp.wav')
            elif loc[0] > 0.6:
                play_audio('KeysDetection/VoiceCommands/LookDown.wav')
            else:  
                yideal=1  
                print('Y axis is ok')  
                
        # width is heigher        
        else:
            if loc[1]< 0.4 :
                play_audio('KeysDetection/VoiceCommands/LookLeft.wav')
            elif loc[1] > 0.6:
                play_audio('KeysDetection/VoiceCommands/LookRight.wav')
            else:
                xideal=1
                print('X axis is ok')
                
            if loc[0] < 0.25:
                play_audio('KeysDetection/VoiceCommands/LookUp.wav')
            elif loc[0] > 0.75:
                play_audio('KeysDetection/VoiceCommands/LookDown.wav')
            else: 
                yideal=1   
                print('Y axis is ok')    
                
    #image is close to a square                    
    else:
        if loc[1]< 0.4 :
            play_audio('KeysDetection/VoiceCommands/LookLeft.wav')
        elif loc[1] > 0.6:
            play_audio('KeysDetection/VoiceCommands/LookRight.wav')
        else:
            xideal=1
            print('X axis is ok')
            
        if loc[0] < 0.4:
            play_audio('KeysDetection/VoiceCommands/LookUp.wav')
        elif loc[0] > 0.6:
            play_audio('KeysDetection/VoiceCommands/LookDown.wav')
        else:
            yideal=1    
            print('Y axis is ok')  
    
    # Checking for the ideal prespective
    if xideal ==1 and yideal==1:
        picam2.stop()
        play_audio('KeysDetection/VoiceCommands/InFront.wav')
        isIdeal = True                          
    return isIdeal
               
    

def key():
    isIdeal=False
    while isIdeal== False:
        try :
            isIdeal = position()
            #os.remove(path)
        except IndexError:
            print('No Keys infront of you')
            play_audio('KeysDetection/VoiceCommands/NoKeys.wav')
            #os.remove(path)
            continue
        except FileNotFoundError:
            print('No such file, Process Terminated')
            #picam2.stop()
            play_audio('KeysDetection/VoiceCommands/KeysTerminated.wav')
            break

if __name__ == '__main__':
    '''picam2 = Picamera2()
    picam2.still_configuration.main.size = (2592, 1944)
    picam2.still_configuration.align()
    picam2.configure("still")
    picam2.set_controls({"ExposureTime": 60000, "AnalogueGain": 15.0, "Saturation": 1.3})
    picam2.start()
    '''
    camera = cv2.VideoCapture(0 , cv2.CAP_V4L2 )
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    model = YOLO('KeysDetection/best.pt')
    model.fuse()
    key()