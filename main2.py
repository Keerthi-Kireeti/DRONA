import pyttsx3
import speech_recognition as sr
import random
import webbrowser
import datetime
from plyer import notification
import pyautogui
import wikipedia 
import pywhatkit as pwk
from google import genai
import screen_brightness_control as sbc

client = genai.Client(api_key="AIzaSyALJhabAmr03IiZKVTWySL7s__fIWbUlq4")

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
        '''if request ("ok Drona" | "hey Drona"):
                speak("Yes boss, how can I assist you?")'''
        match request:                    
            case "play music":
                speak("yes sir, Playing your favorite music from Spotify")
                songs = [
                    
                    "https://open.spotify.com/track/78BWCd70D1X6LMkDZm1UoF?si=d9057420c43e4afb",
                    "https://open.spotify.com/track/3yHyiUDJdz02FZ6jfUbsmY?si=59cd98813cb34ec3",
                    "https://open.spotify.com/track/5bQ6oDLqvw8tywmnSmwEyL?si=7ed728bcb1df4ed3"
                ]
                webbrowser.open(random.choice(songs))
            
            case "increase brightness":
                sbc.set_brightness(sbc.get_brightness()[0] + 25)
                speak("yes sir, increased")
            
            case "decrease brightness":
                sbc.set_brightness(sbc.get_brightness()[0] - 25)
                speak("yes sir, decreased")    
            
            case "screenshot":
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
            
            case "add this work":
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
            
            case "open YouTube":
                webbrowser.open("https://www.youtube.com/@PaceAutonomous")
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
                
            case "order a shirt":
                pyautogui.hotkey('alt', '/')
                pyautogui.sleep(1)
                pyautogui.write('polo shirt', interval=0.25)
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
            
            case _ if "wikipedia" in request:
                query = request.replace("Drona", "").replace("search wikipedia", "").strip()
                result = wikipedia.summary(query, sentences=2)
                speak(result)
            
            case _ if "WhatsApp" in request:
                pwk.sendwhatmsg("+917036740869", "Hi", 9, 57, 15)
                speak("yes sir, Message sent")    
                
            case _ if "search Google" in request:
                query = request.replace("Drona", "").replace("search Google", "").strip()
                webbrowser.open(f"https://www.google.com/search?q={query}")
                speak("yes sir, Opening Google")    
            case _:
            #query = request.replace("", "Drona").strip()
                response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=[request])
                speak(response.text)    


def main_process():
    while True:
        request = command()
        if request:
            handle_request(request)

main_process()
