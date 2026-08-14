"""
CST8002 Programming Language Research Project
Practical Project Part 4

Author: REN YOU

References:
[1] Matplotlib Development Team, "Bar charts," matplotlib.org,
    [online]. Available:
    https://matplotlib.org/stable/gallery/lines_bars_and_markers/bar_colors.html
    [Accessed: Aug. 14, 2026].
[2] Matplotlib Development Team, "Matplotlib license," matplotlib.org,
    [online]. Available: https://matplotlib.org/stable/users/project/license.html
    [Accessed: Aug. 14, 2026].
"""

from pathlib import Path

import matplotlib.pyplot as plt


def render_vertical_bar_chart(
    labels: list[str],
    values: list[float],
    group_by_field: str,
    author_name: str,
    output_directory: Path,
    show_window: bool = True,
) -> Path:
    """
    Render a vertical bar chart from aggregated category totals.

    Args:
        labels: Category labels for the x-axis.
        values: Numeric totals matching each label.
        group_by_field: Dataset column used for grouping (for the chart title).
        author_name: Student name shown in the chart title.
        output_directory: Folder where the PNG file is saved.
        show_window: When True, open an interactive matplotlib window.

    Returns:
        Path to the saved PNG chart file.
    """
    output_directory.mkdir(parents=True, exist_ok=True)
    output_path = output_directory / "vertical_bar_chart.png"

    figure, axes = plt.subplots(figsize=(10, 6))
    axes.bar(range(len(labels)), values, color="steelblue")
    axes.set_xticks(range(len(labels)))
    axes.set_xticklabels(labels, rotation=45, ha="right")
    axes.set_xlabel(group_by_field)
    axes.set_ylabel("Sum of OriginalValue")
    axes.set_title(
        f"Vertical Bar Chart by {group_by_field} | Program by {author_name}"
    )
    axes.grid(axis="y", linestyle="--", alpha=0.4)
    figure.tight_layout()

    figure.savefig(output_path, dpi=120)
    if show_window:
        plt.show()
    else:
        plt.close(figure)

    return output_path


def print_ascii_bar_chart(
    labels: list[str],
    values: list[float],
    group_by_field: str,
    author_name: str,
) -> None:
    """
    Print an ASCII vertical-style bar chart fallback in the console.

    Args:
        labels: Category labels.
        values: Numeric totals matching each label.
        group_by_field: Dataset column used for grouping.
        author_name: Student name printed with the chart.
    """
    print(f"ASCII Vertical Bar Chart by {group_by_field}")
    print(f"Program by {author_name}")
    print("-" * 72)

    if not values:
        print("No values available to chart.")
        print()
        return

    max_value = max(values) if max(values) > 0 else 1.0
    bar_width = 40

    for label, value in zip(labels, values):
        filled = int((value / max_value) * bar_width)
        bar = "#" * filled
        print(f"{label[:24]:<24} | {bar} {value:,.2f}")

    print("-" * 72)
    print()
