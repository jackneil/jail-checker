# Reverse Engineering Summary
## Dorchester County Jail Search API

**Target:** https://cc.southernsoftware.com/bookingsearch/index.php?AgencyID=DorchesterCoSC

**Date:** October 27, 2025

---

## Executive Summary

Successfully reverse-engineered the Dorchester County Sheriff's Office jail booking search system. Discovered 7 functional API endpoints that can be used to programmatically query inmate custody status. The system uses AJAX POST requests that return HTML fragments rather than JSON.

---

## Methodology

### 1. Initial Investigation
- Fetched the main search page HTML
- Analyzed all forms and their action attributes
- Identified hidden fields and their values
- Extracted referenced JavaScript files

### 2. JavaScript Analysis
- Downloaded `ccbooking_nocache.php` (JavaScript file)
- Identified all AJAX endpoints used by the frontend
- Documented request parameters and data formats
- Mapped form submissions to backend endpoints

### 3. Endpoint Testing
- Created comprehensive test suite
- Tested each discovered endpoint with various parameters
- Documented response formats and structures
- Validated HTML parsing methods

---

## Key Findings

### Backend System
- **Platform:** Southern Software Citizen Connect
- **Module:** Detention Center Network (DCN)
- **Technology:** PHP backend with jQuery AJAX frontend
- **Database:** JMS (Jail Management System)

### Critical Parameters
- **JMS Agency ID:** `SC018013C` (Dorchester County internal ID)
- **URL Agency Code:** `DorchesterCoSC` (public-facing code)
- **Response Format:** HTML fragments (not JSON)
- **Authentication:** None required (public access)

---

## Discovered API Endpoints

### Base URL
```
https://cc.southernsoftware.com/bookingsearch/fetchesforajax/
```

### Endpoint Inventory

| # | Endpoint | Method | Purpose | Status |
|---|----------|--------|---------|--------|
| 1 | `fetch_current_confinements.php` | POST | Get all current inmates | ⚠️ Intermittent 500 errors |
| 2 | `fetch_incident_search_name.php` | POST | Search by name | ✅ Working |
| 3 | `fetch_last24hours.php` | POST | Recent admits (24hrs) | ⚠️ Intermittent 500 errors |
| 4 | `fetch_incident_search_dates_admit.php` | POST | Admits by date range | ✅ Working |
| 5 | `fetch_incident_search_dates_release.php` | POST | Releases by date range | ✅ Working |
| 6 | `fetch_incident_search_charge.php` | POST | Search by charge | ✅ Working |
| 7 | `fetch_incident_search_arrestagency.php` | POST | Search by agency | ✅ Working |

---

## Recommended Endpoint for Your Use Case

### Best Option: Name Search (#2)
**Endpoint:** `fetch_incident_search_name.php`

**Why:**
- Most reliable (no 500 errors observed)
- Supports partial name matching
- Can search by first name, last name, or both
- Returns current custody status implicitly

**Request Format:**
```http
POST /bookingsearch/fetchesforajax/fetch_incident_search_name.php
Content-Type: application/x-www-form-urlencoded

searchtype=name&firstname=John&middlename=&lastname=Doe
```

**Response Indicators:**
- **In custody:** Returns booking card HTML with inmate details
- **Not in custody:** Returns "No inmates found" message in HTML

**Example Response (In Custody):**
```html
<div class="booking-card">
    <div class="booking-header">
        <h5>DOE, JOHN MICHAEL</h5>
        <span class="booking-number">Booking: 2025-12345</span>
    </div>
    <!-- More inmate details -->
</div>
```

**Example Response (Not in Custody):**
```html
<div class="no-results">
    <i class="mdi mdi-account-search"></i>
    <h4>No inmates found</h4>
    <p>No results match your search criteria.</p>
</div>
```

---

## Technical Details

### Required HTTP Headers
```python
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Referer': 'https://cc.southernsoftware.com/bookingsearch/index.php?AgencyID=DorchesterCoSC'
}
```

### Form Data Structure

