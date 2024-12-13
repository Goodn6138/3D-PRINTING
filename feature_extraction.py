import zipfile
import os
import pandas as pd
from pathlib import Path
from skimage import io, color
import matplotlib.pyplot as plt
import cv2

# Unzipping the file
zip_file_path = r"C:\Users\Admin\Downloads\lacuna-malaria-detection-challenge20240829-19463-1cpojqt.zip"  # Replace with the path to your zip file
extract_path = r"C:\Users\Admin\Downloads\lacuna"  # Replace with the folder path where you want to extract

# Unzip the folder
if not os.path.exists(extract_path):
    os.makedirs(extract_path)

with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
    zip_ref.extractall(extract_path)

print(f"Files extracted to {extract_path}")

# Set up paths for CSV and images
DATA_DIR = Path(extract_path)  # The folder where the zip content is extracted
IMAGE_DIR = Path(r"C:\Users\Admin\Downloads\image_threshold")#DATA_DIR / 'images/threshold'  # Path to images directory

# Load train, test, and sample submission files
train = pd.read_csv(DATA_DIR / 'Train.csv')
test = pd.read_csv(DATA_DIR / 'Test.csv')
ss = pd.read_csv(DATA_DIR / 'SampleSubmission.csv')

# Add absolute image path columns
train['image_path'] = [IMAGE_DIR / x for x in train.Image_ID]
test['image_path'] = [IMAGE_DIR / x for x in test.Image_ID]

# Map string classes to integer labels (label encoding targets)
train['class_id'] = train['class'].map({'Trophozoite': 0, 'WBC': 1, 'NEG': 2})

# Path for saving thresholded images
threshold_image_path = DATA_DIR/'thresholded_images'
if not threshold_image_path.exists():
    threshold_image_path.mkdir()

# Loop through all images in the train dataset and process each one
for idx, image_path in enumerate(train['image_path']):
    if image_path.exists():  # Check if the image exists before processing
        try:
            # Load the image
            image = io.imread(image_path)

            # Convert the image to grayscale
            gray_image = color.rgb2gray(image)

            # Apply the threshold filter
            threshold_image = gray_image > 0.5

            # Save the thresholded image
            io.imsave(threshold_image_path / f'thresholded_{idx+1}.png', threshold_image)

        except Exception as e:
            print(f"Error processing image {image_path}: {e}")
            
    else:
        print(f"Image not found: {image_path}")
        break
