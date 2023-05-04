#!/usr/bin/env python
# coding: utf-8

# In[14]:


import cv2
import pytesseract
import numpy as np
from pytesseract import Output
from gtts import gTTS
import os
import time
import sys
#pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
 
img_source = cv2.imread('Testing3.png')
 
 
def get_grayscale(image):
     return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
 
 
def thresholding(image):
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
 
 
# def opening(image):
#     kernel = np.ones((5, 5), np.uint8)
#     return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)

 
 
gray = get_grayscale(img_source)
thresh = thresholding(gray)
# opening = opening(gray)

 

#d = pytesseract.image_to_data(thresh, output_type=Output.DICT, lang='eng')
i= pytesseract.image_to_string(thresh,lang='eng')
print(i)
#print(d['text'])
#print(d)
#n_boxes = len(d['text'])
 
#    back to RGB
#     if len(img.shape) == 2:
#         img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
 
#     for i in range(n_boxes):
#         if int(d['conf'][i]) > 60:
#             (text, x, y, w, h) = (d['text'][i], d['left'][i], d['top'][i], d['width'][i], d['height'][i])
#             # don't show empty text
#             if text and text.strip() != "":
#                 img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
#                 img = cv2.putText(img, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)
#                 print(d['text'][i])
 
#     cv2.imshow('img', img)
#     cv2.waitKey(0)
# def Clean_Text(fullText):
#     Edited_Text = fullText.replace('_',"")
#     Edited_Text = Edited_Text.replace('__',"")
#     Edited_Text = Edited_Text.replace('W/', 'with')
#     Edited_Text = Edited_Text.replace('/' , 'or' )                                
#     Edited_Text = Edited_Text.replace('|',"")
#     Edited_Text = Edited_Text.replace(',',"")
#     Edited_Text = Edited_Text.replace('.',"")
#     return  Edited_Text 
  
speech = gTTS(text = i, lang = 'en')
file1 = str("hello.mp3")
#speech.save(file1)
#os.system('start hello.mp3')
#time.sleep(1)
#os.remove(file1)
    
    


# In[ ]:




