import re

def parse_address(address):
    # Basic pattern to handle typical U.S. street addresses
    match = re.search(r'^(\d+)\s+(.*?)(?:,|)\s+([A-Za-z\s]+?),\s*([A-Z]{2})\s+(\d{5})$', address)
    if match:
        # Address components are extracted based on expected pattern matches
        return {
            'street_number': match.group(1),
            'street_name': match.group(2),
            'city': match.group(3),
            'state': match.group(4),
            'zip_code': match.group(5)
        }
    else:
        # Attempt a simpler extraction for unusual or incomplete addresses
        simpler_match = re.search(r'([A-Z]{2})\s+(\d{5})$', address)
        if simpler_match:
            # Only state and ZIP code are reliably extracted
            return {
                'state': simpler_match.group(1),
                'zip_code': simpler_match.group(2),
                'needs_review': True  # Flag to indicate that the address needs manual review
            }
        else:
            return {'needs_review': True}

# Example tests with diverse addresses
addresses = [
    "11747 Independence Way Woodbury, MN  55129",
    "3640 Plum Creek Drive St Cloud, MN  56301",
    "Minnesota 56 Brownsdale, MN  55918",  # Example of non-standard format
    "2 Windy Hill Road Sunfish Lake, MN  55077",
    "6781 NW 12th St Ocala , FL  34482"
]

for addr in addresses:
    print(parse_address(addr))
