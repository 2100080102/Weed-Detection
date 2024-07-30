import os
import shutil
import random

data_dir = "D:\\Users\\acer\\PycharmProjects\\WeedDetection\\deep_weeds\\3.0.0\\deep_weeds_dataset\\images"
train_dir = os.path.join(data_dir, 'train')
validation_dir = os.path.join(data_dir, 'validation')
test_dir = os.path.join(data_dir, 'test')

# Create directories if they don't exist
os.makedirs(train_dir, exist_ok=True)
os.makedirs(validation_dir, exist_ok=True)
os.makedirs(test_dir, exist_ok=True)

# Define split ratios
train_ratio = 0.8
validation_ratio = 0.1
test_ratio = 1 - train_ratio - validation_ratio

# List all files in the main directory
all_files = os.listdir(data_dir)
image_files = [file for file in all_files if file.endswith('.jpg')]  # Adjust file extension as needed

# Shuffle the list of files
random.shuffle(image_files)

# Split the dataset
num_images = len(image_files)
train_split = int(train_ratio * num_images)
validation_split = int((train_ratio + validation_ratio) * num_images)

# Move images to respective directories
for i, file in enumerate(image_files):
    if i < train_split:
        shutil.move(os.path.join(data_dir, file), os.path.join(train_dir, file))
    elif i < validation_split:
        shutil.move(os.path.join(data_dir, file), os.path.join(validation_dir, file))
    else:
        shutil.move(os.path.join(data_dir, file), os.path.join(test_dir, file))
