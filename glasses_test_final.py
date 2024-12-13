import cv2
import pytesseract
import requests
import datetime
import pyttsx3  # Speech synthesis (text-to-speech)
import threading as thread
import speech_recognition as sr
import cohere

# Initialize Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# ESP32CAM URL
URL = "http://192.168.1.13"  # Replace with your ESP32CAM URL
AWB = True

# Initialize camera stream
cap = cv2.VideoCapture(URL + ":81/stream")

# Initialize speech recognition and synthesis
rec = sr.Recognizer()  # Microphone listener
engine = pyttsx3.init()  # Text-to-speech engine

# Initialize AI (Cohere)
api_key = 'pQjiTygxrqjSEjHHilJicUWiFpXPVv7ZapihqKo7'
ai = cohere.Client(api_key)
conversation_hist = []

def generate_response(prompt):
    response = ai.generate(prompt=prompt, max_tokens=200)
    return response.generations[0].text.strip()

def update_conversation_hist(user_input, model_response):
    conversation_hist.append(f'User: {user_input}')
    conversation_hist.append(f'Model: {model_response}')

# Function to set resolution for ESP32CAM
def set_resolution(url: str, index: int = 1, verbose: bool = False):
    try:
        if verbose:
            resolutions = """
            10: UXGA(1600x1200)\n9: SXGA(1280x1024)\n8: XGA(1024x768)\n7: SVGA(800x600)
            6: VGA(640x480)\n5: CIF(400x296)\n4: QVGA(320x240)\n3: HQVGA(240x176)\n0: QQVGA(160x120)
            """
            print("Available resolutions\n{}".format(resolutions))

        if index in [10, 9, 8, 7, 6, 5, 4, 3, 0]:
            requests.get(url + "/control?var=framesize&val={}".format(index))
        else:
            print("Wrong index")
    except Exception as e:
        print(f"SET_RESOLUTION: Something went wrong - {e}")

# Function to set quality for ESP32CAM
def set_quality(url: str, value: int = 1, verbose: bool = False):
    try:
        if 10 <= value <= 63:
            requests.get(url + "/control?var=quality&val={}".format(value))
        else:
            print("Invalid quality value")
    except Exception as e:
        print(f"SET_QUALITY: Something went wrong - {e}")

# Function to toggle AWB
def set_awb(url: str, awb: int = 1):
    try:
        awb = not awb
        requests.get(url + "/control?var=awb&val={}".format(1 if awb else 0))
    except Exception as e:
        print(f"SET_AWB: Something went wrong - {e}")
    return awb

# Extract text from image using pytesseract
def extract_text_from_image(frame):
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray_frame)
    return text

# Save the current frame
def save_frame(frame):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"captured_frame_{timestamp}.png"
    cv2.imwrite(filename, frame)
    print(f"Frame saved as {filename}")

# OCR and speech recognition thread
def OCR():
    print("........RUNNING OCR ALGORITHM..............")
    last_str = ''
    while True:
        if cap.isOpened():
            ret, img = cap.read()
            if not ret:
                print("Failed to grab frame")
                break

            text = extract_text_from_image(img)

            if text and last_str != text:
                print(f"Extracted Text: {text}")

                with sr.Microphone() as source:
                    audio = rec.listen(source)
                try:
                    commands = rec.recognize_google(audio)
                    print(f"USER: {commands}")
                except Exception as e:
                    print(f"Error recognizing speech: {e}")
                    continue

                prompt = text + '\n' + commands
                full_prompt = '\n'.join(conversation_hist) + f'\nUser: {prompt}\nModel:'
                model_response = generate_response(full_prompt)
                print(f"Model: {model_response}")

                update_conversation_hist(commands, model_response)
                engine.say(model_response)
                engine.runAndWait()
                last_str = text

            k = cv2.waitKey(10) & 0xff
            if k == 27:  # Press 'Esc' to exit
                break

    cam.release()
    cv2.destroyAllWindows()

# Frame display thread
def show():
    while True:
        if cap.isOpened():
            ret, frame = cap.read()
            if ret:
                # Display the camera feed
                cv2.imshow("Camera Feed", frame)

                key = cv2.waitKey(1)

                if key == ord('r'):
                    idx = int(input("Select resolution index: "))
                    set_resolution(URL, index=idx, verbose=True)

                elif key == ord('q'):
                    val = int(input("Set quality (10 - 63): "))
                    set_quality(URL, value=val)

                elif key == ord('a'):
                    global AWB
                    AWB = set_awb(URL, AWB)

                elif key == ord('s'):
                    # Save the current frame
                    save_frame(frame)

                elif key == 27:  # Press 'Esc' to exit
                    break

    cv2.destroyAllWindows()
    cap.release()

# Run threads for showing camera feed and OCR
thread1 = thread.Thread(target=show)
thread2 = thread.Thread(target=OCR)
thread1.start()
thread2.start()
