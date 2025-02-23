import google.generativeai as genai
from typing_extensions import TypedDict
from typing import Literal

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
  "temperature": 1,
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

### Model Instructions:
1. Identify all companies and brands advertised during the game.
   - Extract brand names and the time frames where they appeared.
   - Capture all brands displayed in a single frame. A frame may contain multiple brand advertisements, each of which must be included in the response.

2. Classify each ad or commercial type into one of the following categories:
   - **'on-site'** (stadium, track-side, court-side ads),
   - **'player'** (player-related ads such as logos on shirts, helmets, shoes, cars, etc.),
   - **'broadcast'** (digital commercials or other types of media),
   - **'other'** (other forms of advertising that don't fit into the previous categories).

3. Calculate the total exposure time for each brand:
   - Sum all durations where the brand name or logo was visible in the video.
   - If the same brand is advertised in multiple types of ads (e.g., 'on-site' and 'player'), calculate the total exposure time separately for each type.

4. Format the response strictly in JSON format:
   - Each brand occurrence must include **start and end timestamps**.
   - Ensure **each instance** when a brand appeared is listed with timestamps.
   - If timestamps are missing, the response is incomplete.

5. Enrich the response with additional details about each advertised company:
   - Include the **industry** and **country of headquarters**.

Example Output:

Suppose the brand **Red Bull** appears in a Formula 1 video:
- As a track-side ad visible for 120 seconds (on-site).
- As a logo on the driver's car visible for 180 seconds (player).
- As a logo on the driver's helmet visible for 60 seconds (player).

The output would look like this:

```json 
[
    {
        "brand_name": "Red Bull",
        "total_sec_displayed": 120,
        "ad_type": "on-site",
        "industry": "retail",
        "country": "Austria"
    },
    {
        "brand_name": "Red Bull",
        "total_sec_displayed": 240,
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

model2 = genai.GenerativeModel(model_name="gemini-1.5-pro-latest")

