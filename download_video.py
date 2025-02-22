import requests
import argparse
import yt_dlp


# Function to download video from a URL
def download_video(video_url, filename):
    ydl_opts = {
        'outtmpl': filename,  # Save the video with the given filename
        'format': 'bestvideo+bestaudio/best',  # Get the best quality available
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])
    print(f"Video downloaded: {filename}")


def main():
    parser = argparse.ArgumentParser(description="Download a YouTube video.")
    parser.add_argument("video_url", type=str, help="URL of the YouTube video")
    parser.add_argument("filename", type=str, help="Filename to save the video as")

    args = parser.parse_args()

    download_video(args.video_url, args.filename)
    
    

if __name__ == "__main__":
    # Set up argument parsing for the video URL and the filename to save as
    main()
