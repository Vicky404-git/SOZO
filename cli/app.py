import typer
from .commands import register_commands

app = typer.Typer()
register_commands(app)