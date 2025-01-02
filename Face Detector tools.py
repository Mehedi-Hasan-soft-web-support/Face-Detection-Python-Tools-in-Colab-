from google.colab import files
from zipfile import ZipFile
import os
import cv2
import numpy as np
from mtcnn.mtcnn import MTCNN
from PIL import Image

# Ensure an output directory
output_dir = "cropped_faces"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Upload files
uploaded = files.upload()

# Initialize the MTCNN detector
detector = MTCNN()

def crop_faces(image_path, output_dir):
    """Detect and crop faces from an image."""
    img = cv2.imread(image_path)
    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    detections = detector.detect_faces(rgb_img)
    face_count = 0

    for i, detection in enumerate(detections):
        x, y, width, height = detection['box']
        # Ensure positive coordinates
        x, y = max(0, x), max(0, y)
        cropped_face = rgb_img[y:y+height, x:x+width]

        # Save the cropped face in original resolution
        face_path = os.path.join(output_dir, f"{os.path.basename(image_path)}_face_{i+1}.jpg")
        Image.fromarray(cropped_face).save(face_path, "JPEG", quality=95)  # Save with high quality
        face_count += 1

    return face_count

# Process all uploaded images
for filename in uploaded.keys():
    crop_faces(filename, output_dir)

# Zip the cropped faces
zip_filename = "cropped_faces.zip"
with ZipFile(zip_filename, 'w') as zipf:
    for root, dirs, files in os.walk(output_dir):
        for file in files:
            zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), output_dir))

# Provide the ZIP file for download
from google.colab import files
files.download(zip_filename)


#  Ekhon sob data ami kheye felbo ,,,,,,,,,, Hahahahahahahahhahahahaah
#  Ekhon sob data ami kheye felbo ,,,,,,,,,, Hahahahahahahahhahahahaah
#  Ekhon sob data ami kheye felbo ,,,,,,,,,, Hahahahahahahahhahahahaah


import shutil
import os

folder_path = "/content/cropped_faces"

try:
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
except FileNotFoundError:
    print("Folder not found.")
