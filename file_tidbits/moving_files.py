import shutil

def move_files(src, dest):
    # Move the file to a new location
    shutil.move(src, dest)
        
#move_files('./files/02_file.txt', './files/subfolder/02_file.txt')
#move_files('./files/subfolder', './files/xyz') # Move the folder to a new location