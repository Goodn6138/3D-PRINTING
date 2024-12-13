import cohere
import speech_recognition as sr
import time

api_key = 'pQjiTygxrqjSEjHHilJicUWiFpXPVv7ZapihqKo7'  
co = cohere.Client(api_key)

preamble = """
This innovative tool transforms the way we interact with written documents by enabling real-time, conversational access to PDFs. By utilizing AI and voice recognition, users can call and converse with their PDFs, asking questions in natural speech as if they were having a phone conversation. The system listens, processes queries, and responds with accurate, context-aware answers derived directly from the content of the document. This breakthrough offers a hands-free, intuitive approach to extracting information from complex texts, making research and document review faster and more interactive.
"""


def speech_rec():
    # Initialize the recognizer
    recognizer = sr.Recognizer()
    
    # Use the microphone as the source
    with sr.Microphone() as source:
        print("Please speak your command:")
        # Adjust for ambient noise and record audio
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        
    try:
        # Recognize speech using Google Web Speech API
        command = recognizer.recognize_google(audio)
        print(f"You said: {command}")
        return command
    except sr.UnknownValueError:
        print("Sorry, I could not understand the audio.")
        return None
    except sr.RequestError:
        print("Could not request results from the speech recognition service.")
        return None

