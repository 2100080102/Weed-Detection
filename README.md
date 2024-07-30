# Weed-Detection
This project focuses on detecting weeds using a deep learning model implemented with TensorFlow. The project includes various components for data preprocessing, model training, and a web interface for users to upload images and receive predictions.

## Table of Contents
- [Project Overview](#project-overview)
- [Dataset](#dataset)
- [About Folders](#about-folders)
- [Usage](#usage)

# **Project Overview**

The goal of this project is to create a weed detection system that can identify different types of weeds in images. The project leverages the DeepWeeds dataset, which can be downloaded from the TensorFlow Datasets catalog. The system provides a web interface for users to upload images and get predictions on whether the uploaded images contain weeds.

# **Dataset**
The dataset used in this project is the DeepWeeds dataset. For demonstration purposes, only 20 images from each of the train, test, and validation sets are included in this repository. The full dataset can be imported from the [TensorFlow Datasets catalog](https://www.tensorflow.org/datasets/catalog/deep_weeds) or you can visit [AlexOlsen](https://github.com/AlexOlsen/DeepWeeds?tab=readme-ov-file)

## **About Folders**

`dataset/`: Contains a sample of 20 images each from the train, test, and validation sets.

`images/`: Contains the images uploaded by the user.

`preprocessing/`: Contains preprocessing scripts.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;•`preprocessing.py`: Script for preprocessing the dataset.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;•`splitting.py`: Script for splitting the dataset into train, test, and validation sets.

`templates/`: Contains HTML files for the web interface.

`app.py`: The main Flask application file that runs the web server.

`generate_secret_key.py`: Script to generate a secret key for Flask sessions.

`main.py`: Script for training and evaluating the model.

## **Usage**
That's it you're just away of 3 steps now all you need to is

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **Step 1:** Sign up for an account to get started.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **Step 2:** Upload images of your crops and fields through our user-friendly interface.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **Step 3:** Our advanced AI algorithms will analyze the images and identify any weeds present.


## **Note**
This project cannot be cloned directly and run successfully due to the dataset dependency. Even if the project is downloaded and imported, it will not run properly without the complete DeepWeeds dataset. The project will function correctly only if the dataset is fully set up and available in the `dataset/` directory.
