# Description: Extracts text from a PDF file that matches a given pattern.
"""
In Kind \b[A-Za-z\s,]+\b\s*Total Cash Date: This matches the exact string "In Kind ",
followed by one or more word characters or spaces or commas (the name),
followed by any amount of whitespace, followed by the exact string "Total
Cash Date".

(?:[^\n]*\n)+?: This is a non-capturing group that matches any number of 
characters that are not a newline, followed by a newline. The +? makes it
match one or more times, but as few times as possible.

.*?Total: This matches any number of any characters (as few as possible), followed by the exact string "Total".
"""

import re
import PyPDF2

def extract_text_by_pattern(pdf_path, pattern):
    with open(pdf_path, "rb") as file:
        pdf_reader = PyPDF2.PdfReader(file)
        matching_text = []
        for page in pdf_reader.pages:
            text = page.extract_text()
            if text:
                found = re.findall(pattern, text)
                matching_text.extend(found)
    return matching_text

# Example usage
pdf_path = './jensen.pdf'
pattern = r'(In Kind \b[A-Za-z\s,]+\b\s*Total Cash Date\s*(?:[^\n]*\n)+?.*?Total)'
extracted_text = extract_text_by_pattern(pdf_path, pattern)
print(len(extracted_text))
