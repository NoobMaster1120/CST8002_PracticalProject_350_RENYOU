"""
CST8002 Programming Language Research Project
Practical Project Part 2

Professor: Update with your professor's name from Brightspace
Due Date: See Brightspace for due date
Author: REN YOU

References:
[1] Python Software Foundation, "csv — CSV File Reading and Writing," docs.python.org,
    [online]. Available: https://docs.python.org/3/library/csv.html
    [Accessed: Jun. 14, 2026].
[2] Python Software Foundation, "8. Errors and Exceptions," Python Tutorial, docs.python.org,
    [online]. Available: https://docs.python.org/3/tutorial/errors.html
    [Accessed: Jun. 14, 2026].
"""

import csv
from pathlib import Path

from model.natural_gas_record import NaturalGasRecord

DEFAULT_RECORD_LIMIT = 100


def load_records_from_csv(
    file_path: Path,
    record_limit: int = DEFAULT_RECORD_LIMIT,
) -> list[NaturalGasRecord]:
    """
    Open a CSV dataset and load rows into record objects.

    Args:
        file_path: Path to the CSV dataset file.
        record_limit: Maximum number of data rows to load after the header.

    Returns:
        A list of NaturalGasRecord objects parsed from the file.

    Raises:
        FileNotFoundError: If the dataset file does not exist.
        OSError: If the file cannot be opened or read.
        ValueError: If a row cannot be parsed into a record object.
    """
    if not file_path.exists():
        raise FileNotFoundError(f"Dataset file not found: {file_path}")

    records: list[NaturalGasRecord] = []

    try:
        with file_path.open(mode="r", encoding="utf-8-sig", newline="") as csv_file:
            reader = csv.DictReader(csv_file)

            for row in reader:
                if row is None:
                    continue

                record = NaturalGasRecord.from_csv_row(row)
                records.append(record)

                if len(records) >= record_limit:
                    break
    except FileNotFoundError:
        raise
    except OSError as error:
        raise OSError(f"Unable to read dataset file: {file_path}") from error
    except (KeyError, TypeError, ValueError) as error:
        raise ValueError(f"Invalid data found while parsing {file_path}") from error

    return records
