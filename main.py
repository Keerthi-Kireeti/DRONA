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

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  
engine.setProperty('rate', 175)


def speak(audio):
    audio = mtranslate.translate(audio, to_language="en" , from_language="en-in")
    print(audio)
    engine.say(audio)
    engine.runAndWait()
    
def command():
    content= " "
    while content == " ":
        # obtain audio from the microphone
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Say something!")
            audio = r.listen(source)    
        try:
            content =  r.recognize_google(audio,language='en-in')
            #content = mtranslate.translate(content, to_language="hi")
            print("You Said..........." + content)
        except Exception as e:
            print("Please try again...")
        
    return content

def main_process():
    while True:
        request = command()
        if "wake up " in request:
           speak("yess boss  , how can i assist you")
        elif "play music" in request:
            speak("Playing your favorite music from spotify")
            song = random.randint(1,3)
            if song == 1 :
                webbrowser.open("https://open.spotify.com/track/78BWCd70D1X6LMkDZm1UoF?si=d9057420c43e4afb")
            elif song == 2 :
                webbrowser.open("https://open.spotify.com/track/3yHyiUDJdz02FZ6jfUbsmY?si=59cd98813cb34ec3")
            elif song == 3 :
                webbrowser.open("https://open.spotify.com/track/5bQ6oDLqvw8tywmnSmwEyL?si=7ed728bcb1df4ed3")
        elif "play your music" in request:
            speak("playing my song")
            webbrowser.open("https://open.spotify.com/track/7ALFR7mKgmkRNRP8uq9vnN?si=9786a8856a634fbb")            
        elif "increase volume" in request:
                    speak("Increasing volume")
                    pyautogui.press("volumeup")
        elif "decrease volume" in request:
                    speak("Decreasing volume")
                    pyautogui.press("volumedown")
        elif "what's the time" in request:
                now_time = datetime.datetime.now().strftime("%H %M")
                speak("current time is"+ str(now_time))    
        elif "what's the date" in request:
                now_time = datetime.datetime.now().strftime("%d %m %Y")
                speak("today it's"+ str(now_time))         
        elif "new task" in request:
            task = request.replace("new task","")
            task=task.strip() 
            if task != "":
                speak("Adding task :"+ task)
                with open ("todo.txt","a") as file:
                    file.write(task + "\n")  
        #deletion of tasks             
        elif "delete task" in request:
            task = request.replace("delete task", "").strip()
            if task != "":
                with open("todo.txt", "r") as file:
                    tasks = file.readlines()
                
                with open("todo.txt", "w") as file:
                    found = False
                    for line in tasks:
                        if line.strip() != task:
                            file.write(line)
                        else:
                            found = True
                    
                if found:
                    speak("Deleted task: " + task)
                else:
                    speak("Task not found: " + task)
                   
        elif "read out the task" in request:
            with open ("todo.txt","r") as file:
                speak("The list goes by :"+ file.read())  
        elif "notify task" in request:
            with open ("todo.txt","r") as file:
                tasks = file.read()              
            notification.notify(
                title = "Today's task", 
                message = tasks
            ) 
        elif "open YouTube" in request:
            webbrowser.open("www.youtube.com")
            speak("opening youtube")
               
        elif "open Instagram" in request:
            webbrowser.open("www.instagram.com")
            speak("opening instagram")            
        
        elif "open Snapchat" in request:
            webbrowser.open("www.snapchat.com")
            speak("opening snapchat")
                
        elif "open LinkediIn" in request:
            webbrowser.open("www.linkedin.com")
            speak("opening LinkedIn")
        
        elif "open our college" in request:
            webbrowser.open("https://pace.ac.in/")
            speak("opening official web page of PACE institue of technology and sciences")
        elif "open ecap" in request:
            webbrowser.open("https://ecap.pace.ac.in/default.aspx")
            speak("opening pace ecap portal")    
                    
        elif "open" in request:
            query = request.replace("open", "")
            pyautogui.press("super")
            pyautogui.typewrite(query)
            pyautogui.sleep(2)
            pyautogui.press("enter")
            speak("opening"+query)
        elif "close" in request:
            pyautogui.hotkey('alt', 'F4')
            speak("closing")     
               
        elif "wikipedia" in request:
            request = request.replace("Drona ", "")
            request = request.replace("search wikipedia ", "")
            result = wikipedia.summary(request, sentences=2) 
            speak(result)
        
        elif "search Google" in request:
            request = request.replace("Drona ", "")
            request = request.replace("search Google ", "")
            webbrowser.open("https://www.google.com/search?q="+request) 
            speak("Opening google")
            
        elif "WhatsApp" in request:
            pwk.sendwhatmsg("+917036740869", "Hi", 9, 57, 15)
            speak("Message sent")
            
        '''elif "send a mail" in request:
            pwk.send_mail("23kq1a05g9@pace.ac.in",user_config.gmail_password,"Hello", "Hi how are you","23kq1a05g6@pace.ac.in")
            speak("mail sent")'''
            
            
main_process()
       