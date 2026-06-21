"""
CST8002 Programming Language Research Project
Practical Project Part 2

Author: REN YOU

References:
[1] Python Software Foundation, "unittest — Unit testing framework," docs.python.org,
    [online]. Available: https://docs.python.org/3/library/unittest.html
    [Accessed: Jun. 14, 2026].
[2] Python Software Foundation, "csv — CSV File Reading and Writing," docs.python.org,
    [online]. Available: https://docs.python.org/3/library/csv.html
    [Accessed: Jun. 14, 2026].
"""

import tempfile
import unittest
from pathlib import Path

from business.record_service import RecordService
from model.natural_gas_record import NaturalGasRecord
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


if __name__ == "__main__":
    unittest.main()
