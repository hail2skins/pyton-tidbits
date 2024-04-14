import shutil

def copy_file(src, dest):
    shutil.copy(src, dest)
    
def copy_folders(src, dest):
    shutil.copytree(src, dest)
    
    
#copy_file('./files/02_file.txt', './files/subfolder/02_file_copy.txt')
copy_folders('./files', './files_copy')