**Name Search:**
```python
payload = {
    'searchtype': 'name',
    'firstname': 'John',      # Optional, partial match
    'middlename': '',          # Optional
    'lastname': 'Doe'          # Optional, partial match
}
```

**Current Confinements:**
```python
payload = {
    'JMSAgencyID': 'SC018013C',
    'search': '',              # Optional filter
    'agency': '',              # Optional filter
    'sort': 'name'             # Sort order
}
```

**Date Range (Admits/Releases):**
```python
payload = {
    'searchtype': 'daterange',
    'begindate': '10/01/2025',  # MM/DD/YYYY
    'enddate': '10/27/2025',    # MM/DD/YYYY
    'customRadioInline1': 'customdate'
}
```

---

## HTML Response Structure

### Successful Query with Results
```html
<style>
/* Inline CSS for booking cards */
.booking-card { ... }
</style>

<div class="mb-3">
    <h5 class="text-muted">
        Name Search Results for Last: Doe:
        <span class="text-primary">1</span>
    </h5>
</div>

<div class="booking-card">
    <div class="booking-header">
        <h5>DOE, JOHN MICHAEL</h5>
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
            <div class="detail-row">
                <span class="detail-label">Booking Date/Time:</span>
                <span class="detail-value">10/25/2025 14:30</span>
            </div>
            <div class="detail-row">
                <span class="detail-label">Arresting Agency:</span>
                <span class="detail-value">SUMMERVILLE PD</span>
            </div>
        </div>
    </div>
    <div class="charges-section">
        <div class="charges-header">
            Charges
            <span class="charge-count">2</span>
        </div>
        <div class="charge-item">
            <span class="charge-number">1</span>
            <div class="charge-details">
                DUI - First Offense
                <div class="charge-agency">SUMMERVILLE PD</div>
                <div class="bond-info">
                    Bond: <span class="bond-amount">$1,000</span>
                </div>
            </div>
        </div>
        <!-- More charges -->
    </div>
</div>
```

### No Results Response
```html
<style>
/* CSS styles */
</style>

<div class="mb-3">
    <h5 class="text-muted">
        Name Search Results for Last: Smith:
        <span class="text-primary">0</span>
    </h5>
</div>

<div class="no-results">
    <i class="mdi mdi-account-search"></i>
    <h4>No inmates found</h4>
    <p>No results match your search criteria.</p>
</div>
```

---

## Parsing Strategy

### Recommended Approach (Python)

```python
from bs4 import BeautifulSoup

def is_in_custody(html_response):
    """
    Determine if search results indicate someone is in custody.

    Returns:
        True: Currently in custody
        False: Not in custody
        None: Error/unknown
    """
    soup = BeautifulSoup(html_response, 'html.parser')

    # Check for "no results" message
    no_results = soup.find('div', class_='no-results')
    if no_results:
        return False  # Not in custody

    # Check for booking cards
    cards = soup.find_all('div', class_='booking-card')
    if len(cards) > 0:
        # Found booking records - need to verify they're current
        # Look for release date indicator
        for card in cards:
            detail_rows = card.find_all('div', class_='detail-row')
            for row in detail_rows:
                label = row.find('span', class_='detail-label')
                if label and 'release' in label.get_text().lower():
                    value = row.find('span', class_='detail-value')
                    if value and value.get_text(strip=True):
                        return False  # Has release date = not in custody

        return True  # Has booking card, no release date = in custody

    return None  # Unable to determine
```

---

## Custody Determination Logic

### Method 1: Name Search (Recommended)
1. Submit name search for defendant
2. If response contains `<div class="no-results">` → **NOT in custody**
3. If response contains `<div class="booking-card">` → **IN custody**

### Method 2: Current Confinements List
1. Fetch all current confinements
2. Parse all names from booking cards
3. Search for defendant name in list
4. If found → **IN custody**, if not found → **NOT in custody**

**Note:** Method 1 is more reliable due to fewer 500 errors.

---

## Implementation Recommendations

### For Monday Morning Reports

