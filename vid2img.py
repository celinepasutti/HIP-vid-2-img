import cv2

def extract_and_crop_images_from_video(video_path, output_folder, x):
    # Open the video file
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print("Error: Could not open video file.")
        return
    
    frame_count = 0
    extracted_count = 0
    
    while True:
        # Read a frame from the video
        ret, frame = cap.read()
        
        if not ret:
            break
        
        # Crop the frame to a square aspect ratio
        height, width, _ = frame.shape
        if height > width:
            # Vertical crop (tall video)
            offset = (height - width) // 2
            square_frame = frame[offset:offset+width, :]
        else:
            # Horizontal crop (wide video)
            offset = (width - height) // 2
            square_frame = frame[:, offset:offset+height]
        
        # Check if the current frame number is a multiple of x
        if frame_count % x == 0:
            # Save the cropped frame as an image
            output_path = f"{output_folder}/frame_{frame_count}.jpg"
            cv2.imwrite(output_path, square_frame)
            extracted_count += 1
            print(f"Extracted and cropped frame {frame_count} to {output_path}")
        
        frame_count += 1
    
    cap.release()
    print(f"Extraction complete. Extracted {extracted_count} frames.")

# Example usage
video_path = 'path/to/your/video.mp4'
output_folder = 'path/to/output/folder'
x = 10  # Extract an image every 10 frames

extract_and_crop_images_from_video(video_path, output_folder, x)

