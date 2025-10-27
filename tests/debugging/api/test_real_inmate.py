"""
Test the jail API with a real inmate currently in custody.

This script:
1. Fetches the current confinement list to find real inmates
2. Picks one inmate from the list
3. Tests our API client with that inmate's name
4. Verifies we get "in custody" result
"""

import sys
sys.path.insert(0, r'C:\Github\jail-checker\src')

import requests
from bs4 import BeautifulSoup
from jail_api import JailAPIClient
from models import Defendant

print("="*80)
print("JAIL API VERIFICATION TEST")
print("="*80)

# Step 1: Get current inmates from the jail
print("\n[Step 1] Fetching current inmates from jail...")

url = "https://cc.southernsoftware.com/bookingsearch/fetchesforajax/fetch_current_confinements.php"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Referer': 'https://cc.southernsoftware.com/bookingsearch/index.php?AgencyID=DorchesterCoSC'
}

payload = {
    'JMSAgencyID': 'SC018013C',
    'search': '',
    'agency': '',
    'sort': 'name',
    'IDX': 1
}

response = requests.post(url, headers=headers, data=payload)

if response.status_code != 200:
    print(f"ERROR: Failed to fetch inmates. Status code: {response.status_code}")
    sys.exit(1)

print(f"✓ Successfully fetched data from jail (Status: {response.status_code})")

# Step 2: Parse the response to extract inmate names
soup = BeautifulSoup(response.text, 'html.parser')

# Look for inmate cards or name elements
# The API returns HTML with booking information
# We need to find names in the response

# Try to find any text that looks like names
print("\n[Step 2] Parsing inmate data...")
print(f"Response length: {len(response.text)} characters")

# Show a sample of the response to understand format
print("\nFirst 500 characters of response:")
print(response.text[:500])
print("\n...")

# Try to extract names from common HTML patterns
names = []

# Pattern 1: Look for booking cards
booking_cards = soup.find_all('div', class_='booking-card')
if booking_cards:
    print(f"\nFound {len(booking_cards)} booking cards")
    for card in booking_cards[:5]:  # Look at first 5
        # Try to find name element
        name_elem = card.find('div', class_='name') or card.find('h3') or card.find('strong')
        if name_elem:
            names.append(name_elem.get_text(strip=True))

# Pattern 2: Look for table rows
rows = soup.find_all('tr')
if rows and not booking_cards:
    print(f"\nFound {len(rows)} table rows")
    for row in rows[:10]:
        cells = row.find_all('td')
        if cells and len(cells) > 0:
            # First cell might be name
            text = cells[0].get_text(strip=True)
            if text and len(text) > 3 and ',' in text:  # Looks like a name
                names.append(text)

# Pattern 3: Just look for any text with comma (name format)
if not names:
    print("\nTrying pattern matching on raw text...")
    import re
    # Look for "Last, First" pattern
    name_pattern = r'\b[A-Z][a-z]+,\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)?\b'
    found_names = re.findall(name_pattern, response.text)
    if found_names:
        names = list(set(found_names))[:10]  # Unique names, max 10

if not names:
    print("\nERROR: Could not find any inmate names in the response")
    print("Response might be empty or formatted differently than expected")
    print("\nFull response:")
    print(response.text)
    sys.exit(1)

print(f"\n✓ Found {len(names)} inmate names")
print("\nFirst few inmates:")
for i, name in enumerate(names[:5], 1):
    print(f"  {i}. {name}")

# Step 3: Pick one inmate and test our API
test_name = names[0]
print(f"\n[Step 3] Testing API with inmate: {test_name}")

# Parse the name
if ',' in test_name:
    parts = test_name.split(',', 1)
    last_name = parts[0].strip()
    first_parts = parts[1].strip().split()
    first_name = first_parts[0] if first_parts else ""
    middle_name = ' '.join(first_parts[1:]) if len(first_parts) > 1 else ""
else:
    parts = test_name.split()
    first_name = parts[0] if parts else ""
    last_name = parts[-1] if len(parts) > 1 else ""
    middle_name = ' '.join(parts[1:-1]) if len(parts) > 2 else ""

print(f"  Parsed name: First='{first_name}', Middle='{middle_name}', Last='{last_name}'")

# Create defendant and search
defendant = Defendant(
    last_name=last_name,
    first_name=first_name,
    middle_name=middle_name
)

print(f"\n[Step 4] Searching jail database for: {defendant.full_name}")

client = JailAPIClient()
result = client.check_custody(defendant)
client.close()

print("\n" + "="*80)
print("TEST RESULTS")
print("="*80)
print(f"Defendant: {result.defendant_name}")
print(f"In Custody: {result.in_custody}")
print(f"Status: {result.status_summary}")

if result.in_custody:
    print("\n✓ SUCCESS: API correctly identified inmate as IN CUSTODY")
    if result.booking_number:
        print(f"  Booking Number: {result.booking_number}")
    if result.booking_date:
        print(f"  Booking Date: {result.booking_date}")
    if result.charges_at_booking:
        print(f"  Charges: {result.charges_at_booking}")
else:
    print("\n✗ FAILURE: API did not detect inmate as in custody")
    print("  This inmate is confirmed to be in custody (from current confinements list)")
    print("  But our API search returned 'not in custody'")
    print("\n  Possible issues:")
    print("  - Name parsing/formatting mismatch")
    print("  - Search endpoint not working as expected")
    print("  - HTML parsing issue in jail_api.py")

if result.error_message:
    print(f"\nError Message: {result.error_message}")

print("\n" + "="*80)
