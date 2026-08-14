"""
CST8002 Programming Language Research Project
Practical Project Part 4

Author: REN YOU

References:
[1] Python Software Foundation, "input — Input Functions," docs.python.org,
    [online]. Available: https://docs.python.org/3/library/functions.html#input
    [Accessed: Jun. 20, 2026].
[2] GeeksforGeeks, "Types of Linked List," geeksforgeeks.org,
    [online]. Available: https://www.geeksforgeeks.org/dsa/types-of-linked-list/
    [Accessed: Jun. 20, 2026].
[3] Matplotlib Development Team, "Bar charts," matplotlib.org,
    [online]. Available:
    https://matplotlib.org/stable/gallery/lines_bars_and_markers/bar_colors.html
    [Accessed: Aug. 14, 2026].
[4] Matplotlib Development Team, "Matplotlib license," matplotlib.org,
    [online]. Available: https://matplotlib.org/stable/users/project/license.html
    [Accessed: Aug. 14, 2026].
"""

from pathlib import Path

from business.record_service import SUPPORTED_CHART_GROUP_FIELDS, RecordService
from model.natural_gas_record import NaturalGasRecord
from persistence.csv_reader import DEFAULT_RECORD_LIMIT
from presentation.chart_view import print_ascii_bar_chart, render_vertical_bar_chart


