import cv2
import os

def format_frame_count(frame_count):
    return str(frame_count).zfill(4)

def extract_and_crop_images_from_video(video_path, output_folder, num_photos, crop):
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print(f"Error: Could not open video file {video_path}.")
        return
    
    # total frames
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if total_frames < num_photos:
        print(f"Warning: The video {video_path} has fewer frames ({total_frames}) than the number of photos requested ({num_photos}).")
        return

    # interval
    frame_interval = total_frames // num_photos
    
    frame_count = 0
    extracted_count = 0
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    video_output_folder = os.path.join(output_folder, video_name)
    
    if not os.path.exists(video_output_folder):
        os.makedirs(video_output_folder)
    
    while True: 
        ret, frame = cap.read()
        
        if not ret:
            break
        
        if frame_count % frame_interval == 0 and extracted_count < num_photos:
            if crop:
                # crop
                height, width, _ = frame.shape
                if height > width:  # vertical
                    offset = (height - width) // 2
                    square_frame = frame[offset:offset+width, :]
                else:  # horizontal
                    offset = (width - height) // 2
                    square_frame = frame[:, offset:offset+height]
            else:
                square_frame = frame
            
            output_path = f"{video_output_folder}/frame_{frame_count}.jpg"
            cv2.imwrite(output_path, square_frame)
            extracted_count += 1
            print(f"Extracted frame {frame_count} to {output_path}")
        
        frame_count += 1
    
    cap.release()
    print(f"Extraction complete for {video_path}. Extracted {extracted_count} frames.")

def process_videos_in_folder(folder_path, output_folder, num_photos, crop):
    for filename in os.listdir(folder_path):
        if filename.endswith(('.mp4', '.mov', '.MOV')):
            video_path = os.path.join(folder_path, filename)
            extract_and_crop_images_from_video(video_path, output_folder, num_photos, crop)


folder_path = './media/videos'
output_folder = './media/images'

process_videos_in_folder(folder_path, output_folder, num_photos=10, crop=False)