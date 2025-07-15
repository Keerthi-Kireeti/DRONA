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
import threading
import object_detection
# Initialize Ollama client
client = ollama.Client()

# Initialize TTS engine once
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 175)

# Optimized Speak Function (Runs in Background)
def speak(audio):
    print(audio)
    threading.Thread(target=lambda: (engine.say(audio), engine.runAndWait())).start()

# Optimized Speech Recognition
def command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 0.6  # Faster response
        print("Listening...")
        audio = r.listen(source, timeout=5)  # Timeout reduces delay
    
    try:
        content = r.recognize_google(audio, language='en-in')
        print("You Said:", content)
        return content.lower()
    except sr.UnknownValueError:
        print("Could not understand, try again...")
        return ""
    except sr.RequestError:
        print("Speech service down")
        return ""

# Faster Web Search (Avoids Web Delay)
def open_url(url):
    os.system(f"start {url}" if os.name == 'nt' else f"xdg-open {url}")

# Handling Commands Faster
def handle_request(request):
    match request:
        case "wake up":
            speak("Yes boss, how can I assist you?")
        
        case "play music":
            speak("Playing your favorite music.")
            songs = [
                "https://open.spotify.com/track/78BWCd70D1X6LMkDZm1UoF",
                "https://open.spotify.com/track/3yHyiUDJdz02FZ6jfUbsmY",
                "https://open.spotify.com/track/0HqZX76SFLDz2aW8aiqi7G",
                "https://open.spotify.com/track/0pqnGHJpmpxLKifKRmU6WP"
            ]
            open_url(random.choice(songs))
        
        case "increase brightness":
            sbc.set_brightness(min(100, sbc.get_brightness()[0] + 25))
            speak("Increased brightness")

        case "decrease brightness":
            sbc.set_brightness(max(0, sbc.get_brightness()[0] - 25))
            speak("Decreased brightness")
        
        case "take a screenshot":
            speak("Captured screenshot")
            pyautogui.screenshot("screenshot.png")
        
        case "increase volume":
            pyautogui.press("volumeup")
            speak("Increased volume")
        
        case "decrease volume":
            pyautogui.press("volumedown")
            speak("Decreased volume")
        
        case "what's the time":
            speak(f"Current time is {datetime.datetime.now().strftime('%H:%M')}")
        
        case "what's the date":
            speak(f"Today's date is {datetime.datetime.now().strftime('%d %m %Y')}")

        case "detect objects":
            speak("Starting object detection")
            object_detection.start_detection()  

        case "note this work":
            speak("Adding your task")
            with open("todo.txt", "a") as file:
                file.write(request.replace("note this work", "").strip() + "\n")
        
        case "delete task":
            task = request.replace("delete task", "").strip()
            with open("todo.txt", "r+") as file:
                tasks = file.readlines()
                file.seek(0)
                file.writelines([t for t in tasks if t.strip() != task])
                file.truncate()
            speak(f"Deleted task: {task}")

        case "read out the task":
            with open("todo.txt", "r") as file:
                speak("Your tasks are: " + file.read())
        
        case "notify task":
            with open("todo.txt", "r") as file:
                notification.notify(title="Today's task", message=file.read())

        case "open college youtube":
            open_url("https://www.youtube.com/@PaceAutonomous")
            speak("Opening your college YouTube channel")

        case "open youtube":
            open_url("https://www.youtube.com")
            speak("Opening YouTube")
        
        case "open instagram":
            open_url("https://www.instagram.com")
            speak("Opening Instagram")
        
        case "open linkedin":
            open_url("https://www.linkedin.com")
            speak("Opening LinkedIn")

        case "open our college":
            open_url("https://pace.ac.in/")
            speak("Opening PACE college website")
        
        case "open ecap":
            open_url("https://ecap.pace.ac.in/default.aspx")
            speak("Opening PACE ECAP portal")

        case "open amazon":
            open_url("https://www.amazon.in")
            speak("Opening Amazon")
        
        case "open flipkart":
            open_url("https://www.flipkart.in")
            speak("Opening Flipkart")

        case _ if request.startswith("order a"):
            query = request.replace("order a", "").strip()
            speak(f"Ordering {query}")
            pyautogui.typewrite(query)
            pyautogui.press("enter")

        case _ if request.startswith("open "):
            app = request.replace("open", "").strip()
            pyautogui.hotkey("win", "s")
            pyautogui.typewrite(app)
            pyautogui.press("enter")
            speak(f"Opening {app}")

        case _ if request.startswith("close "):
            pyautogui.hotkey("alt", "F4")
            speak("Closing application")

        case _ if "search wikipedia" in request:
            query = request.replace("search wikipedia", "").strip()
            result = wikipedia.summary(query, sentences=2)
            speak(result)

        case _ if "whatsapp" in request:
            pwk.sendwhatmsg("+918885199116", "Hello Pavani Mam", 12, 3, 20)
            speak("Message sent")

        case _ if "search google" in request:
            query = request.replace("search google", "").strip()
            open_url(f"https://www.google.com/search?q={query}")
            speak("Searching Google")

        case _:
            model="wizardlm2"
            prompt=request
            response = client.generate(model=model,prompt=prompt)
            speak(response.text)
# Main loop optimized with threading

def main_process():
    while True:
        request = command()
        if request:
            handle_request(request)
# Start execution
main_process()
