"""
CST8002 Programming Language Research Project
Practical Project Part 4

Author: REN YOU

References:
[1] K. Fakhroutdinov, "Multi-Layered Application: UML Model Diagram Example," uml-diagrams.org,
    [online]. Available: https://www.uml-diagrams.org/multi-layered-application-uml-model-diagram-example.html
    [Accessed: Jun. 20, 2026].
[2] GeeksforGeeks, "Types of Linked List," geeksforgeeks.org,
    [online]. Available: https://www.geeksforgeeks.org/dsa/types-of-linked-list/
    [Accessed: Jun. 20, 2026].
[3] Matplotlib Development Team, "Bar charts," matplotlib.org,
    [online]. Available:
    https://matplotlib.org/stable/gallery/lines_bars_and_markers/bar_colors.html
    [Accessed: Aug. 14, 2026].
"""

from pathlib import Path

from model.natural_gas_record import NaturalGasRecord
from model.singly_linked_list import NaturalGasLinkedList
from persistence.csv_reader import DEFAULT_RECORD_LIMIT, load_records_from_csv
from persistence.csv_writer import save_records_to_csv

SUPPORTED_CHART_GROUP_FIELDS = ("CSD", "Period")


class RecordService:
    """
    Business layer service that manages the in-memory singly linked list of records.

    All CRUD operations on records are handled here instead of in the presentation layer.
    """

    def __init__(self) -> None:
        """Initialize an empty in-memory record collection."""
        self._records: NaturalGasLinkedList = NaturalGasLinkedList()

    def get_record_count(self) -> int:
        """Return the number of records currently stored in memory."""
        return len(self._records)

    def get_all_records(self) -> list[NaturalGasRecord]:
        """Return a copy of all records currently stored in memory."""
        return self._records.to_list()

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
        return self._records.get(one_based_index - 1)

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
        loaded_records = load_records_from_csv(dataset_path, record_limit)
        self._records.replace_all(loaded_records)
        return len(self._records)

    def add_record(self, record: NaturalGasRecord) -> None:
        """
        Append a new record object to the in-memory linked list.

        Args:
            record: Parsed record object to store.
        """
        self._records.append(record)

    def update_record(self, one_based_index: int, record: NaturalGasRecord) -> None:
        """
        Replace an existing record in the in-memory linked list.

        Args:
            one_based_index: User-facing record number starting at 1.
            record: Updated record object.

        Raises:
            IndexError: If the requested record number is out of range.
        """
        self._records.set(one_based_index - 1, record)

    def delete_record(self, one_based_index: int) -> NaturalGasRecord:
        """
        Remove a record from the in-memory linked list.

        Args:
            one_based_index: User-facing record number starting at 1.

        Returns:
            The removed record object.

        Raises:
            IndexError: If the requested record number is out of range.
        """
        return self._records.delete(one_based_index - 1)

    def persist_to_disk(self, output_directory: Path) -> Path:
        """
        Write all in-memory records to a new CSV file in the output directory.

        Args:
            output_directory: Folder where the generated CSV file will be saved.

        Returns:
            Path to the newly created CSV file.
        """
        return save_records_to_csv(self._records, output_directory)

    def aggregate_original_value_by(
        self,
        group_by_field: str,
        top_n: int | None = None,
    ) -> list[tuple[str, float]]:
        """
        Aggregate OriginalValue totals from the linked list by one category field.

        Args:
            group_by_field: Dataset column used for grouping (CSD or Period).
            top_n: Optional maximum number of categories to return after sorting
                by total descending. None returns all categories.

        Returns:
            List of (label, total_original_value) pairs sorted by total descending.

        Raises:
            ValueError: If group_by_field is not a supported chart grouping field.
        """
        if group_by_field not in SUPPORTED_CHART_GROUP_FIELDS:
            raise ValueError(
                f"Unsupported chart group field: {group_by_field}. "
                f"Choose one of: {', '.join(SUPPORTED_CHART_GROUP_FIELDS)}"
            )

        totals: dict[str, float] = {}
        for record in self._records:
            if group_by_field == "CSD":
                label = record.get_CSD()
            else:
                label = str(record.get_Period())

            totals[label] = totals.get(label, 0.0) + record.get_OriginalValue()

        sorted_totals = sorted(totals.items(), key=lambda item: item[1], reverse=True)
        if top_n is not None:
            return sorted_totals[:top_n]
        return sorted_totals
