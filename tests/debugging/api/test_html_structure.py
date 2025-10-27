"""Test script to see what HTML structure the live API returns."""

import requests
from bs4 import BeautifulSoup
import time

# Set up session
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
    'Referer': 'https://cc.southernsoftware.com/bookingsearch/index.php?AgencyID=DorchesterCoSC',
}

session = requests.Session()
session.headers.update(headers)

# Initialize session
print("Initializing session...")
response = requests.get(
    'https://cc.southernsoftware.com/bookingsearch/index.php?AgencyID=DorchesterCoSC',
    headers=headers,
    timeout=30
)
for cookie in response.cookies:
    session.cookies.set_cookie(cookie)

time.sleep(1)

# Fetch first page of confinements
print("Fetching page 1 of current confinements...")
payload = {
    'JMSAgencyID': 'SC018013C',
    'search': '',
    'agency': '',
    'sort': 'name',
    'IDX': '1'
}

response = session.post(
    'https://cc.southernsoftware.com/bookingsearch/fetchesforajax/fetch_current_confinements.php',
    data=payload,
    headers={'Content-Type': 'application/x-www-form-urlencoded'},
    timeout=30
)

print(f"Response status: {response.status_code}")
print(f"Response length: {len(response.text)} chars")
print()

# Save HTML to file for inspection
with open(r'C:\Github\jail-checker\tests\debugging\html\debug_live_api_response.html', 'w', encoding='utf-8') as f:
    f.write(response.text)
print("Saved full HTML to debug_live_api_response.html")
print()

# Parse and check structure
soup = BeautifulSoup(response.text, 'html.parser')

# Try to find booking cards
booking_cards = soup.find_all('div', class_='booking-card')
print(f"Found {len(booking_cards)} booking cards")

if booking_cards:
    first_card = booking_cards[0]
    print("\n=== First Card HTML ===")
    print(first_card.prettify()[:1000])
    print()

    # Check for detail rows
    detail_rows = first_card.find_all('div', class_='detail-row')
    print(f"\nFound {len(detail_rows)} detail rows in first card")

    for row in detail_rows[:5]:
        label_elem = row.find('span', class_='detail-label')
        value_elem = row.find('span', class_='detail-value')
        if label_elem and value_elem:
            print(f"  {label_elem.get_text().strip()}: {value_elem.get_text().strip()}")
else:
    print("\n=== First 1000 chars of response ===")
    print(response.text[:1000])
