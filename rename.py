import os


def rename_files(input_dir):
    # Iterate through all files in the input directory
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            # Check if the file is a PNG image
            if file.lower().endswith(".png") and "jump" in file.lower():
                input_path = os.path.join(root, file)

                # Create the corresponding relative path for renaming
                relative_path = os.path.relpath(input_path, input_dir)

                # Extract the filename without extension
                filename, extension = os.path.splitext(relative_path)

                # Split the filename by underscores
                # filename = filename.split("\\")[1]
                parts = filename.split("_")
                # print(parts)
                # Remove the prefix up until the second underscore
                # new_filename = "_".join(parts[2:])
                new_filename = parts[-2] + "_" + parts[-1][1:]
                # new_filename = "Idle_" + parts[1]
                new_filename = "_".join(new_filename.split(" "))
                print(new_filename)
                # print(new_filename)
                # Create the new relative path
                new_relative_path = os.path.join(os.path.dirname(relative_path), new_filename + extension)

                # Rename the file
                os.rename(input_path, os.path.join(input_dir, new_relative_path))


if __name__ == "__main__":
    # Set the input directory
    for i in range(1, 4):
        input_directory = "assets/Golem_0" + str(i)
        rename_files(input_directory)

    # Call the function to rename files

    print("File renaming complete.")
