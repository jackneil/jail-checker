"""
Test script to demonstrate all Dorchester County jail search API endpoints.

This script tests each endpoint that was discovered through reverse engineering
the booking search website.
"""

import requests
import json
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

# Base configuration
BASE_URL = "https://cc.southernsoftware.com/bookingsearch"
AGENCY_ID = "SC018013C"  # Dorchester County JMS Agency ID

# Standard headers to mimic browser requests
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Referer': f'{BASE_URL}/index.php?AgencyID=DorchesterCoSC',
    'Content-Type': 'application/x-www-form-urlencoded',
}


def test_search_by_name(first_name="", middle_name="", last_name=""):
    """
    Search for inmates by name.

    Endpoint: fetchesforajax/fetch_incident_search_name.php
    Method: POST

    Parameters:
        firstname: First name (partial match allowed)
        middlename: Middle name (optional)
        lastname: Last name (partial match allowed)
        searchtype: 'name'
    """
    print("\n" + "=" * 80)
    print("TEST: Search by Name")
    print("=" * 80)

    url = f"{BASE_URL}/fetchesforajax/fetch_incident_search_name.php"

    payload = {
        'searchtype': 'name',
        'firstname': first_name,
        'middlename': middle_name,
        'lastname': last_name,
    }

    print(f"Searching for: First='{first_name}', Middle='{middle_name}', Last='{last_name}'")
    print(f"URL: {url}")
    print(f"Payload: {payload}\n")

    try:
        response = requests.post(url, headers=HEADERS, data=payload, timeout=30)
        print(f"Status Code: {response.status_code}")
        print(f"Content Length: {len(response.text)} bytes")

        if response.status_code == 200:
            # Save response
            with open('C:\\Github\\jail-checker\\test_name_search.html', 'w', encoding='utf-8') as f:
                f.write(response.text)
            print("[OK] Saved response to test_name_search.html")

            # Parse and extract key info
            soup = BeautifulSoup(response.text, 'html.parser')

            # Look for result cards or tables
            cards = soup.find_all('div', class_='card')
            print(f"\nResults found: {len(cards)} records")

            # Try to extract some sample data
            if cards and len(cards) > 0:
                print("\nSample result (first record):")
                first_card = cards[0]
                text = first_card.get_text(strip=True)
                if text:
                    print(text[:500])  # First 500 chars

            return response.text
        else:
            print(f"[ERROR] Request failed: {response.status_code}")
            return None

    except Exception as e:
        print(f"[ERROR] Exception: {e}")
        return None


def test_current_confinements():
    """
    Get all current inmates in custody.

    Endpoint: fetchesforajax/fetch_current_confinements.php
    Method: POST

    Parameters:
        JMSAgencyID: Agency identifier (SC018013C for Dorchester)
        search: Search filter (optional)
        agency: Agency filter (optional)
        sort: Sort order (name, date, etc.)
        IDX: Page index for pagination (optional)
    """
    print("\n" + "=" * 80)
    print("TEST: Get Current Confinements")
    print("=" * 80)

    url = f"{BASE_URL}/fetchesforajax/fetch_current_confinements.php"

    payload = {
        'JMSAgencyID': AGENCY_ID,
        'search': '',
        'agency': '',
        'sort': 'name',
    }

    print(f"URL: {url}")
    print(f"Payload: {payload}\n")

    try:
        response = requests.post(url, headers=HEADERS, data=payload, timeout=30)
        print(f"Status Code: {response.status_code}")
        print(f"Content Length: {len(response.text)} bytes")

        if response.status_code == 200:
            # Save response
            with open('C:\\Github\\jail-checker\\test_current_confinements.html', 'w', encoding='utf-8') as f:
                f.write(response.text)
            print("[OK] Saved response to test_current_confinements.html")

            # Parse and extract info
            soup = BeautifulSoup(response.text, 'html.parser')

            # Look for inmate records
            cards = soup.find_all('div', class_='card')
            print(f"\nCurrent inmates in custody: {len(cards)} records")

            if cards and len(cards) > 0:
                print("\nSample inmate record:")
                first_card = cards[0]
                text = first_card.get_text(strip=True)
                if text:
                    print(text[:500])

            return response.text
        else:
            print(f"[ERROR] Request failed: {response.status_code}")
            return None

    except Exception as e:
        print(f"[ERROR] Exception: {e}")
        return None


