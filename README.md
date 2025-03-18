# Folder Monitoring and Tar Creation System

## Overview
Python script to monitor a specified directory for new folders, automatically creates tar archives when new folders appear, and maintains detailed logs of all operations.

Script - `dpx_to_tar_conv_v2.py`

## Features
- Real-time folder monitoring
- Automatic tar archive creation
- Copy completion verification
- Content validation
- Detailed logging system
- Cross-platform compatibility

## How It Works
1. **Folder Detection**: Continuously monitors a specified directory for new folders
2. **Copy Verification**: Ensures folder copying is complete before processing
3. **Tar Creation**: Creates a tar archive of each new folder
4. **Validation**: Verifies tar contents match the original folder
5. **Logging**: Maintains detailed operation logs and folder records

## Configuration

### Setting the Watch Path
Modify the `WATCH_PATH` variable in the script according to your system:

For Windows:
```
WATCH_PATH = "C:\\Users\\YourName\\Documents\\WatchFolder"
WATCH_PATH = "D:\\Data\\InputFolders"
```

For Linux/Mac:
```
WATCH_PATH = "/home/username/watch_folder"
WATCH_PATH = "/mnt/data/input"
```

## Log Files
The system maintains two log files:

1. `folder_tar_operations.log`
   - Detailed operation logs
   - Creation and validation status
   - File listings and error messages

2. `folder_records.txt`
   - Simple record of processed folders
   - Timestamps of operations
   - Current status of folders

## Requirements
- Python 3.x
- Read/Write permissions for watch directory
- Sufficient disk space for tar archives

## Note
- Original folders remain unchanged after tar creation
- The script only processes new folders, existing folders are not affected
- Interrupting the script (Ctrl+C) will safely stop the monitoring process
- If a folder appears on the provided path when the script is not running, the folder will not be tarred. If required, we need to remove the folder from the path and run the script and put the folder to the same path once again to tar it.