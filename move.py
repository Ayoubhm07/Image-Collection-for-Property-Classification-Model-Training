import os
import shutil


def consolidate_images(source_dir, target_dir):
    """
    Copies all images from subdirectories of 'source_dir' into 'target_dir'.
    """
    # Ensure the target directory exists
    os.makedirs(target_dir, exist_ok=True)

    # Iterate through all subdirectories in the source directory
    for subdir, dirs, files in os.walk(source_dir):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                # Construct full file path
                file_path = os.path.join(subdir, file)
                # Construct target file path
                target_file_path = os.path.join(target_dir, file)
                # Copy file to target directory
                shutil.copy(file_path, target_file_path)
                print(f"Copied: {file_path} to {target_file_path}")


# Define your directories here
source_directory = 'C:/Users/HP/Desktop/RealEstateImages/data'
target_directory = 'C:/Users/HP/Desktop/RealEstateImage/data'

# Call the function
consolidate_images(source_directory, target_directory)
