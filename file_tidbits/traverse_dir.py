import os

def traverse(dir):
    for folder, dirs, files in os.walk(dir):
        print(f'Folder: {folder}')
        for dir in dirs:
            print(f'\tSubdirectory: {dir}')
        for file in files:
            print(f'\t{file}')
            
traverse('./files')
            