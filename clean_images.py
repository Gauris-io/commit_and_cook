import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from rembg import remove
from PIL import Image

# Folder configuration
IMAGE_FOLDER = "./public/images"
processing_files = set()

class ImageHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            self.process_image(event.src_path)

    def process_image(self, file_path):
        filename = os.path.basename(file_path)
        
        # Filter for image formats
        if not filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            return
            
        if file_path in processing_files:
            return

        print(f"Detected new file: {filename}")
        
        try:
            # Short sleep to ensure the file is fully written to disk
            time.sleep(0.5)
            
            with Image.open(file_path) as img:
                # 1. Logic Check: If image already has transparency, keep it
                if img.mode == 'RGBA':
                    print(f"Skipping {filename}: Already has transparency.")
                    return

                # 2. Process: Remove background for non-transparent images
                print(f"Removing background from {filename}...")
                output_data = remove(img)
                
                # Convert path to .png to support the new transparency
                new_filename = os.path.splitext(filename)[0] + ".png"
                new_path = os.path.join(IMAGE_FOLDER, new_filename)
                
                processing_files.add(new_path)
                output_data.save(new_path)
                
                # 3. Clean up: Delete the old background-filled image
                if file_path != new_path:
                    os.remove(file_path)
                    print(f"Deleted original: {filename}")
                
                print(f"Success! {new_filename} is now ready for your UI.")
                
        except Exception as e:
            print(f"Error processing {filename}: {e}")
        finally:
            time.sleep(1)
            if file_path in processing_files: processing_files.remove(file_path)

if __name__ == "__main__":
    event_handler = ImageHandler()
    observer = Observer()
    observer.schedule(event_handler, IMAGE_FOLDER, recursive=False)
    
    print(f"Watcher started on {IMAGE_FOLDER}...")
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()