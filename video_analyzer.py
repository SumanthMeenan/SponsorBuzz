import os
import google.generativeai as genai
from model import model, model2

# Choose a Gemini model.
from configure import configure_api
configure_api() 

video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv']
# Select only videos from the list
files = os.listdir("data/")
video_files = [file for file in files if any(file.lower().endswith(ext) for ext in video_extensions)]

# generate and print response
print(video_files[0])
response = model.generate_content(["Analyse this video", video_files[0]],
                                  request_options={"timeout": 600})

print(response.text)

files = genai.list_files()
for file in files:
    print(f"File ID: {file.name}, Status: {file.state}")

retrieved_file = genai.get_file('files/jp9bezo4gmhw')
print(f"Retrieved File ID: {retrieved_file.name}, Status: {retrieved_file.state.name}")

response2 = model2.generate_content(["Analyse this video", retrieved_file],
                                  request_options={"timeout": 600})
print("response 2: ", response2.text)



















