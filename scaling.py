from PIL import Image
import os


def scale_images(input_dir, output_dir, scale_factor):
    # Iterate through all files and subdirectories in the input directory
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            # Check if the file is a PNG image
            if file.lower().endswith(".png"):
                input_path = os.path.join(root, file)

                # Create the corresponding relative path for the output directory
                relative_path = os.path.relpath(input_path, input_dir)
                output_path = os.path.join(output_dir, relative_path)

                # Create output directory if it doesn't exist
                os.makedirs(os.path.dirname(output_path), exist_ok=True)

                # Open the image
                with Image.open(input_path) as img:
                    print("found file")
                    # Calculate new dimensions
                    width, height = img.size
                    new_width = 640
                    new_height = 640

                    # Resize the image while maintaining the aspect ratio
                    resized_img = img.resize((new_width, new_height), Image.ANTIALIAS)

                    # Save the resized image
                    resized_img.save(output_path)


if __name__ == "__main__":
    # Set the input and output directories
    scale_factor = 0.1
    input_directory = "../here"
    output_directory = "../here"
    scale_images(input_directory, output_directory, scale_factor)

    print("Image scaling complete.")
