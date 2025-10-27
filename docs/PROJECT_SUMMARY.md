# Jail Custody Checker - Project Summary

## What Was Built

A complete Python-based system to check defendant custody status in the Dorchester County SC jail database, with support for both CSV and PDF input files and automated report generation.

## Key Features

✅ **Multiple Input Formats**
- CSV files (Active Cases By Assigned Personnel Detail)
- PDF files (Prosecutor Worklist Report)
- Automatic format detection

✅ **Robust API Client**
- Reverse-engineered Southern Software Citizen Connect API
- Automatic retry logic for failed requests
- Configurable rate limiting (default: 1.5s between requests)
- Respectful of server resources

✅ **Comprehensive Reporting**
- JSON output for programmatic use / future web interface
- Excel spreadsheet with three sheets:
  - Summary statistics
  - All results (color-coded)
  - In-custody only (filtered)

✅ **Production Ready**
- Pydantic v2 models for data validation
- Extensive doctests in all modules
- Unit tests for critical functions
- Error handling and logging
- Windows batch files for easy operation

## Project Structure

```
jail-checker/
├── src/                          # Source code
│   ├── models.py                 # Pydantic v2 data models
│   ├── parsers.py                # CSV & PDF parsers
│   ├── jail_api.py               # API client
│   ├── reports.py                # Report generators
│   └── main.py                   # Main CLI script
├── tests/                        # Test suite
│   └── unit/                     # Unit tests
│       ├── test_models.py
│       └── test_parsers.py
├── input/                        # Input files folder
├── output/                       # Generated reports folder
├── requirements.txt              # Python dependencies
├── setup.bat                     # One-click setup
├── run_check.bat                 # One-click run
├── README_USAGE.md               # User documentation
├── API_DOCUMENTATION.md          # Technical API docs
└── PROJECT_SUMMARY.md            # This file
```

## Quick Start

### 1. Setup (One Time)

Double-click `setup.bat` or run:
```cmd
setup.bat
```

This installs all required Python packages.

### 2. Prepare Input

Place your defendant list in the `input/` folder:
- CSV: `Active Cases By Assigned Personnel Detail.csv`
- PDF: `Prosecutor Worklist Report.pdf`

### 3. Run Check

Double-click `run_check.bat` and enter the file path, or run:
```cmd
run_check.bat "input\Active Cases By Assigned Personnel Detail.csv"
```

### 4. Review Results

Find reports in the `output/` folder:
- `*_custody_YYYYMMDD_HHMMSS.json` - JSON format
- `*_custody_YYYYMMDD_HHMMSS.xlsx` - Excel spreadsheet

## Monday Morning Workflow

Your typical weekly workflow:

1. **Export defendant list** from your case management system
   - Save as CSV or PDF in the `input/` folder

2. **Run the checker**:
   ```cmd
   run_check.bat "input\Active Cases By Assigned Personnel Detail.csv"
   ```

3. **Review console output** - shows in-custody defendants immediately

4. **Open Excel report** - detailed view with all information

5. **Take action** - contact defendants in custody as needed

## Technical Implementation

### API Integration

- **Endpoint**: `fetch_incident_search_name.php`
- **Method**: POST with first/middle/last name
- **Response**: HTML (parsed with BeautifulSoup4)
- **Rate Limiting**: 1.5s delay between requests (configurable)

### Input Processing

**CSV Parser**:
- Uses pandas for robust CSV handling
- Extracts: name, case number, charges, status
- Handles various name formats

**PDF Parser**:
- Uses pdfplumber for text extraction
- Regex-based pattern matching
- Deduplicates entries across pages

### Output Generation

**JSON Report**:
- Complete structured data
- ISO timestamp formats
- Ready for web interface consumption

**Excel Report**:
- Three-sheet workbook with formatting
- Color-coded rows:
  - Red: In custody
  - Green: Not in custody
  - Yellow: Errors
- Frozen header rows for easy scrolling

## Code Quality

### Doctests
Every function includes doctest examples in docstrings:
```python
def parse_defendant_name(name_str: str) -> tuple[str, str, str]:
    """
    >>> parse_defendant_name("Smith, John Michael")
    ('John', 'Michael', 'Smith')
    """
```

Run doctests:
```cmd
conda activate jail_checker
python -m doctest src\models.py -v
```

### Unit Tests
Separate test files for each module in `tests/unit/`:
```cmd
conda activate jail_checker
python tests\unit\test_models.py
python tests\unit\test_parsers.py
```

### Error Handling
- Graceful handling of network errors
- Timeout management
- Retry logic with exponential backoff
- Detailed error logging

## Dependencies

All specified in `requirements.txt`:
- **pydantic** (v2+) - Data validation
- **requests** - HTTP client
- **beautifulsoup4** - HTML parsing
- **pandas** - CSV processing
- **pdfplumber** - PDF extraction
- **openpyxl** - Excel generation
- **lxml** - Better HTML parsing

## Future Enhancements

### JavaScript/HTML Version (Planned)

A browser-based version will provide:
- Drag-and-drop file upload
- Client-side processing (no server needed)
- Real-time results display
- No Python installation required

The JSON output format is already designed for this future implementation.

### Potential Improvements

- Batch processing optimization
- Scheduled automated runs
- Email notifications for in-custody defendants
- Integration with case management systems
- Historical tracking of custody status changes

## Performance

- **Processing Speed**: ~2 seconds per defendant (1.5s delay + 0.5s processing)
- **Typical Workload**: 200 defendants = ~6-7 minutes
- **Accuracy**: Direct API queries, real-time data
- **Reliability**: Retry logic handles temporary failures

## Sample Data

Your repo includes sample files for testing:
- `Active Cases By Assigned Personnel Detail.csv` (242 cases)
- `Prosecutor Worklist Report.pdf` (206 cases)

Both contain real defendant names from your 1st Circuit Solicitor's Office active caseload.

## API Documentation

Complete technical documentation available in:
- `API_DOCUMENTATION.md` - Full endpoint reference
- `REVERSE_ENGINEERING_SUMMARY.md` - Investigation methodology
- `QUICK_REFERENCE.md` - One-page cheat sheet

## Support & Troubleshooting

See `README_USAGE.md` for:
- Common error messages and solutions
- Advanced configuration options
- Troubleshooting guide
- Usage examples

## License & Usage

Internal tool for 1st Circuit Solicitor's Office use.

## Credits

**Developed by**: Claude Code (Anthropic)
**For**: 1st Circuit Solicitor's Office, Dorchester County, SC
**Date**: October 2025
**API**: Southern Software Citizen Connect
**Python Environment**: jail_checker conda env (Python 3.11)

---

## Getting Started Now

1. Run `setup.bat` to install dependencies
2. Place a defendant list in `input/`
3. Run `run_check.bat "input\your_file.csv"`
4. Check the results in `output/`

That's it! You're ready for your Monday morning custody checks.
