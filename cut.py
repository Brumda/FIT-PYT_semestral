from PIL import Image
import os


def cut_image_into_pieces(input_image_path, output_folder):
    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Open the image
    image = Image.open(input_image_path)

    # Get the size of the image
    width, height = image.size

    # Calculate the number of pieces in both dimensions
    num_pieces_width = width // 64
    num_pieces_height = height // 64

    # Loop through each piece and save it
    for i in range(num_pieces_width):
        for j in range(num_pieces_height):
            left = i * 64
            upper = j * 64
            right = left + 64
            lower = upper + 64

            # Crop the image to get the piece
            piece = image.crop((left, upper, right, lower))

            # Save the piece
            piece.save(os.path.join(output_folder, f"piece_{j}_{i}.png"))


# Example usage:
input_image_path = "../assets/SkeletonEnemy/Skeleton enemy/Skeleton enemy.png"
output_folder = "../assets/SkeletonEnemy/Skeleton enemy/cut"
cut_image_into_pieces(input_image_path, output_folder)
