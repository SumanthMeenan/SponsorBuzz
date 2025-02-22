import os
import PIL 
import google.generativeai as genai
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
import re
import time
from typing_extensions import TypedDict
from typing import Literal
from model import model 

# Choose a Gemini model.
from configure import configure_api
configure_api() 
#model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest")

# # Create a prompt to detect bounding boxes.
# prompt = "Return a bounding box for each of the objects in this image in [ymin, xmin, ymax, xmax] format."
# sample_file_2 = PIL.Image.open('data/piranha.jpg')
# response = model.generate_content([sample_file_2, prompt])
# print(response)

import requests

# Function to download video from a URL
def download_video(video_url, filename):
    response = requests.get(video_url, stream=True)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                f.write(chunk)
        print(f"Video downloaded: {filename}")
    else:
        print("Failed to download video")

# Example video URL
video_url = 'https://www.youtube.com/watch?v=C5ZDl4epfbM'
local_video_filename = 'data/tennis_1.mp4'

# Download the video
download_video(video_url, local_video_filename)
print("video downloaded")


video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv']
# Select only videos from the list
files = os.listdir("data/")
video_files = [file for file in files if any(file.lower().endswith(ext) for ext in video_extensions)]

# generate and print response
# response = model.generate_content(["Analyse this video", video_files[0]],
#                                   request_options={"timeout": 600})

print(video_files)
response = model.generate_content(["Analyse this video", "tennis_1.mp4"],
                                  request_options={"timeout": 600})

print(response.text)


import cv2
import google.generativeai as genai
from PIL import Image
import numpy as np

# Initialize Gemini model
model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest")
import cv2
from PIL import Image
from model import model2 

# Initialize model (ensure you are correctly passing the model name or using the right model from the gemini API)

# # Create the prompt.
# prompt = "Summarize this video. Then create a quiz with answer key based on the information in the video."

files = genai.list_files()
for file in files:
    print(f"File ID: {file.name}, Status: {file.state}")

retrieved_file = genai.get_file('files/jp9bezo4gmhw')
print(f"Retrieved File ID: {retrieved_file.name}, Status: {retrieved_file.state.name}")

response2 = model2.generate_content(["Analyse this video", retrieved_file],
                                  request_options={"timeout": 600})
print("response 2: ", response2.text)
# # Make the LLM request.
# print("Making LLM inference request...")
# response = model.generate_content([video_file, prompt],
#                                   request_options={"timeout": 600})

# print(response)


