def test_last_24_hours():
    """
    Get inmates admitted in the last 24 hours.

    Endpoint: fetchesforajax/fetch_last24hours.php
    Method: POST

    Parameters:
        JMSAgencyID: Agency identifier
        IDX: Page index for pagination (optional)
    """
    print("\n" + "=" * 80)
    print("TEST: Get Last 24 Hours Admits")
    print("=" * 80)

    url = f"{BASE_URL}/fetchesforajax/fetch_last24hours.php"

    payload = {
        'JMSAgencyID': AGENCY_ID,
    }

    print(f"URL: {url}")
    print(f"Payload: {payload}\n")

    try:
        response = requests.post(url, headers=HEADERS, data=payload, timeout=30)
        print(f"Status Code: {response.status_code}")
        print(f"Content Length: {len(response.text)} bytes")

        if response.status_code == 200:
            with open('C:\\Github\\jail-checker\\test_last24hours.html', 'w', encoding='utf-8') as f:
                f.write(response.text)
            print("[OK] Saved response to test_last24hours.html")

            soup = BeautifulSoup(response.text, 'html.parser')
            cards = soup.find_all('div', class_='card')
            print(f"\nAdmits in last 24 hours: {len(cards)} records")

            return response.text
        else:
            print(f"[ERROR] Request failed: {response.status_code}")
            return None

    except Exception as e:
        print(f"[ERROR] Exception: {e}")
        return None


def test_date_range_admits(begin_date, end_date):
    """
    Get inmates admitted within a date range.

    Endpoint: fetchesforajax/fetch_incident_search_dates_admit.php
    Method: POST

    Parameters:
        searchtype: 'daterange'
        begindate: Start date (MM/DD/YYYY)
        enddate: End date (MM/DD/YYYY)
        customRadioInline1: 'customdate' or 'last24hours' or 'currentweek'
    """
    print("\n" + "=" * 80)
    print("TEST: Search Admits by Date Range")
    print("=" * 80)

    url = f"{BASE_URL}/fetchesforajax/fetch_incident_search_dates_admit.php"

    payload = {
        'searchtype': 'daterange',
        'begindate': begin_date,
        'enddate': end_date,
        'customRadioInline1': 'customdate',
    }

    print(f"Date range: {begin_date} to {end_date}")
    print(f"URL: {url}")
    print(f"Payload: {payload}\n")

    try:
        response = requests.post(url, headers=HEADERS, data=payload, timeout=30)
        print(f"Status Code: {response.status_code}")
        print(f"Content Length: {len(response.text)} bytes")

        if response.status_code == 200:
            with open('C:\\Github\\jail-checker\\test_daterange_admits.html', 'w', encoding='utf-8') as f:
                f.write(response.text)
            print("[OK] Saved response to test_daterange_admits.html")

            soup = BeautifulSoup(response.text, 'html.parser')
            cards = soup.find_all('div', class_='card')
            print(f"\nAdmits in date range: {len(cards)} records")

            return response.text
        else:
            print(f"[ERROR] Request failed: {response.status_code}")
            return None

    except Exception as e:
        print(f"[ERROR] Exception: {e}")
        return None


def test_date_range_releases(begin_date, end_date):
    """
    Get inmates released within a date range.

    Endpoint: fetchesforajax/fetch_incident_search_dates_release.php
    Method: POST

    Parameters:
        searchtype: 'daterange'
        begindate: Start date (MM/DD/YYYY)
        enddate: End date (MM/DD/YYYY)
        customRadioInline1: 'customdate' or 'last24hours' or 'currentweek'
    """
    print("\n" + "=" * 80)
    print("TEST: Search Releases by Date Range")
    print("=" * 80)

    url = f"{BASE_URL}/fetchesforajax/fetch_incident_search_dates_release.php"

    payload = {
        'searchtype': 'daterange',
        'begindate': begin_date,
        'enddate': end_date,
        'customRadioInline1': 'customdate',
    }

    print(f"Date range: {begin_date} to {end_date}")
    print(f"URL: {url}")
    print(f"Payload: {payload}\n")

    try:
        response = requests.post(url, headers=HEADERS, data=payload, timeout=30)
        print(f"Status Code: {response.status_code}")
        print(f"Content Length: {len(response.text)} bytes")

        if response.status_code == 200:
            with open('C:\\Github\\jail-checker\\test_daterange_releases.html', 'w', encoding='utf-8') as f:
                f.write(response.text)
            print("[OK] Saved response to test_daterange_releases.html")

            soup = BeautifulSoup(response.text, 'html.parser')
            cards = soup.find_all('div', class_='card')
            print(f"\nReleases in date range: {len(cards)} records")

            return response.text
        else:
            print(f"[ERROR] Request failed: {response.status_code}")
            return None

    except Exception as e:
        print(f"[ERROR] Exception: {e}")
        return None


