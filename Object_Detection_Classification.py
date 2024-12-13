import cv2
import numpy as np
import tensorflow as tf
from tensorflow.lite.python.interpreter import Interpreter

tflite_model_path = r"C:\Users\Admin\Downloads\ei-ai_esp32-object-detection-tensorflow-lite-int8-quantized-model.lite"
interpreter = Interpreter(model_content = open(tflite_model_path , 'rb').read())

interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
print(output_details)

img_path = r"C:\Users\Admin\Downloads\EduScope_08_04_2024__14_15_26.jpg"
image = cv2.imread(img_path)

input_shape = input_details[0]['shape']
input_height = input_shape[1]
input_width = input_shape[2]
input_data = cv2.resize(image, (input_width, input_height))

input_data = input_data.astype(np.int8)
input_data = np.expand_dims(input_data , axis = 0)


interpreter.set_tensor(input_details[0]['index'], input_data)

interpreter.invoke()
output_tensor = interpreter.get_tensor(output_details[0]['index'])

for y in range(output_tensor.shape[0]):
    for x in range(output_tensor.shape[1]):
        # Assuming the first value is the confidence score and the second is bounding box data
        confidence = output_tensor[y, x, 0]
        if confidence > 0.5:  # Confidence threshold
            # Assuming bounding box data needs to be decoded from int8
            bbox = output_tensor[y, x, 1]  # This part depends on your model specifics
            # Further extraction may be needed depending on model output interpretation

            # This part might require conversion of bounding box data to pixel coordinates
            # Drawing bounding boxes if detected
            # Example drawing code (assuming bounding box data provides relative coordinates):
            start_point = (int(x * image.shape[1]), int(y * image.shape[0]))  # Scale back to image size
            # Add bounding box drawing logic here, depending on interpretation

            # Example: Draw bounding box and confidence
            cv2.rectangle(image, start_point, (start_point[0] + 10, start_point[1] + 10), (0, 255, 0), 2)
            cv2.putText(image, f"Confidence: {confidence:.2f}", (start_point[0], start_point[1] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

# Display or save the result
cv2.imshow("Detected Objects", image)
cv2.waitKey(0)  # Press any key to close the window
cv2.destroyAllWindows()

# To save the output image, use:
# cv2.imwrite("output_image.jpg", image)
