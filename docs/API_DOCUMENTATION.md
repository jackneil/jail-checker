# Dorchester County Jail Search API Documentation

**Reverse-Engineered from:** https://cc.southernsoftware.com/bookingsearch/index.php?AgencyID=DorchesterCoSC

**System:** Southern Software Citizen Connect - Detention Center Network (DCN)

**Date:** October 27, 2025

---

## Overview

The Dorchester County Sheriff's Office uses Southern Software's Citizen Connect platform for public access to inmate booking information. The system uses AJAX endpoints to query a backend database and return HTML fragments containing inmate records.

### Key Information

- **Base URL:** `https://cc.southernsoftware.com/bookingsearch`
- **Agency ID (Dorchester County):** `SC018013C` (JMS Agency ID)
- **URL Agency Parameter:** `DorchesterCoSC`
- **Response Format:** HTML fragments (not JSON)
- **Authentication:** None required (public access)

---

## API Endpoints

All endpoints are located under `/bookingsearch/fetchesforajax/` and use **POST** requests.

### 1. Get Current Confinements (All Inmates Currently in Custody)

**Use Case:** This is the primary endpoint for checking if specific individuals are currently in custody.

**Endpoint:** `fetchesforajax/fetch_current_confinements.php`

**Method:** POST

**Parameters:**
```
JMSAgencyID: SC018013C (required)
search: "" (optional - search filter)
agency: "" (optional - filter by arresting agency)
sort: "name" (optional - sort order: name, date, etc.)
IDX: 1 (optional - page number for pagination)
```

**Example Request:**
```python
import requests

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
    'sort': 'name'
}

response = requests.post(url, headers=headers, data=payload)
```

**Response Format:** HTML fragment containing card elements for each inmate

**Response Structure:**
- Returns styled HTML with `.booking-card` CSS classes
- Each inmate is in a separate card div
- Contains: Name, booking number, mugshot, charges, bond info, dates
- Use BeautifulSoup or similar to parse the HTML

---

### 2. Search by Name

**Use Case:** Search for inmates by first, middle, or last name (supports partial matches).

**Endpoint:** `fetchesforajax/fetch_incident_search_name.php`

**Method:** POST

**Parameters:**
```
searchtype: "name" (required)
firstname: "" (optional - partial match allowed)
middlename: "" (optional)
lastname: "" (optional - partial match allowed)
```

**Example Request:**
```python
url = "https://cc.southernsoftware.com/bookingsearch/fetchesforajax/fetch_incident_search_name.php"

payload = {
    'searchtype': 'name',
    'firstname': 'John',
    'middlename': '',
    'lastname': 'Doe'
}

response = requests.post(url, headers=headers, data=payload)
```

**Notes:**
- You can search by last name only
- Partial matches work (e.g., "Smi" will match "Smith")
- Case-insensitive search

---

### 3. Get Last 24 Hours Admits

**Use Case:** Get all inmates admitted in the last 24 hours.

**Endpoint:** `fetchesforajax/fetch_last24hours.php`

**Method:** POST

**Parameters:**
```
JMSAgencyID: SC018013C (required)
IDX: 1 (optional - page number for pagination)
```

**Example Request:**
```python
url = "https://cc.southernsoftware.com/bookingsearch/fetchesforajax/fetch_last24hours.php"

payload = {
    'JMSAgencyID': 'SC018013C'
}

response = requests.post(url, headers=headers, data=payload)
```

---

### 4. Search Admits by Date Range

**Use Case:** Get all inmates admitted within a specific date range.

**Endpoint:** `fetchesforajax/fetch_incident_search_dates_admit.php`

**Method:** POST

**Parameters:**
```
searchtype: "daterange" (required)
begindate: "MM/DD/YYYY" (required)
enddate: "MM/DD/YYYY" (required)
customRadioInline1: "customdate" | "last24hours" | "currentweek"
```

**Example Request:**
```python
url = "https://cc.southernsoftware.com/bookingsearch/fetchesforajax/fetch_incident_search_dates_admit.php"

payload = {
    'searchtype': 'daterange',
    'begindate': '10/01/2025',
    'enddate': '10/27/2025',
    'customRadioInline1': 'customdate'
}

response = requests.post(url, headers=headers, data=payload)
```

**Notes:**
- Date format must be MM/DD/YYYY
- Maximum date range appears to be ~365 days
- Using date ranges > 31 days may trigger warnings

---

### 5. Search Releases by Date Range

**Use Case:** Get all inmates released within a specific date range.

**Endpoint:** `fetchesforajax/fetch_incident_search_dates_release.php`

**Method:** POST

**Parameters:**
```
searchtype: "daterange" (required)
begindate: "MM/DD/YYYY" (required)
enddate: "MM/DD/YYYY" (required)
customRadioInline1: "customdate" | "last24hours" | "currentweek"
```

