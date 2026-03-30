import speech_recognition as sr
import webbrowser
import pyttsx3

engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

r = sr.Recognizer()

with sr.Microphone() as source:
    print("Say something...")
    audio = r.listen(source)

try:
    command = r.recognize_google(audio).lower()
    print("You said:", command)

    if "open youtube" in command:
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")

    elif "open google" in command:
        speak("Opening Google")
        webbrowser.open("https://www.google.com")

    else:
        speak("I don't understand")

except:
    print("Could not understand audio")