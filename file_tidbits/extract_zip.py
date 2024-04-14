import zipfile

def extract_zip(zip_file, extract_dir):
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)
        
extract_zip("./files.zip", "./extracted_files")

def extract_file_zip(zip_file, file, extract_dir):
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extract(file, extract_dir)
        
extract_file_zip("./files.zip", "01_file_test.csv", "./extracted_files")