"""
Parsers for defendant lists from CSV and PDF files.

This module provides functions to extract defendant information from:
- CSV files (Active Cases By Assigned Personnel Detail)
- PDF files (Prosecutor Worklist Report)
"""

import re
import csv
import logging
from pathlib import Path
from typing import List, Optional
import pdfplumber
import pandas as pd

from models import Defendant

# Configure logging
logger = logging.getLogger(__name__)


def parse_defendant_name(name_str: str) -> tuple[str, str, str]:
    """
    Parse a defendant name string into first, middle, and last names.

    Handles formats like:
    - "Last, First Middle"
    - "Last, First M."
    - "Last, First"
    - "First Last"

    >>> parse_defendant_name("Smith, John Michael")
    ('John', 'Michael', 'Smith')
    >>> parse_defendant_name("Doe, Jane M.")
    ('Jane', 'M.', 'Doe')
    >>> parse_defendant_name("Johnson, Bob")
    ('Bob', '', 'Johnson')
    """
    name_str = name_str.strip()

    # Handle "Last, First Middle" format
    if ',' in name_str:
        parts = name_str.split(',', 1)
        last_name = parts[0].strip()
        first_middle = parts[1].strip()

        # Split first and middle
        name_parts = first_middle.split()
        if len(name_parts) >= 2:
            first_name = name_parts[0]
            middle_name = ' '.join(name_parts[1:])
        elif len(name_parts) == 1:
            first_name = name_parts[0]
            middle_name = ""
        else:
            first_name = ""
            middle_name = ""

        return (first_name, middle_name, last_name)

    # Handle "First Last" or "First Middle Last" format
    parts = name_str.split()
    if len(parts) >= 3:
        first_name = parts[0]
        middle_name = ' '.join(parts[1:-1])
        last_name = parts[-1]
    elif len(parts) == 2:
        first_name = parts[0]
        middle_name = ""
        last_name = parts[1]
    elif len(parts) == 1:
        # Only one name, assume it's the last name
        first_name = ""
        middle_name = ""
        last_name = parts[0]
    else:
        first_name = ""
        middle_name = ""
        last_name = ""

    return (first_name, middle_name, last_name)


def parse_csv_file(file_path: str | Path) -> List[Defendant]:
    """
    Parse a CSV file containing defendant information.

    Expected CSV format: Active Cases By Assigned Personnel Detail
    Columns: CaseNumbers, Title, Defendants, InitiatedOn, Type, Disposition, etc.

    >>> import tempfile
    >>> import os
    >>> with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv', newline='') as f:
    ...     f.write('CaseNumbers,Title,Defendants,InitiatedOn,Type\\n')
    ...     f.write('2024GS001,Theft,Smith John Michael,01/15/2024,General Sessions\\n')
    ...     f.write('2024GS002,Assault,Doe Jane,02/20/2024,General Sessions\\n')
    ...     temp_path = f.name
    >>> defendants = parse_csv_file(temp_path)
    >>> len(defendants)
    2
    >>> defendants[0].last_name
    'Smith'
    >>> defendants[0].first_name
    'John'
    >>> os.unlink(temp_path)

    Args:
        file_path: Path to the CSV file

    Returns:
        List of Defendant objects

    Raises:
        FileNotFoundError: If the CSV file doesn't exist
        ValueError: If required columns are missing
    """
    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"CSV file not found: {file_path}")

    try:
        # Read CSV with pandas for better handling
        # Skip first 3 rows (textbox headers, title row, empty row) to get to actual column headers
        df = pd.read_csv(file_path, skiprows=3)

        # Check for required columns
        if 'Defendants' not in df.columns:
            raise ValueError("CSV file must contain 'Defendants' column")

        defendants = []

        for index, row in df.iterrows():
            # Skip header rows or empty rows
            if pd.isna(row.get('Defendants')) or str(row.get('Defendants')).strip() == '':
                continue

            # Skip the summary/header row
            defendant_name = str(row['Defendants']).strip()
            if 'ACTIVE CASES' in defendant_name.upper() or defendant_name == 'Defendants':
                continue

            # Parse the name
            first, middle, last = parse_defendant_name(defendant_name)

            if not last:  # Skip if we couldn't parse a last name
                continue

            # Extract other fields
            case_number = str(row.get('CaseNumbers', '')).strip() if pd.notna(row.get('CaseNumbers')) else None
            charges = str(row.get('Title', '')).strip() if pd.notna(row.get('Title')) else None
            incident_date = str(row.get('InitiatedOn', '')).strip() if pd.notna(row.get('InitiatedOn')) else None
            case_status = str(row.get('CaseStatus', '')).strip() if pd.notna(row.get('CaseStatus')) else None

            defendant = Defendant(
                last_name=last,
                first_name=first,
                middle_name=middle,
                case_number=case_number,
                charges=charges,
                incident_date=incident_date,
                case_status=case_status
            )

            defendants.append(defendant)

        return defendants

    except Exception as e:
        raise ValueError(f"Error parsing CSV file: {str(e)}")


