import zipfile

def read_zip(zipf):
    with zipfile.ZipFile(zipf, "r") as archive:
        lst = archive.namelist()
        for file in lst:
            info = archive.getinfo(file)
            print(f"File name: {info.filename}")
            
            
            
            
read_zip("./files.zip")