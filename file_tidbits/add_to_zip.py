import zipfile

to_add = [
    '/.files/01_file.txt',
    '/.files/01_file.csv',
    
]

def add_to_zip(zipf, files, opt):
    with zipfile.ZipFile(zipf, opt) as archive:
        for file in files:
            lst = archive.namelist()
            if not file in lst:
                archive.write(file)
                print("Files added successfully")
            else: 
                print("File already exists in the archive")
                
add_to_zip("files.zip", to_add, "a")