def test_search_by_charge(charge):
    """
    Search for inmates by charge/offense.

    Endpoint: fetchesforajax/fetch_incident_search_charge.php
    Method: POST

    Parameters:
        charge: Charge description (partial match allowed)
    """
    print("\n" + "=" * 80)
    print("TEST: Search by Charge")
    print("=" * 80)

    url = f"{BASE_URL}/fetchesforajax/fetch_incident_search_charge.php"

    payload = {
        'charge': charge,
    }

    print(f"Searching for charge: '{charge}'")
    print(f"URL: {url}")
    print(f"Payload: {payload}\n")

    try:
        response = requests.post(url, headers=HEADERS, data=payload, timeout=30)
        print(f"Status Code: {response.status_code}")
        print(f"Content Length: {len(response.text)} bytes")

        if response.status_code == 200:
            with open('C:\\Github\\jail-checker\\test_charge_search.html', 'w', encoding='utf-8') as f:
                f.write(response.text)
            print("[OK] Saved response to test_charge_search.html")

            soup = BeautifulSoup(response.text, 'html.parser')
            cards = soup.find_all('div', class_='card')
            print(f"\nResults with charge '{charge}': {len(cards)} records")

            return response.text
        else:
            print(f"[ERROR] Request failed: {response.status_code}")
            return None

    except Exception as e:
        print(f"[ERROR] Exception: {e}")
        return None


def test_search_by_arresting_agency(agency):
    """
    Search for inmates by arresting agency.

    Endpoint: fetchesforajax/fetch_incident_search_arrestagency.php
    Method: POST

    Parameters:
        ArrestAgency: Agency name/code
    """
    print("\n" + "=" * 80)
    print("TEST: Search by Arresting Agency")
    print("=" * 80)

    url = f"{BASE_URL}/fetchesforajax/fetch_incident_search_arrestagency.php"

    payload = {
        'ArrestAgency': agency,
    }

    print(f"Searching for agency: '{agency}'")
    print(f"URL: {url}")
    print(f"Payload: {payload}\n")

    try:
        response = requests.post(url, headers=HEADERS, data=payload, timeout=30)
        print(f"Status Code: {response.status_code}")
        print(f"Content Length: {len(response.text)} bytes")

        if response.status_code == 200:
            with open('C:\\Github\\jail-checker\\test_agency_search.html', 'w', encoding='utf-8') as f:
                f.write(response.text)
            print("[OK] Saved response to test_agency_search.html")

            soup = BeautifulSoup(response.text, 'html.parser')
            cards = soup.find_all('div', class_='card')
            print(f"\nResults for agency '{agency}': {len(cards)} records")

            return response.text
        else:
            print(f"[ERROR] Request failed: {response.status_code}")
            return None

    except Exception as e:
        print(f"[ERROR] Exception: {e}")
        return None


def run_all_tests():
    """Run all test cases."""
    print("\n")
    print("*" * 80)
    print("DORCHESTER COUNTY JAIL API - COMPREHENSIVE TEST SUITE")
    print("*" * 80)

    # Test 1: Current confinements (most important for your use case)
    test_current_confinements()

    # Test 2: Last 24 hours
    test_last_24_hours()

    # Test 3: Search by name (test with common name)
    test_search_by_name(first_name="", middle_name="", last_name="Smith")

    # Test 4: Date range admits (last 7 days)
    today = datetime.now()
    week_ago = today - timedelta(days=7)
    test_date_range_admits(
        week_ago.strftime("%m/%d/%Y"),
        today.strftime("%m/%d/%Y")
    )

    # Test 5: Date range releases (last 7 days)
    test_date_range_releases(
        week_ago.strftime("%m/%d/%Y"),
        today.strftime("%m/%d/%Y")
    )

    # Test 6: Search by charge
    test_search_by_charge("DUI")

    # Test 7: Search by agency
    test_search_by_arresting_agency("SUMMERVILLE - SC0180200")

    print("\n")
    print("*" * 80)
    print("ALL TESTS COMPLETE")
    print("*" * 80)
    print("\nCheck the following files for detailed responses:")
    print("  - test_current_confinements.html (all current inmates)")
    print("  - test_last24hours.html (recent admits)")
    print("  - test_name_search.html (name search results)")
    print("  - test_daterange_admits.html (admits by date)")
    print("  - test_daterange_releases.html (releases by date)")
    print("  - test_charge_search.html (search by charge)")
    print("  - test_agency_search.html (search by agency)")


if __name__ == "__main__":
    run_all_tests()
