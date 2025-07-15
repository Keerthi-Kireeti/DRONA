import tkinter as tk
from tkinter import Label, Button
from PIL import Image, ImageTk, ImageSequence
import threading
import speech_recognition as sr
import pyttsx3
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
        status_label.config(text="Listening...")
        root.update()
        try:
            audio = r.listen(source, timeout=5)
            text = r.recognize_google(audio, language='en-in')
            status_label.config(text=f"You said: {text}")
            handle_request(text)
        except sr.UnknownValueError:
            status_label.config(text="Sorry, I couldn't understand.")
        except sr.RequestError:
            status_label.config(text="Could not request results.")

def handle_request(request):
    match request:
        case "wake up":
            speak("Yes boss, how can I assist you?")                  
        case "play music":
            speak("yes sir, Playing your favorite music from Spotify")
            songs = [
                "https://open.spotify.com/track/78BWCd70D1X6LMkDZm1UoF?si=d9057420c43e4afb",
                "https://open.spotify.com/track/3yHyiUDJdz02FZ6jfUbsmY?si=59cd98813cb34ec3",
                "https://open.spotify.com/track/5bQ6oDLqvw8tywmnSmwEyL?si=7ed728bcb1df4ed3"
            ]
            webbrowser.open(random.choice(songs))
        case _:
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=[request])
            speak(response.text)

def start_listening():
    threading.Thread(target=command, daemon=True).start()

def update_gif(frame=0):
    frame = frame % len(frames)
    gif_label.config(image=frames[frame])
    root.after(50, update_gif, frame + 1)

# Create the main window
root = tk.Tk()
root.title("Voice Assistant")
root.attributes('-fullscreen', True)  # Make it full screen
root.configure(bg="black")

# Load and resize the GIF
gif_path = "mic.gif"  # Ensure this GIF is in the same directory
image = Image.open(gif_path)
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
image = image.resize((screen_width, screen_height), Image.Resampling.LANCZOS)
frames = [ImageTk.PhotoImage(img) for img in ImageSequence.Iterator(image)]

# GIF Label
gif_label = Label(root, bg="black")
gif_label.place(x=0, y=0, width=screen_width, height=screen_height)

# Status Label
status_label = Label(root, text="Click to Start Listening", fg="white", bg="black", font=("Arial", 16))
status_label.pack(pady=20)

# Button Styling
button = Button(root, text="Start Listening", command=start_listening, font=("Arial", 16, "bold"), fg="black", bg="white", padx=20, pady=10, border=5)
button.pack()

update_gif()
root.mainloop()
