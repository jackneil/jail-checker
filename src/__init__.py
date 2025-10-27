"""
Jail Custody Checker - Check defendant custody status in Dorchester County jail.
"""

__version__ = "1.0.0"

from .models import Defendant, CustodyResult, CustodyReport
from .parsers import parse_file, parse_csv_file, parse_pdf_file
from .jail_api import JailAPIClient
from .reports import generate_json_report, generate_excel_report

__all__ = [
    "Defendant",
    "CustodyResult",
    "CustodyReport",
    "parse_file",
    "parse_csv_file",
    "parse_pdf_file",
    "JailAPIClient",
    "generate_json_report",
    "generate_excel_report",
]
