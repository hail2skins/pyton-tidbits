import os
from datetime import datetime

def get_date(timestamp):
    return datetime.fromtimestamp(timestamp).strftime('%b-%d-%Y')

def get_file_attrs(dir):
    with os.scandir(dir) as dir:
        for file in dir:
            if file.is_file():
                inf = file.stat()
                print(f'Modified {get_date(inf.st_mtime)} {file.name}')
    

get_file_attrs('./files')   

