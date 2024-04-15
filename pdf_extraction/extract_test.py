# import re
# import PyPDF2

# def extract_contributions(pdf_path):
#     with open(pdf_path, "rb") as file:
#         pdf_reader = PyPDF2.PdfReader(file)
#         text_data = []
#         for page in pdf_reader.pages:#[7:9]:  # Assuming you need only pages 8 and 9 (0-indexed)
#             text = page.extract_text()
#             if text:
#                 contributions = re.findall(r'(In Kind \b[A-Za-z\s,]+\b\s*Total Cash Date\s*(?:[^\n]*\n)+?.*?Total)', text, re.DOTALL)
#                 #contributions = re.findall(r'(In Kind (.*?), (.*) Total)', text, re.DOTALL) # This regex returns less specific/good data.
#                 text_data.extend(contributions)
#         return text_data

# # Example usage
# pdf_path = './pdf_extraction/jensen.pdf'
# extracted_data = extract_contributions(pdf_path)
# for data in extracted_data[:20]:
#     print(f"{data} \n")
    
    
    
import re
import PyPDF2

def extract_contributions(pdf_path):
    with open(pdf_path, "rb") as file:
        pdf_reader = PyPDF2.PdfReader(file)
        data = []
        for page in pdf_reader.pages:
            text = page.extract_text()
            if text:
                contributions = re.findall(r'(In Kind (\b[A-Za-z\s,]+\b)\s*Total Cash Date\s*([^\n]*\n)+?.*?Total)', text, re.DOTALL)
                for contribution in contributions:
                    data_dict = {}
                    names = contribution[1].strip('\n').split(',')
                    data_dict['last_name'] = names[0].strip()
                    data_dict['first_name'] = names[1].strip() if len(names) > 1 else ''
                    data_dict['address'] = contribution[2].strip()
                    data_dict['contributions'] = []
                    contribution_lines = contribution[0].split('\n')[3:-1]  # Skip the first 3 lines and the last line
                    for line in contribution_lines:
                        contribution_dict = {}
                        parts = line.split()
                        if len(parts) >= 2:
                            contribution_dict['date'] = parts[0]
                            contribution_dict['amount'] = parts[1]
                            data_dict['contributions'].append(contribution_dict)
                    data.append(data_dict)
        return data

# Example usage
pdf_path = './pdf_extraction/jensen.pdf'
extracted_data = extract_contributions(pdf_path)
for data in extracted_data[:20]:
    print(f"{data}")