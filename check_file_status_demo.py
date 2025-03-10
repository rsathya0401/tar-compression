import os
import time
import json
import logging
from datetime import datetime

# Configuration
WATCH_PATH = "/Users/SathyaNarayanan/Desktop/CODE/tar-compression"  # Change as needed
SCAN_INTERVAL = 5  # seconds
STABILITY_CHECK_TIME = 5  # seconds

# Setup logging
logging.basicConfig(
    filename=f"{os.path.splitext(__file__)[0]}.txt",
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Record file path
RECORD_FILE = f"{os.path.splitext(__file__)[0]}_record.txt"

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

def record_folder(folder_path, status="detected"):
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
    existing_folders = get_existing_folders()
    logging.info(f"Found {len(existing_folders)} existing folders")
    for folder in existing_folders:
        record_folder(folder, "existing")
    
    known_folders = existing_folders.copy()
    
    try:
        while True:
            current_folders = get_existing_folders()
            
            # Check for new folders
            new_folders = current_folders - known_folders
            for folder in new_folders:
                logging.info(f"New folder detected: {folder}")
                record_folder(folder)
                
                # Check if folder is being copied
                while not is_folder_stable(folder):
                    logging.info(f"Folder still being copied: {folder}")
                    time.sleep(SCAN_INTERVAL)
                
                logging.info(f"Folder copy completed: {folder}")
                record_folder(folder, "completed")
                known_folders.add(folder)
            
            time.sleep(SCAN_INTERVAL)
            
    except KeyboardInterrupt:
        logging.info("Monitoring stopped by user")
    except Exception as e:
        logging.error(f"Error during monitoring: {e}")

if __name__ == "__main__":
    main()
