"""
CST8002 Programming Language Research Project
Practical Project Part 1

Professor: Update with your professor's name from Brightspace
Due Date: See Brightspace for due date
Author: Ren

References:
[1] Python Software Foundation, "csv — CSV File Reading and Writing," docs.python.org,
    [online]. Available: https://docs.python.org/3/library/csv.html
    [Accessed: May 30, 2026].
"""

from pathlib import Path
import sys

from file_io.csv_reader import DEFAULT_RECORD_LIMIT, load_records_from_csv
from records.natural_gas_record import NaturalGasRecord

AUTHOR_NAME = "Ren"
DATASET_FILE = Path(__file__).resolve().parent / "data" / "download.csv"
RECORD_LIMIT = DEFAULT_RECORD_LIMIT


def print_header() -> None:
    """Display the author name so it remains visible during program output."""
    print("=" * 72)
    print(f"Author: {AUTHOR_NAME}")
    print("CST8002 Practical Project Part 1 - Natural Gas Production Records")
    print("=" * 72)
    print()


def print_record(index: int, record: NaturalGasRecord) -> None:
    """Print one record object to the console."""
    print(f"Record {index}")
    print(f"  CSDUID: {record.get_CSDUID()}")
    print(f"  CSD: {record.get_CSD()}")
    print(f"  Period: {record.get_Period()}")
    print(f"  IndicatorSummaryDescription: {record.get_IndicatorSummaryDescription()}")
    print(f"  UnitOfMeasure: {record.get_UnitOfMeasure()}")
    print(f"  OriginalValue: {record.get_OriginalValue():,.2f}")
    print()


def display_records(records: list[NaturalGasRecord]) -> None:
    """Loop over the record list and display each parsed record."""
    print(f"Loaded {len(records)} record(s) from: {DATASET_FILE.name}")
    print("-" * 72)

    for index, record in enumerate(records, start=1):
        print_record(index, record)


def main() -> int:
    """Program entry point."""
    print_header()

    try:
        records = load_records_from_csv(DATASET_FILE, record_limit=RECORD_LIMIT)
    except FileNotFoundError as error:
        print(f"Error: {error}")
        return 1

    if not records:
        print("No records were loaded from the dataset.")
        return 1

    display_records(records)
    print(f"Author: {AUTHOR_NAME}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
