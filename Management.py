import os
from os.path import splitext, exists, join
from shutil import move
from time import sleep

import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Define source and destination directories
source_dir = "C:\\Users\\satan\\Downloads"
dest_dir_sfx = "C:\\Users\\satan\\OneDrive\\Desktop\\Organized\\SFX"
dest_dir_music = "C:\\Users\\satan\\OneDrive\\Desktop\\Organized\\Music"
dest_dir_video = "C:\\Users\\satan\\OneDrive\\Desktop\\Organized\\Video"
dest_dir_image = "C:\\Users\\satan\\OneDrive\\Desktop\\Organized\\Image"
dest_dir_documents = "C:\\Users\\satan\\OneDrive\\Desktop\\Organized\\Documents"
dest_dir_other = "C:\\Users\\satan\\OneDrive\\Desktop\\Organized\\Other"

# Define file extensions for different categories
audio_extensions = [".m4a", ".flac", ".mp3", ".wav", ".wma", ".aac"]
video_extensions = [".webm", ".mpg", ".mp2", ".mpeg", ".mpe", ".mpv", ".ogg",
                    ".mp4", ".mp4v", ".m4v", ".avi", ".wmv", ".mov", ".qt", ".flv", ".swf", ".avchd"]
image_extensions = [".jpg", ".jpeg", ".jpe", ".jif", ".jfif", ".jfi", ".png", ".gif", ".webp", ".tiff", ".tif", ".psd", ".raw", ".arw", ".cr2", ".nrw",
                    ".k25", ".bmp", ".dib", ".heif", ".heic", ".ind", ".indd", ".indt", ".jp2", ".j2k", ".jpf", ".jpf", ".jpx", ".jpm", ".mj2", ".svg", ".svgz", ".ai", ".eps", ".ico"]
document_extensions = [".doc", ".docx", ".odt", ".pdf", ".xls", ".xlsx", ".ppt", ".pptx"]

# Define a class to handle file system events
class MoverHandler(FileSystemEventHandler):
    def on_modified(self, event):
        # When there is a change in the source directory, this method will be called
        with os.scandir(source_dir) as entries:
            # Iterate through all entries in the source directory
            for entry in entries:
                name = entry.name
                # Check the type of file and move it accordingly
                self.check_audio_files(entry, name)
                self.check_video_files(entry, name)
                self.check_image_files(entry, name)
                self.check_document_files(entry, name)
                self.move_other_files(entry, name)  # Check and move other files

    # Methods to check and move different types of files
    def check_audio_files(self, entry, name):
        # Check if the file is an audio file and move it accordingly
        if any(name.endswith(ext) for ext in audio_extensions):
            if entry.stat().st_size < 10_000_000 or "SFX" in name:
                dest = dest_dir_sfx
            else:
                dest = dest_dir_music
            move_file(dest, entry, name)
            logging.info(f"Moved audio file: {name}")

    def check_video_files(self, entry, name):
        # Check if the file is a video file and move it accordingly
        if any(name.endswith(ext) for ext in video_extensions):
            move_file(dest_dir_video, entry, name)
            logging.info(f"Moved video file: {name}")

    def check_image_files(self, entry, name):
        # Check if the file is an image file and move it accordingly
        if any(name.endswith(ext) for ext in image_extensions):
            move_file(dest_dir_image, entry, name)
            logging.info(f"Moved image file: {name}")

    def check_document_files(self, entry, name):
        # Check if the file is a document file and move it accordingly
        if any(name.endswith(ext) for ext in document_extensions):
            move_file(dest_dir_documents, entry, name)
            logging.info(f"Moved document file: {name}")

    def move_other_files(self, entry, name):  
        # Check if the file does not belong to any category, then move to the Other folder
        if (not any(name.endswith(ext) for ext in audio_extensions) and
            not any(name.endswith(ext) for ext in video_extensions) and
            not any(name.endswith(ext) for ext in image_extensions) and
            not any(name.endswith(ext) for ext in document_extensions)):
            move(entry.path, dest_dir_other)
            logging.info(f"Moved other file: {name}")

# Function to move files ensuring unique file names
def move_file(dest, entry, name):
    if exists(join(dest, name)):
        counter = 1
        filename, extension = splitext(name)
        new_name = f"{filename}({counter}){extension}"
        while exists(join(dest, new_name)):
            counter += 1
            new_name = f"{filename}({counter}){extension}"
        move(entry, join(dest, new_name))
    else:
        move(entry, dest)

if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    
    # Initialize file system observer
    path = source_dir
    event_handler = MoverHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    
    # Keep the script running
    try:
        while True:
            sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

#            __
#           / _)
#    .-^^^-/ /
# __/       /
#<__.|_|-|_|
