"""
Unit tests for parsers module.

Run with: python -m pytest tests/unit/test_parsers.py -v
Or run doctests: python -m doctest src/parsers.py -v
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from parsers import parse_defendant_name


def test_parse_defendant_name_with_middle():
    """
    Test parsing name with middle name.

    >>> parse_defendant_name("Smith, John Michael")
    ('John', 'Michael', 'Smith')
    """
    result = parse_defendant_name("Smith, John Michael")
    assert result == ("John", "Michael", "Smith")


def test_parse_defendant_name_without_middle():
    """
    Test parsing name without middle name.

    >>> parse_defendant_name("Doe, Jane")
    ('Jane', '', 'Doe')
    """
    result = parse_defendant_name("Doe, Jane")
    assert result == ("Jane", "", "Doe")


def test_parse_defendant_name_with_initial():
    """
    Test parsing name with middle initial.

    >>> parse_defendant_name("Johnson, Bob Q.")
    ('Bob', 'Q.', 'Johnson')
    """
    result = parse_defendant_name("Johnson, Bob Q.")
    assert result == ("Bob", "Q.", "Johnson")


def test_parse_defendant_name_multiple_middle():
    """
    Test parsing name with multiple middle names.

    >>> parse_defendant_name("Washington, George Thomas Patrick")
    ('George', 'Thomas Patrick', 'Washington')
    """
    result = parse_defendant_name("Washington, George Thomas Patrick")
    assert result == ("George", "Thomas Patrick", "Washington")


def test_parse_defendant_name_no_comma():
    """
    Test parsing name without comma (First Last format).

    >>> parse_defendant_name("John Smith")
    ('John', '', 'Smith')
    """
    result = parse_defendant_name("John Smith")
    assert result == ("John", "", "Smith")


def test_parse_defendant_name_three_parts_no_comma():
    """
    Test parsing three-part name without comma.

    >>> parse_defendant_name("John Michael Smith")
    ('John', 'Michael', 'Smith')
    """
    result = parse_defendant_name("John Michael Smith")
    assert result == ("John", "Michael", "Smith")


if __name__ == "__main__":
    import doctest
    doctest.testmod()

    # Run tests
    test_parse_defendant_name_with_middle()
    test_parse_defendant_name_without_middle()
    test_parse_defendant_name_with_initial()
    test_parse_defendant_name_multiple_middle()
    test_parse_defendant_name_no_comma()
    test_parse_defendant_name_three_parts_no_comma()

    print("All parser tests passed!")
