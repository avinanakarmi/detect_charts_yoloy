import cv2
import os

def draw_bounding_boxes(image_path, annotation_file):
    # Read the image
    image = cv2.imread(image_path)

    # Read YOLO-format annotation file
    with open(annotation_file, 'r') as file:
        lines = file.readlines()

    # Loop through each line in the annotation file
    for line in lines:
        # Parse the YOLO annotation line
        class_id, x_center, y_center, width, height = map(float, line.strip().split())
        
        # Get image dimensions
        image_height, image_width, _ = image.shape

        # Convert YOLO normalized values to pixel values
        x_center = int(x_center * image_width)
        y_center = int(y_center * image_height)
        bbox_width = int(width * image_width)
        bbox_height = int(height * image_height)

        # Calculate top-left corner and bottom-right corner of the bounding box
        x1 = x_center - bbox_width // 2
        y1 = y_center - bbox_height // 2
        x2 = x_center + bbox_width // 2
        y2 = y_center + bbox_height // 2

        # Draw the bounding box on the image (using a random color for visibility)
        color = (0, 255, 0)  # Green color (you can change this)
        thickness = 2  # Line thickness
        cv2.rectangle(image, (x1, y1), (x2, y2), color, thickness)

    # Display the image with the bounding boxes
    cv2.imshow("Image with Bounding Boxes", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Example usage
image_path = "./datasets/charts/images/test/PMC1790633___g006.jpg"  # Replace with your image path
annotation_file = "./datasets/charts/labels/test/PMC1790633___g006.txt"  # Replace with your annotation file path (YOLO format)
draw_bounding_boxes(image_path, annotation_file)
