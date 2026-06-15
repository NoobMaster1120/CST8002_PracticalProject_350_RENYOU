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

import csv
from pathlib import Path

from records.natural_gas_record import NaturalGasRecord

DEFAULT_RECORD_LIMIT = 5


def load_records_from_csv(
    file_path: Path,
    record_limit: int = DEFAULT_RECORD_LIMIT,
) -> list[NaturalGasRecord]:
    """Open a CSV dataset and load the first few rows into record objects."""
    if not file_path.exists():
        raise FileNotFoundError(f"Dataset file not found: {file_path}")

    records: list[NaturalGasRecord] = []

    with file_path.open(mode="r", encoding="utf-8-sig", newline="") as csv_file:
        reader = csv.DictReader(csv_file)

        for row in reader:
            if row is None:
                continue

            record = NaturalGasRecord.from_csv_row(row)
            records.append(record)

            if len(records) >= record_limit:
                break

    return records
