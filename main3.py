import pyttsx3
import speech_recognition as sr
import random
import webbrowser
import datetime
from plyer import notification
import pyautogui
import wikipedia 
import pywhatkit as pwk
import ollama
import screen_brightness_control as sbc
import os
import object_detection

client = ollama.Client()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  
engine.setProperty('rate', 175)

def speak(audio):
    print(audio)
    engine.say(audio)
    engine.runAndWait()

def command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)
    
    try:
        content = r.recognize_google(audio, language='en-in')
        print("You Said: " + content)
        return content
    except Exception:
        print("Please try again...")
        return ""
def handle_request(request):
        
        match request:      
            case "wake up":
                speak("Yes boss, how can I assist you?")    
                       
            case "play music":
                speak("yes sir, Playing your favorite music from Spotify")
                songs = [
                    
                    "https://open.spotify.com/track/78BWCd70D1X6LMkDZm1UoF?si=d9057420c43e4afb",   #millon
                    "https://open.spotify.com/track/3yHyiUDJdz02FZ6jfUbsmY?si=59cd98813cb34ec3",   #sataranga
                    "https://open.spotify.com/track/0HqZX76SFLDz2aW8aiqi7G?si=ddcf58a7ed134e5d",   #bones
                    "https://open.spotify.com/track/0pqnGHJpmpxLKifKRmU6WP?si=0a20364df3ac48c4"    #believer
                ]
                webbrowser.open(random.choice(songs))
            
            case "increase brightness":
                sbc.set_brightness(sbc.get_brightness()[0] + 25)
                speak("yes sir, increased")
            
            case "decrease brightness":
                sbc.set_brightness(sbc.get_brightness()[0] - 25)
                speak("yes sir, decreased")    
            
            case "take a screenshot":
                speak("yes sir, captured")
                pyautogui.press("prtsc")
                pyautogui.sleep(2)
                pyautogui.click(200, 220)    
            
            case "decrease volume":
                speak("yes sir, Decreasing volume")
                pyautogui.press("volumedown")
            case "increase volume":
                speak("yes sir, Increasing volume")
                pyautogui.press("volumeup")
            
            case "what's the time":
                now_time = datetime.datetime.now().strftime("%H:%M")
                speak("Current time is " + now_time)
            
            case "what's the date":
                now_date = datetime.datetime.now().strftime("%d %m %Y")
                speak("Today's date is " + now_date)
                
            case "detect objects":
                speak("Starting object detection")
                object_detection.start_detection()   
            
            case "note this work":
                task = request.replace("new task", "").strip()
                if task:
                    speak("yes sir, Adding task: " + task)
                    with open("todo.txt", "a") as file:
                        file.write(task + "\n")
            
            case "delete task":
                task = request.replace("delete task", "").strip()
                if task:
                    with open("todo.txt", "r") as file:
                        tasks = file.readlines()
                    with open("todo.txt", "w") as file:
                        file.writelines([t for t in tasks if t.strip() != task])
                    speak("yes sir, Deleted task: " + task)
            
            case "read out the task":
                with open("todo.txt", "r") as file:
                    speak("yes sir, The list goes by: " + file.read())
            
            case "notify task":
                with open("todo.txt", "r") as file:
                    tasks = file.read()
                notification.notify(title="Today's task", message=tasks)
            
            case "open college YouTube":
                webbrowser.open("https://www.youtube.com/@PaceAutonomous")
                speak("yes sir, Opening  your college YouTube channel")
            
            case "open YouTube":
                webbrowser.open("https://www.youtube.com")
                speak("yes sir, Opening YouTube")
            
            case "open Instagram":
                webbrowser.open("https://www.instagram.com")
                speak("yes sir, Opening Instagram")
            
            case "open Snapchat":
                webbrowser.open("https://www.snapchat.com")
                speak("yes sir, Opening Snapchat")
            
            case "open LinkedIn":
                webbrowser.open("https://www.linkedin.com")
                speak("yes sir, Opening LinkedIn")
            
            case "open our college":
                webbrowser.open("https://pace.ac.in/")
                speak("yes sir, Opening official webpage of PACE Institute of Technology and Sciences")
            
            case "open ecap":
                webbrowser.open("https://ecap.pace.ac.in/default.aspx")
                speak("yes sir, Opening PACE ECAP portal")
            case "open Amazon":
                webbrowser.open("https://www.amazon.in")
                speak("yes sir, Opening Amazon")
                
            case _ if request.startswith("order a"):
                query = request.replace("order", "").strip()
                pyautogui.hotkey('alt', '/')
                pyautogui.hotkey('ctrl','a')
                pyautogui.press("delete")
                pyautogui.typewrite(query)
                pyautogui.sleep(1)
                pyautogui.press("enter")
                speak("sure sir")
                
            case "open Flipkart":
                webbrowser.open("https://www.flipkart.in")
                speak("yes sir, Opening Flipkart")
                    
            case _ if request.startswith("open"):
                query = request.replace("open", "").strip()
                pyautogui.press("super")
                pyautogui.typewrite(query)
                pyautogui.sleep(2)
                pyautogui.press("enter")
                speak("yes sir, Opening " + query)
            
            case _ if request.startswith("close"):
                query = request.replace("close", "").strip()
                pyautogui.hotkey('alt', 'F4')
                speak("yes sir, Closing")
            
            case _ if "search wikipedia" in request:
                query = request.replace("Drona", "").replace("search wikipedia", "").strip()
                result = wikipedia.summary(query, sentences=2)
                speak(result)
            
            case _ if "WhatsApp" in request:
                pwk.sendwhatmsg("+918885199116", "hello pavani mam", 12, 3, 20)
                speak("yes sir, Message sent")    
                
            case _ if "search Google" in request:
                query = request.replace("Drona", "").replace("search Google", "").strip()
                webbrowser.open(f"https://www.google.com/search?q={query}")
                speak("yes sir, Opening Google")    
            case _:
            #query = request.replace("", "Drona").strip()
                model="wizardlm2"
                prompt=request
                response = client.generate(model=model,prompt=prompt)
                speak(response.text)    


def main_process():
    while True:
        request = command()
        if request:
            handle_request(request)

main_process()