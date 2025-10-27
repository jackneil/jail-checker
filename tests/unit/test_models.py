"""
Unit tests for models module.

Run with: python -m pytest tests/unit/test_models.py -v
Or run doctests: python -m doctest src/models.py -v
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from models import Defendant, CustodyResult, CustodyReport


def test_defendant_full_name():
    """
    Test Defendant.full_name property.

    >>> d = Defendant(last_name="Smith", first_name="John", middle_name="Michael")
    >>> d.full_name
    'Smith, John Michael'
    """
    d = Defendant(last_name="Smith", first_name="John", middle_name="Michael")
    assert d.full_name == "Smith, John Michael"

    d2 = Defendant(last_name="Doe", first_name="Jane")
    assert d2.full_name == "Doe, Jane"


def test_defendant_search_name():
    """
    Test Defendant.search_name method.

    >>> d = Defendant(last_name="Smith", first_name="John", middle_name="M")
    >>> d.search_name()
    ('John', 'M', 'Smith')
    """
    d = Defendant(last_name="Smith", first_name="John", middle_name="M")
    assert d.search_name() == ("John", "M", "Smith")


def test_custody_result_status_summary():
    """
    Test CustodyResult.status_summary property.

    >>> result = CustodyResult(defendant_name="Doe, John", in_custody=True, booking_date="10/27/2025")
    >>> result.status_summary
    'IN CUSTODY - Booked: 10/27/2025'
    """
    result = CustodyResult(defendant_name="Doe, John", in_custody=True, booking_date="10/27/2025")
    assert result.status_summary == "IN CUSTODY - Booked: 10/27/2025"

    result2 = CustodyResult(defendant_name="Doe, Jane", in_custody=False)
    assert result2.status_summary == "NOT IN CUSTODY"


def test_custody_report_counts():
    """
    Test CustodyReport count properties.

    >>> results = [
    ...     CustodyResult(defendant_name="A", in_custody=True),
    ...     CustodyResult(defendant_name="B", in_custody=False),
    ...     CustodyResult(defendant_name="C", in_custody=True)
    ... ]
    >>> report = CustodyReport(custody_results=results)
    >>> report.in_custody_count
    2
    >>> report.not_in_custody_count
    1
    """
    results = [
        CustodyResult(defendant_name="A", in_custody=True),
        CustodyResult(defendant_name="B", in_custody=False),
        CustodyResult(defendant_name="C", in_custody=True)
    ]
    report = CustodyReport(custody_results=results)

    assert report.in_custody_count == 2
    assert report.not_in_custody_count == 1
    assert report.total_defendants == 0  # No defendants_checked added


def test_custody_report_in_custody_list():
    """
    Test CustodyReport.get_in_custody_list method.

    >>> results = [
    ...     CustodyResult(defendant_name="Smith", in_custody=True),
    ...     CustodyResult(defendant_name="Doe", in_custody=False)
    ... ]
    >>> report = CustodyReport(custody_results=results)
    >>> in_custody = report.get_in_custody_list()
    >>> len(in_custody)
    1
    >>> in_custody[0].defendant_name
    'Smith'
    """
    results = [
        CustodyResult(defendant_name="Smith", in_custody=True),
        CustodyResult(defendant_name="Doe", in_custody=False)
    ]
    report = CustodyReport(custody_results=results)

    in_custody = report.get_in_custody_list()
    assert len(in_custody) == 1
    assert in_custody[0].defendant_name == "Smith"


if __name__ == "__main__":
    import doctest
    doctest.testmod()

    # Run tests
    test_defendant_full_name()
    test_defendant_search_name()
    test_custody_result_status_summary()
    test_custody_report_counts()
    test_custody_report_in_custody_list()

    print("All tests passed!")
