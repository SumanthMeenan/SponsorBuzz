import google.generativeai as genai
import time
import argparse
import os 
from configure import configure_api 

# Function to Upload File
def upload_file(filename):
    print(f"Uploading file: {filename}...")
    
    try:
        video_file = genai.upload_file(path=filename)

        # Check whether the file is ready to be used.
        while video_file.state.name == "PROCESSING":
            print('.', end='', flush=True)
            time.sleep(10)
            video_file = genai.get_file(video_file.name)

        if video_file.state.name == "FAILED":
            raise ValueError("File upload failed!")

        print(f"\n Completed upload: {video_file.uri}")
    except Exception as e:
        print(f"\n Error: {e}")
        print("File not uploaded.")

# Main execution
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Upload a file to Google Gemini API.")
    parser.add_argument("--f", type=str, required=True, help="Path to the file to be uploaded")
    
    args = parser.parse_args()
    configure_api()
    upload_file(args.f)
