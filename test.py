import pyttsx3

def onWord(name, location, length):
   print ('word', name, location, length)
   if location > 4:
      engine.stop()
engine = pyttsx3.init()
engine.connect('started-word', onWord)
engine.say('The quick brown fox jumped over the lazy dog.')
engine.runAndWait()