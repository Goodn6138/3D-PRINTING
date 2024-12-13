import cv2
import numpy as np

# Load the image
image = cv2.imread(r"C:\Users\Admin\Desktop\images\POOP\2024-01-27-215133_1920x1080_scrot.png")

# Convert the image to the HSV color space for easier color segmentation
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Define the lower and upper bounds of the color to remove (example for a green background)
# These bounds might need adjustment depending on the image
lower_bound = np.array([35, 100, 100])  # Example: light green
upper_bound = np.array([85, 255, 255])  # Example: dark green

# Create a mask with the specified color range
mask = cv2.inRange(hsv, lower_bound, upper_bound)

# Invert the mask to segment out the background
background_mask = cv2.bitwise_not(mask)

# Extract the foreground by applying the mask to the original image
foreground = cv2.bitwise_and(image, image, mask=background_mask)

# Create a white background (you can change this to another color or image)
background = np.full_like(image, 255)  # White background

# Place the extracted foreground onto the new background
final_image = cv2.add(foreground, cv2.bitwise_and(background, background, mask=mask))

# Save or display the result
cv2.imwrite('image_no_background.jpg', final_image)

# To display the image in a window (optional, for testing)
cv2.imshow('No Background', final_image)
cv2.waitKey(0)  # Wait for a key press to close the window
cv2.destroyAllWindows()
