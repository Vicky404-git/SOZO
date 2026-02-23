import typer
from rich import print
from rich.table import Table

from core.database import initialize_database
from core.events import add_event, get_today_events

app = typer.Typer()

# Initialize DB on start
initialize_database()

@app.command()
def add(category: str, value: str):
    """
    Add a new event.
    Example: sozo add eat breakfast
    """
    add_event(category, value)
    print(f"[green]✔ Saved:[/green] {category} → {value}")

@app.command()
def today():
    """
    Show today's events.
    """
    events = get_today_events()

    if not events:
        print("[yellow]No events recorded today.[/yellow]")
        return

    table = Table(title="Today's Events")

    table.add_column("Time")
    table.add_column("Category")
    table.add_column("Value")

    for timestamp, category, value in events:
        time_only = timestamp.split("T")[1][:5]
        table.add_row(time_only, category, value)

    print(table)

if __name__ == "__main__":
    app()