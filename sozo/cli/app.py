import typer
from rich import print
from rich.console import Console
from rich.markdown import Markdown
from pathlib import Path
from sozo.cli.commands import register_commands

# Disable default help so we can customize it
app = typer.Typer(
    add_help_option=False,
    no_args_is_help=False
)

def show_manual_in_terminal():
    manual_path = Path(__file__).resolve().parent.parent.parent / "MANUAL.md"
    
    if not manual_path.exists():
        print("[red]MANUAL.md not found![/red] Make sure it is in the root SOZO folder.")
        raise typer.Exit()
        
    console = Console()
    with open(manual_path, "r", encoding="utf-8") as f:
        md = Markdown(f.read())
    console.print(md)
    raise typer.Exit()

@app.callback(invoke_without_command=True)
def main_callback(
    ctx: typer.Context,
    help: bool = typer.Option(False, "--help", "-h", is_eager=True)
):
    # 1. User typed `sozo --help`
    if help:
        show_manual_in_terminal()
        
    # 2. User typed exactly `sozo` with no other commands
    elif ctx.invoked_subcommand is None:
        print("\n[bold cyan]Sōzō[/bold cyan] — Life as Events")
        print("Type [green]sozo --help[/green] to read the manual in terminal, or [green]sozo manual[/green] to open the file.\n")

register_commands(app)