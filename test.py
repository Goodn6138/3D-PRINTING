import cv2
import serial


path = r"C:\Users\Admin\Downloads\WhatsApp Image 2024-03-14 at 14.50.26.jpeg"
cam = cv2.VideoCapture(path)

_, img = cam.read()

ret, img_buffer = cv2.imencode('.jpg' , img)

data_size = len(img_buffer)

print(data_size)

width, height , _= img.shape
img_bytes = img_buffer.tobytes()


ser = serial.Serial('COM11' , 115200)
ser.write(1)
ser.write(str(height).encode())
ser.write(b',')
ser.write(str(width).encode())
ser.write(b',')
ser.write(str(data_size).encode())
ser.write(b',')
ser.write(img_bytes)
while True:
    print(ser.read(10))

