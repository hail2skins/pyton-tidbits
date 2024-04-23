import re
import PyPDF2
import datetime

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
    
    
# def extract_contributions(pdf_path):
#     with open(pdf_path, "rb") as file:
#         pdf_reader = PyPDF2.PdfReader(file)
#         data = []
#         for page in pdf_reader.pages:
#             text = page.extract_text()
#             if text:
#                 contributions = re.findall(r'(In Kind (\b[A-Za-z\s,]+\b)\s*Total Cash Date\s*([^\n]*\n)+?.*?Total)', text, re.DOTALL)
#                 for contribution in contributions:
#                     data_dict = {}
#                     names = contribution[1].strip('\n').split(',')
#                     data_dict['last_name'] = names[0].strip()
#                     data_dict['first_name'] = names[1].strip() if len(names) > 1 else ''
#                     data_dict['address'] = contribution[2].strip()
#                     data_dict['contributions'] = []
#                     contribution_lines = contribution[0].split('\n')[3:-1]  # Skip the first 3 lines and the last line
#                     for line in contribution_lines:
#                         contribution_dict = {}
#                         parts = line.split()
#                         if len(parts) >= 2:
#                             contribution_dict['date'] = parts[0]
#                             contribution_dict['amount'] = parts[1]
#                             data_dict['contributions'].append(contribution_dict)
#                     data.append(data_dict)
#         return data


def validate_date(date_text):
    try:
        datetime.datetime.strptime(date_text, '%m/%d/%y')  # Check if date is in the correct format
        return True
    except ValueError:
        return False

def validate_amount(amount_text):
    amount_text = amount_text.replace(',', '')  # Remove commas for validation
    try:
        float(amount_text)  # Try converting to float
        return True
    except ValueError:
        return False

def parse_address(address):
    # Enhanced regex to handle more complex street names and separate them from city names
    match = re.search(r'^(\d+)\s+(.*?)(?=\s+(?:\b[A-Z][a-z]+){1,2},\s+[A-Z]{2}\s+\d{5})\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?),\s*([A-Z]{2})\s+(\d{5})$', address)
    if match:
        # Address components are extracted based on expected pattern matches
        return {
            'street_number': match.group(1),
            'street_name': match.group(2),
            'city': match.group(3),
            'state': match.group(4),
            'zip_code': match.group(5),
            'needs_review': False
        }
    else:
        # Attempt a simpler extraction for unusual or incomplete addresses
        simpler_match = re.search(r'([A-Z]{2})\s+(\d{5})$', address)
        if simpler_match:
            return {
                'street_number': None,
                'street_name': None,
                'city': None,
                'state': simpler_match.group(1),
                'zip_code': simpler_match.group(2),
                'needs_review': True  # Flag to indicate that the address needs manual review
            }
        return {
            'street_number': None,
            'street_name': None,
            'city': None,
            'state': None,
            'zip_code': None,
            'needs_review': True
        }


def extract_contributions(pdf_path):
    with open(pdf_path, "rb") as file:
        pdf_reader = PyPDF2.PdfReader(file)
        data = []
        review_count = 0  # Counter for needs_review
        for page in pdf_reader.pages:
            text = page.extract_text()
            if text:
                contributions = re.findall(r'(In Kind (\b[A-Za-z\s,]+\b)\s*Total Cash Date\s*([^\n]*\n)+?.*?Total)', text, re.DOTALL)
                for contribution in contributions:
                    data_dict = {}
                    names = contribution[1].strip('\n').split(',')
                    data_dict['last_name'] = names[0].strip()
                    data_dict['first_name'] = names[1].strip() if len(names) > 1 else ''
                    address_info = parse_address(contribution[2].strip())
                    data_dict.update(address_info)
                    data_dict['contributions'] = []
                    if data_dict.get('needs_review'):
                        review_count += 1
                    contribution_lines = contribution[0].split('\n')[3:-1]
                    for line in contribution_lines:
                        parts = line.split()
                        if len(parts) >= 2 and validate_date(parts[0]) and validate_amount(parts[1]):
                            contribution_dict = {
                                'date': parts[0],
                                'amount': parts[1].replace(',', '')
                            }
                            data_dict['contributions'].append(contribution_dict)
                        else:
                            continue
                    data.append(data_dict)
        return data, review_count

# Example usage
pdf_path = './pdf_extraction/jensen.pdf'
extracted_data, review_count = extract_contributions(pdf_path)
with open('./pdf_extraction/output.txt', 'w') as f:  # 'w' mode to overwrite each time
    for data in extracted_data:
        address_components = [
            data.get('street_number', ''),
            data.get('street_name', ''),
            data.get('city', ''),
            data.get('state', ''),
            data.get('zip_code', '')
        ]
        full_address = ' '.join(filter(None, address_components))
        f.write(f"{full_address} - Needs Review: {data.get('needs_review', False)}\n")
    f.write(f"Total addresses needing review: {review_count}\n")  # Print count at the end of the file

print(f"Total addresses needing review: {review_count}")  # Also print to console