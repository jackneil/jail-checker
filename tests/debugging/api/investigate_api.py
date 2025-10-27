"""
Script to reverse-engineer the Dorchester County jail search API.
"""

import requests
from bs4 import BeautifulSoup
import json
import re

# Target URL
BASE_URL = "https://cc.southernsoftware.com/bookingsearch/index.php?AgencyID=DorchesterCoSC"

def fetch_search_page():
    """Fetch the main search page and analyze its structure."""
    print("=" * 80)
    print("STEP 1: Fetching search page HTML")
    print("=" * 80)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    try:
        response = requests.get(BASE_URL, headers=headers, timeout=30)
        print(f"Status Code: {response.status_code}")
        print(f"Content-Type: {response.headers.get('Content-Type', 'N/A')}")
        print(f"Content-Length: {len(response.text)} bytes\n")

        if response.status_code == 200:
            # Save raw HTML for inspection
            with open('C:\\Github\\jail-checker\\search_page.html', 'w', encoding='utf-8') as f:
                f.write(response.text)
            print("[OK] Saved HTML to search_page.html\n")

            # Parse HTML
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find all forms
            print("-" * 80)
            print("FORMS FOUND:")
            print("-" * 80)
            forms = soup.find_all('form')
            for i, form in enumerate(forms, 1):
                print(f"\nForm #{i}:")
                print(f"  Action: {form.get('action', 'N/A')}")
                print(f"  Method: {form.get('method', 'N/A')}")
                print(f"  ID: {form.get('id', 'N/A')}")
                print(f"  Name: {form.get('name', 'N/A')}")

                # Find all inputs in this form
                inputs = form.find_all(['input', 'select', 'textarea'])
                if inputs:
                    print(f"  Inputs ({len(inputs)}):")
                    for inp in inputs:
                        inp_type = inp.get('type', inp.name)
                        inp_name = inp.get('name', 'N/A')
                        inp_id = inp.get('id', 'N/A')
                        inp_value = inp.get('value', '')
                        print(f"    - {inp_type}: name='{inp_name}', id='{inp_id}', value='{inp_value}'")

            # Find all scripts
            print("\n" + "-" * 80)
            print("JAVASCRIPT FILES REFERENCED:")
            print("-" * 80)
            scripts = soup.find_all('script', src=True)
            for script in scripts:
                print(f"  - {script.get('src')}")

            # Find inline JavaScript
            print("\n" + "-" * 80)
            print("INLINE JAVASCRIPT:")
            print("-" * 80)
            inline_scripts = soup.find_all('script', src=False)
            for i, script in enumerate(inline_scripts, 1):
                script_content = script.string
                if script_content and len(script_content.strip()) > 0:
                    print(f"\n  Script Block #{i}:")
                    print(f"  {'-' * 76}")
                    # Print first 500 chars of each script block
                    content = script_content.strip()
                    if len(content) > 1000:
                        print(f"  {content[:1000]}...")
                        print(f"  [... {len(content) - 1000} more characters ...]")
                    else:
                        print(f"  {content}")

            # Look for AJAX/API endpoints in the HTML
            print("\n" + "-" * 80)
            print("POTENTIAL API ENDPOINTS IN HTML:")
            print("-" * 80)
            # Search for common patterns
            api_patterns = [
                r'(https?://[^\s\'"]+\.php[^\s\'"]*)',
                r'(\/[a-zA-Z0-9_\/]+\.php[^\s\'"]*)',
                r'url\s*:\s*[\'"]([^\'"]+)[\'"]',
                r'fetch\([\'"]([^\'"]+)[\'"]',
                r'ajax\([\'"]([^\'"]+)[\'"]',
            ]

            found_endpoints = set()
            for pattern in api_patterns:
                matches = re.findall(pattern, response.text)
                for match in matches:
                    if isinstance(match, tuple):
                        found_endpoints.update(match)
                    else:
                        found_endpoints.add(match)

            if found_endpoints:
                for endpoint in sorted(found_endpoints):
                    if endpoint and 'php' in endpoint:
                        print(f"  - {endpoint}")
            else:
                print("  No obvious API endpoints found in HTML")

            return response, soup
        else:
            print(f"[ERROR] Failed to fetch page: {response.status_code}")
            # Still try to save and parse the error page
            with open('C:\\Github\\jail-checker\\search_page.html', 'w', encoding='utf-8') as f:
                f.write(response.text)
            print("[OK] Saved error page to search_page.html for analysis\n")

            soup = BeautifulSoup(response.text, 'html.parser')
            return response, soup

    except Exception as e:
        print(f"[ERROR] Error fetching page: {e}")
        import traceback
        traceback.print_exc()
        return None, None


