import google.generativeai as genai
import os 

def configure_api():
    
    print("Configuring Gemini Connection using Google API Key")
    os.environ["GOOGLE_API_KEY"] = ""
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    genai.configure(api_key=GOOGLE_API_KEY)
    print("Successfully Configured")
   
