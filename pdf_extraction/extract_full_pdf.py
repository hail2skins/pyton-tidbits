import PyPDF2

# Function to extract text from specific pages of a PDF file
def extract_text_from_pdf(pdf_path, start_page, end_page):
    # Open the PDF file
    with open(pdf_path, "rb") as file:  # rb = read binary
        # Create a PDF reader object
        pdf_reader = PyPDF2.PdfReader(file)
        
        # Extract text from specified range of pages and collect it in a list
        text_data = []
        # Ensure start and end pages are within the PDF page range
        start_page = max(start_page - 1, 0)  # Convert to 0-based index, ensure non-negative
        end_page = min(end_page, len(pdf_reader.pages))  # Ensure it does not exceed total pages
        
        for page_number in range(start_page, end_page):
            text = pdf_reader.pages[page_number].extract_text()
            if text:
                text_data.append(text)
            else:
                text_data.append("No text found on page " + str(page_number + 1))
    
    return text_data

# Example usage: extract text from page 896 to 896 (you can adjust as needed)
pdf_path = './pdf_extraction/walz.pdf'
start_page = 794
end_page = 797
extracted_text = extract_text_from_pdf(pdf_path, start_page, end_page)
for page_text in extracted_text:
    print(page_text)
