import sys
import typer
import subprocess
from rich import print
from rich.console import Console
from rich.markdown import Markdown
from pathlib import Path

# IMPORT BOTH REGISTERS!
from sozo.cli.commands import register_commands
from sozo.cli.devs import register_dev_commands

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

def update_sozo():
    """Pulls the latest code from Git and syncs dependencies."""
    repo_dir = Path(__file__).resolve().parent.parent.parent
    print("[bold cyan]🔄 Fetching latest Sōzō updates from GitHub...[/bold cyan]")
    try:
        subprocess.run(["git", "pull"], cwd=repo_dir, check=True)
        print("[dim]Syncing dependencies...[/dim]")
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
            cwd=repo_dir, check=True
        )
        print("\n[green]✔ Sōzō is now up to date![/green]")
    except subprocess.CalledProcessError as e:
        print(f"\n[red]Failed to update:[/red] Ensure you have internet access and no uncommitted local conflicts.")
    raise typer.Exit()

@app.callback(invoke_without_command=True)
def main_callback(
    ctx: typer.Context,
    help: bool = typer.Option(False, "--help", "-h", is_eager=True),
    update: bool = typer.Option(False, "--update", "-u", is_eager=True)
):
    if help:
        show_manual_in_terminal()
    elif update:
        update_sozo()
    elif ctx.invoked_subcommand is None:
        print("\n[bold cyan]Sōzō[/bold cyan] — Life as Events")
        print("Type [green]sozo --help[/green] to read the manual in terminal, or [green]sozo manual[/green] to open the file.\n")

# WIRE UP BOTH FILES!
register_commands(app)
register_dev_commands(app)