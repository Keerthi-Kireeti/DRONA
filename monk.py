import pyttsx3
import speech_recognition as sr
import random
import webbrowser
import datetime
from plyer import notification
import pyautogui
import wikipedia 
import pywhatkit as pwk
import user_config
import mtranslate
import torch
import torchvision.transforms as T
from PIL import Image
import cv2
from rfdetr import build_model

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  
engine.setProperty('rate', 175)

def speak(audio):
    audio = mtranslate.translate(audio, to_language="en", from_language="en-in")
    print(audio)
    engine.say(audio)
    engine.runAndWait()

def command():
    content = " "
    while content == " ":
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Say something!")
            audio = r.listen(source)    
        try:
            content = r.recognize_google(audio, language='en-in')
            print("You Said..........." + content)
        except Exception as e:
            print("Please try again...")
    return content

def detect_objects():
    model = build_model()
    model.eval()
    cap = cv2.VideoCapture(0)
    transform = T.Compose([
        T.Resize((800, 800)),
        T.ToTensor()
    ])
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        img_tensor = transform(img).unsqueeze(0)
        
        with torch.no_grad():
            outputs = model(img_tensor)
        
        # Add visualization or processing logic here
        cv2.imshow("Object Detection", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

def main_process():
    while True:
        request = command()
        if "wake up" in request:
           speak("Yes boss, how can I assist you?")
        elif "play music" in request:
            speak("Playing your favorite music from Spotify")
            song = random.randint(1, 3)
            if song == 1:
                webbrowser.open("https://open.spotify.com/track/78BWCd70D1X6LMkDZm1UoF?si=d9057420c43e4afb")
            elif song == 2:
                webbrowser.open("https://open.spotify.com/track/3yHyiUDJdz02FZ6jfUbsmY?si=59cd98813cb34ec3")
            elif song == 3:
                webbrowser.open("https://open.spotify.com/track/5bQ6oDLqvw8tywmnSmwEyL?si=7ed728bcb1df4ed3")
        elif "detect objects" in request:
            speak("Starting object detection")
            detect_objects()
        elif "increase volume" in request:
            speak("Increasing volume")
            pyautogui.press("volumeup")
        elif "decrease volume" in request:
            speak("Decreasing volume")
            pyautogui.press("volumedown")
        elif "what's the time" in request:
            now_time = datetime.datetime.now().strftime("%H %M")
            speak("Current time is " + str(now_time))
        elif "what's the date" in request:
            now_time = datetime.datetime.now().strftime("%d %m %Y")
            speak("Today it's " + str(now_time))
        elif "open YouTube" in request:
            webbrowser.open("www.youtube.com")
            speak("Opening YouTube")
        elif "open Instagram" in request:
            webbrowser.open("www.instagram.com")
            speak("Opening Instagram")
        elif "open Snapchat" in request:
            webbrowser.open("www.snapchat.com")
            speak("Opening Snapchat")
        elif "open LinkedIn" in request:
            webbrowser.open("www.linkedin.com")
            speak("Opening LinkedIn")
        elif "open our college" in request:
            webbrowser.open("https://pace.ac.in/")
            speak("Opening the official webpage of PACE Institute of Technology and Sciences")
        elif "open ecap" in request:
            webbrowser.open("https://ecap.pace.ac.in/default.aspx")
            speak("Opening PACE eCAP portal")
        elif "wikipedia" in request:
            request = request.replace("search wikipedia", "")
            result = wikipedia.summary(request, sentences=2)
            speak(result)
        elif "search Google" in request:
            request = request.replace("search Google", "")
            webbrowser.open("https://www.google.com/search?q=" + request)
            speak("Opening Google")
        elif "WhatsApp" in request:
            pwk.sendwhatmsg("+917036740869", "Hi", 9, 57, 15)
            speak("Message sent")
        elif "open" in request:
            query = request.replace("open", "").strip()
            pyautogui.press("super")
            pyautogui.typewrite(query)
            pyautogui.sleep(2)
            pyautogui.press("enter")
            speak("Opening " + query)
        elif "close" in request:
            pyautogui.hotkey('alt', 'F4')
            speak("Closing")
main_process()