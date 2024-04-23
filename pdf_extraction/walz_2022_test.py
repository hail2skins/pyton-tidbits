import re
import datetime
import PyPDF2

def validate_date(date_text):
    try:
        datetime.datetime.strptime(date_text, '%m/%d/%Y')  # Correct format
        return True
    except ValueError:
        return False

def validate_amount(amount_text):
    amount_text = amount_text.replace(',', '')  # Remove commas
    try:
        float(amount_text)  # Convert to float
        return True
    except ValueError:
        return False

def parse_address(address):
    # Regex to extract the street, city, state, and zip code parts
    match = re.search(r'^(\d+)\s+(.+?)\s+([A-Za-z\s]+),\s+([A-Z]{2})\s+(\d{5})', address)
    if match:
        return {
            'street_number': match.group(1),
            'street_name': match.group(2),
            'city': match.group(3),
            'state': match.group(4),
            'zip_code': match.group(5)[:5],
            'needs_review': False
        }
    else:
        return {'needs_review': True}  # Mark for review if the address does not match the expected format

def extract_contributions(pdf_path):
    with open(pdf_path, "rb") as file:
        pdf_reader = PyPDF2.PdfReader(file)
        data = []
        review_count = 0
        for page_number, page in enumerate(pdf_reader.pages, 1):
            text = page.extract_text()
            print(f"Processing text from page {page_number}")
            if text:
                contributions = re.findall(
                    r"([A-Za-z\s,]+)\n([^\n]*\d{5})\n\s*Employment:.*?\nDate\s+Cash\s+In\s+kind\s+Total\n((?:(?:\d{2}/\d{2}/\d{4}\s+[0-9,]+\.\d{2}\s+0\.00\s+[0-9,]+\.\d{2}\n)+)(?:Total\s+[0-9,]+\.\d{2}\s+0\.00\s+[0-9,]+\.\d{2})?)",
                    text, re.DOTALL
                )
                print(f"{len(contributions)} contributions found on page {page_number}")
                for name, address, contributions_text in contributions:
                    data_dict = {}
                    names = name.strip().split(',')
                    data_dict['last_name'] = names[0].strip()
                    data_dict['first_name'] = ' '.join(names[1:]).strip() if len(names) > 1 else ''
                    
                    address_info = parse_address(address.strip())
                    data_dict.update(address_info)  # Update data_dict with address info
                    
                    contributions_list = []
                    for date, cash in re.findall(r"(\d{2}/\d{2}/\d{4})\s+([0-9,]+\.\d{2})", contributions_text):
                        if validate_date(date):
                            contribution_detail = {
                                'date': date,
                                'amount': cash.replace(',', '')  # Remove commas for validation or database storage
                            }
                            contributions_list.append(contribution_detail)
                            print(f"Adding Contribution: {contribution_detail}")  # Print each contribution detail

                    data_dict['contributions'] = contributions_list
                    
                    data.append(data_dict)
                    if not contributions_list:
                        review_count += 1

                    print("Data Dictionary for Insertion:")
                    print(data_dict)  # Display the complete data dictionary for each donor
        return data, review_count

# Example usage
pdf_path = './pdf_extraction/walz.pdf'
extracted_data, review_count = extract_contributions(pdf_path)
print(f"Extracted {len(extracted_data)} entries, {review_count} need review")
