import serial
import cv2
import numpy as np

ser = serial.Serial('COM11' ,115200 )
cap = cv2.VideoCapture(0)
x1 = open(r'C:\Users\Admin\Desktop\poop.jpg' ,'wb')
x2 = open(r'C:\Users\Admin\Desktop\poop2.jpg', 'wb')

#while True:
for i in range (1):
    ret, frame = cap.read()
    if not ret:
        print ("Error")
        break

    BW_Frame = cv2.cvtColor(frame,  cv2.COLOR_BGR2GRAY)
    ret , image_buffer = cv2.imencode('.jpg' , BW_Frame)
    if not ret:
        print("Error encoding frame")
        continue
    data_size = len(image_buffer)
    print(f"Data Size {data_size} bytes")
    cv2.imshow("TEST" , BW_Frame) 
    # Send image data to Arduino
    ser.write(str(BW_Frame.shape[0]).encode())
    ser.write(b',')
    ser.write(str(BW_Frame.shape[1]).encode())
    ser.write(b',')
    ser.write(str(data_size).encode())
   # print(ser.read(10))
    ser.write(b',')
    ser.write(image_buffer.tobytes())
   # print(image_buffer.tobytes()[0:data_size])
    x1.write(image_buffer.tobytes()[0:data_size])
    # Wait for success message from Arduino
    success_message = ser.read(60000) #ser.readline().strip().decode()
    x2.write(success_message)
    if success_message == image_buffer.tobytes()[0:data_size]:
        print("Transfer successful")
    else:
        print("Transfer failed")
        print(success_message)

    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    

cap.release()
cv2.destroyAllWindows()