def parse_pdf_file(file_path: str | Path) -> List[Defendant]:
    """
    Parse a PDF file containing defendant information.

    Expected PDF format: Prosecutor Worklist Report
    Extracts defendant names and case information from the report.

    >>> import tempfile
    >>> # Note: This doctest would require a real PDF file to test properly
    >>> # For now, we'll skip automatic testing of this function

    Args:
        file_path: Path to the PDF file

    Returns:
        List of Defendant objects

    Raises:
        FileNotFoundError: If the PDF file doesn't exist
        ValueError: If PDF cannot be parsed
    """
    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"PDF file not found: {file_path}")

    defendants = []
    all_case_numbers = []  # Track all case numbers found
    failed_extractions = []  # Track failed extractions

    try:
        with pdfplumber.open(file_path) as pdf:
            for page_num, page in enumerate(pdf.pages, 1):
                # Extract words with their positions
                words = page.extract_words()

                if not words:
                    continue  # Skip pages with no content

                # Find case numbers by position and content
                # Case numbers are at x-position 100-200 and contain "GS"
                case_words = [
                    w for w in words
                    if 'GS' in w['text']
                    and 100 < w['x0'] < 200
                ]

                for case in case_words:
                    # Clean up case number (remove trailing comma if present)
                    case_no = case['text'].rstrip(',')
                    all_case_numbers.append(case_no)

                    # Extract matter number from same row (left column)
                    # Matter numbers are at x-position < 100 and contain a dash
                    matter_words = [
                        w for w in words
                        if abs(w['top'] - case['top']) < 1
                        and w['x0'] < 100
                        and '-' in w['text']
                        and len(w['text']) > 3
                    ]
                    matter_no = matter_words[0]['text'] if matter_words else None

                    # Extract defendant name from same row
                    # Defendant names are in the column at x-position 210-360
                    # and at the same y-position (top) as the case number
                    defendant_words = [
                        w for w in words
                        if abs(w['top'] - case['top']) < 1
                        and 210 < w['x0'] < 360
                    ]

                    if not defendant_words:
                        failed_extractions.append({
                            'case_number': case_no,
                            'page': page_num,
                            'reason': 'No defendant name found in expected column'
                        })
                        continue

                    # Sort words by x-position and join to form name
                    defendant_words_sorted = sorted(defendant_words, key=lambda x: x['x0'])
                    defendant_name = ' '.join([w['text'] for w in defendant_words_sorted])

                    if not defendant_name or not defendant_name.strip():
                        failed_extractions.append({
                            'case_number': case_no,
                            'page': page_num,
                            'reason': 'Defendant name was empty after extraction'
                        })
                        continue

                    # Parse name into first, middle, last
                    first, middle, last = parse_defendant_name(defendant_name)

                    # Only add if we got BOTH first and last name (required by Defendant model)
                    if not (first and first.strip() and last and last.strip()):
                        failed_extractions.append({
                            'case_number': case_no,
                            'page': page_num,
                            'defendant_name': defendant_name,
                            'reason': f'Name parsing failed - first={repr(first)}, last={repr(last)}'
                        })
                        continue

                    defendant = Defendant(
                        last_name=last,
                        first_name=first,
                        middle_name=middle or "",
                        matter_number=matter_no,
                        case_number=case_no
                    )
                    defendants.append(defendant)

        # Log extraction statistics
        logger.info(f"PDF Extraction Summary:")
        logger.info(f"  Total case numbers found: {len(all_case_numbers)}")
        logger.info(f"  Successfully extracted: {len(defendants)}")
        logger.info(f"  Failed extractions: {len(failed_extractions)}")

        if failed_extractions:
            logger.warning(f"Failed to extract {len(failed_extractions)} case(s):")
            for fail in failed_extractions:
                logger.warning(f"  Page {fail['page']} | {fail['case_number']} - {fail['reason']}")

        # Remove duplicates (same defendant might appear on multiple pages)
        seen = set()
        unique_defendants = []
        for d in defendants:
            key = (d.last_name.lower(), d.first_name.lower(), d.case_number)
            if key not in seen:
                seen.add(key)
                unique_defendants.append(d)

        return unique_defendants

    except Exception as e:
        raise ValueError(f"Error parsing PDF file: {str(e)}")


def parse_file(file_path: str | Path) -> List[Defendant]:
    """
    Parse a defendant list file (auto-detect CSV or PDF).

    >>> import tempfile
    >>> import os
    >>> with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv', newline='') as f:
    ...     f.write('CaseNumbers,Defendants\\n')
    ...     f.write('2024GS001,Smith John\\n')
    ...     temp_path = f.name
    >>> defendants = parse_file(temp_path)
    >>> len(defendants)
    1
    >>> os.unlink(temp_path)

    Args:
        file_path: Path to the file (CSV or PDF)

    Returns:
        List of Defendant objects

    Raises:
        FileNotFoundError: If file doesn't exist
        ValueError: If file format is not supported
    """
    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    suffix = file_path.suffix.lower()

    if suffix == '.csv':
        return parse_csv_file(file_path)
    elif suffix == '.pdf':
        return parse_pdf_file(file_path)
    else:
        raise ValueError(f"Unsupported file format: {suffix}. Use .csv or .pdf")


if __name__ == "__main__":
    import doctest
    doctest.testmod()
