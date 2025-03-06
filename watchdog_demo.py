from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import os

class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        print(f"\nFile created: {event}")
        print(f"Is directory?: {event.is_directory}")
        print(f"Event type: {event.event_type}")
    
    def on_modified(self, event):
        print(f"\nFile modified: {event.src_path}")
        print(f"Is directory?: {event.is_directory}")
        print(f"Event type: {event.event_type}")
    
    def on_deleted(self, event):
        print(f"\nFile deleted: {event.src_path}")
        print(f"Is directory?: {event.is_directory}")
        print(f"Event type: {event.event_type}")

if __name__ == "__main__":
    path_to_watch = "."  # current directory
    
    # Set up the observer
    observer = Observer()
    observer.schedule(MyHandler(), path_to_watch, recursive=False)
    observer.start()

    print(f"Monitoring directory: {os.path.abspath(path_to_watch)}")
    print("Press Ctrl+C to stop...")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping the observer...")
        observer.stop()
        observer.join()
        print("Observer stopped")
