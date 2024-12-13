import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import PolygonSelector
from matplotlib.path import Path

# Load the image
image = cv2.imread(r"C:\Users\Admin\Pictures\Saved Pictures\download.jpg")
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Function to create a mask from polygon vertices
def create_mask(image_shape, vertices):
    mask = np.zeros(image_shape[:2], dtype=np.uint8)
    polygon = np.array([vertices], dtype=np.int32)
    cv2.fillPoly(mask, polygon, 255)
    return mask

# Initialize a list to hold polygon vertices
polygon_vertices = []

# Callback function for polygon selector
def onselect(verts):
    global polygon_vertices
    polygon_vertices = verts

# Display the image
fig, ax = plt.subplots()
ax.imshow(image)
polygon_selector = PolygonSelector(ax, onselect, useblit=True, lineprops=dict(color='r'))

plt.show()

# After closing the plot, use the selected vertices to create a mask
if polygon_vertices:
    mask = create_mask(image.shape, polygon_vertices)
    segmented_image = cv2.bitwise_and(image, image, mask=mask)

    # Display the segmented image
    plt.imshow(segmented_image)
    plt.show()

    # Save or further process the segmented image
