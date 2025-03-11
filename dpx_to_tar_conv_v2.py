import os
import time
import tarfile
import logging
from datetime import datetime

# Configuration
WATCH_PATH = "/Users/SathyaNarayanan/Desktop/CODE/tar-compression"  # Change this to your path
SCAN_INTERVAL = 5  # seconds
STABILITY_CHECK_TIME = 5  # seconds

# Setup logging
logging.basicConfig(
    filename="folder_tar_operations.log",
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Record file for tracking folders
RECORD_FILE = "folder_records.txt"

def get_folder_contents(folder_path):
    """Get list of all files and folders recursively with relative paths."""
    contents = []
    folder_name = os.path.basename(folder_path)
    
    for root, dirs, files in os.walk(folder_path):
        relative_root = os.path.relpath(root, os.path.dirname(folder_path))
        if relative_root.startswith(folder_name):
            relative_root = relative_root[len(folder_name):].lstrip(os.sep)
        
        for file in sorted(files):
            file_path = os.path.join(relative_root, file) if relative_root else file
            contents.append(file_path)
        
        for dir in sorted(dirs):
            dir_path = os.path.join(relative_root, dir) if relative_root else dir
            contents.append(dir_path)

    return sorted(contents)

def get_folder_size(folder_path):
    """Calculate total size of a folder"""
    total_size = 0
    for dirpath, _, filenames in os.walk(folder_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size

def is_folder_stable(folder_path):
    """Check if folder is completely copied"""
    initial_size = get_folder_size(folder_path)
    initial_count = sum(len(files) for _, _, files in os.walk(folder_path))
    
    time.sleep(STABILITY_CHECK_TIME)
    
    final_size = get_folder_size(folder_path)
    final_count = sum(len(files) for _, _, files in os.walk(folder_path))
    
    return initial_size == final_size and initial_count == final_count

def create_and_validate_tar(folder_path):
    """Create and validate tar file for given folder"""
    try:
        folder_name = os.path.basename(folder_path)
        parent_dir = os.path.dirname(folder_path)
        tar_path = os.path.join(parent_dir, f"{folder_name}.tar")
        
        logging.info("Starting tar creation process...")
        logging.info(f"Starting tar creation for folder: {folder_name}")
        logging.info(f"Parent directory: {parent_dir}")
        logging.info(f"Creating tar file: {tar_path}")
        
        # Create tar file
        with tarfile.open(tar_path, "w") as tar:
            tar.add(folder_path, arcname=folder_name)
        
        logging.info(f"Successfully created tar file at: {tar_path}")
        
        # Validate tar contents
        logging.info("Starting tar validation...")
        original_contents = get_folder_contents(folder_path)
        logging.info(f"Number of items in original folder: {len(original_contents)}")
        logging.info(f"Original folder contents: {', '.join(original_contents)}")
        
        with tarfile.open(tar_path, "r") as tar:
            tar_contents = [member.name[len(folder_name)+1:] for member in tar.getmembers() 
                          if member.name != folder_name]
            
        tar_contents = sorted(tar_contents)
        logging.info(f"Number of items in tar: {len(tar_contents)}")
        logging.info(f"Tar contents: {', '.join(tar_contents)}")
        
        if sorted(original_contents) == sorted(tar_contents):
            logging.info("Validation Successful! All files and folders are present in the tar file.")
            logging.info("Tar creation process completed.")
            return True
        else:
            logging.error("Validation Failed!")
            missing_items = set(original_contents) - set(tar_contents)
            logging.error(f"Missing items in tar: {', '.join(missing_items)}")
            return False
            
    except Exception as e:
        logging.error(f"Error in tar operation: {e}")
        return False

def record_folder(folder_path, status):
    """Record folder information"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    record = f"{timestamp} - {folder_path} - {status}\n"
    
    with open(RECORD_FILE, 'a') as f:
        f.write(record)

def get_existing_folders():
    """Get list of existing folders"""
    folders = set()
    for item in os.listdir(WATCH_PATH):
        full_path = os.path.join(WATCH_PATH, item)
        if os.path.isdir(full_path):
            folders.add(full_path)
    return folders

def main():
    logging.info(f"Starting folder monitoring on: {WATCH_PATH}")
    
    # Record existing folders
    known_folders = get_existing_folders()
    logging.info(f"Found {len(known_folders)} existing folders")
    for folder in known_folders:
        record_folder(folder, "existing")
    
    try:
        while True:
            current_folders = get_existing_folders()
            new_folders = current_folders - known_folders
            
            for folder in new_folders:
                logging.info(f"New folder detected: {folder}")
                record_folder(folder, "detected")
                
                # Wait for folder to stabilize
                while not is_folder_stable(folder):
                    logging.info(f"Waiting for folder to stabilize: {folder}")
                    time.sleep(SCAN_INTERVAL)
                
                logging.info(f"Folder stable: {folder}")
                
                # Create and validate tar
                if create_and_validate_tar(folder):
                    record_folder(folder, "processed")
                    known_folders.add(folder)
                
            time.sleep(SCAN_INTERVAL)
            
    except KeyboardInterrupt:
        logging.info("Monitoring stopped by user")
    except Exception as e:
        logging.error(f"Error during monitoring: {e}")

if __name__ == "__main__":
    main()
