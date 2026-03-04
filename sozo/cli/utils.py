from rich.table import Table
from rich.console import Console
from rich import print

console = Console()

def display_events(events, title):
    if not events:
        print(f"[yellow]No events found for: {title}[/yellow]")
        return

    table = Table(title=title, show_lines=True)
    table.add_column("ID", style="dim")
    table.add_column("Date", style="cyan")
    table.add_column("Time", style="cyan")
    table.add_column("Category", style="magenta")
    table.add_column("Value")
    table.add_column("Files", style="dim")  # New Column
    table.add_column("Tags", style="blue")
    table.add_column("🔔", justify="center")

    for event in events:
        # Destructure the 7 items (unpacking)
        event_id, timestamp, category, value, remind, tags, files = event
        
        date_part, time_part = timestamp.split("T")
        time_only = time_part[:5]
        
        tag_display = ", ".join([f"#{t.strip()}" for t in tags.split(",") if t]) if tags else "-"
        file_display = files if files else "-"

        table.add_row(
            str(event_id),
            date_part,
            time_only,
            category,
            value,
            file_display,
            tag_display,
            "✔" if remind else "",
        )

    console.print(table)

def display_stats(stats_data):
    if not stats_data:
        print("[yellow]No data to analyze yet.[/yellow]")
        return

    table = Table(title="Activity Stats")
    table.add_column("Category", style="magenta")
    table.add_column("Event Count", justify="right", style="green")

    for category, count in stats_data:
        table.add_row(category, str(count))

    console.print(table)