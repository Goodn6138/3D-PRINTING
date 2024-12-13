import serial
import cv2
import numpy as np
import threading

# Initialize serial port
#ser = serial.Serial('COM11', 115200)

# Function to handle receiving data from Arduino
def receive_data():
    while True:
        success_message = ser.read(10)
        print(success_message)
'''        if success_message == image_buffer.tobytes()[0:10]:
            print("Transfer successful")
        else:
            print("Transfer failed")
            print(success_message)
'''

# Create and start the receive thread
receive_thread = threading.Thread(target=receive_data)
receive_thread.daemon = True
#receive_thread.start()

# Capture video from webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error")
        break

    # Convert frame to grayscale
    BW_Frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Encode frame as JPEG
    ret, image_buffer = cv2.imencode('.jpg', BW_Frame)
    if not ret:
        print("Error encoding frame")
        continue

    # Get image data size
    data_size = len(image_buffer)
    print(f"Data Size {data_size} bytes")

    # Display frame
    cv2.imshow("TEST", BW_Frame)

    # Send image data to Arduino
#    ser.write(str(BW_Frame.shape[0]).encode())
#    ser.write(b',')
#    ser.write(str(BW_Frame.shape[1]).encode())
#    ser.write(b',')
#    ser.write(str(data_size).encode())
#    ser.write(b',')
#    ser.write(image_buffer.tobytes())
#    print(image_buffer.tobytes()[0:10])

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release video capture and close windows
cap.release()
cv2.destroyAllWindows()
