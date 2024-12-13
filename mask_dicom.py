import numpy as np
import pydicom
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

# Load DICOM data
dicom_data = pydicom.dcmread(r"C:\Users\Admin\Downloads\OneDrive_1_21-04-2024\Circle of Willis\1-047.dcm")#\1-049.dcm")
voxel_data = dicom_data.pixel_array

# Downsample the voxel data if necessary
# Perform clustering on the voxel data
n_clusters = 3  # Number of clusters (e.g., tissue types)
kmeans = KMeans(n_clusters=n_clusters, random_state=42)
voxel_flat = voxel_data.reshape(-1, 1)
labels = kmeans.fit_predict(voxel_flat)

# Select the cluster to keep (e.g., cluster 1)
cluster_to_keep = 2

# Create a mask for the selected cluster
mask = (labels == cluster_to_keep).reshape(voxel_data.shape)

# Apply the mask to the voxel data
segmented_voxel_data = np.zeros_like(voxel_data)
segmented_voxel_data[mask] = voxel_data[mask]

# Plotting the original voxel data and the segmented voxel data
fig, ax = plt.subplots(1, 2, figsize=(12, 6))
ax[0].imshow(voxel_data, cmap='gray')
ax[0].set_title('Original Voxel Data')
ax[1].imshow(segmented_voxel_data, cmap='gray')
ax[1].set_title('Segmented Voxel Data (Cluster {})'.format(cluster_to_keep))
plt.show()
