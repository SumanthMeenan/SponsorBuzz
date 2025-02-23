import requests
import argparse
import yt_dlp


# Function to download video from a URL
def download_video(video_url, filename):
    # response = requests.get(video_url, stream=True)
    # if response.status_code == 200:
    #     with open(filename, 'wb') as f:
    #         for chunk in response.iter_content(chunk_size=1024):
    #             f.write(chunk)
    #     print(f"Video downloaded: {filename}")
    # else: 
    #     print("Failed to donwload video")    
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