**Example Request:**
```python
url = "https://cc.southernsoftware.com/bookingsearch/fetchesforajax/fetch_incident_search_dates_release.php"

payload = {
    'searchtype': 'daterange',
    'begindate': '10/01/2025',
    'enddate': '10/27/2025',
    'customRadioInline1': 'customdate'
}

response = requests.post(url, headers=headers, data=payload)
```

---

### 6. Search by Charge

**Use Case:** Find all inmates with specific charges.

**Endpoint:** `fetchesforajax/fetch_incident_search_charge.php`

**Method:** POST

**Parameters:**
```
charge: "DUI" (required - partial match allowed)
```

**Example Request:**
```python
url = "https://cc.southernsoftware.com/bookingsearch/fetchesforajax/fetch_incident_search_charge.php"

payload = {
    'charge': 'DUI'
}

response = requests.post(url, headers=headers, data=payload)
```

**Notes:**
- Partial matches work
- Case-insensitive
- Examples: "DUI", "assault", "theft", etc.

---

### 7. Search by Arresting Agency

**Use Case:** Find all inmates arrested by a specific law enforcement agency.

**Endpoint:** `fetchesforajax/fetch_incident_search_arrestagency.php`

**Method:** POST

**Parameters:**
```
ArrestAgency: "SUMMERVILLE - SC0180200" (required - exact match)
```

**Example Request:**
```python
url = "https://cc.southernsoftware.com/bookingsearch/fetchesforajax/fetch_incident_search_arrestagency.php"

payload = {
    'ArrestAgency': 'SUMMERVILLE - SC0180200'
}

response = requests.post(url, headers=headers, data=payload)
```

**Common Agencies:**
- `DORCHESTER - SC0180000` - Dorchester County Sheriff
- `SUMMERVILLE - SC0180200` - Summerville PD
- `ST GEORGE PD - SC0180100` - St. George PD
- `RIDGEVILLE - SC0180400` - Ridgeville PD
- `HARLEYVILLE - SC0180300` - Harleyville PD
- `SC HIGHWAY PATROL - SCSHP0000` - SC Highway Patrol
- `CHARLESTON - SC0100000` - Charleston County

---

## Response Parsing

### HTML Structure

All endpoints return HTML fragments (not JSON). The response contains:

1. **CSS Styles** (inline at top of response)
2. **Result Cards** - Each inmate is in a div with class `.booking-card`
3. **No Results Message** - If no matches found

### Sample Response Structure

```html
<style>
/* CSS styles for booking cards */
.booking-card { ... }
.booking-header { ... }
</style>

<div class="mb-3">
    <h5 class="text-muted">Current Confinements: <span class="text-primary">42</span></h5>
</div>

<!-- Inmate Record 1 -->
<div class="booking-card">
    <div class="booking-header">
        <h5>LASTNAME, FIRSTNAME MIDDLE</h5>
        <span class="booking-number">Booking: 2025-12345</span>
    </div>
    <div class="row">
        <div class="col-md-3">
            <img class="booking-mugshot" src="...">
        </div>
        <div class="col-md-9 booking-details">
            <div class="detail-row">
                <span class="detail-label">Race/Sex:</span>
                <span class="detail-value">W / M</span>
            </div>
            <div class="detail-row">
                <span class="detail-label">Date of Birth:</span>
                <span class="detail-value">01/01/1990</span>
            </div>
            <!-- More details -->
        </div>
    </div>
    <div class="charges-section">
        <div class="charges-header">Charges</div>
        <!-- Charge details -->
    </div>
</div>

<!-- More inmate records... -->
```

### Parsing with Python

```python
from bs4 import BeautifulSoup

def parse_inmate_records(html_response):
    """Parse HTML response and extract inmate information."""
    soup = BeautifulSoup(html_response, 'html.parser')

    inmates = []
    cards = soup.find_all('div', class_='booking-card')

    for card in cards:
        inmate = {}

        # Get name and booking number from header
        header = card.find('div', class_='booking-header')
        if header:
            name_elem = header.find('h5')
            if name_elem:
                inmate['name'] = name_elem.get_text(strip=True)

            booking_elem = header.find('span', class_='booking-number')
            if booking_elem:
                inmate['booking_number'] = booking_elem.get_text(strip=True)

        # Get detail rows
        detail_rows = card.find_all('div', class_='detail-row')
        for row in detail_rows:
            label_elem = row.find('span', class_='detail-label')
            value_elem = row.find('span', class_='detail-value')

            if label_elem and value_elem:
                label = label_elem.get_text(strip=True).replace(':', '')
                value = value_elem.get_text(strip=True)
                inmate[label.lower().replace(' ', '_')] = value

        # Get charges
        charges_section = card.find('div', class_='charges-section')
        if charges_section:
            charge_items = charges_section.find_all('div', class_='charge-item')
            inmate['charges'] = []
            for charge in charge_items:
                charge_text = charge.get_text(strip=True)
                inmate['charges'].append(charge_text)

        inmates.append(inmate)

    return inmates

# Usage
response = requests.post(url, headers=headers, data=payload)
inmates = parse_inmate_records(response.text)

for inmate in inmates:
    print(f"Name: {inmate.get('name')}")
    print(f"Booking: {inmate.get('booking_number')}")
    print(f"DOB: {inmate.get('date_of_birth')}")
    print()
```

