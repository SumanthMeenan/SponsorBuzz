import requests
import argparse

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

if __name__ == "__main__":
    # Set up argument parsing for the video URL and the filename to save as
    parser = argparse.ArgumentParser(description="Download a video from a URL.")
    parser.add_argument("video_url", type=str, help="URL of the video to download")
    parser.add_argument("filename", type=str, help="Filename to save the video as")

    # Parse arguments
    args = parser.parse_args()

    # Download the video
    download_video(args.video_url, args.filename)
    print(f"Video downloaded and saved as {args.filename}")


