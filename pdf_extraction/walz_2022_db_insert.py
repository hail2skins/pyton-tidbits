import re
import PyPDF2
import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import datetime
from decouple import config

def connect_db():
    # # Connect to the PostgreSQL server
    # conn = psycopg2.connect(
    #     host=config('LOCALHOST_DB_HOST'), 
    #     user=config('LOCALHOST_DB_USER'), 
    #     password=config('LOCALHOST_DB_PASSWORD'), 
    #     dbname=config('LOCALHOST_DB_NAME'),
    #     )
    # conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    # return conn
    
    # Connect to the PostgreSQL server
    conn = psycopg2.connect(
        host=config('DEV_DB_HOST'),
        dbname=config('DEV_DB_NAME'),
        user=config('DEV_DB_USER'),
        password=config('DEV_DB_PASSWORD')
        )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    return conn

def insert_data(conn, data, entity_id=1):  # Default entity_id to 1
    cursor = conn.cursor()
    review_count = 0
    for donor in data:
        try:
            # Ensure all required fields are present
            if not all(k in donor for k in ('last_name', 'first_name', 'street_number', 'street_name', 'city', 'state', 'zip_code', 'needs_review', 'contributions')):
                print("Missing data fields in donor information, skipping:", donor)
                continue

            # Insert into donors table as before
            cursor.execute("""
                INSERT INTO donors_donor (last_name, first_name, street_number, street_name, city, state, zip_code, needs_review) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id
            """, (donor['last_name'], donor['first_name'], donor['street_number'], donor['street_name'], donor['city'], donor['state'], donor['zip_code'], donor['needs_review']))
            donor_id = cursor.fetchone()[0]
            
            for contribution in donor['contributions']:
                # Include entity_id in the INSERT statement
                cursor.execute("""
                    INSERT INTO donors_contribution (donor_id, entity_id, date, amount) 
                    VALUES (%s, %s, %s, %s)
                """, (donor_id, entity_id, contribution['date'], contribution['amount']))
        except KeyError as e:
            print(f"Key error: {e} in donor data, please check the data structure.")
            review_count += 1
        except Exception as e:
            print(f"Unexpected error: {e}, rolling back transaction.")
            conn.rollback()
            continue

    conn.commit()
    cursor.close()
    print(f"All data has been successfully inserted. {review_count} addresses need review.")
    return review_count




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


    
    # Main execution
if __name__ == "__main__":
    conn = connect_db()
    pdf_path = './pdf_extraction/walz.pdf'
    extracted_data = extract_contributions(pdf_path)
    print(f"Extracted {len(extracted_data)} donors.")
    
    if extracted_data:
        review_count = insert_data(conn, extracted_data, entity_id=2)  # Pass the entity_id here if different from 1
        print(f"{review_count} addresses need review.")
    
    conn.close()
