"""
CST8002 Programming Language Research Project
Practical Project Part 3

Professor: Update with your professor's name from Brightspace
Due Date: See Brightspace for due date
Author: Ren

References:
[1] Python Software Foundation, "8. Classes," Python Tutorial, docs.python.org,
    [online]. Available: https://docs.python.org/3/tutorial/classes.html
    [Accessed: Jun. 20, 2026].
[2] Python Software Foundation, "csv — CSV File Reading and Writing," docs.python.org,
    [online]. Available: https://docs.python.org/3/library/csv.html
    [Accessed: Jun. 20, 2026].
"""

from typing import Any


CSV_FIELD_NAMES = [
    "CSDUID",
    "CSD",
    "Period",
    "IndicatorSummaryDescription",
    "UnitOfMeasure",
    "OriginalValue",
]


class NaturalGasRecord:
    """
    Entity object representing one row from the natural gas production dataset.

    Field names match the dataset column names exactly.
    """

    def __init__(
        self,
        CSDUID: int,
        CSD: str,
        Period: int,
        IndicatorSummaryDescription: str,
        UnitOfMeasure: str,
        OriginalValue: float,
    ) -> None:
        """
        Initialize a record with parsed values from one CSV row.

        Args:
            CSDUID: Census subdivision unique identifier.
            CSD: Census subdivision name.
            Period: Reporting year.
            IndicatorSummaryDescription: Indicator description text.
            UnitOfMeasure: Measurement unit for the value.
            OriginalValue: Reported production value.
        """
        self.CSDUID = CSDUID
        self.CSD = CSD
        self.Period = Period
        self.IndicatorSummaryDescription = IndicatorSummaryDescription
        self.UnitOfMeasure = UnitOfMeasure
        self.OriginalValue = OriginalValue

    def get_CSDUID(self) -> int:
        """Return the CSDUID field value."""
        return self.CSDUID

    def set_CSDUID(self, CSDUID: int) -> None:
        """Set the CSDUID field value."""
        self.CSDUID = CSDUID

    def get_CSD(self) -> str:
        """Return the CSD field value."""
        return self.CSD

    def set_CSD(self, CSD: str) -> None:
        """Set the CSD field value."""
        self.CSD = CSD

    def get_Period(self) -> int:
        """Return the Period field value."""
        return self.Period

    def set_Period(self, Period: int) -> None:
        """Set the Period field value."""
        self.Period = Period

    def get_IndicatorSummaryDescription(self) -> str:
        """Return the IndicatorSummaryDescription field value."""
        return self.IndicatorSummaryDescription

    def set_IndicatorSummaryDescription(self, IndicatorSummaryDescription: str) -> None:
        """Set the IndicatorSummaryDescription field value."""
        self.IndicatorSummaryDescription = IndicatorSummaryDescription

    def get_UnitOfMeasure(self) -> str:
        """Return the UnitOfMeasure field value."""
        return self.UnitOfMeasure

    def set_UnitOfMeasure(self, UnitOfMeasure: str) -> None:
        """Set the UnitOfMeasure field value."""
        self.UnitOfMeasure = UnitOfMeasure

    def get_OriginalValue(self) -> float:
        """Return the OriginalValue field value."""
        return self.OriginalValue

    def set_OriginalValue(self, OriginalValue: float) -> None:
        """Set the OriginalValue field value."""
        self.OriginalValue = OriginalValue

    @classmethod
    def from_csv_row(cls, row: dict[str, str]) -> "NaturalGasRecord":
        """
        Build a record object from one CSV dictionary row.

        Args:
            row: Mapping of column names to string cell values.

        Returns:
            A NaturalGasRecord with each CSV column stored in a separate field.
        """
        return cls(
            CSDUID=int(row["CSDUID"]),
            CSD=row["CSD"].strip(),
            Period=int(row["Period"]),
            IndicatorSummaryDescription=row["IndicatorSummaryDescription"].strip(),
            UnitOfMeasure=row["UnitOfMeasure"].strip(),
            OriginalValue=float(row["OriginalValue"]),
        )

    def to_csv_row(self) -> dict[str, str]:
        """
        Convert the record object back into a CSV row dictionary.

        Returns:
            Dictionary keyed by dataset column names with string values.
        """
        return {
            "CSDUID": str(self.CSDUID),
            "CSD": self.CSD,
            "Period": str(self.Period),
            "IndicatorSummaryDescription": self.IndicatorSummaryDescription,
            "UnitOfMeasure": self.UnitOfMeasure,
            "OriginalValue": f"{self.OriginalValue:.5f}",
        }

    def to_display_dict(self) -> dict[str, Any]:
        """
        Return record fields as a dictionary for formatted console output.

        Returns:
            Dictionary keyed by dataset column names.
        """
        return {
            "CSDUID": self.CSDUID,
            "CSD": self.CSD,
            "Period": self.Period,
            "IndicatorSummaryDescription": self.IndicatorSummaryDescription,
            "UnitOfMeasure": self.UnitOfMeasure,
            "OriginalValue": self.OriginalValue,
        }

    def __str__(self) -> str:
        """Return a readable single-line summary of the record."""
        return (
            f"CSDUID={self.CSDUID}, CSD={self.CSD}, Period={self.Period}, "
            f"IndicatorSummaryDescription={self.IndicatorSummaryDescription}, "
            f"UnitOfMeasure={self.UnitOfMeasure}, OriginalValue={self.OriginalValue}"
        )
