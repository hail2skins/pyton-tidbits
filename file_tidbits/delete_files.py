import os

def delete_files(file):
    if os.path.isfile(file):
        try:
           os.remove(file)
           print("File deleted successfully")
        except OSError as e:
            print("Error: %s : %s" % (file, e.strerror))
    else:
        print("Error: %s file not found" % file)
        
delete_files("./files/subfolder/02_file_copy.txt")
            