---

## Custody Status Determination

To determine if someone is currently in custody:

1. **Use Endpoint #1** (`fetch_current_confinements.php`) to get ALL current inmates
2. Parse the HTML response to extract names
3. Compare against your defendant list
4. Anyone NOT in the current confinements list is NOT in custody

**Alternative approach:**

1. Use Endpoint #2 (`fetch_incident_search_name.php`) for each defendant
2. Check if results are returned
3. If results show "No inmates found", they are NOT in custody
4. If results are found, verify the "Confinement End Date" field:
   - If empty or shows "Still Confined" → Currently IN custody
   - If shows a date → Released on that date

---

## Important Notes

### Rate Limiting
- No obvious rate limiting detected
- Be respectful with requests (e.g., 1-2 seconds between requests)
- Consider caching results for your weekly reports

### Pagination
- Results are paginated (appears to be ~50 records per page)
- Use the `IDX` parameter to fetch additional pages
- IDX=1 is the first page, IDX=2 is the second, etc.

### Error Handling
- Some endpoints may return HTTP 500 errors intermittently
- Always check `response.status_code == 200`
- HTML responses may contain error messages in the content

### Required Headers
Minimal required headers for successful requests:

```python
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Referer': 'https://cc.southernsoftware.com/bookingsearch/index.php?AgencyID=DorchesterCoSC'
}
```

### Session Management
- No session cookies required
- Each request is independent
- No authentication needed

---

## Recommended Workflow for Weekly Reports

### Monday Morning Check

```python
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Your defendant list
defendants = [
    {"first": "John", "last": "Doe"},
    {"first": "Jane", "last": "Smith"},
    # ... more defendants
]

# Configuration
BASE_URL = "https://cc.southernsoftware.com/bookingsearch"
AGENCY_ID = "SC018013C"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Referer': f'{BASE_URL}/index.php?AgencyID=DorchesterCoSC'
}

def check_custody_status(first_name, last_name):
    """Check if a defendant is currently in custody."""
    url = f"{BASE_URL}/fetchesforajax/fetch_incident_search_name.php"

    payload = {
        'searchtype': 'name',
        'firstname': first_name,
        'middlename': '',
        'lastname': last_name
    }

    try:
        response = requests.post(url, headers=HEADERS, data=payload, timeout=30)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # Check for "No inmates found" message
            no_results = soup.find('div', class_='no-results')
            if no_results:
                return False, "Not in custody"

            # Check if they have an active confinement
            cards = soup.find_all('div', class_='booking-card')
            if cards:
                # Parse the first result to check confinement status
                # Look for release date or "Still Confined" indicator
                return True, f"IN CUSTODY - {len(cards)} record(s) found"

            return False, "Not in custody"
        else:
            return None, f"Error: HTTP {response.status_code}"

    except Exception as e:
        return None, f"Error: {str(e)}"

# Generate Monday report
print(f"Custody Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 80)

in_custody = []
not_in_custody = []
errors = []

for defendant in defendants:
    status, message = check_custody_status(defendant['first'], defendant['last'])

    full_name = f"{defendant['first']} {defendant['last']}"

    if status is True:
        in_custody.append(full_name)
    elif status is False:
        not_in_custody.append(full_name)
    else:
        errors.append((full_name, message))

    # Be respectful - wait between requests
    import time
    time.sleep(1)

# Print report
print(f"\nIN CUSTODY ({len(in_custody)}):")
for name in in_custody:
    print(f"  - {name}")

print(f"\nNOT IN CUSTODY ({len(not_in_custody)}):")
for name in not_in_custody:
    print(f"  - {name}")

if errors:
    print(f"\nERRORS ({len(errors)}):")
    for name, error in errors:
        print(f"  - {name}: {error}")
```

---

## Testing

Test files have been created in this repository:
- `investigate_api.py` - Initial investigation script
- `test_api_endpoints.py` - Comprehensive endpoint testing
- Various `test_*.html` - Sample responses from each endpoint

To run tests:
```bash
python test_api_endpoints.py
```

---

## Legal Considerations

- This is publicly accessible data
- No authentication or authorization bypass required
- Data is provided by the Dorchester County Sheriff's Office for public access
- Follow applicable laws regarding use of public records
- Be respectful of the system and don't overwhelm it with requests

---

## Support

For issues with the booking system itself:
- **Dorchester County Sheriff's Office**
- Phone: (843) 832-0300
- Address: 212 Deming Way, Summerville, SC

For the Citizen Connect platform:
- **Southern Software, Inc.**
- Website: https://www.southernsoftware.com

---

## Revision History

- **v1.0** (2025-10-27): Initial documentation from reverse engineering
