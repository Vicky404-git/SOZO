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
        relates_to: int = typer.Option(None, "--relates-to", "-r", help="ID of an older event this connects to"),
    ):
        full_value = " ".join(value)
        try:
            final_tags = add_event(category, full_value, at, remind, tags, files, relates_to)
            
            tag_str = f" [cyan]#{', #'.join(final_tags)}[/cyan]" if final_tags else ""
            file_str = f" 📎 [dim]{', '.join(files)}[/dim]" if files else ""
            rel_str = f" 🔗 [magenta]Linked to #{relates_to}[/magenta]" if relates_to else ""
            
            print(f"[green]✔ Saved:[/green] {category} → {full_value}{tag_str}{file_str}{rel_str}")
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
        
        if sys.platform == "win32":
            os.startfile(manual_path)
        elif sys.platform == "darwin": 
            subprocess.call(["open", str(manual_path)])
        else:  
            subprocess.call(["xdg-open", str(manual_path)])
            
    @app.command()
    def commit(msg: str = typer.Option(None, "--msg", "-m", help="Provide a manual message to skip auto-generation")):
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
        import subprocess
        from sozo.core.services import add_event, detect_project
        
        if not ctx.args:
            print("[yellow]Please provide git commands. Example: sozo git push origin main[/yellow]")
            return

        command_str = " ".join(ctx.args)
        print(f"[dim]Running: git {command_str}[/dim]")
        result = subprocess.run(["git"] + ctx.args)
        
        if result.returncode == 0:
            project = detect_project()
            tags = ["git"]
            if project:
                tags.append(project)
                
            add_event("programming", f"Git Execute: git {command_str}", tags=tags)
            print(f"[blue]✔ Action logged to Sōzō[/blue]")
            
    @app.command()
    def timeline(period: str = typer.Argument("week", help="View 'week' or 'month'")):
        from sozo.core.services import get_timeline
        from sozo.cli.utils import display_timeline
        
        grouped = get_timeline(period)
        display_timeline(grouped, f"{period.capitalize()} Timeline")
        
    @app.command()
    def note(
        title: str,
        category: str = typer.Option("study", "--category", "-c", help="Category (default: study)"),
        tags: list[str] = typer.Option(None, "--tag", "-t", help="Add tags"),
    ):
        from sozo.core.services import create_note
        import os
        import sys
        import subprocess
        
        try:
            print(f"[dim]Forging new note...[/dim]")
            filepath, final_tags = create_note(title, category, tags)
            
            tag_str = f" [cyan]#{', #'.join(final_tags)}[/cyan]" if final_tags else ""
            print(f"[green]✔ Note created and logged:[/green] {title}{tag_str}")
            print(f"📎 [dim]Opening {filepath.name}...[/dim]")
            
            if sys.platform == "win32":
                os.startfile(filepath)
            elif sys.platform == "darwin":  
                subprocess.call(["open", str(filepath)])
            else:  
                subprocess.call(["xdg-open", str(filepath)])
                
        except Exception as e:
            print(f"[red]Error creating note:[/red] {e}")
            
    
    @app.command()
    def file(name: str):
        from sozo.core.services import get_file_history
        from sozo.cli.utils import display_events
        events = get_file_history(name)
        display_events(events, f"History for '{name}'")

    @app.command()
    def ingest(
        txt_file: str = typer.Argument(..., help="Path to your raw .txt file"),
        title: str = typer.Argument(..., help="Title for the formatted note"),
        category: str = typer.Option("study", "--category", "-c", help="Category (e.g., lecture, study)"),
        tags: list[str] = typer.Option(None, "--tag", "-t", help="Add tags"),
    ):
        from sozo.core.services import ingest_raw_file
        import os
        import sys
        import subprocess
        
        try:
            print("[dim]Reading file and querying AI...[/dim]")
            filepath, final_tags = ingest_raw_file(txt_file, title, category, tags)
            
            tag_str = f" [cyan]#{', #'.join(final_tags)}[/cyan]" if final_tags else ""
            print(f"[green]✔ AI Formatting Complete![/green] {title}{tag_str}")
            print(f"📎 [dim]Opening {filepath.name}...[/dim]")
            
            if sys.platform == "win32":
                os.startfile(filepath)
            elif sys.platform == "darwin":  
                subprocess.call(["open", str(filepath)])
            else:  
                subprocess.call(["xdg-open", str(filepath)])
                
        except Exception as e:
            print(f"[red]Failed to ingest file:[/red] {e}")
            

    @app.command()
    def graph():
        """View the Obsidian-style knowledge graph of your vault."""
        from sozo.core.services import build_knowledge_graph
        from sozo.cli.utils import display_graph
        
        graph_data = build_knowledge_graph()
        display_graph(graph_data)

    @app.command()
    def dash():
        """Open the Notion-style command center dashboard."""
        from sozo.core.services import get_stats, show_today, get_timeline
        from sozo.cli.utils import display_dashboard
        
        # Gather all the data needed for the dashboard panels
        stats = get_stats()
        today = show_today()
        timeline = get_timeline("week")
        
        display_dashboard(stats, today, timeline)