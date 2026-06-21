"""
CST8002 Programming Language Research Project
Practical Project Part 2

Author: REN YOU

References:
[1] K. Fakhroutdinov, "Multi-Layered Application: UML Model Diagram Example," uml-diagrams.org,
    [online]. Available: https://www.uml-diagrams.org/multi-layered-application-uml-model-diagram-example.html
    [Accessed: Jun. 14, 2026].
[2] Python Software Foundation, "Built-in Types," docs.python.org,
    [online]. Available: https://docs.python.org/3/library/stdtypes.html
    [Accessed: Jun. 14, 2026].
"""

from pathlib import Path

from model.natural_gas_record import NaturalGasRecord
from persistence.csv_reader import DEFAULT_RECORD_LIMIT, load_records_from_csv
from persistence.csv_writer import save_records_to_csv


class RecordService:
    """
    Business layer service that manages the in-memory list of record objects.

    All CRUD operations on records are handled here instead of in the presentation layer.
    """

    def __init__(self) -> None:
        """Initialize an empty in-memory record collection."""
        self._records: list[NaturalGasRecord] = []

    def get_record_count(self) -> int:
        """Return the number of records currently stored in memory."""
        return len(self._records)

    def get_all_records(self) -> list[NaturalGasRecord]:
        """Return a copy of all records currently stored in memory."""
        return list(self._records)

    def get_record(self, one_based_index: int) -> NaturalGasRecord:
        """
        Return one record from the in-memory collection.

        Args:
            one_based_index: User-facing record number starting at 1.

        Returns:
            The selected NaturalGasRecord object.

        Raises:
            IndexError: If the requested record number is out of range.
        """
        return self._records[one_based_index - 1]

    def reload_from_dataset(
        self,
        dataset_path: Path,
        record_limit: int = DEFAULT_RECORD_LIMIT,
    ) -> int:
        """
        Replace in-memory records by reading from the dataset file again.

        Args:
            dataset_path: Path to the source CSV dataset.
            record_limit: Maximum number of records to load.

        Returns:
            Number of records loaded into memory.
        """
        self._records = load_records_from_csv(dataset_path, record_limit)
        return len(self._records)

    def add_record(self, record: NaturalGasRecord) -> None:
        """
        Append a new record object to the in-memory collection.

        Args:
            record: Parsed record object to store.
        """
        self._records.append(record)

    def update_record(self, one_based_index: int, record: NaturalGasRecord) -> None:
        """
        Replace an existing record in the in-memory collection.

        Args:
            one_based_index: User-facing record number starting at 1.
            record: Updated record object.

        Raises:
            IndexError: If the requested record number is out of range.
        """
        self._records[one_based_index - 1] = record

    def delete_record(self, one_based_index: int) -> NaturalGasRecord:
        """
        Remove a record from the in-memory collection.

        Args:
            one_based_index: User-facing record number starting at 1.

        Returns:
            The removed record object.

        Raises:
            IndexError: If the requested record number is out of range.
        """
        return self._records.pop(one_based_index - 1)

    def persist_to_disk(self, output_directory: Path) -> Path:
        """
        Write all in-memory records to a new CSV file in the output directory.

        Args:
            output_directory: Folder where the generated CSV file will be saved.

        Returns:
            Path to the newly created CSV file.
        """
        return save_records_to_csv(self._records, output_directory)
