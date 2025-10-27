# Jail Custody Checker

Automated tool to check defendant custody status in Dorchester County SC jail database.

## Setup

### 1. Run Setup (One Time)

Simply double-click `setup.bat` or run:

```cmd
setup.bat
```

This will:
- Check if `jail_checker` conda environment exists
- Create it with Python 3.11 if needed
- Install all required packages

### 2. Prepare Input Files

Move your defendant lists to the `input/` folder:
- PDF format: `Prosecutor Worklist Report.pdf` **(RECOMMENDED - more complete data)**
- CSV format: `Active Cases By Assigned Personnel Detail.csv` (names/case numbers may be truncated)

**Note:** PDF format provides complete defendant names and case numbers, while CSV exports may truncate long names with "...". The script automatically prefers PDF when both formats are present.

## Usage

### Easy Way (Recommended)

Simply run the batch script - it auto-detects the most recent file:

```cmd
run_check.bat
```

The script will automatically find and use the most recent CSV or PDF file in the `input/` folder.

**Or specify a file manually:**

```cmd
run_check.bat "input\Active Cases By Assigned Personnel Detail.csv"
```

### Manual Usage

Activate the environment and run directly:

```cmd
conda activate jail_checker
python src\main.py "input\Active Cases By Assigned Personnel Detail.csv"
```

### Advanced Options

Specify custom output directory:
```cmd
conda activate jail_checker
python src\main.py input\defendants.csv --output results
```

Adjust request delay (be respectful to the server):
```cmd
conda activate jail_checker
python src\main.py input\defendants.csv --delay 2.0
```

Enable verbose logging:
```cmd
conda activate jail_checker
python src\main.py input\defendants.csv --verbose
```

### All Options

```
usage: main.py [-h] [--output OUTPUT] [--delay DELAY] [--timeout TIMEOUT]
               [--max-retries MAX_RETRIES] [--verbose]
               input_file

Check defendant custody status in Dorchester County jail

positional arguments:
  input_file            Path to input file (CSV or PDF with defendant list)

options:
  -h, --help            show this help message and exit
  --output OUTPUT, -o OUTPUT
                        Output directory for reports (default: output/)
  --delay DELAY, -d DELAY
                        Delay in seconds between API requests (default: 1.5)
  --timeout TIMEOUT, -t TIMEOUT
                        Request timeout in seconds (default: 30)
  --max-retries MAX_RETRIES, -r MAX_RETRIES
                        Maximum number of retry attempts (default: 3)
  --verbose, -v         Enable verbose logging
```

## Output

The tool generates two reports in the `output/` folder:

1. **JSON Report** (`*_custody_YYYYMMDD_HHMMSS.json`)
   - Machine-readable format
   - Complete data including all fields
   - Use for further processing or web interface

2. **Excel Report** (`*_custody_YYYYMMDD_HHMMSS.xlsx`)
   - Human-readable spreadsheet
   - Three sheets:
     - **Summary**: Overview statistics
     - **All Results**: Complete list with color coding
     - **In Custody Only**: Filtered list of defendants in custody
   - Color coded:
     - Red: In custody
     - Green: Not in custody
     - Yellow: Errors

## Monday Morning Workflow

**It's now just 2 steps:**

1. Drop your updated defendant list into the `input/` folder
   - **Use PDF format if available** (Prosecutor Worklist Report - more complete data)
   - CSV also works (Active Cases By Assigned Personnel Detail - but names may be truncated)

2. Run the checker:
   ```cmd
   run_check.bat
   ```
   That's it! The script automatically finds files and prefers PDF for better accuracy.

3. Check the console output for in-custody defendants

4. Open the Excel report in `output/` folder for detailed review

5. Review the "In Custody Only" sheet for quick reference

**Pro tip:** The script shows which file it selected, so you can verify it picked the right one. It will choose PDF over CSV when both are present.

## PDF Input Format (RECOMMENDED)

Expected format: Prosecutor Worklist Report

**Why PDF is better:**
- Complete defendant names (no truncation)
- Full case numbers (e.g., 2024GS18-00001)
- More accurate jail database searches

The parser will extract:
- Case numbers (complete, not truncated)
- Defendant names (complete, in "Last, First Middle" format)
- Available case information

## CSV Input Format (Fallback)

**Data Quality Warning:** CSV exports may truncate long names and case numbers with "..." (e.g., "Shawndez Syriek S..." instead of "Smalls, Shawndez Syriek"). This can result in less accurate jail database searches.

Expected columns:
- `Defendants`: Defendant name (required, may be truncated)
- `CaseNumbers`: Case number (optional, may be truncated)
- `Title`: Charges (optional)
- `InitiatedOn`: Incident date (optional)
- `CaseStatus`: Case status (optional)

Name format: "Last, First Middle" or "First Middle Last"

## Troubleshooting

### Environment Not Found

If you get "jail_checker environment not found":
```cmd
setup.bat
```

This will create the environment and install dependencies.

### ModuleNotFoundError

Reinstall dependencies:
```cmd
conda activate jail_checker
pip install -r requirements.txt
```

### Connection Errors

- Check your internet connection
- The jail website might be temporarily down
- Try increasing the timeout: `--timeout 60`

### Rate Limiting

If you get blocked:
- Increase delay between requests: `--delay 3.0`
- Run in smaller batches
- Wait a few minutes and try again

### No Defendants Found

- Check that your CSV has a "Defendants" column
- Verify the PDF is a Prosecutor Worklist Report
- Try opening the file manually to confirm it has data

## Running Tests

Run unit tests:
```cmd
conda activate jail_checker
python tests\unit\test_models.py
python tests\unit\test_parsers.py
```

Run doctests:
```cmd
conda activate jail_checker
python -m doctest src\models.py -v
python -m doctest src\parsers.py -v
python -m doctest src\jail_api.py -v
```

## Project Structure

```
jail-checker/
├── src/
│   ├── __init__.py       # Package initialization
│   ├── models.py          # Pydantic v2 data models
│   ├── parsers.py         # CSV & PDF parsers
│   ├── jail_api.py        # Jail database API client
│   ├── reports.py         # Report generators
│   └── main.py            # Main CLI script
├── tests/
│   ├── unit/             # Unit tests
│   │   ├── test_models.py
│   │   └── test_parsers.py
│   └── debugging/        # Debugging tests (empty)
├── input/                # Place defendant lists here
├── output/               # Generated reports saved here
├── requirements.txt      # Python dependencies
├── README_USAGE.md       # This file
└── API_DOCUMENTATION.md  # Technical API docs
```

## Technical Details

- **API**: Southern Software Citizen Connect
- **Endpoint**: `https://cc.southernsoftware.com/bookingsearch/fetchesforajax/fetch_incident_search_name.php`
- **Method**: POST
- **Rate Limiting**: 1.5 second delay between requests (default)
- **Response Format**: HTML (parsed with BeautifulSoup)

See `API_DOCUMENTATION.md` for complete technical details.

## Future Enhancements

A JavaScript+HTML version is planned that will:
- Allow drag-and-drop of CSV/PDF files
- Process files entirely in the browser
- Display results in a web interface
- No server or Python installation required

The JSON output format is designed to be compatible with this future web version.

## Support

For issues or questions:
1. Check this README
2. Review API_DOCUMENTATION.md
3. Check the reverse engineering documentation
4. Enable verbose logging to see detailed error messages

## License

Internal use only - 1st Circuit Solicitor's Office
