# Image Segmentation Conversion Script

This script is designed to convert labeled images for image segmentation. It takes images and corresponding label files, processes them, and saves the segmented images in an "output" directory. The labels are assumed to be in a specific format, where each label file contains coordinates for different classes.

## Usage

1. Place your images in the "images" directory and the label files in the "labels" directory.
2. Run the script, and it will process each image and generate a segmented version.
3. The segmented images are saved in the "output" directory.

## Requirements

- Python 3
- OpenCV (cv2)
- NumPy

## How it Works

1. The script reads the image and label files from their respective directories.
2. It processes the label data, extracting coordinates for each class and converting them to a segmentation mask.
3. The segmentation mask is then merged with the original image to create a segmented output image.
4. The resulting images are saved in the "output" directory.

## Note

- The script expects label files to be in a specific format and may not work with all types of label data.
- Make sure to install the required Python packages (OpenCV and NumPy) before running the script.


This will process the images and labels in their respective directories and save the segmented images in the "output" directory.

For more information on the script and its usage, refer to the code comments in the script itself.

Feel free to modify the script or the directories to suit your specific needs.

Happy image segmentation!
