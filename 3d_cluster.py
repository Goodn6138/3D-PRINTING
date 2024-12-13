import numpy as np
import cv2
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import pydicom
import os

# Load the DICOM file or directory containing multiple DICOM slices
dicom_dir = r"C:\Users\Admin\Downloads\OneDrive_1_21-04-2024\Circle of Willis"

# Read all DICOM files in the directory
slices = []
for filename in os.listdir(dicom_dir):
    if filename.endswith('.dcm'):
        dicom_path = os.path.join(dicom_dir, filename)
        dicom = pydicom.dcmread(dicom_path)
        slices.append(dicom.pixel_array)

# Convert the list of slices into a 3D numpy array
volume = np.stack(slices, axis=0)

# Normalize the image to the range 0-255
volume = cv2.normalize(volume, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

# If the volume is grayscale, convert each slice to RGB
if volume.ndim == 3:
    volume_rgb = np.stack([cv2.cvtColor(slice, cv2.COLOR_GRAY2RGB) for slice in volume], axis=0)
else:
    volume_rgb = volume

# Reshape the 3D volume to a 2D array of pixels
pixels = volume_rgb.reshape(-1, 3)

# K-means clustering
n_clusters = 3  # number of segments
kmeans = KMeans(n_clusters=n_clusters, random_state=42)
labels = kmeans.fit_predict(pixels)

# Reshape the labels back to the original 3D volume shape
segmented_volume = labels.reshape(volume_rgb.shape[:3])

# Plotting one of the original slices and the corresponding segmented slice
slice_idx = volume_rgb.shape[0] // 2  # choose the middle slice for visualization
original_slice = volume_rgb[slice_idx]
segmented_slice = segmented_volume[slice_idx]

fig, ax = plt.subplots(1, 2, figsize=(12, 6))
ax[0].imshow(original_slice, cmap='gray')
ax[0].set_title('Original Slice')
ax[1].imshow(segmented_slice, cmap='viridis')
ax[1].set_title('Segmented Slice')
plt.show()
