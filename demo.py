import pyttsx3
engine = pyttsx3.init()
engine.say("popz lawde ke ball")
engine.runAndWait()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  
engine.setProperty('rate', 100)