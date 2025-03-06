import os
import tarfile
import time

# Configuration
FOLDER_TO_TAR = r"C:\path\to\your\folder"  # Change this path
FOLDER_TO_TAR = "/Users/SathyaNarayanan/Downloads/114_QXI-00254-22-13_2025_03_4_xp4"  # Change this path


def create_tar():
    """Create tar file from folder."""
    try:
        # Get folder name and parent directory
        folder_name = os.path.basename(FOLDER_TO_TAR)
        parent_dir = os.path.dirname(FOLDER_TO_TAR)
        print("Folder name:", folder_name)
        print("Parent directory:", parent_dir)
        
        # Create tar file path (same location as folder)
        tar_path = os.path.join(parent_dir, f"{folder_name}.tar")
        
        print(f"Creating tar file: {tar_path}")
        
        # Create tar file
        with tarfile.open(tar_path, "w") as tar:
            # Add folder to tar with arcname as folder name
            tar.add(FOLDER_TO_TAR, arcname=folder_name)
        
        print(f"Successfully created tar file at: {tar_path}")
        
    except Exception as e:
        print(f"Error creating tar file: {e}")

if __name__ == "__main__":
    if not os.path.exists(FOLDER_TO_TAR):
        print(f"Error: Folder not found: {FOLDER_TO_TAR}")
    else:
        create_tar()
