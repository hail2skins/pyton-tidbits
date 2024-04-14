# This script extracts text from a PDF file and writes it to a text file.

import PyPDF2

def extract_text_to_file(pdf_path, output_file):
    with open(pdf_path, "rb") as file, open(output_file, "w", encoding='utf-8') as out:
        pdf_reader = PyPDF2.PdfReader(file)
        for page in pdf_reader.pages:
            text = page.extract_text()
            if text:
                out.write(text + "\n")
