import serial
import time

serial_port = 'COM11'
baud_rate = 115200

ser = serial.Serial(serial_port, baud_rate)

image_path = r'C:\Users\Admin\Desktop\poop.jpg'

with open(image_path, 'rb') as img_file:
    image_data = img_file.read()


delimiter_start = b'<<START>>'
delimiter_end = b'<<END>>'

ser.write(delimiter_start)
ser.write(image_data)
ser.write(delimiter_end)

print("Image sent to ESP32")

recv_data = b''
start_time = time.time()
timeout = 10

while True:
    if ser.in_waiting > 0:
        recv_data += ser.read(ser.in_waiting)
    if recv_data.endswith(delimiter_end):
        break
    if time.time() - start_time > timeout:
        print("Timed out waiting for echo")
        break

echoed_image = r'C:\Users\Admin\Desktop\poop3.jpg'
with open(echoed_image , 'wb') as echoed_file:
    echoed_file.write(recv_data.replace(delimiter_start, b'').replace(delimiter_end, b''))
ser.close()
