from ultralytics import YOLO
import cv2
import numpy as np

# Load the YOLO model
model = YOLO("yolov10n.pt")

def detect_objects(image_path):
    # Load image
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Image at path {image_path} could not be loaded.")
    
    # Convert image from BGR to RGB
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Perform detection
    results = model(img_rgb)
    
    # Inspect results
    print(results)  # Debugging line to understand the structure of results
    
    # Extract bounding boxes
    boxes = results[0].boxes.xyxy.numpy()  # Assuming results[0] contains the desired detections

    return img, boxes

def create_mask(img, boxes):
    mask = np.zeros(img.shape[:2], dtype=np.uint8)

    for box in boxes:
        x1, y1, x2, y2 = map(int, box[:4])
        mask[y1:y2, x1:x2] = 255

    return mask

def remove_background(image_path):
    img, boxes = detect_objects(image_path)
    mask = create_mask(img, boxes)

    # Apply the mask to the image
    result = cv2.bitwise_and(img, img, mask=mask)

    # Convert the background to white (optional)
    background = np.full_like(img, 255)
    background_masked = cv2.bitwise_and(background, background, mask=cv2.bitwise_not(mask))
    final_result = cv2.add(result, background_masked)

    return final_result

# Usage
image_path = "./media/images/mug/frame_0044.jpg"
output = remove_background(image_path)
cv2.imwrite("output_image.png", output)

