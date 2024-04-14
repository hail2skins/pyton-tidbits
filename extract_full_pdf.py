# Description: This script extracts text from all pages of a PDF file using the PyPDF2 library.

import PyPDF2

# Function to extract text from all pages of a PDF file
def extract_text_from_pdf(pdf_path):
    # Open the PDF file
    with open(pdf_path, "rb") as file: # rb = read binary
        # Create a PDF reader object
        pdf_reader = PyPDF2.PdfReader(file)
        
        # Extract text from each page and collect it in a list
        text_data = []
        for page in pdf_reader.pages:
            text_data.append(page.extract_text())
    
    return text_data

# Example usage
pdf_path = './jensen.pdf'
extracted_text = extract_text_from_pdf(pdf_path)
for page_text in extracted_text:
    print(page_text)
