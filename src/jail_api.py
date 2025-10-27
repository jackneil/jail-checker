"""
API client for querying Dorchester County jail database.

Uses the reverse-engineered Southern Software Citizen Connect API.
"""

import re
import time
import logging
from typing import Optional, List, Dict
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock
import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from models import Defendant, CustodyResult

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# API configuration
JAIL_API_BASE_URL = "https://cc.southernsoftware.com/bookingsearch"
JAIL_API_MAIN_PAGE = f"{JAIL_API_BASE_URL}/index.php?AgencyID=DorchesterCoSC"
JAIL_API_CONFINEMENTS = f"{JAIL_API_BASE_URL}/fetchesforajax/fetch_current_confinements.php"
DEFAULT_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Referer': JAIL_API_MAIN_PAGE,
}
DEFAULT_DELAY_SECONDS = 0.5  # Delay between requests to be respectful


class JailAPIClient:
    """
    Client for querying the Dorchester County jail database.

    >>> client = JailAPIClient()
    >>> isinstance(client.session, requests.Session)
    True
    """

    def __init__(
        self,
        delay_seconds: float = DEFAULT_DELAY_SECONDS,
        max_retries: int = 3,
        timeout: int = 30
    ):
        """
        Initialize the jail API client.

        >>> client = JailAPIClient(delay_seconds=2.0, max_retries=5)
        >>> client.delay_seconds
        2.0
        >>> client.max_retries
        5

        Args:
            delay_seconds: Seconds to wait between requests (default 0.5)
            max_retries: Maximum number of retry attempts (default 3)
            timeout: Request timeout in seconds (default 30)
        """
        self.delay_seconds = delay_seconds
        self.max_retries = max_retries
        self.timeout = timeout
        self.last_request_time = 0

        # Thread-safe rate limiting
        self._rate_limit_lock = Lock()

        # Cache for current confinements
        self._current_inmates: Optional[Dict[str, Dict]] = None

        # Create session with retry logic
        self.session = requests.Session()

        retry_strategy = Retry(
            total=max_retries,
            status_forcelist=[429, 502, 503, 504],  # Don't retry 500s
            allowed_methods=["HEAD", "GET", "POST", "OPTIONS"],
            backoff_factor=2
        )

        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)

        self.session.headers.update(DEFAULT_HEADERS)

        # Initialize session
        self._session_initialized = False

    def _respect_rate_limit(self):
        """
        Enforce rate limiting by waiting if necessary (thread-safe).

        >>> client = JailAPIClient(delay_seconds=0.1)
        >>> import time
        >>> start = time.time()
        >>> client._respect_rate_limit()
        >>> client._respect_rate_limit()
        >>> elapsed = time.time() - start
        >>> elapsed >= 0.1  # Should have waited at least delay_seconds
        True
        """
        with self._rate_limit_lock:
            if self.last_request_time > 0:
                elapsed = time.time() - self.last_request_time
                if elapsed < self.delay_seconds:
                    sleep_time = self.delay_seconds - elapsed
                    logger.debug(f"Rate limiting: sleeping for {sleep_time:.2f} seconds")
                    time.sleep(sleep_time)
            self.last_request_time = time.time()

    def _ensure_session_initialized(self):
        """Ensure session is initialized by visiting main page once."""
        if self._session_initialized:
            return

        try:
            logger.info("Initializing session with jail database...")
            # Simple GET request without retries to avoid triggering rate limits
            response = requests.get(
                JAIL_API_MAIN_PAGE,
                headers=DEFAULT_HEADERS,
                timeout=self.timeout,
                cookies=self.session.cookies
            )
            # Transfer any cookies to our session
            for cookie in response.cookies:
                self.session.cookies.set_cookie(cookie)

            self._session_initialized = True
            logger.info("Session initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize session: {str(e)}")
            raise

    def _fetch_single_page(self, page_idx: int) -> Dict[str, Dict]:
        """
        Fetch a single page of current confinements.

        Args:
            page_idx: Page number to fetch (1-indexed)

        Returns:
            Dictionary mapping normalized names to inmate details for this page
        """
        self._respect_rate_limit()

        payload = {
            'JMSAgencyID': 'SC018013C',
            'search': '',
            'agency': '',
            'sort': 'name',
            'IDX': str(page_idx)
        }

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        response = self.session.post(
            JAIL_API_CONFINEMENTS,
            data=payload,
            headers=headers,
            timeout=self.timeout
        )

        if response.status_code != 200:
            logger.warning(f"Page {page_idx} returned status {response.status_code}")
            return {}

        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all booking cards
        booking_cards = soup.find_all('div', class_='booking-card')
        if not booking_cards:
            logger.debug(f"No inmates found on page {page_idx}")
            return {}

        logger.info(f"Page {page_idx}: Found {len(booking_cards)} inmates")

        inmates = {}
        for card in booking_cards:
            try:
                # Extract name from header
                header = card.find('h5')
                if not header:
                    continue
                full_name = header.get_text().strip()

                # Parse name components
                name_parts = full_name.split()
                if len(name_parts) < 2:
                    continue

                first_name = name_parts[0]
                last_name = name_parts[-1]
                middle_name = ' '.join(name_parts[1:-1]) if len(name_parts) > 2 else ''

                # Extract all detail fields
                detail_rows = card.find_all('div', class_='detail-row')
                booking_date = None
                arrest_datetime = None
                arresting_agency = None
                bond_amount = None

                for row in detail_rows:
                    label_elem = row.find('span', class_='detail-label')
                    value_elem = row.find('span', class_='detail-value')
                    if label_elem and value_elem:
                        label = label_elem.get_text().strip()
                        value = value_elem.get_text().strip()

                        if 'Booked:' in label:
                            booking_date = value
                        elif 'Arrest Date/Time:' in label:
                            arrest_datetime = value
                        elif 'Arresting Agency:' in label:
                            arresting_agency = value
                        elif 'Bond Total:' in label:
                            bond_amount = value

                # Extract charges
                charges_list = []
                charge_items = card.find_all('div', class_='charge-item')
                for item in charge_items:
                    charge_details = item.find('div', class_='charge-details')
                    if charge_details:
                        # Get first div text (the charge description)
                        charge_text = charge_details.find('div')
                        if charge_text:
                            charges_list.append(charge_text.get_text().strip())
                charges = '; '.join(charges_list) if charges_list else None

                # Extract mugshot URL
                mugshot_img = card.find('img', class_='booking-mugshot')
                mugshot_url = mugshot_img.get('src') if mugshot_img else None

                # Extract booking ID from "View Full Details" link
                details_link = card.find('a', href=re.compile(r'BookingID='))
                booking_number = None
                if details_link:
                    href = details_link.get('href', '')
                    booking_match = re.search(r'BookingID=(\d+)', href)
                    if booking_match:
                        booking_number = booking_match.group(1)

                # Create multiple lookup keys for matching flexibility
                keys = [
                    self._normalize_name(last_name, first_name, middle_name),
                    self._normalize_name(last_name, first_name, ''),  # Without middle
                ]

                inmate_data = {
                    'full_name': full_name,
                    'first_name': first_name,
                    'middle_name': middle_name,
                    'last_name': last_name,
                    'booking_date': booking_date,
                    'arrest_datetime': arrest_datetime,
                    'arresting_agency': arresting_agency,
                    'bond_amount': bond_amount,
                    'charges': charges,
                    'mugshot_url': mugshot_url,
                    'booking_number': booking_number,
                }

                for key in keys:
                    inmates[key] = inmate_data

            except Exception as e:
                logger.warning(f"Error parsing booking card on page {page_idx}: {str(e)}")
                continue

        return inmates

    def _fetch_current_confinements(self) -> Dict[str, Dict]:
        """
        Fetch ALL pages of current confinements using parallel requests.

        Returns:
            Dictionary mapping normalized names to inmate details
        """
        if self._current_inmates is not None:
            return self._current_inmates

        # Ensure session is initialized first
        self._ensure_session_initialized()

        logger.info("Fetching current confinements from jail (parallel)...")
        inmates = {}

        # Fetch pages in batches using ThreadPoolExecutor
        # Use max_workers=3 to respect rate limiting while still parallelizing
        batch_size = 20
        current_batch_start = 1
        max_batches = 3  # Most jails have < 60 pages (3 batches)

        with ThreadPoolExecutor(max_workers=3) as executor:
            for batch_num in range(max_batches):
                # Submit all pages in current batch
                future_to_page = {}
                for page_idx in range(current_batch_start, current_batch_start + batch_size):
                    future = executor.submit(self._fetch_single_page, page_idx)
                    future_to_page[future] = page_idx

                # Collect results as they complete
                empty_pages = 0
                pages_with_data = 0

                for future in as_completed(future_to_page):
                    page_idx = future_to_page[future]
                    try:
                        page_inmates = future.result()
                        if page_inmates:
                            inmates.update(page_inmates)
                            pages_with_data += 1
                        else:
                            empty_pages += 1
                    except Exception as e:
                        logger.error(f"Error fetching page {page_idx}: {str(e)}")
                        empty_pages += 1

                logger.info(f"Batch {batch_num + 1}: {pages_with_data} pages with data, {empty_pages} empty")

                # If all pages in batch were empty, stop fetching
                if empty_pages == batch_size:
                    logger.info("All pages in batch were empty, stopping pagination")
                    break

                # If last page had data, continue to next batch
                current_batch_start += batch_size

        total_pages_checked = current_batch_start - 1
        logger.info(f"Loaded {len(inmates)} inmate name variations (checked up to page {total_pages_checked})")
        self._current_inmates = inmates
        return inmates

    @staticmethod
    def _normalize_name(last: str, first: str, middle: str = '') -> str:
        """
        Normalize name for matching (lowercase, no extra spaces).

        >>> JailAPIClient._normalize_name("Smith", "John", "Q")
        'smith john q'
        >>> JailAPIClient._normalize_name("ADAMS", "AVERY", "ARRON")
        'adams avery arron'
        """
        parts = [last, first]
        if middle:
            parts.append(middle)
        return ' '.join(p.lower().strip() for p in parts if p)

    def check_custody(self, defendant: Defendant) -> CustodyResult:
        """
        Check if a defendant is currently in custody by matching against current confinements list.

        >>> client = JailAPIClient()
        >>> # Note: This doctest would require mocking the actual API call
        >>> # For demonstration, we'll skip automatic testing of this function

        Args:
            defendant: Defendant object with name information

        Returns:
            CustodyResult object with custody status information
        """
        first_name, middle_name, last_name = defendant.search_name()

        logger.info(f"Checking custody for: {defendant.full_name}")

        try:
            # Fetch current confinements (uses cache after first call)
            inmates = self._fetch_current_confinements()

            # Try to find match with multiple name variations
            lookup_keys = [
                self._normalize_name(last_name, first_name, middle_name),
                self._normalize_name(last_name, first_name, ''),  # Without middle name
            ]

            for key in lookup_keys:
                if key in inmates:
                    inmate = inmates[key]
                    logger.info(f"IN CUSTODY: {defendant.full_name} matched as {inmate['full_name']}")
                    return CustodyResult(
                        defendant_name=defendant.full_name,
                        matter_number=defendant.matter_number,
                        case_number=defendant.case_number,
                        in_custody=True,
                        booking_number=inmate.get('booking_number'),
                        booking_date=inmate.get('booking_date'),
                        custody_location='Dorchester County Detention Center',
                        charges_at_booking=inmate.get('charges'),
                        bond_amount=inmate.get('bond_amount'),
                        mugshot_url=inmate.get('mugshot_url'),
                        status_summary=f"IN CUSTODY - Matched as {inmate['full_name']}"
                    )

            # Not found in current confinements
            logger.info(f"Not in custody: {defendant.full_name}")
            return CustodyResult(
                defendant_name=defendant.full_name,
                matter_number=defendant.matter_number,
                case_number=defendant.case_number,
                in_custody=False
            )

        except Exception as e:
            logger.error(f"Error checking custody for {defendant.full_name}: {str(e)}")
            return CustodyResult(
                defendant_name=defendant.full_name,
                matter_number=defendant.matter_number,
                case_number=defendant.case_number,
                in_custody=False,
                error_message=f"Error: {str(e)}"
            )

    def close(self):
        """
        Close the session.

        >>> client = JailAPIClient()
        >>> client.close()
        >>> # Session is now closed
        """
        self.session.close()

    def __enter__(self):
        """
        Context manager entry.

        >>> with JailAPIClient() as client:
        ...     isinstance(client, JailAPIClient)
        True
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Context manager exit.

        >>> with JailAPIClient() as client:
        ...     pass  # Client is automatically closed
        """
        self.close()


if __name__ == "__main__":
    import doctest
    doctest.testmod()
