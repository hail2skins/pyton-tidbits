import re
import PyPDF2

def extract_text_from_specific_pages(pdf_path, start_page, end_page):
    with open(pdf_path, "rb") as file:
        pdf_reader = PyPDF2.PdfReader(file)
        text_data = []
        for page_num in range(start_page - 1, end_page):  # Zero-based index; adjust accordingly
            page = pdf_reader.pages[page_num]
            text = page.extract_text()
            if text:
                text_data.append(text)
        return text_data

def extract_campaign_data(text):
    campaign_info = {}

    # Regex to dynamically capture data following each label
    committee_name_match = re.search(r"Committee name:\s*(.*?)\s*(?=\n|$)", text)
    candidate_name_match = re.search(r"Candidate name:\s*(.*?)\s*(?=\n|$)", text)
    office_district_match = re.search(r"Office and District:\s*(.*?)\s*(?=\n|$)", text)
    treasurer_name_match = re.search(r"Treasurer name:\s*(.*?)\s*(?=\n|$)", text)
    treasurer_address_match = re.search(r"Treasurer address:\s*(.*?)\s*(?=\n|$)", text)

    # Extract and clean up data for each field
    if committee_name_match:
        campaign_info['committee_name'] = committee_name_match.group(1).strip()
    if candidate_name_match:
        full_name = candidate_name_match.group(1).strip().split()
        campaign_info['candidate_firstname'] = full_name[0]
        campaign_info['candidate_lastname'] = full_name[-1]
        if len(full_name) == 3:  # Check for middle name
            campaign_info['candidate_middle'] = full_name[1]
    if office_district_match:
        campaign_info['office_district'] = office_district_match.group(1).strip()
    if treasurer_name_match:
        treasurer_full_name = treasurer_name_match.group(1).strip().split()
        campaign_info['treasurer_firstname'] = treasurer_full_name[0]
        campaign_info['treasurer_lastname'] = treasurer_full_name[-1]
        if len(treasurer_full_name) == 3:
            campaign_info['treasurer_middle'] = treasurer_full_name[1]
    if treasurer_address_match:
        campaign_info['treasurer_address'] = treasurer_address_match.group(1).strip()

    return campaign_info


# Example usage
pdf_path = './pdf_extraction/jensen.pdf'  # Adjust the path to your PDF
start_page = 1  # Starting page
end_page = 1    # Ending page, can be the same as start_page if only one page is processed

# Extract text from the specified pages
extracted_texts = extract_text_from_specific_pages(pdf_path, start_page, end_page)

# Assuming the first page contains the campaign data
if extracted_texts:
    for page_text in extracted_texts:
        campaign_data = extract_campaign_data(page_text)
        if campaign_data:  # Check if any data was extracted
            print(campaign_data)
