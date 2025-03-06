import os
import tarfile
import time
import logging

# Configuration
FOLDER_TO_TAR = "/Users/SathyaNarayanan/Downloads/114_QXI-00254-22-13_2025_03_4_xp4"

# Setup logging
logging.basicConfig(
    filename=f"{os.path.splitext(__file__)[0]}.txt",
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def get_folder_contents(folder_path):
    """Get list of all files and folders recursively with relative paths."""
    contents = []
    folder_name = os.path.basename(folder_path)
    
    for root, dirs, files in os.walk(folder_path):
        # Get path relative to the base folder
        relative_root = os.path.relpath(root, os.path.dirname(folder_path))
        
        # Remove the folder name from the beginning of the path
        if relative_root.startswith(folder_name):
            relative_root = relative_root[len(folder_name):].lstrip(os.sep)
        
        # Add files
        for file in files:
            if relative_root:
                file_path = os.path.join(relative_root, file)
            else:
                file_path = file
            contents.append(file_path)
        
        # Add directories
        for dir in dirs:
            if relative_root:
                dir_path = os.path.join(relative_root, dir)
            else:
                dir_path = dir
            contents.append(dir_path)

    return sorted(contents)

def validate_tar(tar_path, original_folder):
    """Validate if tar contains all files from original folder."""
    try:
        # Get original folder contents
        original_contents = get_folder_contents(original_folder)
        folder_name = os.path.basename(original_folder)
        
        logging.info(f"Starting tar validation...")
        logging.info(f"Number of items in original folder: {len(original_contents)}")
        
        # Log original contents in a single line
        logging.info(f"Original folder contents: {', '.join(original_contents)}")
        
        # Get tar contents
        tar_contents = []
        with tarfile.open(tar_path, "r") as tar:
            for member in tar.getmembers():
                # Skip the root folder itself
                if member.name == folder_name:
                    continue
                    
                # Remove the folder name from the beginning of the path
                if member.name.startswith(folder_name + '/'):
                    relative_path = member.name[len(folder_name + '/'):].rstrip('/')
                    if relative_path:  # Skip empty paths
                        tar_contents.append(relative_path)
        
        tar_contents = sorted(tar_contents)
        logging.info(f"Number of items in tar: {len(tar_contents)}")
        
        # Log tar contents in a single line
        logging.info(f"Tar contents: {', '.join(tar_contents)}")
        
        # Compare contents
        missing_items = []
        for item in original_contents:
            normalized_item = item.rstrip('/').rstrip('\\')
            if normalized_item not in tar_contents:
                missing_items.append(item)
        
        if missing_items:
            logging.error("Validation Failed!")
            logging.error(f"Missing items in tar: {', '.join(missing_items)}")
            return False
        else:
            logging.info("Validation Successful! All files and folders are present in the tar file.")
            return True
            
    except Exception as e:
        logging.error(f"Error during validation: {e}")
        return False

def create_tar():
    """Create tar file from folder."""
    try:
        # Get folder name and parent directory
        folder_name = os.path.basename(FOLDER_TO_TAR)
        parent_dir = os.path.dirname(FOLDER_TO_TAR)
        logging.info(f"Starting tar creation for folder: {folder_name}")
        logging.info(f"Parent directory: {parent_dir}")
        
        # Create tar file path (same location as folder)
        tar_path = os.path.join(parent_dir, f"{folder_name}.tar")
        logging.info(f"Creating tar file: {tar_path}")
        
        # Create tar file
        with tarfile.open(tar_path, "w") as tar:
            # Add folder to tar with arcname as folder name
            tar.add(FOLDER_TO_TAR, arcname=folder_name)
        
        logging.info(f"Successfully created tar file at: {tar_path}")
        
        # Validate the tar file
        validate_tar(tar_path, FOLDER_TO_TAR)
        
    except Exception as e:
        logging.error(f"Error creating tar file: {e}")

if __name__ == "__main__":
    logging.info("Starting tar creation process...")
    if not os.path.exists(FOLDER_TO_TAR):
        logging.error(f"Error: Folder not found: {FOLDER_TO_TAR}")
    else:
        create_tar()
    logging.info("Tar creation process completed.")