class MenuController:
    """
    Presentation layer controller for all user interactions.

    This class displays menus, reads user input, and delegates work to RecordService.
    """

    def __init__(
        self,
        record_service: RecordService,
        dataset_path: Path,
        output_directory: Path,
        author_name: str,
    ) -> None:
        """
        Initialize the menu controller.

        Args:
            record_service: Business layer service for record operations.
            dataset_path: Default CSV dataset used for reload operations.
            output_directory: Folder where exported CSV files are written.
            author_name: Student name displayed on screen.
        """
        self._record_service = record_service
        self._dataset_path = dataset_path
        self._output_directory = output_directory
        self._author_name = author_name

    def print_header(self) -> None:
        """Display the author name so it remains visible during program output."""
        print("=" * 72)
        print(f"Program by {self._author_name}")
        print("CST8002 Practical Project Part 4 - Natural Gas Production Records")
        print("In-memory collection: Singly Linked List")
        print("Part 4 feature: Vertical Bar Chart (matplotlib)")
        print(f"Loaded records in memory: {self._record_service.get_record_count()}")
        print("=" * 72)
        print()

    def print_menu(self) -> None:
        """Display the interactive menu options."""
        print("Menu Options")
        print("  1. Reload data from dataset")
        print("  2. Save in-memory data to a new CSV file")
        print("  3. Display one record")
        print("  4. Display multiple records")
        print("  5. Create a new record")
        print("  6. Edit a record")
        print("  7. Delete a record")
        print("  8. Create vertical bar chart")
        print("  0. Exit")
        print()

    def print_record(self, index: int, record: NaturalGasRecord) -> None:
        """
        Print one record object to the console.

        Args:
            index: Position of the record in the loaded list.
            record: Parsed record object from the dataset.
        """
        print(f"Record {index}")
        print(f"  CSDUID: {record.get_CSDUID()}")
        print(f"  CSD: {record.get_CSD()}")
        print(f"  Period: {record.get_Period()}")
        print(
            "  IndicatorSummaryDescription: "
            f"{record.get_IndicatorSummaryDescription()}"
        )
        print(f"  UnitOfMeasure: {record.get_UnitOfMeasure()}")
        print(f"  OriginalValue: {record.get_OriginalValue():,.5f}")
        print()

    def display_multiple_records(self) -> None:
        """Display all records currently held in memory."""
        records = self._record_service.get_all_records()

        if not records:
            print("No records are currently loaded in memory.")
            print()
            return

        print(f"Displaying {len(records)} record(s)")
        print("-" * 72)

        for index, record in enumerate(records, start=1):
            self.print_record(index, record)
            if index % 10 == 0:
                print(f"Program by {self._author_name}")
                print("-" * 72)

    def display_one_record(self) -> None:
        """Display a single record selected by the user."""
        if self._record_service.get_record_count() == 0:
            print("No records are currently loaded in memory.")
            print()
            return

        record_number = self._read_int(
            f"Enter record number (1-{self._record_service.get_record_count()}): "
        )

        try:
            record = self._record_service.get_record(record_number)
        except IndexError:
            print("Invalid record number.")
            print()
            return

        self.print_record(record_number, record)

    def reload_data(self) -> None:
        """Reload records from the dataset file into memory."""
        try:
            loaded_count = self._record_service.reload_from_dataset(
                self._dataset_path,
                DEFAULT_RECORD_LIMIT,
            )
        except FileNotFoundError as error:
            print(f"Error: {error}")
            print()
            return
        except OSError as error:
            print(f"File I/O error: {error}")
            print()
            return
        except ValueError as error:
            print(f"Data parsing error: {error}")
            print()
            return

        print(
            f"Reloaded {loaded_count} record(s) from {self._dataset_path.name} "
            "into memory."
        )
        print()

    def save_data(self) -> None:
        """Persist in-memory records to a new CSV file with a UUID file name."""
        if self._record_service.get_record_count() == 0:
            print("No records are currently loaded in memory.")
            print()
            return

        try:
            output_file = self._record_service.persist_to_disk(self._output_directory)
        except OSError as error:
            print(f"File I/O error: {error}")
            print()
            return

        print(f"Saved {self._record_service.get_record_count()} record(s) to:")
        print(f"  {output_file}")
        print()

    def create_record(self) -> None:
        """Create a new record from user input and store it in memory."""
        print("Enter values for the new record.")
        record = NaturalGasRecord(
            CSDUID=self._read_int("CSDUID: "),
            CSD=self._read_text("CSD: "),
            Period=self._read_int("Period: "),
            IndicatorSummaryDescription=self._read_text(
                "IndicatorSummaryDescription: "
            ),
            UnitOfMeasure=self._read_text("UnitOfMeasure: "),
            OriginalValue=self._read_float("OriginalValue: "),
        )
        self._record_service.add_record(record)
        print("New record added to memory.")
        print()

    def edit_record(self) -> None:
        """Edit an existing record selected by the user."""
        if self._record_service.get_record_count() == 0:
            print("No records are currently loaded in memory.")
            print()
            return

        record_number = self._read_int(
            f"Enter record number to edit (1-{self._record_service.get_record_count()}): "
        )

        try:
            existing_record = self._record_service.get_record(record_number)
        except IndexError:
            print("Invalid record number.")
            print()
            return

        print("Enter updated values. Press Enter to keep the current value.")
        updated_record = NaturalGasRecord(
            CSDUID=self._read_int_or_default(
                "CSDUID",
                existing_record.get_CSDUID(),
            ),
            CSD=self._read_text_or_default("CSD", existing_record.get_CSD()),
            Period=self._read_int_or_default(
                "Period",
                existing_record.get_Period(),
            ),
            IndicatorSummaryDescription=self._read_text_or_default(
                "IndicatorSummaryDescription",
                existing_record.get_IndicatorSummaryDescription(),
            ),
            UnitOfMeasure=self._read_text_or_default(
                "UnitOfMeasure",
                existing_record.get_UnitOfMeasure(),
            ),
            OriginalValue=self._read_float_or_default(
                "OriginalValue",
                existing_record.get_OriginalValue(),
            ),
        )
        self._record_service.update_record(record_number, updated_record)
        print(f"Record {record_number} updated in memory.")
        print()

    def delete_record(self) -> None:
        """Delete an existing record selected by the user."""
        if self._record_service.get_record_count() == 0:
            print("No records are currently loaded in memory.")
            print()
            return

        record_number = self._read_int(
            f"Enter record number to delete (1-{self._record_service.get_record_count()}): "
        )

        try:
            removed_record = self._record_service.delete_record(record_number)
        except IndexError:
            print("Invalid record number.")
            print()
            return

        print(f"Deleted record {record_number}: {removed_record}")
        print()

    def create_vertical_bar_chart(self) -> None:
        """
        Ask the user how to customize a vertical bar chart, then render it.

        Aggregation happens in the business layer. Matplotlib rendering and the
        ASCII fallback live in the presentation chart view module.
        """
        if self._record_service.get_record_count() == 0:
            print("No records are currently loaded in memory.")
            print()
            return

        print(f"Program by {self._author_name}")
        print("Create a vertical bar chart of OriginalValue totals.")
        print("Choose a grouping field:")
        print("  1. CSD")
        print("  2. Period")
        field_choice = input("Enter choice (1 or 2): ").strip()

        if field_choice == "1":
            group_by_field = "CSD"
        elif field_choice == "2":
            group_by_field = "Period"
        else:
            print("Invalid grouping choice.")
            print()
            return

        top_n = self._read_int(
            "Enter max number of bars to show (for example 10): "
        )
        if top_n <= 0:
            print("Number of bars must be greater than zero.")
            print()
            return

        try:
            aggregated = self._record_service.aggregate_original_value_by(
                group_by_field,
                top_n=top_n,
            )
        except ValueError as error:
            print(f"Error: {error}")
            print()
            return

        if not aggregated:
            print("No chart data could be produced from the loaded records.")
            print()
            return

        labels = [item[0] for item in aggregated]
        values = [item[1] for item in aggregated]

        print(
            f"Prepared {len(labels)} bar(s) grouped by {group_by_field} "
            f"from the singly linked list."
        )
        print(f"Supported fields: {', '.join(SUPPORTED_CHART_GROUP_FIELDS)}")
        print()

        print_ascii_bar_chart(
            labels=labels,
            values=values,
            group_by_field=group_by_field,
            author_name=self._author_name,
        )

        try:
            chart_path = render_vertical_bar_chart(
                labels=labels,
                values=values,
                group_by_field=group_by_field,
                author_name=self._author_name,
                output_directory=self._output_directory,
                show_window=True,
            )
            print(f"Vertical bar chart saved to: {chart_path}")
            print("Close the chart window to continue using the menu.")
            print()
        except Exception as error:
            print(f"Matplotlib chart window could not be shown: {error}")
            print("ASCII chart above can still be used for the demonstration.")
            print()

    def run(self) -> None:
        """Run the interactive menu until the user chooses to exit."""
        while True:
            self.print_header()
            self.print_menu()
            choice = input("Enter menu choice: ").strip()

            if choice == "1":
                self.reload_data()
            elif choice == "2":
                self.save_data()
            elif choice == "3":
                self.display_one_record()
            elif choice == "4":
                self.display_multiple_records()
            elif choice == "5":
                self.create_record()
            elif choice == "6":
                self.edit_record()
            elif choice == "7":
                self.delete_record()
            elif choice == "8":
                self.create_vertical_bar_chart()
            elif choice == "0":
                print(f"Program by {self._author_name}")
                print("Exiting program.")
                break
            else:
                print("Invalid menu choice. Please try again.")
                print()

    def _read_text(self, prompt: str) -> str:
        """Read a non-empty text value from the user."""
        while True:
            value = input(prompt).strip()
            if value:
                return value
            print("Value cannot be empty.")

    def _read_int(self, prompt: str) -> int:
        """Read an integer value from the user."""
        while True:
            value = input(prompt).strip()
            try:
                return int(value)
            except ValueError:
                print("Please enter a valid integer.")

    def _read_float(self, prompt: str) -> float:
        """Read a floating-point value from the user."""
        while True:
            value = input(prompt).strip()
            try:
                return float(value)
            except ValueError:
                print("Please enter a valid number.")

    def _read_text_or_default(self, field_name: str, current_value: str) -> str:
        """Read text input or keep the current value when Enter is pressed."""
        value = input(f"{field_name} [{current_value}]: ").strip()
        return current_value if value == "" else value

    def _read_int_or_default(self, field_name: str, current_value: int) -> int:
        """Read integer input or keep the current value when Enter is pressed."""
        while True:
            value = input(f"{field_name} [{current_value}]: ").strip()
            if value == "":
                return current_value
            try:
                return int(value)
            except ValueError:
                print("Please enter a valid integer.")

    def _read_float_or_default(self, field_name: str, current_value: float) -> float:
        """Read float input or keep the current value when Enter is pressed."""
        while True:
            value = input(f"{field_name} [{current_value}]: ").strip()
            if value == "":
                return current_value
            try:
                return float(value)
            except ValueError:
                print("Please enter a valid number.")
