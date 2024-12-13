import cv2
import numpy as np
import tensorflow as tf
from tensorflow.lite.interpreter import Interpreter

tflite_model_path = r"C:\Users\Admin\Downloads\model10.tflite"
interpreter = Interpreter(model_content = open(tflite_model_path, 'rb').read())
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

input_shape = input_details[0]['shape']
input_height, input_width, _ = input_shape[1:]

cap = cv2.VideoCapture(0)

while True:
    _ , frame = cap.read()
    if not ret:
        break
    resized_frame = cv2.resize(frame, (input_width , input_height))
    input_data = np.expand_dims(resized_frame.astype(np.float32),axis=0)

    input_data = input_data/255

    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()

    output_data = interpreter.get_tensor(output_details[0]['index'])
    predicted_class = np.argmax(output_data)

    cv2.putText(frame, f'Predicted Class: {preddited_class}' , (10,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2)
    cv2.imshow("POOP" , frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
