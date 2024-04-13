import os, glob
from pathlib import Path

# glob with no recursion
def glob_match(dir, search):
    for file in glob.glob(os.path.join(dir, search)):
        print(file)
        
# with recursion
def glob_match_recursion(dir, search):
    for file in glob.glob(os.path.join(dir, '**', search), recursive=True):
        print(file)
        
# with Path and rglob for recursion
def path_match(dir, search):
    for file in Path(dir).rglob(search):
        print(file)
        
# with Path and glob for no recursion
def path_match_with_path(dir, search):
    for file in Path(dir).glob(search):
        print(file)
        
        
glob_match('./files', '*2*.t*')

glob_match_recursion('./files', '*.t*')

path_match('./files', '*2*.t*')

path_match_with_path('./files', '*2*.t*')
