import os
import pydicom
import matplotlib.pyplot as plt
import keyboard  # Install this library using: pip install keyboard

# Directory containing DICOM files
dicom_dir = r"C:\Users\Admin\Downloads\OneDrive_1_21-04-2024\Circle of Willis"

# Get list of DICOM files
dicom_files = [os.path.join(dicom_dir, f) for f in os.listdir(dicom_dir) if f.endswith('.dcm')]
dicom_files.sort()  # Sort files alphabetically

current_index = 0

# Function to display DICOM image
def display_dicom(dicom_file):
    dicom_data = pydicom.dcmread(dicom_file)
    image = dicom_data.pixel_array
    plt.imshow(image, cmap='gray')
    plt.title(dicom_file)
    plt.show()

def on_up_arrow():
    global current_index
    if current_index > 0:
        current_index -= 1
        display_dicom(dicom_files[current_index])

def on_down_arrow():
    global current_index
    if current_index < len(dicom_files) - 1:
        current_index += 1
        display_dicom(dicom_files[current_index])

# Register event handlers for up and down arrow keys
keyboard.on_press_key('up', lambda _: on_up_arrow())
keyboard.on_press_key('down', lambda _: on_down_arrow())

# Display the first DICOM image
display_dicom(dicom_files[current_index])

# Wait for key events
keyboard.wait('esc')
