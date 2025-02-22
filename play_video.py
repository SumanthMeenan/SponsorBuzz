import cv2
import argparse

def play_video(video_path):
    # Open video file
    cap = cv2.VideoCapture(video_path)
    
    # Check if video was opened successfully
    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    # Get the total number of frames
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"Total frames in video: {total_frames}")

    # Process and display frames
    while cap.isOpened():
        ret, frame = cap.read()  # Read a new frame
        if not ret:
            break  # If no frame is read, exit the loop
        
        # Display the current frame
        cv2.imshow("Video Frame", frame)

        # Wait for 500ms and check if 'q' is pressed to exit the video display
        if cv2.waitKey(500) & 0xFF == ord('q'):
            break

    # Release the video capture object and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # Set up argument parsing for the input video path
    parser = argparse.ArgumentParser(description="Play a video with bounding boxes.")
    parser.add_argument("video_path", type=str, help="Path to the video file to play")

    args = parser.parse_args()

    # Call the function to play the video
    play_video(args.video_path)
