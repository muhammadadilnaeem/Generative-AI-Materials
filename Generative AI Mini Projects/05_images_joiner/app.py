
# import the necessary packages
import os
from PIL import Image

# Function to join images vertically
def join_images_vertically(folder_path, output_image):
    # Get a sorted list of image files in the folder
    image_files = sorted(
        [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))],
        key=lambda x: int(os.path.splitext(x)[0])  # Sort by numeric filename
    )
    
    # Open all images and store them in a list
    images = [Image.open(os.path.join(folder_path, img)) for img in image_files]
    
    # Calculate the total width and height of the final image
    total_width = max(img.width for img in images)
    total_height = sum(img.height for img in images)
    
    # Create a new blank image with a white background
    combined_image = Image.new('RGB', (total_width, total_height), (255, 255, 255))
    
    # Paste each image into the combined image
    y_offset = 0 # Initial y-offset( vertical position) for pasting images
    for img in images:
        combined_image.paste(img, (0, y_offset))
        y_offset += img.height
    
    # Save the final image
    combined_image.save(output_image)
    print(f"Vertical image saved as {output_image}")

# Example usage:
join_images_vertically(r'input_images', r'output_images/output2.jpg')
