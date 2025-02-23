import os
import json
import csv
import argparse
import google.generativeai as genai
from model import model
from configure import configure_api

# Configure API
configure_api()

# Define allowed video extensions
video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv']

def analyze_video(video_path):
    """Generates AI response for the given video."""
    if not os.path.exists(video_path):
        print(f"Error: File '{video_path}' not found.")
        return None

    response = model.generate_content(["Analyse this video", video_path],
                                      request_options={"timeout": 600})
    return response.text

def response_to_json(llm_output, json_filename, csv_filename):
    """Converts AI response to JSON and CSV files."""
    try:
        data = json.loads(llm_output)

        # Save JSON file
        with open(json_filename, "w", encoding="utf-8") as json_file:
            json.dump(data, json_file, indent=4)
        print(f"JSON file saved as {json_filename}")

        # Save CSV file
        with open(csv_filename, "w", newline="", encoding="utf-8") as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(data[0].keys())  # Header
            for entry in data:
                csv_writer.writerow(entry.values())

        print(f"CSV file saved as {csv_filename}")

    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")

def main():
    """Main function to handle argument parsing and processing."""
    parser = argparse.ArgumentParser(description="Analyze sports video ads and extract brand details.")
    parser.add_argument("video_path", type=str, help="Path to the video file for analysis")
    parser.add_argument("--json", type=str, default="ads_data.json", help="Output JSON filename (default: ads_data.json)")
    parser.add_argument("--csv", type=str, default="ads_data.csv", help="Output CSV filename (default: ads_data.csv)")

    args = parser.parse_args()

    # Analyze video
    llm_output = analyze_video(args.video_path)
    
    if llm_output:
        response_to_json(llm_output, args.json, args.csv)

if __name__ == "__main__":
    main()
