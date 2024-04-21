import re
import PyPDF2
import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import datetime

def create_database():
    # Connect to the default database
    conn = psycopg2.connect(host="localhost", user="postgres", password="P@ssw0rd", dbname="postgres")
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)  # Allows us to execute database creation statements
    cursor = conn.cursor()

    # Check if the database exists
    cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'contributions_db'")
    exists = cursor.fetchone()
    if not exists:
        # Create the database if it doesn't exist
        cursor.execute("CREATE DATABASE contributions_db")
    
    cursor.close()
    conn.close()

def connect_db():
    # # Connect to the PostgreSQL server
    # conn = psycopg2.connect(host="localhost", dbname="contributions_db", user="postgres", password="P@ssw0rd")
    # conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    # return conn
    
    # Connect to the PostgreSQL server
    conn = psycopg2.connect(host="hamcoisawsdev.cha6q6wsia21.us-east-2.rds.amazonaws.com", dbname="hamco-dev", user="dbadmin", password="Sk!n54ever")
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    return conn

def create_tables(conn):
    cursor = conn.cursor()
    # Drop existing tables if they exist
    cursor.execute("""
        DROP TABLE IF EXISTS contributions;
        DROP TABLE IF EXISTS donors;
    """)
    # Create the 'donors' table with a 'needs_review' boolean field
    cursor.execute("""
        CREATE TABLE donors (
            id SERIAL PRIMARY KEY,
            last_name VARCHAR(255),
            first_name VARCHAR(255),
            street_number VARCHAR(255),
            street_name TEXT,
            city VARCHAR(255),
            state CHAR(2),
            zip CHAR(5),
            needs_review BOOLEAN DEFAULT FALSE
        )
    """)
    # Create the 'contributions' table
    cursor.execute("""
        CREATE TABLE contributions (
            id SERIAL PRIMARY KEY,
            donor_id INTEGER REFERENCES donors(id),
            date DATE,
            amount NUMERIC(10, 2)
        )
    """)
    # Commit changes and close cursor
    conn.commit()
    cursor.close()


def insert_data(conn, data):
    cursor = conn.cursor()
    review_count = 0  # Initialize review count
    for donor in data:
        # Include the needs_review in the INSERT statement
        cursor.execute("""
            INSERT INTO donors (last_name, first_name, street_number, street_name, city, state, zip, needs_review) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id
        """, (donor['last_name'], donor['first_name'], donor['street_number'], donor['street_name'], donor['city'], donor['state'], donor['zip_code'], donor['needs_review']))
        donor_id = cursor.fetchone()[0]
        if donor['needs_review']:
            review_count += 1
        for contribution in donor['contributions']:
            cursor.execute("""
                INSERT INTO contributions (donor_id, date, amount) 
                VALUES (%s, %s, %s)
            """, (donor_id, contribution['date'], contribution['amount']))
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
                    data_dict.update(address_info)  # Update data_dict with address info
                    data_dict['contributions'] = []
                    contribution_lines = contribution[0].split('\n')[3:-1]
                    for line in contribution_lines:
                        parts = line.split()
                        if len(parts) >= 2 and validate_date(parts[0]) and validate_amount(parts[1]):
                            contribution_dict = {
                                'date': parts[0],
                                'amount': parts[1].replace(',', '')  # Clean amount data here as well
                            }
                            data_dict['contributions'].append(contribution_dict)
                        else:
                            print(f"Skipping invalid data {parts}")
                    data.append(data_dict)
        return data



# Main execution
# Main execution
if __name__ == "__main__":
    #create_database()  # Ensure the database exists
    conn = connect_db()  # Connect to the database
    #create_tables(conn)  # Create necessary tables if not already present
    
    pdf_path = './pdf_extraction/jensen.pdf'
    extracted_data = extract_contributions(pdf_path)
    print(f"Extracted {len(extracted_data)} donors.")
    
    if extracted_data:
        review_count = insert_data(conn, extracted_data)
        print(f"{review_count} addresses need review.")
    
    conn.close()  # Close the database connection
