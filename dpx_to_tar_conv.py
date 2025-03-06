import os
import time
import tarfile
import shutil
import logging
import sys
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Configuration
# SOURCE_DIR = r"C:\source_folder"  # Change as needed
# BACKUP_DIR = r"C:\backup_folder"  # Change as needed
# TAR_DIR = r"C:\tar_folder"        # Change as needed

SOURCE_DIR = r"C:\source_folder"  # Change as needed
BACKUP_DIR = r"C:\backup_folder"  # Change as needed
TAR_DIR = r"C:\tar_folder"        # Change as needed

# Setup logging
logging.basicConfig(
    filename=f"{os.path.splitext(__file__)[0]}.txt",
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def is_file_ready(file_path):
    """Check if file is completely copied."""
    try:
        initial_size = os.path.getsize(file_path)
        time.sleep(1)  # Wait 1 second
        final_size = os.path.getsize(file_path)
        return initial_size == final_size
    except Exception as e:
        logging.error(f"Error checking file readiness: {e}")
        return False

def create_tar(source_file):
    """Create tar file from dpx file."""
    try:
        base_name = os.path.basename(source_file)
        tar_path = os.path.join(TAR_DIR, f"{os.path.splitext(base_name)[0]}.tar")
        
        with tarfile.open(tar_path, "w") as tar:
            tar.add(source_file, arcname=base_name)
        
        logging.info(f"Created tar file: {tar_path}")
        return tar_path
    except Exception as e:
        logging.error(f"Error creating tar file: {e}")
        return None

def verify_tar(original_file, tar_path):
    """Verify tar contents match original file."""
    try:
        with tarfile.open(tar_path, "r") as tar:
            members = tar.getmembers()
            if len(members) != 1:
                logging.error(f"Incorrect number of files in tar: {len(members)}")
                return False
            
            if members[0].name != os.path.basename(original_file):
                logging.error("Filename mismatch in tar")
                return False
            
            if members[0].size != os.path.getsize(original_file):
                logging.error("File size mismatch")
                return False
        
        logging.info(f"Tar verification successful: {tar_path}")
        return True
    except Exception as e:
        logging.error(f"Error verifying tar: {e}")
        return False

def move_to_backup(file_path):
    """Move original file to backup location."""
    try:
        backup_path = os.path.join(BACKUP_DIR, os.path.basename(file_path))
        shutil.move(file_path, backup_path)
        logging.info(f"Moved original file to backup: {backup_path}")
        return True
    except Exception as e:
        logging.error(f"Error moving file to backup: {e}")
        return False

class DPXHandler(FileSystemEventHandler):
    def on_created(self, event):
        # event is a FileCreatedEvent object with these main attributes:
        print(event.src_path)    # Full path of the created file
        print(event.is_directory)  # True if it's a directory, False if file
        print(event.event_type)    # 'created' in this case
        
        # Our existing code uses:
        if event.is_directory:  # Check if it's a directory
            return
        if not event.src_path.lower().endswith('.dpx'):  # Check file extension
            return

        logging.info(f"New DPX file detected: {event.src_path}")
        
        # Wait for file to be completely copied
        while not is_file_ready(event.src_path):
            time.sleep(1)
        
        # Process the file
        tar_path = create_tar(event.src_path)
        if tar_path and verify_tar(event.src_path, tar_path):
            move_to_backup(event.src_path)

def main():
    # Create directories if they don't exist
    for directory in [SOURCE_DIR, BACKUP_DIR, TAR_DIR]:
        os.makedirs(directory, exist_ok=True)

    logging.info("Starting DPX monitoring service")
    
    event_handler = DPXHandler()
    observer = Observer()
    observer.schedule(event_handler, SOURCE_DIR, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        logging.info("Stopping DPX monitoring service")
    
    observer.join()

if __name__ == "__main__":
    main()
