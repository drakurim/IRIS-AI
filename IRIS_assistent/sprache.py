import speech_recognition as sr
from sprecher import sprich

def sprache_erkennen():
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as quelle:
            print("Ich höre...")
            recognizer.adjust_for_ambient_noise(quelle, duration=1)
            try:
                audio = recognizer.listen(quelle, timeout=5, phrase_time_limit=5)
                text = recognizer.recognize_google(audio, language="de-DE")
                print("Du hast gesagt:", text)
                return text
            except sr.UnknownValueError:
                sprich("Oh, ein weiteres Meisterwerk des Murmelns. Nicht verstanden.")
            except sr.WaitTimeoutError:
                sprich("Timeout. Überraschung: Du hast nichts gesagt.")
            except sr.RequestError:
                sprich("Google hat genug von dir. Anfrage fehlgeschlagen.")
    except OSError:
        sprich("Natürlich gibt es kein Mikrofon. Wozu reden, wenn du sowieso nicht zuhörst?")
        eingabe = input("Iris sagt: Na gut. Tipper es halt: ")
        return eingabe.strip()
    return ""