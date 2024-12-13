import speech_recognition as sr

rec = sr.Recognizer()

with sr.Microphone() as source:
    print("SAY: ")
    audio = rec.listen(source)

try:
    text = rec.recognize_google(audio)
    print("SAID: " + text)
except Exception as e:
    print(e)
    
