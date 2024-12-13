import cohere
import subprocess as sb


api_key = 'pQjiTygxrqjSEjHHilJicUWiFpXPVv7ZapihqKo7'  # AI PORTION

co = cohere.Client(api_key)

preamble = """
This document describes the creation of an AI-powered operating system interface designed to interpret natural language instructions and respond exclusively with Windows OS command-line (cmd) commands. The system leverages Python's os library to execute these commands based on user input.

The core functionality of the AI is to listen to text-based queries from the user, analyze the input, and return only the corresponding cmd commands required to perform the task. This approach ensures that users receive clear and concise command-line instructions, which can then be executed manually or automatically, enabling seamless control over the Windows operating system via conversational language."""

def digest(message):
    return co.chat(message = message , preamble = preamble).text


def execute(command):
     # Split the string based on newlines
    commands = command.split('\n')
    
    for command in commands:
        try:
            print(f"Executing: {command}")
            sb.run(command, shell=True, check=True)
        except sb.CalledProcessError as e:
            print(f"Error executing command: {e}")


message = "save this info in an excell sheeet , name : paul , sex : male, then open it"
x = digest(message)
execute(x)
