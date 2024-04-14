import os, fnmatch

def match(dir, pattern):
    for file in os.listdir(dir):
        if fnmatch.fnmatch(file, pattern):
            print(file)
            
match('./files', '*_file.csv')
#more advanced pattern matching
match('./files', 'file[0-9].csv')
#more advanced with more wildcards
match('./files', '*_file*.*')

