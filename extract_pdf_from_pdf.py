import PyPDF2

def extract_pages(pdf_path, output_path, start_page, end_page):
    # Create a PDF reader object
    with open(pdf_path, "rb") as infile:
        reader = PyPDF2.PdfReader(infile)
        writer = PyPDF2.PdfWriter()
        
        # Page numbers are zero-indexed in PyPDF2, adjust accordingly
        for page_num in range(start_page - 1, end_page):
            # Add pages to the writer object
            writer.add_page(reader.pages[page_num])
        
        # Write out the new PDF
        with open(output_path, "wb") as outfile:
            writer.write(outfile)

# Specify the path to your original PDF and the output PDF
pdf_path = './jensen.pdf'
output_path = './extracted_pages.pdf'

# Call the function with the range of pages you want to extract
extract_pages(pdf_path, output_path, 8, 15)
