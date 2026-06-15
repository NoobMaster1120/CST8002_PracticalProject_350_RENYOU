"""
CST8002 Programming Language Research Project
Practical Project Part 1

Professor: Update with your professor's name from Brightspace
Due Date: See Brightspace for due date
Author: Ren

References:
[1] Python Software Foundation, "8. Classes," Python Tutorial, docs.python.org,
    [online]. Available: https://docs.python.org/3/tutorial/classes.html
    [Accessed: May 30, 2026].
"""

from typing import Any


class NaturalGasRecord:
    """Entity object representing one row from the natural gas production dataset."""

    def __init__(
        self,
        CSDUID: int,
        CSD: str,
        Period: int,
        IndicatorSummaryDescription: str,
        UnitOfMeasure: str,
        OriginalValue: float,
    ) -> None:
        """Initialize a record with parsed values from one CSV row."""
        self.CSDUID = CSDUID
        self.CSD = CSD
        self.Period = Period
        self.IndicatorSummaryDescription = IndicatorSummaryDescription
        self.UnitOfMeasure = UnitOfMeasure
        self.OriginalValue = OriginalValue

    def get_CSDUID(self) -> int:
        """Return the CSDUID field value."""
        return self.CSDUID

    def get_CSD(self) -> str:
        """Return the CSD field value."""
        return self.CSD

    def get_Period(self) -> int:
        """Return the Period field value."""
        return self.Period

    def get_IndicatorSummaryDescription(self) -> str:
        """Return the IndicatorSummaryDescription field value."""
        return self.IndicatorSummaryDescription

    def get_UnitOfMeasure(self) -> str:
        """Return the UnitOfMeasure field value."""
        return self.UnitOfMeasure

    def get_OriginalValue(self) -> float:
        """Return the OriginalValue field value."""
        return self.OriginalValue

    @classmethod
    def from_csv_row(cls, row: dict[str, str]) -> "NaturalGasRecord":
        """Build a record object from one CSV dictionary row."""
        return cls(
            CSDUID=int(row["CSDUID"]),
            CSD=row["CSD"].strip(),
            Period=int(row["Period"]),
            IndicatorSummaryDescription=row["IndicatorSummaryDescription"].strip(),
            UnitOfMeasure=row["UnitOfMeasure"].strip(),
            OriginalValue=float(row["OriginalValue"]),
        )

    def to_display_dict(self) -> dict[str, Any]:
        """Return record fields as a dictionary for formatted console output."""
        return {
            "CSDUID": self.CSDUID,
            "CSD": self.CSD,
            "Period": self.Period,
            "IndicatorSummaryDescription": self.IndicatorSummaryDescription,
            "UnitOfMeasure": self.UnitOfMeasure,
            "OriginalValue": self.OriginalValue,
        }
