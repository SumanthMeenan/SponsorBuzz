import cv2
import re
import google.generativeai as genai
from PIL import Image
import argparse
from configure import configure_api

# Configure API
configure_api()

# Initialize the model
model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
)

def process_video(input_video_path, output_video_path):
    # Load the video
    cap = cv2.VideoCapture(input_video_path)
    
    # Check if video was opened successfully
    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    # Get video properties
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    # Get the total number of frames
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"Total frames in video: {total_frames}")

    # Define video writer
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

    frame_counter = 0

    # Process frames
    while cap.isOpened() and frame_counter < 3:  # Change this to process more frames if needed
        print(f"Processing frame {frame_counter + 1}")
        ret, frame = cap.read()
        if not ret:
            break
        frame_counter += 1
        
        # Convert frame to PIL Image
        image_pil = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        
        # Get bounding boxes from Gemini
        prompt = "Return bounding boxes for each brand logo in [ymin, xmin, ymax, xmax] format."
        response = model.generate_content([image_pil, prompt])
        print("Model response:", response.text)

        # Parse the response and extract bounding boxes and brand names
        if response.text:
            for line in response.text.split("\n"):
                parts = line.split(":")
                print('Parts:', parts)

                # Check if we have valid parts
                if len(parts) == 2:
                    bbox_str, brand_name = parts
                    try:
                        # Clean up the bounding box string to remove any leading characters like '-'
                        match = re.search(r'\[([\d, ]+)\]', bbox_str)

                        if match:
                            # Extract the bounding box as a string and convert to a list of integers
                            bounding_box = list(map(int, match.group(1).split(', ')))
                            print("Bounding box:", bounding_box)
                        else:
                            print("No bounding box found.")

                        ymin, xmin, ymax, xmax = bounding_box

                        # Draw bounding box on the frame
                        cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)  # Green box
                        cv2.putText(frame, brand_name.strip(), (xmin, ymin - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)  # Green text
                        cv2.imshow("Frame with Bounding Boxes", frame)

                    except Exception as e:
                        print(f"Skipping invalid bounding box: {bbox_str.strip()}, Error: {e}")
                        continue  # Skip this line if it's not valid

        # Write processed frame to output video
        out.write(frame)

    # Release resources
    cap.release()
    out.release()
    cv2.destroyAllWindows()

    print(f"Processed video saved as {output_video_path}")

if __name__ == "__main__":
    # Set up argument parsing for input and output video files
    parser = argparse.ArgumentParser(description="Process a video and generate output with bounding boxes.")
    parser.add_argument("input_video", type=str, help="Path to the input video file")
    parser.add_argument("output_video", type=str, help="Path to save the output video with bounding boxes")

    args = parser.parse_args()

    # Call the function to process the video
    process_video(args.input_video, args.output_video)
