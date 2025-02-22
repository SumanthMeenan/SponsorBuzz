import os
import PIL 
import google.generativeai as genai
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
import re
import time
from typing_extensions import TypedDict
from typing import Literal

# Choose a Gemini model.
from configure import configure_api
configure_api() 
#model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest")

# # Create a prompt to detect bounding boxes.
# prompt = "Return a bounding box for each of the objects in this image in [ymin, xmin, ymax, xmax] format."
# sample_file_2 = PIL.Image.open('data/piranha.jpg')
# response = model.generate_content([sample_file_2, prompt])
# print(response)

# define JSON structure for model output
class AdDisplayInfo(TypedDict):
    brand_name: str
    total_sec_displayed: int
    ad_type: Literal["on-site", "player", "broadcast", "other"]
    industry: Literal[
        "financial services",
        "manufacturing",
        "healthcare",
        "technology",
        "retail",
        "logistics",
        "automotive",
        "hospitality",
        "media",
        "education",
        "other"
    ]
    country: str

# Set up model config
generation_config = {
  "temperature": 0.2,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "application/json",
  "response_schema": list[AdDisplayInfo]
}

sys_instruction = """
You are an expert video reviewer tasked with analyzing sports events and extracting information about all brands and companies advertised during the game. 
This includes different types of ads: on-site ads (e.g., stadium, track-side), player ads (e.g., on jerseys, shoes, or equipment), and broadcast ads (e.g., digital commercials). 
The three types of sports events you will analyze are:

1. **Soccer**: This includes on-field stadium ads, player ads (e.g., logos on shirts, equipment), and broadcast ads.
2. **Basketball**: This includes court-side ads, player ads (e.g., logos on jerseys, shoes), and broadcast ads.
3. **Racing (Formula 1)**: This includes track-side ads, car and driver ads (e.g., logos on the cars, driver suits, helmets), and broadcast ads.

The model must follow these steps:

1. Identify all companies and brands advertised during the game. 
    - Extract brand names and the time frames where they appeared.
    - Capture all brands displayed in a single frame. A frame may contain multiple brand advertisements, each of which must be included in the response.

2. Classify each ad or commercial type into one of the following categories:
    - **'on-site'** (stadium, track-side, court-side ads),
    - **'player'** (player-related ads such as logos on shirts, helmets, shoes, cars, etc.),
    - **'broadcast'** (digital commercials or other types of media),
    - **'other'** (other forms of advertising that don't fit into the previous categories).

3. Calculate the total exposure time for each brand in seconds:
    - Sum all durations where the brand name or logo was visible in the video.
    - If the same brand is advertised with multiple types of ads (e.g., 'on-site' and 'player'), calculate the total exposure time separately for each type.

4. Enrich the response with additional details about each advertised company, such as its industry and country of headquarter.

### Example:

Suppose the brand **Red Bull** appears in a Formula 1 video:
- As a track-side ad visible for 120 seconds (on-site).
- As a logo on the driver's car visible for 180 seconds (player).
- As a logo on the driver's helmet visible for 60 seconds (player).

The output would look like this:

```json
[
    {
        "brand_name": "Red Bull",
        "total_sec_displayed": integer (total seconds),
        "ad_type": "on-site",
        "industry": "retail",
        "country": "Austria"
    },
    {
        "brand_name": "Red Bull",
        "total_sec_displayed": integer (total seconds),
        "ad_type": "player",
        "industry": "retail",
        "country": "Austria"
    }
]
"""


model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
  system_instruction=sys_instruction,
)

video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv']
# Select only videos from the list
files = os.listdir("data/")
video_files = [file for file in files if any(file.lower().endswith(ext) for ext in video_extensions)]

# generate and print response
response = model.generate_content(["Analyse this video", video_files[0]],
                                  request_options={"timeout": 600})
print(response.text)








# # Create the prompt.
# prompt = "Summarize this video. Then create a quiz with answer key based on the information in the video."

# files = genai.list_files()
# for file in files:
#     print(f"File ID: {file.name}, Status: {file.state}")


# # Make the LLM request.
# print("Making LLM inference request...")
# response = model.generate_content([video_file, prompt],
#                                   request_options={"timeout": 600})

# print(response)


















