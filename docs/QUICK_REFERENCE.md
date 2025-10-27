# Quick Reference Card
## Dorchester County Jail API

---

## Essential Information

**Base URL:** `https://cc.southernsoftware.com/bookingsearch/fetchesforajax/`

**Agency ID:** `SC018013C`

**Method:** POST (all endpoints)

**Response:** HTML fragments

---

## Most Useful Endpoint: Name Search

**URL:** `fetch_incident_search_name.php`

**Payload:**
```python
{
    'searchtype': 'name',
    'firstname': 'John',
    'middlename': '',
    'lastname': 'Doe'
}
```

**In Custody Response:** Contains `<div class="booking-card">`

**Not in Custody Response:** Contains `<div class="no-results">`

---

## Minimal Working Example

```python
import requests
from bs4 import BeautifulSoup

url = "https://cc.southernsoftware.com/bookingsearch/fetchesforajax/fetch_incident_search_name.php"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
}

payload = {
    'searchtype': 'name',
    'firstname': 'John',
    'middlename': '',
    'lastname': 'Doe'
}

response = requests.post(url, headers=headers, data=payload)
soup = BeautifulSoup(response.text, 'html.parser')

if soup.find('div', class_='no-results'):
    print("NOT in custody")
elif soup.find('div', class_='booking-card'):
    print("IN CUSTODY")
```

---

## All 7 Endpoints

| Endpoint | Purpose | Key Parameter |
|----------|---------|---------------|
| `fetch_incident_search_name.php` | Search by name | lastname |
| `fetch_current_confinements.php` | All current inmates | JMSAgencyID |
| `fetch_last24hours.php` | Recent admits | JMSAgencyID |
| `fetch_incident_search_dates_admit.php` | Admits by date | begindate, enddate |
| `fetch_incident_search_dates_release.php` | Releases by date | begindate, enddate |
| `fetch_incident_search_charge.php` | Search by charge | charge |
| `fetch_incident_search_arrestagency.php` | Search by agency | ArrestAgency |

---

## Rate Limiting

**Recommended:** 1 second between requests

```python
import time
time.sleep(1)
```

---

## Error Handling

```python
try:
    response = requests.post(url, headers=headers, data=payload, timeout=30)

    if response.status_code != 200:
        print(f"Error: HTTP {response.status_code}")
        return

    # Process response...

except Exception as e:
    print(f"Error: {e}")
```

---

## Common Arresting Agencies

- `DORCHESTER - SC0180000` - Dorchester Sheriff
- `SUMMERVILLE - SC0180200` - Summerville PD
- `ST GEORGE PD - SC0180100` - St. George PD
- `RIDGEVILLE - SC0180400` - Ridgeville PD
- `SC HIGHWAY PATROL - SCSHP0000` - SC Highway Patrol

---

## Date Format

**Format:** `MM/DD/YYYY`

**Example:** `10/27/2025`

```python
from datetime import datetime
today = datetime.now().strftime("%m/%d/%Y")
```

---

## Parsing HTML

```python
from bs4 import BeautifulSoup

soup = BeautifulSoup(response.text, 'html.parser')

# Check custody status
no_results = soup.find('div', class_='no-results')
if no_results:
    status = "NOT IN CUSTODY"
else:
    cards = soup.find_all('div', class_='booking-card')
    status = f"IN CUSTODY ({len(cards)} record(s))"

# Extract name from card
card = soup.find('div', class_='booking-card')
if card:
    header = card.find('div', class_='booking-header')
    name = header.find('h5').get_text(strip=True)

    booking_num = header.find('span', class_='booking-number')
    booking = booking_num.get_text(strip=True)

# Extract details
detail_rows = card.find_all('div', class_='detail-row')
for row in detail_rows:
    label = row.find('span', class_='detail-label').get_text(strip=True)
    value = row.find('span', class_='detail-value').get_text(strip=True)
    print(f"{label}: {value}")
```

---

## Testing

```bash
# Run comprehensive tests
python test_api_endpoints.py

# Check specific name
python -c "
import requests
from bs4 import BeautifulSoup

r = requests.post(
    'https://cc.southernsoftware.com/bookingsearch/fetchesforajax/fetch_incident_search_name.php',
    data={'searchtype': 'name', 'firstname': '', 'middlename': '', 'lastname': 'Smith'}
)

soup = BeautifulSoup(r.text, 'html.parser')
print('In custody' if soup.find('div', class_='booking-card') else 'Not in custody')
"
```

---

## Troubleshooting

**HTTP 500 Error:**
- Try different endpoint (name search is most reliable)
- Wait a few seconds and retry

**No results but should be in custody:**
- Check spelling
- Try last name only
- Check for aliases/middle names

**Parsing fails:**
- Check HTML structure hasn't changed
- View raw response: `print(response.text[:1000])`

---

## Contact Info

**Dorchester County Sheriff's Office**
- Phone: (843) 832-0300
- Address: 212 Deming Way, Summerville, SC

---

**See Full Documentation:** `API_DOCUMENTATION.md`
