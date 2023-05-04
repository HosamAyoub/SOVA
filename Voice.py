from gtts import gTTS
from playsound import playsound 
import os 

speech = gTTS(text = 'Hi, Hesham', lang = 'en')
file1 = str("hello.mp3")
speech.save(file1)
playsound(file1)
print ('after')
os.remove(file1)
