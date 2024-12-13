import cv2  # For webcam capture
import numpy as np
import pyvista as pv
from pyvista import examples

# Initialize webcam capture
cap = cv2.VideoCapture(0)  # '0' refers to the default webcam

# Load a sample 3D object (airplane mesh)
mesh = examples.load_airplane()

# Initialize the PyVista plotter
plotter = pv.Plotter()

# Add the mesh to the scene
plotter.add_mesh(mesh, color='orange')

# Camera settings
camera_position = (3140., 2919., 2375.)  # Camera position in 3D space
focus_point = mesh.center  # Focus at the center of the mesh
view_up = (0, 0, 1)  # Direction considered "up" in the camera's view

# Set the camera position
plotter.camera_position = (camera_position, focus_point, view_up)

# Ensure the window is interactive and allows updating
plotter.show(interactive_update=True, auto_close=False)

# Capture and set the background
while True:
    ret, frame = cap.read()  # Capture a frame from the webcam
    if not ret:
        print("Failed to capture video frame.")
        break

    # Convert the frame from BGR (OpenCV default) to RGB for PyVista
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Update the background with the captured frame
    plotter.set_background(frame_rgb)

    # Redraw the plotter to reflect the updated background
    plotter.update()

    # Check for a key press to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Clean up
cap.release()
cv2.destroyAllWindows()
plotter.close()  # Close the PyVista plotter
