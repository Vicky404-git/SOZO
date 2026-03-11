import sys
import typer
import subprocess
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

def update_sozo():
    """Pulls the latest code from Git and syncs dependencies."""
    # Find the root directory of the cloned repo
    repo_dir = Path(__file__).resolve().parent.parent.parent
    
    print("[bold cyan]🔄 Fetching latest Sōzō updates from GitHub...[/bold cyan]")
    try:
        # 1. Pull the latest code
        subprocess.run(["git", "pull"], cwd=repo_dir, check=True)
        
        # 2. Check for new requirements and install them safely
        print("[dim]Syncing dependencies...[/dim]")
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
            cwd=repo_dir, 
            check=True
        )
        
        print("\n[green]✔ Sōzō is now up to date![/green]")
    except subprocess.CalledProcessError as e:
        print(f"\n[red]Failed to update:[/red] Ensure you have internet access and no uncommitted local conflicts.")
    
    raise typer.Exit()

@app.callback(invoke_without_command=True)
def main_callback(
    ctx: typer.Context,
    help: bool = typer.Option(False, "--help", "-h", is_eager=True),
    update: bool = typer.Option(False, "--update", "-u", is_eager=True) # <-- NEW FLAG
):
    # 1. User typed `sozo --help`
    if help:
        show_manual_in_terminal()
        
    # 2. User typed `sozo --update`
    elif update:
        update_sozo()
        
    # 3. User typed exactly `sozo` with no other commands
    elif ctx.invoked_subcommand is None:
        print("\n[bold cyan]Sōzō[/bold cyan] — Life as Events")
        print("Type [green]sozo --help[/green] to read the manual in terminal, or [green]sozo manual[/green] to open the file.\n")

register_commands(app)