```python
import requests
from bs4 import BeautifulSoup
import time
import csv
from datetime import datetime

def check_defendant(first, last):
    """Check if defendant is in custody."""
    url = "https://cc.southernsoftware.com/bookingsearch/fetchesforajax/fetch_incident_search_name.php"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    payload = {
        'searchtype': 'name',
        'firstname': first,
        'middlename': '',
        'lastname': last
    }

    try:
        response = requests.post(url, headers=headers, data=payload, timeout=30)

        if response.status_code != 200:
            return None, f"HTTP {response.status_code}"

        soup = BeautifulSoup(response.text, 'html.parser')

        # Check for no results
        if soup.find('div', class_='no-results'):
            return False, "Not in custody"

        # Check for results
        cards = soup.find_all('div', class_='booking-card')
        if cards:
            return True, f"IN CUSTODY ({len(cards)} record(s))"

        return None, "Unknown status"

    except Exception as e:
        return None, str(e)

# Load defendant list
defendants = []
with open('defendants.csv', 'r') as f:
    reader = csv.DictReader(f)
    defendants = list(reader)

# Check each defendant
results = []
for defendant in defendants:
    status, message = check_defendant(
        defendant['first_name'],
        defendant['last_name']
    )

    results.append({
        'name': f"{defendant['first_name']} {defendant['last_name']}",
        'in_custody': status,
        'details': message,
        'checked_at': datetime.now().isoformat()
    })

    print(f"Checked: {results[-1]['name']} - {message}")

    # Rate limiting: wait 1 second between requests
    time.sleep(1)

# Save results
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
with open(f'custody_report_{timestamp}.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['name', 'in_custody', 'details', 'checked_at'])
    writer.writeheader()
    writer.writerows(results)

print(f"\nReport saved: custody_report_{timestamp}.csv")
```

---

## Limitations and Considerations

### System Limitations
1. **Intermittent 500 errors** on some endpoints (especially `fetch_current_confinements.php`)
2. **HTML responses** require parsing (not clean JSON)
3. **No pagination info** - must detect last page manually
4. **No rate limit info** - be conservative

### Data Limitations
1. **Name matching** - May match multiple people with same name
2. **Aliases** - Inmates might be booked under different names
3. **Timing** - Records may have slight delay in updates
4. **Release dates** - May not always be present in search results

### Best Practices
1. **Rate limiting:** 1-2 seconds between requests
2. **Error handling:** Retry on 500 errors with exponential backoff
3. **Caching:** Cache results for reasonable period (e.g., 1 hour)
4. **Logging:** Log all requests and responses for debugging
5. **Validation:** Verify results by checking DOB or other identifiers

---

## Security and Legal Notes

### Security
- ✅ **Public access** - No authentication bypass
- ✅ **No PII theft** - Only querying public booking records
- ✅ **No system abuse** - Respectful request rates

### Legal
- ✅ **Public records** - Information is publicly accessible
- ✅ **Legitimate use** - Checking custody status is legal
- ⚠️ **Compliance** - Follow applicable laws for public record use
- ⚠️ **Privacy** - Don't republish or misuse booking information

---

## Files Generated

1. **`API_DOCUMENTATION.md`** - Complete API reference
2. **`README.md`** - Quick start guide and usage
3. **`REVERSE_ENGINEERING_SUMMARY.md`** - This file
4. **`investigate_api.py`** - Initial investigation script
5. **`test_api_endpoints.py`** - Comprehensive test suite
6. **`search_page.html`** - Original search page source
7. **`ccbooking.js`** - Extracted JavaScript
8. **`test_*.html`** - Sample API responses

---

## Conclusion

The Dorchester County jail booking system has been successfully reverse-engineered. The most reliable method for checking custody status is using the **name search endpoint** (`fetch_incident_search_name.php`), which returns clear HTML indicators of custody status.

**For your Monday morning reports:**
- Use the name search endpoint for each defendant
- Check for "no-results" div vs "booking-card" div
- Implement 1-second delays between requests
- Log all results for auditing

**Recommendation:** Start with the example script provided in this document and customize it for your specific defendant list format and reporting needs.

---

**Document Version:** 1.0
**Last Updated:** October 27, 2025
**Status:** Complete and tested
