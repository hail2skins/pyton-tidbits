# Description: Extract text from specific pages of a PDF file

import PyPDF2

def extract_text_from_specific_pages(pdf_path, start_page, end_page):
    with open(pdf_path, "rb") as file:
        pdf_reader = PyPDF2.PdfReader(file)
        text_data = []
        # Adjust for zero-based index; PyPDF2 uses zero-based indexing for pages
        for page_num in range(start_page - 1, end_page):
            page = pdf_reader.pages[page_num]
            text_data.append(page.extract_text())
    return text_data

# Example usage
pdf_path = './jensen.pdf'
start_page = 8
end_page = 9
extracted_text = extract_text_from_specific_pages(pdf_path, start_page, end_page)
for page_text in extracted_text:
    print(page_text[:1000])

