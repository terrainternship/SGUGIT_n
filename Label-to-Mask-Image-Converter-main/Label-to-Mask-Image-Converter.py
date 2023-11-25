import os
import cv2
import numpy as np

# Paths to image and label directories
images_dir = "images"
labels_dir = "labels"
output_dir = "output"

# Create a directory to save results if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Get a list of label files in the "labels" directory
label_files = os.listdir(labels_dir)

for label_file in label_files:
    # Extract the file name without the extension
    base_name = os.path.splitext(label_file)[0]

    # Read the image
    img_path = os.path.join(images_dir, base_name + ".jpg")
    img = cv2.imread(img_path)

    # Read the label from the .txt file
    label_path = os.path.join(labels_dir, label_file)
    with open(label_path, "r") as file:
        lines = file.readlines()

    mask = np.zeros_like(img, dtype=np.uint8)

    for line in lines:
        points = line.strip().split()

        # Check if we have at least two coordinates
        if len(points) >= 4:
            # Determine the color based on the class
            class_color = (0, 255, 0) if int(points[0]) == 0 else (0, 0, 255)
            # Convert segmentation coordinates
            points = [(int(float(points[i]) * img.shape[1]), int(float(points[i + 1]) * img.shape[0])) for i in range(1, len(points), 2)]

            # Create a segmentation mask
            if len(points) > 2:  # To avoid an error with insufficient points
                pts = np.array(points, np.int32)
                pts = pts.reshape((-1, 1, 2))
                cv2.fillPoly(mask, [pts], class_color)

    # Merge the image with the mask
    result = cv2.addWeighted(img, 1, mask, 0.5, 0)

    # Save the segmented image to the "output" directory
    output_path = os.path.join(output_dir, base_name + ".jpg")
    cv2.imwrite(output_path, result)

    print(f"Conversion completed for file: {label_file}")

print("All files processed.")
