import cv2
import numpy as np
from tensorflow.lite.python.interpreter import Interpreter
import matplotlib.pyplot as plt

# Load the TFLite model
model_path = r"C:\Users\Admin\Downloads\ei-ai_esp32-object-detection-tensorflow-lite-int8-quantized-model.lite"  # Update with your TFLite model path
interpreter = Interpreter(model_content=open(model_path, 'rb').read())
interpreter.allocate_tensors()

# Get input details
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Load an image with OpenCV
image_path = r"C:\Users\Admin\Downloads\EduScope_08_04_2024__14_15_26.jpg"  # Update with your image path
image = cv2.imread(image_path)

# Resize the image to the expected input size
input_shape = input_details[0]['shape']
input_height, input_width = input_shape[1:3]

resized_image = cv2.resize(image, (input_width, input_height))
input_dtype = input_details[0]['dtype']

# Convert to grayscale if needed and prepare the input
input_data = resized_image#cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)
input_data = np.expand_dims(input_data, axis=-1).astype(input_dtype)  # Add channel dimension
input_data = np.expand_dims(input_data, axis=0)  # Add batch dimension

# Set the input tensor
interpreter.set_tensor(input_details[0]['index'], input_data)

# Run inference
interpreter.invoke()

# Get the output tensor
output_data = interpreter.get_tensor(output_details[0]['index'])

# Dequantize the output data based on quantization parameters
scale, zero_point = output_details[0]['quantization']
output_data_dequantized = (output_data - zero_point) * scale

# Define a threshold for object detection
threshold = 0.5

# Create a copy of the resized image to draw on
output_image = resized_image.copy()

# Process the output data and draw on the image
grid_height, grid_width = output_data_dequantized.shape[1:3]

# Iterate over the grid to find objects
for row in range(grid_height):
    for col in range(grid_width):
        # First channel is object presence
        presence_score = output_data_dequantized[0, row, col, 0]
        if presence_score > threshold:
            # Second channel contains localization information
            localization_info = output_data_dequantized[0, row, col, 1]
            
            # Define a basic bounding box or point based on localization
            grid_cell_width = input_width / grid_width
            grid_cell_height = input_height / grid_height
            
            # Calculate the center of the grid cell
            center_x = col * grid_cell_width + (grid_cell_width / 2)
            center_y = row * grid_cell_height + (grid_cell_height / 2)
            
            # Draw a circle at the center
            cv2.circle(output_image, (int(center_x), int(center_y)), 5, (0, 0, 255), -1)

# Display the image with detected objects
plt.imshow(cv2.cvtColor(output_image, cv2.COLOR_BGR2RGB))
plt.axis('off')
plt.show()
