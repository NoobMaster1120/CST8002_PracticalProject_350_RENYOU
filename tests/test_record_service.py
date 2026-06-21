"""
CST8002 Programming Language Research Project
Practical Project Part 3

Professor: Update with your professor's name from Brightspace
Due Date: See Brightspace for due date
Author: REN YOU

References:
[1] Python Software Foundation, "unittest — Unit testing framework," docs.python.org,
    [online]. Available: https://docs.python.org/3/library/unittest.html
    [Accessed: Jun. 20, 2026].
[2] GeeksforGeeks, "Types of Linked List," geeksforgeeks.org,
    [online]. Available: https://www.geeksforgeeks.org/dsa/types-of-linked-list/
    [Accessed: Jun. 20, 2026].
"""

import tempfile
import unittest
from pathlib import Path

from business.record_service import RecordService
from model.natural_gas_record import NaturalGasRecord
from model.singly_linked_list import SinglyLinkedList
from persistence.csv_reader import load_records_from_csv


class TestRecordService(unittest.TestCase):
    """Proof-of-concept unit tests for record loading and creation."""

    SAMPLE_ROW = {
        "CSDUID": "4805026",
        "CSD": "Drumheller",
        "Period": "2003",
        "IndicatorSummaryDescription": "Natural Gas Production",
        "UnitOfMeasure": "m3",
        "OriginalValue": "104493.20000",
    }

    def test_from_csv_row_places_data_into_correct_fields(self) -> None:
        """Verify CSV parsing stores each column in the matching record field."""
        record = NaturalGasRecord.from_csv_row(self.SAMPLE_ROW)

        self.assertEqual(record.get_CSDUID(), 4805026)
        self.assertEqual(record.get_CSD(), "Drumheller")
        self.assertEqual(record.get_Period(), 2003)
        self.assertEqual(
            record.get_IndicatorSummaryDescription(),
            "Natural Gas Production",
        )
        self.assertEqual(record.get_UnitOfMeasure(), "m3")
        self.assertAlmostEqual(record.get_OriginalValue(), 104493.2)

    def test_add_record_increases_in_memory_count(self) -> None:
        """Verify adding a record increases the business layer collection size."""
        service = RecordService()
        record = NaturalGasRecord.from_csv_row(self.SAMPLE_ROW)

        service.add_record(record)

        self.assertEqual(service.get_record_count(), 1)
        self.assertEqual(service.get_record(1).get_CSD(), "Drumheller")

    def test_load_records_from_missing_file_raises_file_not_found(self) -> None:
        """Verify missing dataset files raise FileNotFoundError."""
        missing_file = Path(tempfile.gettempdir()) / "missing-natural-gas.csv"

        with self.assertRaises(FileNotFoundError):
            load_records_from_csv(missing_file)


class TestSinglyLinkedList(unittest.TestCase):
    """Unit tests for the custom singly linked list data structure."""

    def test_append_and_get_store_records_in_order(self) -> None:
        """Verify append and get preserve insertion order."""
        linked_list: SinglyLinkedList[int] = SinglyLinkedList()
        linked_list.append(10)
        linked_list.append(20)
        linked_list.append(30)

        self.assertEqual(len(linked_list), 3)
        self.assertEqual(linked_list.get(0), 10)
        self.assertEqual(linked_list.get(2), 30)

    def test_delete_removes_middle_node(self) -> None:
        """Verify delete removes the requested node and returns its data."""
        linked_list: SinglyLinkedList[str] = SinglyLinkedList()
        linked_list.append("first")
        linked_list.append("second")
        linked_list.append("third")

        removed = linked_list.delete(1)

        self.assertEqual(removed, "second")
        self.assertEqual(linked_list.to_list(), ["first", "third"])

    def test_replace_all_rebuilds_list_contents(self) -> None:
        """Verify replace_all clears old nodes and stores a new sequence."""
        linked_list: SinglyLinkedList[int] = SinglyLinkedList()
        linked_list.append(1)
        linked_list.replace_all([4, 5, 6])

        self.assertEqual(linked_list.to_list(), [4, 5, 6])


if __name__ == "__main__":
    unittest.main()
