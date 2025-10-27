"""
Test the updated jail API with known inmates.
"""
import sys
sys.path.insert(0, r'C:\Github\jail-checker\src')

from jail_api import JailAPIClient
from models import Defendant

print("=" * 80)
print("TESTING UPDATED JAIL API")
print("=" * 80)

# Test with Avery Arron Adams (we know he's in custody)
print("\n[Test 1] Known inmate: AVERY ARRON ADAMS")
defendant1 = Defendant(last_name="ADAMS", first_name="AVERY", middle_name="ARRON")
client = JailAPIClient()
result1 = client.check_custody(defendant1)
print(f"  Result: {result1.status_summary}")
print(f"  In Custody: {result1.in_custody}")

# Test with someone we know is NOT in custody
print("\n[Test 2] Known non-inmate: John Smith")
defendant2 = Defendant(last_name="Smith", first_name="John")
result2 = client.check_custody(defendant2)
print(f"  Result: {result2.status_summary}")
print(f"  In Custody: {result2.in_custody}")

# Test with another known inmate
print("\n[Test 3] Known inmate: DALTON LOREN ADAMS")
defendant3 = Defendant(last_name="ADAMS", first_name="DALTON", middle_name="LOREN")
result3 = client.check_custody(defendant3)
print(f"  Result: {result3.status_summary}")
print(f"  In Custody: {result3.in_custody}")

client.close()

print("\n" + "=" * 80)
print("TEST COMPLETE")
print("=" * 80)
