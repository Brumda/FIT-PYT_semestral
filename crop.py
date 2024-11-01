from PIL import Image
import os


def crop_image(input_dir, output_dir):
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
                    # Crop the image to 64x48 (left, top, right, bottom)
                    cropped_img = img.crop((0, 0, 64, 48))

                    # Save the cropped image
                    cropped_img.save(output_path)


if __name__ == "__main__":
    # Set the input and output directories
    input_directory = "../assets/SkeletonEnemy/Animations"
    output_directory = "../assets/test/SkeletonEnemy/Animations"
    crop_image(input_directory, output_directory)

    print("Image cropping complete.")
