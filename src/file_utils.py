import os
import shutil

def copy_to_dir(source, destination):
    if os.path.exists(destination):
        shutil.rmtree(destination)
        
    os.mkdir(destination)
    
    for entry in os.listdir(source):
        entry_path = os.path.join(source, entry)
        if os.path.isfile(entry_path):
            shutil.copy(entry_path, destination)
            print(f"copied: {entry_path}, to {destination}")
        else:
            entry_destination_path = os.path.join(destination, entry)
            os.mkdir(entry_destination_path)
            copy_to_dir(entry_path, entry_destination_path)