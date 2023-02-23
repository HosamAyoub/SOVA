#!/usr/bin/env python
# coding: utf-8

# In[7]:


import ultralytics
from ultralytics import YOLO
import os 
import cv2
import numpy as np
#from picamera2 import Picamera2 , Preview
import time

# In[8]:

#picam2 = Picamera2()
model = YOLO('Wallet.pt')
model.fuse()


# In[20]:

def callImage():
    #img_path = input("Enter PATH of Image : ")
    os.system ("libcamera-still -t 1 -o test.jpg -n")
    img_path = "test.jpg"
    #picam2.start_preview(Preview.QTGL)
    #picam2.start()
    #picam2.start_and_capture_file("test11.jpg")
    #time.sleep(5)
    
    img = cv2.imread(img_path)
    results = model(img, conf=0.5 , save=True)
    return results,img, img_path


# In[21]:


def position():
    '''
    This function takes only the results of the Yolo custom model and 
    gives instructions on how to reach the desired object
     
    '''
    isIdeal = False
    results , img, path = callImage()
    # getting the location of box corners 
    xright =results[0].boxes.xyxy.cpu().numpy()[0][2] 
    xleft =results[0].boxes.xyxy.cpu().numpy()[0][0] 
    yright =results[0].boxes.xyxy.cpu().numpy()[0][3] 
    yleft =results[0].boxes.xyxy.cpu().numpy()[0][1] 

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
                os.system('mpg321 VoiceCommands/LookLeft.mp3')
            elif loc[1] > 0.75:
                os.system('mpg321 VoiceCommands/LookRight.mp3')      
            else:
                xideal=1
                print('X axis is ok')
                    
            if loc[0] < 0.4:
                os.system('mpg321 VoiceCommands/LookUp.mp3') 
            elif loc[0] > 0.6:
                os.system('mpg321 VoiceCommands/LookDown.mp3')
            else:  
                yideal=1  
                print('Y axis is ok')  
                
        # width is heigher        
        else:
            if loc[1]< 0.4 :
                os.system('mpg321 VoiceCommands/LookLeft.mp3')
            elif loc[1] > 0.6:
                os.system('mpg321 VoiceCommands/LookRight.mp3') 
            else:
                xideal=1
                print('X axis is ok')
                
            if loc[0] < 0.25:
                os.system('mpg321 VoiceCommands/LookUp.mp3')
            elif loc[0] > 0.75:
                 os.system('mpg321 VoiceCommands/LookDown.mp3')
            else: 
                yideal=1   
                print('Y axis is ok')    
                
    #image is close to a square                    
    else:
        if loc[1]< 0.4 :
            os.system('mpg321 VoiceCommands/LookLeft.mp3')
        elif loc[1] > 0.6:
            os.system('mpg321 VoiceCommands/LookRight.mp3') 
        else:
            xideal=1
            print('X axis is ok')
            
        if loc[0] < 0.4:
            os.system('mpg321 VoiceCommands/LookUp.mp3')
        elif loc[0] > 0.6:
             os.system('mpg321 VoiceCommands/LookDown.mp3')
        else:
            yideal=1    
            print('Y axis is ok')  
    
    # Checking for the ideal prespective
    if xideal ==1 and yideal==1:
        os.system('mpg321 VoiceCommands/InFront.mp3')
        isIdeal = True                          
    return isIdeal,path
               
    


# In[22]:


isIdeal,path = position()
#os.remove(path)
while isIdeal== False:
    isIdeal,path = position()
os.remove(path)
    
    


# In[ ]:




