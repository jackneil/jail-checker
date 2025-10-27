"""
Main script for checking defendant custody status.

Usage:
    python main.py input/defendants.csv
    python main.py input/prosecutor_report.pdf --output output/
"""

import sys
import argparse
from pathlib import Path
from datetime import datetime
import logging

from models import CustodyReport
from parsers import parse_file
from jail_api import JailAPIClient
from reports import generate_json_report, generate_excel_report

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def check_custody_for_all(defendants, api_client: JailAPIClient) -> list:
    """
    Check custody status for all defendants.

    Args:
        defendants: List of Defendant objects
        api_client: JailAPIClient instance

    Returns:
        List of CustodyResult objects
    """
    results = []

    logger.info(f"Checking custody for {len(defendants)} defendants...")

    for i, defendant in enumerate(defendants, 1):
        logger.info(f"[{i}/{len(defendants)}] Checking: {defendant.full_name}")

        result = api_client.check_custody(defendant)
        results.append(result)

        if result.in_custody:
            logger.warning(f"  *** IN CUSTODY: {defendant.full_name} ***")
        elif result.error_message:
            logger.error(f"  ERROR: {result.error_message}")
        else:
            logger.info(f"  Not in custody")

    return results


def main():
    """
    Main entry point for the custody checker.

    >>> # This function is tested manually, not via doctest
    """
    parser = argparse.ArgumentParser(
        description="Check defendant custody status in Dorchester County jail"
    )

    parser.add_argument(
        'input_file',
        type=str,
        help='Path to input file (CSV or PDF with defendant list)'
    )

    parser.add_argument(
        '--output',
        '-o',
        type=str,
        default='output',
        help='Output directory for reports (default: output/)'
    )

    parser.add_argument(
        '--delay',
        '-d',
        type=float,
        default=1.5,
        help='Delay in seconds between API requests (default: 1.5)'
    )

    parser.add_argument(
        '--timeout',
        '-t',
        type=int,
        default=30,
        help='Request timeout in seconds (default: 30)'
    )

    parser.add_argument(
        '--max-retries',
        '-r',
        type=int,
        default=3,
        help='Maximum number of retry attempts (default: 3)'
    )

    parser.add_argument(
        '--verbose',
        '-v',
        action='store_true',
        help='Enable verbose logging'
    )

    args = parser.parse_args()

    # Configure logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Validate input file
    input_path = Path(args.input_file)
    if not input_path.exists():
        logger.error(f"Input file not found: {input_path}")
        sys.exit(1)

    # Create output directory
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        # Parse input file
        logger.info(f"Parsing input file: {input_path}")
        defendants = parse_file(input_path)
        logger.info(f"Found {len(defendants)} defendants")

        if not defendants:
            logger.error("No defendants found in input file")
            sys.exit(1)

        # Create API client
        with JailAPIClient(
            delay_seconds=args.delay,
            max_retries=args.max_retries,
            timeout=args.timeout
        ) as api_client:

            # Check custody for all defendants
            custody_results = check_custody_for_all(defendants, api_client)

        # Create report
        report = CustodyReport(
            source_file=str(input_path),
            defendants_checked=defendants,
            custody_results=custody_results
        )

        # Print summary
        print("\n" + "=" * 70)
        print(report.summary())
        print("=" * 70 + "\n")

        # Generate timestamp for output files
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        base_name = input_path.stem

        # Generate reports
        json_output = output_dir / f"{base_name}_custody_{timestamp}.json"
        excel_output = output_dir / f"{base_name}_custody_{timestamp}.xlsx"

        logger.info(f"Generating JSON report: {json_output}")
        generate_json_report(report, json_output)

        logger.info(f"Generating Excel report: {excel_output}")
        generate_excel_report(report, excel_output)

        # Print in-custody list
        in_custody = report.get_in_custody_list()
        if in_custody:
            print(f"\n*** DEFENDANTS IN CUSTODY ({len(in_custody)}) ***")
            print("-" * 70)
            for result in in_custody:
                print(f"  • {result.defendant_name}")
                if result.booking_date:
                    print(f"    Booked: {result.booking_date}")
                if result.charges_at_booking:
                    print(f"    Charges: {result.charges_at_booking}")
                if result.bond_amount:
                    print(f"    Bond: {result.bond_amount}")
                print()
        else:
            print("\n*** NO DEFENDANTS CURRENTLY IN CUSTODY ***\n")

        print(f"\nReports saved to:")
        print(f"  JSON:  {json_output}")
        print(f"  Excel: {excel_output}\n")

        logger.info("Custody check complete!")

    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        sys.exit(1)

    except ValueError as e:
        logger.error(f"Error parsing input file: {e}")
        sys.exit(1)

    except KeyboardInterrupt:
        logger.warning("\nOperation cancelled by user")
        sys.exit(130)

    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
