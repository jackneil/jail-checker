"""
Pydantic v2 models for jail custody checker.

This module defines the data models for defendants, custody results, and reports.
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, field_validator


class Defendant(BaseModel):
    """
    Represents a defendant from the prosecutor's list.

    >>> d = Defendant(last_name="Smith", first_name="John", case_number="2024GS001")
    >>> d.full_name
    'Smith, John'
    >>> d.search_name()
    ('John', '', 'Smith')
    """

    last_name: str = Field(..., description="Defendant's last name")
    first_name: str = Field(..., description="Defendant's first name")
    middle_name: Optional[str] = Field(default="", description="Defendant's middle name or initial")
    matter_number: Optional[str] = Field(default=None, description="Matter number from prosecutor list")
    case_number: Optional[str] = Field(default=None, description="Case number from prosecutor list")
    charges: Optional[str] = Field(default=None, description="Charges description")
    incident_date: Optional[str] = Field(default=None, description="Incident date")
    case_status: Optional[str] = Field(default=None, description="Current case status")

    @property
    def full_name(self) -> str:
        """
        Returns formatted full name (Last, First Middle).

        >>> d = Defendant(last_name="Johnson", first_name="Jane", middle_name="Marie")
        >>> d.full_name
        'Johnson, Jane Marie'
        """
        if self.middle_name:
            return f"{self.last_name}, {self.first_name} {self.middle_name}"
        return f"{self.last_name}, {self.first_name}"

    def search_name(self) -> tuple[str, str, str]:
        """
        Returns name components for jail API search (first, middle, last).

        >>> d = Defendant(last_name="Doe", first_name="John", middle_name="Q")
        >>> d.search_name()
        ('John', 'Q', 'Doe')
        """
        return (self.first_name, self.middle_name or "", self.last_name)

    @field_validator('last_name', 'first_name')
    @classmethod
    def validate_name_not_empty(cls, v: str) -> str:
        """
        Validates that required name fields are not empty.

        >>> Defendant(last_name="", first_name="John")
        Traceback (most recent call last):
        ...
        pydantic_core._pydantic_core.ValidationError: ...
        """
        if not v or not v.strip():
            raise ValueError("Name fields cannot be empty")
        return v.strip()


class CustodyResult(BaseModel):
    """
    Represents the custody status result from jail database query.

    >>> result = CustodyResult(defendant_name="Smith, John", in_custody=True)
    >>> result.in_custody
    True
    """

    defendant_name: str = Field(..., description="Full name of defendant")
    matter_number: Optional[str] = Field(default=None, description="Matter number from prosecutor list")
    case_number: Optional[str] = Field(default=None, description="Case number from prosecutor list")
    in_custody: bool = Field(..., description="Whether defendant is currently in custody")
    booking_number: Optional[str] = Field(default=None, description="Jail booking number")
    booking_date: Optional[str] = Field(default=None, description="Date booked into custody")
    custody_location: Optional[str] = Field(default=None, description="Jail/detention center location")
    charges_at_booking: Optional[str] = Field(default=None, description="Charges at time of booking")
    bond_amount: Optional[str] = Field(default=None, description="Bond amount if set")
    mugshot_url: Optional[str] = Field(default=None, description="URL to mugshot image")
    query_timestamp: datetime = Field(default_factory=datetime.now, description="When this query was performed")
    error_message: Optional[str] = Field(default=None, description="Error message if query failed")

    @property
    def status_summary(self) -> str:
        """
        Returns a human-readable summary of custody status.

        >>> result = CustodyResult(defendant_name="Doe, Jane", in_custody=True, booking_date="10/27/2025")
        >>> result.status_summary
        'IN CUSTODY - Booked: 10/27/2025'
        >>> result2 = CustodyResult(defendant_name="Doe, Jane", in_custody=False)
        >>> result2.status_summary
        'NOT IN CUSTODY'
        """
        if self.error_message:
            return f"ERROR: {self.error_message}"
        if self.in_custody:
            if self.booking_date:
                return f"IN CUSTODY - Booked: {self.booking_date}"
            return "IN CUSTODY"
        return "NOT IN CUSTODY"


class CustodyReport(BaseModel):
    """
    Represents a complete custody check report for multiple defendants.

    >>> defendants = [Defendant(last_name="Smith", first_name="John")]
    >>> results = [CustodyResult(defendant_name="Smith, John", in_custody=True)]
    >>> report = CustodyReport(defendants_checked=defendants, custody_results=results)
    >>> report.total_defendants
    1
    >>> report.in_custody_count
    1
    """

    search_date: datetime = Field(default_factory=datetime.now, description="Date/time report was generated")
    source_file: Optional[str] = Field(default=None, description="Path to input file (CSV or PDF)")
    defendants_checked: List[Defendant] = Field(default_factory=list, description="List of defendants checked")
    custody_results: List[CustodyResult] = Field(default_factory=list, description="Custody status results")

    @property
    def total_defendants(self) -> int:
        """
        Returns total number of defendants checked.

        >>> report = CustodyReport(defendants_checked=[Defendant(last_name="A", first_name="B")])
        >>> report.total_defendants
        1
        """
        return len(self.defendants_checked)

    @property
    def in_custody_count(self) -> int:
        """
        Returns count of defendants currently in custody.

        >>> results = [
        ...     CustodyResult(defendant_name="A, B", in_custody=True),
        ...     CustodyResult(defendant_name="C, D", in_custody=False)
        ... ]
        >>> report = CustodyReport(custody_results=results)
        >>> report.in_custody_count
        1
        """
        return sum(1 for r in self.custody_results if r.in_custody)

    @property
    def not_in_custody_count(self) -> int:
        """
        Returns count of defendants not in custody.

        >>> results = [
        ...     CustodyResult(defendant_name="A, B", in_custody=True),
        ...     CustodyResult(defendant_name="C, D", in_custody=False),
        ...     CustodyResult(defendant_name="E, F", in_custody=False)
        ... ]
        >>> report = CustodyReport(custody_results=results)
        >>> report.not_in_custody_count
        2
        """
        return sum(1 for r in self.custody_results if not r.in_custody)

    @property
    def error_count(self) -> int:
        """
        Returns count of queries that resulted in errors.

        >>> results = [
        ...     CustodyResult(defendant_name="A, B", in_custody=False, error_message="Timeout"),
        ...     CustodyResult(defendant_name="C, D", in_custody=False)
        ... ]
        >>> report = CustodyReport(custody_results=results)
        >>> report.error_count
        1
        """
        return sum(1 for r in self.custody_results if r.error_message)

    def get_in_custody_list(self) -> List[CustodyResult]:
        """
        Returns list of all defendants currently in custody.

        >>> results = [
        ...     CustodyResult(defendant_name="Smith, John", in_custody=True),
        ...     CustodyResult(defendant_name="Doe, Jane", in_custody=False)
        ... ]
        >>> report = CustodyReport(custody_results=results)
        >>> len(report.get_in_custody_list())
        1
        >>> report.get_in_custody_list()[0].defendant_name
        'Smith, John'
        """
        return [r for r in self.custody_results if r.in_custody]

    def summary(self) -> str:
        """
        Returns a text summary of the report.

        >>> results = [
        ...     CustodyResult(defendant_name="A, B", in_custody=True),
        ...     CustodyResult(defendant_name="C, D", in_custody=False)
        ... ]
        >>> report = CustodyReport(custody_results=results)
        >>> "Total: 2" in report.summary()
        True
        >>> "In Custody: 1" in report.summary()
        True
        """
        return f"""Custody Check Summary
{'=' * 50}
Date: {self.search_date.strftime('%Y-%m-%d %H:%M:%S')}
Source: {self.source_file or 'N/A'}

Total Defendants Checked: {self.total_defendants}
In Custody: {self.in_custody_count}
Not in Custody: {self.not_in_custody_count}
Errors: {self.error_count}
"""
