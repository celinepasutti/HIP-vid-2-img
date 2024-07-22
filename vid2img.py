import cv2

def extract_and_crop_images_from_video(video_path, output_folder, frame_parameter):
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print("Error: Could not open video file.")
        return
    
    frame_count = 0
    extracted_count = 0
    
    while True: 
        ret, frame = cap.read()
        
        if not ret:
            break
        
        # crop to a square
        height, width, _ = frame.shape
        if height > width: # vertical
            offset = (height - width) // 2
            square_frame = frame[offset:offset+width, :]
        else: # horizontal
            offset = (width - height) // 2
            square_frame = frame[:, offset:offset+height]
        
        if frame_count % frame_parameter == 0:
            output_path = f"{output_folder}/frame_{frame_count}.jpg"
            cv2.imwrite(output_path, square_frame)
            extracted_count += 1
            print(f"Extracted and cropped frame {frame_count} to {output_path}")
        
        frame_count += 1
    
    cap.release()
    print(f"Extraction complete. Extracted {extracted_count} frames.")

video_path = './media/videos/makeup.MOV'
output_folder = './media/images'
frame_parameter = 10

extract_and_crop_images_from_video(video_path, output_folder, frame_parameter)

