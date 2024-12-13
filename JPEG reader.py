import serial
import time

ser = serial.Serial('COM11' , 115200)
time.sleep(2)

image_path = r'C:\Users\Admin\Desktop\poop.jpg'

with open(image_path, 'rb') as f:
    image_data= f.read()


ser.write(str(len(image_data)).encode() + b'\n')

ser.write(image_data)
ser.re
echoed_data = ser.read(len(image_data))

new_image = open(r'C:\Users\Admin\Desktop\poop3.jpg' , 'wb')
new_image.write(echoed_data)
