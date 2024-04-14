import zipfile

to_zip = [
    './files/01_file_test.csv',
    './files/01_file_test.txt',
]

def zip_files(zipf, files, opt):
    with zipfile.ZipFile(zipf, opt, allowZip64=True) as archive:
        for file in files:
            archive.write(file)
        print("Files zipped successfully")
        
zip_files("./files.zip", to_zip, "w")