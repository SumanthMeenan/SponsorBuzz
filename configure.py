import google.generativeai as genai
import os 

from dotenv import load_dotenv
import os
    
def configure_api():
    
    print("Configuring Gemini Connection using Google API Key")
    load_dotenv()  # Loads environment variables from .env file
    google_api_key = os.getenv("GOOGLE_API_KEY")

    if google_api_key:
        print("API Key retrieved successfully!")
    else:
        print("API Key not found.")
    genai.configure(api_key=google_api_key)
    print("Successfully Configured")
   
