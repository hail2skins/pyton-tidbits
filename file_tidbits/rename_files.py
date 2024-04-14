import os
from pathlib import Path

def rename_files(src, dest):
    # Rename the file
    os.rename(src, dest)
    
def rename_files_1(src, dest):
    # Rename the file
    Path(src).rename(dest)
    
#rename_files('./files/02_file.txt', './files/02_file_renamed.txt')
#rename_files_1('./files/02_file_renamed.txt', './files/02_file.txt')