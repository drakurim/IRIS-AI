import pyttsx3

engine = pyttsx3.init()
voices = engine.getProperty("voices")

def sprich(text: str):
    engine.say(text)
    engine.runAndWait()