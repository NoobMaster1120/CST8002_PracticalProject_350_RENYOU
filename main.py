"""
CST8002 Programming Language Research Project
Practical Project Part 2

Professor: Update with your professor's name from Brightspace
Due Date: See Brightspace for due date
Author: Ren

References:
[1] Python Software Foundation, "unittest — Unit testing framework," docs.python.org,
    [online]. Available: https://docs.python.org/3/library/unittest.html
    [Accessed: Jun. 14, 2026].
[2] Python Software Foundation, "csv — CSV File Reading and Writing," docs.python.org,
    [online]. Available: https://docs.python.org/3/library/csv.html
    [Accessed: Jun. 14, 2026].
"""

import sys
from pathlib import Path

from business.record_service import RecordService
from persistence.csv_reader import DEFAULT_RECORD_LIMIT
from presentation.menu import MenuController

AUTHOR_NAME = "Ren"
DATASET_FILE = Path(__file__).resolve().parent / "data" / "download.csv"
OUTPUT_DIRECTORY = Path(__file__).resolve().parent / "output"


def main() -> int:
    """
    Program entry point.

    Returns:
        Process exit code. Zero means success, one means failure.
    """
    record_service = RecordService()
    menu = MenuController(
        record_service=record_service,
        dataset_path=DATASET_FILE,
        output_directory=OUTPUT_DIRECTORY,
        author_name=AUTHOR_NAME,
    )

    menu.print_header()

    try:
        loaded_count = record_service.reload_from_dataset(
            DATASET_FILE,
            DEFAULT_RECORD_LIMIT,
        )
    except FileNotFoundError as error:
        print(f"Error: {error}")
        print("The program cannot continue without the dataset file.")
        return 1
    except OSError as error:
        print(f"File I/O error: {error}")
        return 1
    except ValueError as error:
        print(f"Data parsing error: {error}")
        return 1

    print(
        f"Loaded {loaded_count} record(s) from {DATASET_FILE.name} on startup."
    )
    print()

    menu.run()
    return 0


if __name__ == "__main__":
    sys.exit(main())
