import tensorflow as tf
import numpy as np
import cv2
from tensorflow.lite.python.interpreter import Interpreter
 
#import pathlib

tflite_model_path = r"C:\Users\Admin\Downloads\ei-ai_esp32-object-detection-tensorflow-lite-int8-quantized-model.lite"
img_path = r"C:\Users\Admin\Downloads\EduScope_08_04_2024__14_15_26.jpg"
interpreter = Interpreter(model_content = open(tflite_model_path , 'rb').read())

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

print(input_details)
print(output_details)

interpreter.allocate_tensors()

def draw_rect(image, box):
    y_min = int(max(1, (box[0] * image.height)))
    x_min = int(max(1, (box[1] * image.width)))
    y_max = int(min(image.height, (box[2] * image.height)))
    x_max = int(min(image.width, (box[3] * image.width)))
    
    # draw a rectangle on the image
    cv2.rectangle(image, (x_min, y_min), (x_max, y_max), (255, 255, 255), 2)

#for file in pathlib.Path('images').iterdir():

#    if file.suffix != '.jpg' and file.suffix != '.png':
#        continue
img_path = r"C:\Users\Admin\Downloads\EduScope_08_04_2024__14_15_26.jpg"
img = cv2.imread(r"C:\Users\Admin\Downloads\EduScope_08_04_2024__14_15_26.jpg")
new_img = cv2.resize(img, (input_details[0]['shape'][1], input_details[0]['shape'][2]))
interpreter.set_tensor(input_details[0]['index'], [new_img.astype(np.int8)])

interpreter.invoke()
rects = interpreter.get_tensor(output_details[0]['index'])
#scores = interpreter.get_tensor(output_details[2]['index'])
    
    #for index, score in enumerate(scores[0]):
     #   if score > 0.5:
draw_rect(new_img,rects[0][index])
          
cv2.imshow("image", new_img)
#    cv2.waitKey(0)
