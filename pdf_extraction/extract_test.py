import re
import PyPDF2

def extract_contributions(pdf_path):
    with open(pdf_path, "rb") as file:
        pdf_reader = PyPDF2.PdfReader(file)
        text_data = []
        for page in pdf_reader.pages:#[7:9]:  # Assuming you need only pages 8 and 9 (0-indexed)
            text = page.extract_text()
            if text:
                contributions = re.findall(r'(In Kind \b[A-Za-z\s,]+\b\s*Total Cash Date\s*(?:[^\n]*\n)+?.*?Total)', text, re.DOTALL)
                #contributions = re.findall(r'(In Kind (.*?), (.*) Total)', text, re.DOTALL) # This regex returns less specific/good data.
                text_data.extend(contributions)
        return text_data

# Example usage
pdf_path = './pdf_extraction/jensen.pdf'
extracted_data = extract_contributions(pdf_path)
for data in extracted_data:
    print(f"Individual: {data} \n")