def test_search_submission(soup):
    """Try to submit a test search and capture the backend call."""
    print("\n" + "=" * 80)
    print("STEP 2: Attempting test search submission")
    print("=" * 80)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': BASE_URL,
    }

    # Try to find the search form
    forms = soup.find_all('form')
    if not forms:
        print("[ERROR] No forms found on page")
        return

    # Use the first form (usually the search form)
    form = forms[0]
    action = form.get('action', '')
    method = form.get('method', 'GET').upper()

    print(f"Form action: {action}")
    print(f"Form method: {method}")

    # Build the submission URL
    if action:
        if action.startswith('http'):
            submit_url = action
        elif action.startswith('/'):
            submit_url = f"https://cc.southernsoftware.com{action}"
        else:
            submit_url = f"https://cc.southernsoftware.com/bookingsearch/{action}"
    else:
        # If no action, submit to same page
        submit_url = BASE_URL

    print(f"Submission URL: {submit_url}\n")

    # Collect form inputs and build payload
    inputs = form.find_all(['input', 'select', 'textarea'])
    payload = {}

    for inp in inputs:
        inp_name = inp.get('name')
        inp_type = inp.get('type', inp.name)
        inp_value = inp.get('value', '')

        if inp_name:
            # Set default values for common fields
            if 'name' in inp_name.lower() and 'last' in inp_name.lower():
                payload[inp_name] = 'Smith'
            elif 'name' in inp_name.lower() and 'first' in inp_name.lower():
                payload[inp_name] = 'John'
            elif inp_type == 'hidden':
                payload[inp_name] = inp_value
            elif inp_type == 'text' and not payload.get(inp_name):
                payload[inp_name] = ''
            elif inp_type == 'submit':
                continue
            else:
                payload[inp_name] = inp_value

    # Add AgencyID if not in payload
    if 'AgencyID' not in payload:
        payload['AgencyID'] = 'DorchesterCoSC'

    print("Payload:")
    for key, value in payload.items():
        print(f"  {key}: {value}")

    try:
        print(f"\nSubmitting {method} request...")

        if method == 'POST':
            response = requests.post(submit_url, data=payload, headers=headers, timeout=30, allow_redirects=True)
        else:
            response = requests.get(submit_url, params=payload, headers=headers, timeout=30, allow_redirects=True)

        print(f"Response Status: {response.status_code}")
        print(f"Response URL: {response.url}")
        print(f"Content-Type: {response.headers.get('Content-Type', 'N/A')}")
        print(f"Content-Length: {len(response.text)} bytes")

        # Save response
        with open('C:\\Github\\jail-checker\\search_result.html', 'w', encoding='utf-8') as f:
            f.write(response.text)
        print("\n[OK] Saved response to search_result.html")

        # Try to determine response format
        content_type = response.headers.get('Content-Type', '').lower()
        if 'json' in content_type:
            print("\nResponse format: JSON")
            try:
                data = response.json()
                print(json.dumps(data, indent=2)[:500])
            except:
                print("Could not parse as JSON")
        elif 'xml' in content_type:
            print("\nResponse format: XML")
        else:
            print("\nResponse format: HTML")
            # Parse results
            result_soup = BeautifulSoup(response.text, 'html.parser')

            # Look for result tables
            tables = result_soup.find_all('table')
            print(f"\nTables found: {len(tables)}")

            if tables:
                print("\nFirst table structure:")
                first_table = tables[0]
                headers = first_table.find_all('th')
                if headers:
                    print(f"  Headers: {[th.get_text(strip=True) for th in headers]}")

                rows = first_table.find_all('tr')
                print(f"  Rows: {len(rows)}")

                if len(rows) > 1:
                    print("\n  Sample row:")
                    cells = rows[1].find_all(['td', 'th'])
                    for cell in cells:
                        print(f"    - {cell.get_text(strip=True)}")

    except Exception as e:
        print(f"[ERROR] Error submitting search: {e}")
        import traceback
        traceback.print_exc()


def check_for_api_endpoints():
    """Look for API endpoints by checking common paths."""
    print("\n" + "=" * 80)
    print("STEP 3: Checking for API endpoints")
    print("=" * 80)

    common_paths = [
        '/bookingsearch/api/',
        '/bookingsearch/search.php',
        '/bookingsearch/results.php',
        '/bookingsearch/ajax/',
        '/bookingsearch/api.php',
        '/api/',
        '/search/',
    ]

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    for path in common_paths:
        url = f"https://cc.southernsoftware.com{path}"
        try:
            response = requests.head(url, headers=headers, timeout=10, allow_redirects=False)
            print(f"{url}: {response.status_code}")
            if response.status_code in [200, 301, 302]:
                print(f"  -> Might be valid!")
        except:
            print(f"{url}: No response")


if __name__ == "__main__":
    print("\nDORCHESTER COUNTY JAIL API INVESTIGATION")
    print("=" * 80)

    response, soup = fetch_search_page()

    if soup:
        test_search_submission(soup)

    check_for_api_endpoints()

    print("\n" + "=" * 80)
    print("INVESTIGATION COMPLETE")
    print("=" * 80)
    print("\nCheck the following files for details:")
    print("  - search_page.html (original search form)")
    print("  - search_result.html (search results)")
