import os

def ends_with(dir, search):
    for file in os.listdir(dir):
        if file.endswith(search):
            print(file)
            
def starts_with(dir, search):
    for file in os.listdir(dir):
        if file.startswith(search):
            print(file)
            
def contains(dir, search):
    for file in os.listdir(dir):
        if search in file:
            print(file)
            
#ends_with('./files', '.txt')
#starts_with('./files', '02')
contains('./files', '_file.csv') #can't use wildcards as that's fnmatch's job