import typer
from rich import print

from sozo.core.services import (
    add_event, list_events, remove_event, show_today, search_events, get_stats, export_to_md
)
from sozo.core.kosmo import start_kosmo
from sozo.cli.utils import display_events, display_stats

def register_commands(app: typer.Typer):

    @app.command()
    def add(
        category: str,
        value: list[str],
        at: str = typer.Option(None, "--at"),
        remind: bool = typer.Option(False, "--remind"),
        tags: list[str] = typer.Option(None, "--tag", "-t", help="Add tags"),
        files: list[str] = typer.Option(None, "--file", "-f", help="Link a file"),
    ):
        full_value = " ".join(value)
        try:
            # add_event now returns the final tags list (including auto-project)
            final_tags = add_event(category, full_value, at, remind, tags, files)
            
            tag_str = f" [cyan]#{', #'.join(final_tags)}[/cyan]" if final_tags else ""
            file_str = f" 📎 [dim]{', '.join(files)}[/dim]" if files else ""
            
            print(f"[green]✔ Saved:[/green] {category} → {full_value}{tag_str}{file_str}")
        except Exception as e:
            print(f"[red]Error:[/red] {e}")

    @app.command()
    def export(
        tag: str = typer.Option(None, "--tag", "-t", help="Export only specific tag"),
        out: str = typer.Option("timeline.md", "--out", "-o", help="Output file name")
    ):
        try:
            export_to_md(tag, out)
            print(f"[green]✔ Exported timeline to {out}[/green]")
        except Exception as e:
            print(f"[red]Failed to export: {e}[/red]")

    @app.command(name="list")
    def list_cmd(date: str = None):
        events = list_events(date)
        display_events(events, "All Events")

    @app.command()
    def today():
        events = show_today()
        display_events(events, "Today's Events")

    @app.command()
    def search(query: str):
        events = search_events(query)
        display_events(events, f"Search Results for '{query}'")

    @app.command()
    def stats():
        data = get_stats()
        display_stats(data)

    @app.command()
    def delete(event_id: int):
        remove_event(event_id)
        print(f"[red]✔ Event {event_id} deleted.[/red]")

    @app.command()
    def kosmo():
        start_kosmo()
        
    @app.command()
    def manual():
        import os
        import sys
        import subprocess
        from pathlib import Path
        from rich import print

        manual_path = Path(__file__).resolve().parent.parent.parent / "MANUAL.md"

        if not manual_path.exists():
            print("[red]MANUAL.md not found![/red] Please ensure it is in the root SOZO folder.")
            return

        print("[green]Opening MANUAL.md in your default viewer...[/green]")
        
        # Automatically detect the OS and open the file directly
        if sys.platform == "win32":
            os.startfile(manual_path)
        elif sys.platform == "darwin":  # macOS
            subprocess.call(["open", str(manual_path)])
        else:  # Linux
            subprocess.call(["xdg-open", str(manual_path)])
            
    @app.command()
    def commit(msg: str = typer.Option(None, "--msg", "-m", help="Provide a manual message to skip auto-generation")):
        """Auto-stages, generates a message, commits, and logs to Sōzō."""
        from sozo.core.services import execute_auto_commit
        try:
            print("[dim]Analyzing changes...[/dim]")
            commit_msg, files = execute_auto_commit(msg)
            
            print(f"[green]✔ Committed successfully![/green]")
            print(f"📝 [bold]Message:[/bold] {commit_msg}")
            print(f"📎 [bold]Files:[/bold] {', '.join(files)}")
            print("[blue]✔ Logged to Sōzō timeline.[/blue]")
            
        except Exception as e:
            print(f"[red]Error:[/red] {e}")

    @app.command(context_settings={"allow_extra_args": True, "ignore_unknown_options": True})
    def git(ctx: typer.Context):
        """Run ANY git command (push, pull, clone) and log it automatically."""
        import subprocess
        from sozo.core.services import add_event, detect_project
        
        if not ctx.args:
            print("[yellow]Please provide git commands. Example: sozo git push origin main[/yellow]")
            return

        command_str = " ".join(ctx.args)
        
        # Run the system git command in the terminal
        print(f"[dim]Running: git {command_str}[/dim]")
        result = subprocess.run(["git"] + ctx.args)
        
        # If the git command worked, log it to Sōzō
        if result.returncode == 0:
            project = detect_project()
            tags = ["git"]
            if project:
                tags.append(project)
                
            # Log the action
            add_event("programming", f"Git Execute: git {command_str}", tags=tags)
            print(f"[blue]✔ Action logged to Sōzō[/blue]")