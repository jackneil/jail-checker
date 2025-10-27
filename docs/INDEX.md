# Dorchester County Jail Checker - Project Index

Complete reverse-engineering documentation for the Dorchester County Sheriff's Office jail booking search system.

---

## Documentation Files

### 📖 Start Here

1. **`README.md`** - Project overview and quick start guide
   - What this project does
   - Basic usage examples
   - Monday morning workflow
   - Installation instructions

2. **`QUICK_REFERENCE.md`** - One-page cheat sheet
   - Essential information at a glance
   - Minimal working examples
   - Common troubleshooting tips

### 📚 Detailed Documentation

3. **`API_DOCUMENTATION.md`** - Complete API reference (⭐ MOST COMPREHENSIVE)
   - All 7 endpoints documented
   - Full request/response examples
   - Parsing strategies
   - Error handling
   - Legal considerations

4. **`REVERSE_ENGINEERING_SUMMARY.md`** - Technical deep dive
   - Methodology used
   - Findings and analysis
   - HTML response structures
   - Implementation recommendations
   - System limitations

---

## Code Files

### 🔬 Investigation Scripts

5. **`investigate_api.py`** - Initial reverse-engineering script
   - Fetches and analyzes search page HTML
   - Extracts forms and JavaScript
   - Tests form submission
   - Discovers API endpoints
   - Run: `python investigate_api.py`

6. **`test_api_endpoints.py`** - Comprehensive test suite
   - Tests all 7 discovered endpoints
   - Validates request/response formats
   - Saves sample responses
   - Run: `python test_api_endpoints.py`

---

## Generated Files

### 📄 HTML Responses (for reference)

- `search_page.html` - Original booking search form
- `search_result.html` - Sample search result page
- `test_name_search.html` - Name search response
- `test_current_confinements.html` - Current confinements response
- `test_last24hours.html` - Last 24 hours response
- `test_daterange_admits.html` - Date range admits response
- `test_daterange_releases.html` - Date range releases response
- `test_charge_search.html` - Charge search response
- `test_agency_search.html` - Agency search response

### 📜 JavaScript Files

- `ccbooking.js` - Extracted frontend JavaScript code

---

## Key Information Summary

### System Details
- **Platform:** Southern Software Citizen Connect (DCN)
- **Agency:** Dorchester County Sheriff's Office, SC
- **Base URL:** `https://cc.southernsoftware.com/bookingsearch`
- **Agency ID:** `SC018013C`
- **Response Format:** HTML fragments (not JSON)
- **Authentication:** None required

### Best Endpoint for Your Use Case
**Name Search** (`fetch_incident_search_name.php`)
- Search by first name, last name, or both
- Returns clear custody status indicators
- Most reliable (no 500 errors)
- Supports partial matching

---

## Quick Navigation

### Want to check if someone is in custody?
→ See `QUICK_REFERENCE.md` (minimal example)

### Need full API documentation?
→ See `API_DOCUMENTATION.md` (all endpoints)

### Want to understand how it was discovered?
→ See `REVERSE_ENGINEERING_SUMMARY.md` (methodology)

### Ready to implement for Monday reports?
→ See `README.md` section "Monday Morning Workflow"

### Need to test the endpoints?
→ Run `python test_api_endpoints.py`

---

## Recommended Reading Order

### For Quick Implementation:
1. `README.md` - Understand the project
2. `QUICK_REFERENCE.md` - Copy working example
3. Customize for your defendant list
4. Done!

### For Complete Understanding:
1. `README.md` - Project overview
2. `REVERSE_ENGINEERING_SUMMARY.md` - How it was discovered
3. `API_DOCUMENTATION.md` - Full API reference
4. `QUICK_REFERENCE.md` - Implementation tips

### For Developers:
1. `REVERSE_ENGINEERING_SUMMARY.md` - Technical analysis
2. `API_DOCUMENTATION.md` - Endpoint specifications
3. Review `investigate_api.py` - See investigation methods
4. Review `test_api_endpoints.py` - See test patterns

---

## Usage Examples by Scenario

### Scenario 1: Check One Person
```python
# See: QUICK_REFERENCE.md
# Minimal example with just name search
```

### Scenario 2: Monday Morning Report (Multiple Defendants)
```python
# See: README.md section "Monday Morning Workflow"
# Loop through CSV of defendants
```

### Scenario 3: Get All Current Inmates
```python
# See: API_DOCUMENTATION.md section "Get Current Confinements"
# Fetch full list and parse
```

### Scenario 4: Search by Date Range
```python
# See: API_DOCUMENTATION.md sections 4 & 5
# Get admits or releases in date range
```

---

## Dependencies

### Required Python Packages
```bash
pip install requests beautifulsoup4
```

### Python Version
- Python 3.6+ recommended
- Tested on Python 3.12

---

## File Sizes (Approximate)

| File | Type | Size | Purpose |
|------|------|------|---------|
| `API_DOCUMENTATION.md` | Docs | 25 KB | Complete API reference |
| `REVERSE_ENGINEERING_SUMMARY.md` | Docs | 18 KB | Technical deep dive |
| `README.md` | Docs | 10 KB | Quick start guide |
| `QUICK_REFERENCE.md` | Docs | 4 KB | Cheat sheet |
| `investigate_api.py` | Code | 8 KB | Investigation script |
| `test_api_endpoints.py` | Code | 12 KB | Test suite |

---

## Project Status

✅ **Complete** - All endpoints discovered and documented

**Last Updated:** October 27, 2025

**Status:**
- ✅ All 7 endpoints identified
- ✅ Request formats documented
- ✅ Response formats documented
- ✅ Parsing examples provided
- ✅ Test scripts working
- ✅ Error handling documented

---

## Next Steps for You

1. **Read** `README.md` to understand the project
2. **Review** `QUICK_REFERENCE.md` for quick implementation
3. **Create** your defendant list (CSV or JSON)
4. **Customize** the example script for your needs
5. **Test** with a few defendants
6. **Schedule** for Monday mornings
7. **Monitor** for any API changes

---

## Support

### For Technical Issues
- Review the documentation in this repository
- Check `test_*.html` files for response examples
- Run `test_api_endpoints.py` to verify endpoints

### For Jail System Issues
- **Dorchester County Sheriff's Office**
- Phone: (843) 832-0300
- Address: 212 Deming Way, Summerville, SC

### For Citizen Connect Platform
- **Southern Software, Inc.**
- Website: https://www.southernsoftware.com

---

## Legal Notice

This project documents the public booking search API provided by the Dorchester County Sheriff's Office. All documented endpoints are publicly accessible and require no authentication. No security measures were bypassed in this investigation.

Use this documentation responsibly and in accordance with applicable laws regarding the use of public records.

---

## Version History

- **v1.0** (2025-10-27): Initial release
  - All 7 endpoints documented
  - Test suite created
  - Comprehensive documentation written

---

**Project Repository:** `C:\Github\jail-checker`

**Documentation Index Last Updated:** October 27, 2025
