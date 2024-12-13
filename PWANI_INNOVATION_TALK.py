
import cohere
import subprocess as sb
import speech_recognition as sr
import time


# AI Portion
api_key = 'pQjiTygxrqjSEjHHilJicUWiFpXPVv7ZapihqKo7'  
co = cohere.Client(api_key)

preamble = """
This document describes the creation of an AI-powered operating system interface designed to interpret natural language instructions and respond exclusively with Windows OS command-line (cmd) commands. The system leverages Python's os library to execute these commands based on user input.

.if the user also hasnt specified what browser to use, simply use chrome as the default, also add anything else you feel is important on the chat.The core functionality of the AI is to listen to text-based queries from the user, analyze the input, and return only the corresponding cmd commands required to perform the task. This approach ensures that users receive clear and concise command-line instructions, which can then be executed manually or automatically, enabling seamless control over the Windows operating system via conversational language."""

def digest(message):
    return co.chat(message=message, preamble=preamble).text

def execute(command):
    # Split the string based on newlines
    commands = command.split('\n')
    
    for cmd in commands:
        try:
            print(f"Executing: {cmd}")
            sb.run(cmd, shell=True, check=True)
        except sb.CalledProcessError as e:
            print(f"Error executing command: {e}")

def recognize_speech():
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

# Capture speech input
#print("GET READY")
#time.sleep(5)
#print("GOOOG")
message = recognize_speech()

if message:
    x = digest(message)
    execute(x)
