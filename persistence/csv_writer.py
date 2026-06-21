"""
CST8002 Programming Language Research Project
Practical Project Part 3

Professor: Update with your professor's name from Brightspace
Due Date: See Brightspace for due date
Author: REN YOU

References:
[1] Python Software Foundation, "uuid — UUID objects according to RFC 9562," docs.python.org,
    [online]. Available: https://docs.python.org/3/library/uuid.html
    [Accessed: Jun. 20, 2026].
[2] Python Software Foundation, "csv — CSV File Reading and Writing," docs.python.org,
    [online]. Available: https://docs.python.org/3/library/csv.html
    [Accessed: Jun. 20, 2026].
[3] GeeksforGeeks, "Types of Linked List," geeksforgeeks.org,
    [online]. Available: https://www.geeksforgeeks.org/dsa/types-of-linked-list/
    [Accessed: Jun. 20, 2026].
"""

import csv
import uuid
from collections.abc import Iterable
from pathlib import Path

from model.natural_gas_record import CSV_FIELD_NAMES, NaturalGasRecord


def save_records_to_csv(
    records: Iterable[NaturalGasRecord],
    output_directory: Path,
) -> Path:
    """
    Persist in-memory records to a new CSV file with a UUID-based file name.

    Args:
        records: Record objects currently held in memory.
        output_directory: Folder where the generated CSV file will be written.

    Returns:
        Path to the newly created CSV file.

    Raises:
        OSError: If the output directory cannot be created or the file cannot be written.
    """
    output_directory.mkdir(parents=True, exist_ok=True)
    output_file = output_directory / f"{uuid.uuid4()}.csv"

    try:
        with output_file.open(mode="w", encoding="utf-8", newline="") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=CSV_FIELD_NAMES)
            writer.writeheader()

            for record in records:
                writer.writerow(record.to_csv_row())
    except OSError as error:
        raise OSError(f"Unable to write records to file: {output_file}") from error

    return output_file
