import os

def list_dir(dir):
    for file in os.listdir(dir):
        print(file)

list_dir('./files') # Change to list files in a different directory