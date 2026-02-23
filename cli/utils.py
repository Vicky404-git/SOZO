from rich.table import Table
from rich import print


def display_events(events, title):
    if not events:
        print("[yellow]No events found.[/yellow]")
        return

    table = Table(title=title)
    table.add_column("Time")
    table.add_column("Category")
    table.add_column("Value")

    for timestamp, category, value in events:
        time_only = timestamp.split("T")[1][:5]
        table.add_row(time_only, category, value)

    print(table)


def display_calendar(summary):
    if not summary:
        print("[yellow]No events recorded yet.[/yellow]")
        return

    table = Table(title="Calendar Summary")
    table.add_column("Date")
    table.add_column("Event Count")

    for day, count in summary:
        table.add_row(day, str(count))

    print(table)