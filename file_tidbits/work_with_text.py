
# This function reads the text from a file and prints it to the console.
def read_text(file):
    with open(file) as f:
        print(f.read())
        
# This function reads the text from a file and prints it line by line to the console.
# This uses readlines() method which reads the entire file and returns a list of strings, where each string is a line from the file.
def read_txt_by_line(file):
    with open(file) as f:
        lines = f.readlines()
        for line in lines:
            print(line, end='')
            #line = f.readine()
            
# line by line text file read does the same thing as above but uses a for loop to iterate through the file object itself.
def read_txt_by_line_1(file):
    with open(file) as f:
        for line in f:
            print(line, end='')
            
# Write text to a file
def write_new_text(file, text):
    with open(file, 'w', encoding='utf-8') as f:
        f.write(text)
        
# add lines to existing text file
def add_text(file, text):
    with open(file, 'a', encoding='utf-8') as f:
        f.write('\n')
        f.write(text)
        
read_text('./file_tidbits/files_to_read/backup.py')
read_txt_by_line('./file_tidbits/files_to_read/backup.py')
read_txt_by_line_1('./file_tidbits/files_to_read/backup.py')
write_new_text('./file_tidbits/files_to_read/example.txt', 'This is a new file created by Python.')
add_text('./file_tidbits/files_to_read/example.txt', 'This is a new line added by Python.')
read_text('./file_tidbits/files_to_read/example.txt')
        
        

