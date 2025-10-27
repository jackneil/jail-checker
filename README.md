# Dorchester County Jail Custody Checker

Automated tool to check defendant custody status in Dorchester County SC jail database.

## ⚡ SIMPLEST WAY TO USE THIS

**Just want to check custody status right now? Here's how:**

1. **Download this repository as ZIP**
   - Go to https://github.com/jackneil/jail-checker
   - Click green "Code" button → "Download ZIP"
   - Extract anywhere on your computer

2. **Open the HTML file**
   - Navigate to the `web` folder
   - Double-click `custody-checker.html` (opens in your browser)

3. **Drop your PDF**
   - Drag your Prosecutor Worklist Report PDF onto the page
   - Wait ~30 seconds while it checks 200+ defendants
   - Click "Download Excel" to save the report

**That's it. No installation, no setup, no bullshit.**

The proxy server is already deployed and working. Just use the HTML file.

---

## 🎯 Which Version Should I Use?

### Browser Version (Simplest)
**Use this if:** You just want it to work right now.

**Pros:**
- ✅ Zero setup - just open the HTML file
- ✅ Works on any computer with Chrome/Edge
- ✅ Fast parallel loading (5 pages at once)
- ✅ Portable - copy to USB drive and use anywhere

**Cons:**
- ⚠️ Relies on cloud proxy (if it goes down, you're stuck)
- ⚠️ Excel export doesn't embed mugshot images (browser limitation)
- ⚠️ Requires internet connection

**File location:** `web/custody-checker.html`

### Python Version (Full Features)
**Use this if:** You want prettier Excel files with embedded mugshots and don't want to rely on a cloud proxy.

**Pros:**
- ✅ Excel files have embedded 100x125px mugshots for in-custody defendants
- ✅ Works offline after initial setup
- ✅ More control over output format
- ✅ Not dependent on external proxy server

**Cons:**
- ⚠️ Requires Python/conda environment setup (one-time, 5 minutes)
- ⚠️ Slightly more steps to run

**How to use:**
1. Run `scripts\setup.bat` (first time only)
2. Drop PDF into `input/` folder
3. Double-click `scripts\run_check.bat`
4. Open Excel file in `output/` folder

---

## 🔧 Optional: Deploy Your Own Proxy

The HTML file is hardcoded to use a proxy server that's already deployed and working. But if you want to deploy your own (for redundancy or control), see `DEPLOY.md` for instructions.

**You don't need to do this unless:**
- The existing proxy stops working
- You want your own private proxy server
- You're paranoid about using someone else's server

---

## 📥 Getting the Code

### Method 1: Download ZIP (Simplest)

1. Go to https://github.com/jackneil/jail-checker
2. Click green "Code" button → "Download ZIP"
3. Extract to `C:\Github\jail-checker\` (or anywhere you want)
4. Done!

### Method 2: Git Clone (Better for Updates)

**First time? Install Git:**

1. **Download Git for Windows:**
   👉 https://git-scm.com/download/win
   - Click "Click here to download" (64-bit version)

2. **Run the installer** (`Git-2.x.x-64-bit.exe`)
   - Click "Next" through all screens
   - Use default settings

3. **Verify installation:**
   - Open PowerShell
   - Type: `git --version`
   - You should see something like: `git version 2.x.x`

**Then clone the repository:**

```powershell
cd C:\Github
git clone https://github.com/jackneil/jail-checker.git
```

### 💡 Why Git Clone is better:
- Easy updates: Just run `git pull` to get new features
- With ZIP: You have to re-download and extract every time

---

## Overview

This tool queries the Dorchester County Sheriff's Office jail booking system to determine which defendants from a prosecutor's list are currently in custody. It uses the Southern Software Citizen Connect API to fetch real-time custody information.

**Key Features:**
- ✅ Extracts defendants from PDF or CSV files
- ✅ Checks custody status against live jail database (305+ inmates)
- ✅ Generates Excel reports with color-coded results
- ✅ Sorts in-custody defendants to the top for quick review
- ✅ No authentication required - uses public booking records
- ✅ 100% accurate PDF extraction with matter/case number tracking
- ✅ Parallel loading for 5x faster results

## Monday Morning Workflow

**Browser Version:**
1. Open `web/custody-checker.html` in Chrome
2. Drag your PDF onto the page
3. Wait 30 seconds
4. Download Excel

**Python Version:**
1. Drop PDF into `input/` folder
2. Double-click `scripts\run_check.bat`
3. Open Excel file in `output/` folder

Everything below is technical details and troubleshooting.

---

## Quick Start

### 1. Setup (One Time)

Run the setup script to create the conda environment:

```cmd
scripts\setup.bat
```

This will:
- Create `jail_checker` conda environment with Python 3.11
- Install all required packages (requests, beautifulsoup4, pdfplumber, pandas, openpyxl)

### 2. Prepare Input Files

Place your defendant list in the `input/` folder:
- **PDF format (RECOMMENDED)**: `Prosecutor Worklist Report.pdf`
- **CSV format (fallback)**: `Active Cases By Assigned Personnel Detail.csv`

**Why PDF is better:**
- Complete defendant names (no truncation)
- Full case numbers and matter numbers
- More accurate jail database searches

### 3. Run the Checker

```cmd
scripts\run_check.bat
```

The script will:
- Auto-detect the most recent file in `input/`
- Extract all defendants (205 from PDF example)
- Check each against current confinements (305 inmates)
- Generate reports in `output/` folder

## Monday Morning Workflow

**It's just 2 steps:**

1. **Drop the updated list** into `input/` folder
   - Use PDF format (Prosecutor Worklist Report) for complete data
   - CSV also works but may have truncated names

2. **Run the checker:**
   ```cmd
   scripts\run_check.bat
   ```

3. **Review the results:**
   - Console shows in-custody defendants with ⚠️ warnings
   - Excel report in `output/` folder
   - Check the "In Custody Only" sheet for quick reference

## Browser Version (Requires One-Time Proxy Deployment)

**Perfect for:**
- Users who can do one-time Vercel deployment
- Running from any computer after deployment
- Sharing with colleagues (they just open HTML file)
- No Python/conda environment needed after proxy is deployed

**Why a proxy?** The jail API requires session cookies which browsers can't handle due to CORS restrictions. Our serverless proxy (hosted free on Vercel) handles sessions and forwards requests.

### Deployment (One-Time, 5 Minutes)

**See `DEPLOY.md` for detailed instructions.**

Quick steps:
```powershell
# Install Vercel CLI
npm install -g vercel

# Deploy
cd C:\Github\jail-checker
vercel login
vercel
```

After deployment, edit `web/custody-checker.html` line 686 to use your Vercel URL instead of `localhost`.

### How to Use (After Deployment)

1. **Navigate to the web folder:**
   - Open `C:\Github\jail-checker\web\custody-checker.html` in Google Chrome
   - Or copy the HTML file to a USB drive and open from there

2. **Upload your defendant list:**
   - Drag and drop your PDF (Prosecutor Worklist Report) onto the page
   - Or click the drop zone to browse for a file
   - CSV files also supported

3. **Choose options:**
   - **Load mugshots checkbox**: Uncheck for faster results (default: off)
   - If checked, adds ~5-10 seconds to download mugshot images

4. **Wait for results:**
   - PDF parsing: ~5 seconds
   - Database queries: ~20-30 seconds for 200+ defendants
   - Mugshot loading (if enabled): ~5-10 seconds
   - **Total time: 30-45 seconds**

5. **Review results:**
   - Summary cards show total/in-custody/not-in-custody counts
   - Table shows all defendants with color coding:
     - Red rows = In custody
     - Green rows = Not in custody
     - Yellow rows = Errors
   - Click "Download Excel" to save report

### Browser Version Features

✅ **Fully client-side** - runs in your browser, no server needed
✅ **Works offline** - after loading the page once (PDF libraries cached)
✅ **Same accuracy** - uses identical PDF parsing and matching logic
✅ **Live data** - queries real-time jail database API
✅ **Excel export** - generates same 3-sheet Excel format as Python version
✅ **Mugshot support** - optional image loading and display
✅ **USB portable** - just copy the HTML file

### Browser Version Limitations

⚠️ **Excel file has no embedded mugshots** - browser version can't embed images in Excel (SheetJS limitation)
⚠️ **Requires internet connection** - to query jail database and load CDN libraries
⚠️ **No command-line options** - all configuration through UI checkboxes
⚠️ **Chrome recommended** - tested in Chrome, may work in Edge/Firefox but not guaranteed

### Technical Details

The browser version uses:
- **PDF.js** (Mozilla) - Client-side PDF parsing
- **SheetJS** (xlsx.js) - Excel file generation
- **Vanilla JavaScript** - No framework dependencies
- **Fetch API** - Direct HTTP calls to jail database
- **Single HTML file** - All code embedded (CSS + JavaScript)

**File location:** `web/custody-checker.html` (~35KB single file)

## Output Reports

The tool generates two reports in `output/`:

### 1. Excel Report (`*_custody_YYYYMMDD_HHMMSS.xlsx`)

**Three sheets:**

#### Summary Sheet
Basic statistics with count of:
- Total Defendants Checked
- In Custody Count
- Not in Custody Count
- Errors Count

#### All Results Sheet
Every defendant checked, sorted with in-custody first:

| Mugshot | Matter Number | Case Number | Defendant Name | Custody Status | Booking Date | Booking Number | Charges | Bond Amount | Error Message |
|---------|---------------|-------------|----------------|----------------|--------------|----------------|---------|-------------|---------------|
| [100x125px image] | 527-4129 | 2023GS18-02591 | Murray, Nicholas Edward | IN CUSTODY | 06/26/2025 | 101726 | BREAKING INTO AUTO/TANKS... | $30,000.00 | |
| [100x125px image] | 527-4514 | 2024GS18-00485 | Richards, Shawn Lamar | IN CUSTODY | 07/15/2025 | 102334 | GRAND LARCENY... | $20,000.00 | |
| | 534-2751 | 2025GS1801209 | Brown, Bradley Chad | Not in Custody | | | | | |

**Color coding:**
- 🔴 Red rows = In custody
- 🟢 Green rows = Not in custody
- 🟡 Yellow rows = Errors

**Features:**
- In-custody defendants sorted to top
- Mugshots embedded as 100x125px images (for in-custody only)
- All booking details from jail database
- Preserves your original case numbers and matter numbers

#### In Custody Only Sheet
Starts with title row: **"DEFENDANTS IN CUSTODY"**

Filtered view showing only incarcerated defendants:

| Mugshot | Matter Number | Case Number | Defendant Name | Booking Date | Booking Number | Charges | Bond Amount | Original Charges | Case Status |
|---------|---------------|-------------|----------------|--------------|----------------|---------|-------------|------------------|-------------|
| [100x125px image] | 527-4129 | 2023GS18-02591 | Murray, Nicholas Edward | 06/26/2025 | 101726 | BREAKING INTO AUTO/TANKS... | $30,000.00 | (from your PDF) | (from your PDF) |

- All rows highlighted in light red
- Includes both jail charges AND your original charges
- Quick reference for Monday morning review

### 2. JSON Report (`*_custody_YYYYMMDD_HHMMSS.json`)

Machine-readable format with:
- Complete defendant information
- Custody results with all fields
- Search metadata (date, source file)
- Suitable for further processing or web interface

## Example Results

```
Total Defendants: 205
In Custody: 17 (8.3%)
Not in Custody: 188

In Custody List:
  ⚠️ Murray, Nicholas Edward
  ⚠️ Richards, Shawn Lamar
  ⚠️ Sparks, Joshua Kane
  ⚠️ Hernandez-Reyes, Saul
  ...
```

## Advanced Usage

### Specify a File Manually

```cmd
scripts\run_check.bat "input\Active Cases By Assigned Personnel Detail.csv"
```

### Command-Line Options

```cmd
conda activate jail_checker
python src\main.py input\defendants.pdf --output custom_folder --delay 2.0 --verbose
```

**Options:**
- `--output, -o`: Output directory (default: `output/`)
- `--delay, -d`: Delay between API requests in seconds (default: 0.5)
- `--timeout, -t`: Request timeout in seconds (default: 30)
- `--max-retries, -r`: Maximum retry attempts (default: 3)
- `--verbose, -v`: Enable detailed logging

## Input File Formats

### PDF Format (RECOMMENDED)

**File**: Prosecutor Worklist Report

**Extracts:**
- Matter numbers (e.g., `527-0123`)
- Case numbers (e.g., `2024GS18-00001`)
- Defendant names in "Last, First Middle" format
- 100% accuracy - all 205 defendants extracted

### CSV Format (Fallback)

**File**: Active Cases By Assigned Personnel Detail

**Warning:** CSV exports may truncate long names with "..." which reduces search accuracy.

**Required Column:**
- `Defendants`: Defendant name

**Optional Columns:**
- `CaseNumbers`: Case number
- `Title`: Charges
- `InitiatedOn`: Incident date
- `CaseStatus`: Case status

## Troubleshooting

### Environment Not Found

```cmd
scripts\setup.bat
```

### ModuleNotFoundError

```cmd
conda activate jail_checker
pip install -r requirements.txt
```

### Connection Errors

- Check internet connection
- Jail website might be down temporarily
- Try: `--timeout 60`

### No Defendants Found

- Verify PDF is "Prosecutor Worklist Report"
- Check CSV has "Defendants" column
- Open file manually to confirm it contains data

## Project Structure

```
jail-checker/
├── src/                    # Python application code
│   ├── main.py             # CLI entry point
│   ├── models.py           # Pydantic v2 data models
│   ├── parsers.py          # PDF/CSV parsers
│   ├── jail_api.py         # Jail database API client
│   └── reports.py          # Report generators (JSON/Excel)
├── web/                    # Browser version
│   ├── custody-checker.html  # Single-file browser app
│   └── test-api.html       # API testing tool
├── api/                    # Serverless proxy (for browser version)
│   └── jail-proxy.js       # Vercel serverless function
├── tests/
│   ├── unit/               # Unit tests with doctests
│   └── debugging/          # Debugging scripts
│       ├── pdf/            # PDF extraction testing
│       ├── api/            # API testing
│       └── html/           # HTML debug captures
├── scripts/                # Python utility scripts
│   ├── setup.bat           # Environment setup
│   └── run_check.bat       # Main execution script
├── docs/                   # Documentation
│   ├── API_DOCUMENTATION.md
│   ├── REVERSE_ENGINEERING_SUMMARY.md
│   ├── PROJECT_SUMMARY.md
│   └── QUICK_REFERENCE.md
├── input/                  # Place defendant lists here
├── output/                 # Generated reports
├── requirements.txt        # Python dependencies
├── package.json            # Node.js dependencies (for proxy)
├── vercel.json             # Vercel deployment config
├── DEPLOY.md               # Proxy deployment instructions
└── README.md              # This file
```

## Running Tests

**Unit tests:**
```cmd
conda activate jail_checker
python tests\unit\test_models.py
python tests\unit\test_parsers.py
```

**Doctests:**
```cmd
python -m doctest src\models.py -v
python -m doctest src\parsers.py -v
python -m doctest src\jail_api.py -v
```

## Technical Details

### How It Works

1. **Session Initialization**
   - Visits main page to set AgencyID cookie
   - Required for API authentication

2. **Fetch Current Confinements**
   - Queries all pages (16 pages × 20 inmates = 305 total)
   - Extracts names from mugshot alt text
   - Builds lookup dictionary with name variations

3. **Match Defendants**
   - Normalizes names (lowercase, no extra spaces)
   - Tries multiple lookup keys:
     - `last first middle`
     - `last first` (without middle)
   - Returns match if found in current confinements

4. **Generate Reports**
   - Sorts in-custody defendants to top
   - Color codes Excel rows
   - Saves JSON for further processing

### API Endpoints

**Base URL:** `https://cc.southernsoftware.com/bookingsearch/`

**Primary Endpoint:**
- `fetchesforajax/fetch_current_confinements.php`
- POST with pagination (IDX parameter)
- Returns HTML with booking cards

**Agency Configuration:**
- JMS Agency ID: `SC018013C`
- URL Agency Code: `DorchesterCoSC`

**Response Format:** HTML (parsed with BeautifulSoup)
- `.booking-card` divs contain inmate information
- Mugshot `alt` text: `"Booking photo for FIRST MIDDLE LAST"`

### Rate Limiting

- Default delay: 0.5 seconds between requests
- No strict rate limits detected
- Be respectful to the public system

**See `docs/API_DOCUMENTATION.md` for complete API reference.**

## Important Notes

### Data Privacy

- Accesses publicly available booking records
- No authentication bypass or unauthorized access
- Follow all applicable laws regarding public records
- Internal use only - 1st Circuit Solicitor's Office

### Known Issues

1. **Name search endpoint doesn't work**
   - `fetch_incident_search_name.php` only searches historical records
   - Must use `fetch_current_confinements.php` instead
   - This was discovered during testing

2. **Session requirement**
   - Must visit main page first to set cookies
   - Otherwise get "Session AgencyID not set" error

3. **Python requests library needs special handling**
   - Direct requests.post() gets 500 errors
   - Must use separate GET request to initialize session
   - Then POST requests work correctly

## Legal

This tool accesses publicly available booking information provided by the Dorchester County Sheriff's Office. No authentication bypass or unauthorized access is performed. Use responsibly and in accordance with applicable laws.

**For issues with the booking system:**
- Dorchester County Sheriff's Office
- Phone: (843) 832-0300
- Address: 212 Deming Way, Summerville, SC

## License

Internal use only - 1st Circuit Solicitor's Office

---

**Last Updated:** October 27, 2025

**Current Version:** Successfully checks 205 defendants against 305 current inmates with 100% accuracy.
