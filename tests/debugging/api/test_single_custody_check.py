"""Test script to check custody for a single defendant and see debug output."""

import sys
sys.path.insert(0, r'C:\Github\jail-checker\src')

from models import Defendant
from jail_api import JailAPIClient

# Create a test defendant who we know is in custody (Murray)
defendant = Defendant(
    last_name="Murray",
    first_name="Nicholas",
    middle_name="Edward",
    case_number="TEST001"
)

# Check custody
with JailAPIClient() as client:
    result = client.check_custody(defendant)

    print("\n=== CUSTODY CHECK RESULT ===")
    print(f"Name: {result.defendant_name}")
    print(f"In Custody: {result.in_custody}")
    print(f"Booking Date: {result.booking_date}")
    print(f"Booking Number: {result.booking_number}")
    print(f"Bond Amount: {result.bond_amount}")
    print(f"Charges: {result.charges_at_booking}")
    print(f"Mugshot URL: {result.mugshot_url}")
    print(f"Status: {result.status_summary}")
