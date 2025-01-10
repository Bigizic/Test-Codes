#!/usr/bin/env python3

import os
import base64

def convert_images_to_base64(input_dir):
    """
    Convert all images in the specified directory to Base64 and print the results.

    Args:
        input_dir (str): Path to the directory containing images.
    """
    # Supported image extensions, including .ico
    supported_extensions = (".png", ".jpg", ".jpeg", ".bmp", ".gif", ".ico")

    # Process each file in the input directory
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(supported_extensions):
            image_path = os.path.join(input_dir, filename)
            
            try:
                # Read the image file in binary mode
                with open(image_path, "rb") as image_file:
                    encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

                # Print the Base64 string to the console
                print(f"Base64 of {filename}:\n{encoded_string}\n")
            except Exception as e:
                print(f"Error processing {filename}: {e}")

if __name__ == "__main__":
    # Define input directory
    input_directory = "path_to_your_input_directory"

    # Run the conversion
    convert_images_to_base64('404')
