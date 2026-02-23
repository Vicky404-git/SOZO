import typer
from datetime import datetime
from rich import print

from core.events import add_event, get_events_by_date, get_calendar_summary
from core.kosmo import start_kosmo
from .utils import display_events, display_calendar


def register_commands(app: typer.Typer):

    @app.command()
    def add(
        category: str,
        value: list[str],
        at: str = typer.Option(None, "--at"),
        remind: bool = typer.Option(False, "--remind")
    ):
        full_value = " ".join(value)

        try:
            add_event(category, full_value, at, remind)
            print(f"[green]✔ Saved:[/green] {category} → {full_value}")
        except Exception as e:
            print(f"[red]Error:[/red] {e}")

    @app.command()
    def today():
        today_date = datetime.now().date().isoformat()
        events = get_events_by_date(today_date)
        display_events(events, "Today's Events")

    @app.command()
    def show(date: str):
        events = get_events_by_date(date)
        display_events(events, f"Events on {date}")

    @app.command()
    def calendar():
        summary = get_calendar_summary()
        display_calendar(summary)

    @app.command()
    def kosmo():
        start_kosmo()