import pyttsx3
engine = pyttsx3.init() # object creation
x = 21
rate = engine.getProperty('rate')   # getting details of current speaking rate
engine.setProperty('rate', 100)     # setting up new voice rate
volume = engine.getProperty('volume')   #getting to know current volume level (min=0 and max=1)
engine.setProperty('volume',1.0)    # setting up volume level  between 0 and 1
voices = engine.getProperty('voices')       #getting details of current voice
#engine.setProperty('voice', voices[x].id)   #changing index, changes voices. 1 for female
#engine.setProperty('voice', 'english_rp+f4')
engine.setProperty('voice', 'com.apple.speech.synthesis.voice.samantha')
#print(voices[x].id)
voices = engine.getProperty('voices')

engine.say("I will speak this text")
engine.runAndWait()
