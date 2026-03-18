import typer
import click
from pathlib import Path
from datetime import datetime
from rich import print
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table
from rich.markdown import Markdown

from sozo.core.config import VAULT_PATH
from sozo.core.kosmo import start_kosmo
from sozo.core.services import (
    add_event, edit_event, list_events, remove_event, show_today,
    search_events, get_stats, export_to_md, search_vault,
    build_concept, get_file_history, get_timeline, create_note,
    ingest_raw_file, build_knowledge_graph, log_natural_event
)

from sozo.cli.utils import (
    display_events, display_stats, display_timeline,
    display_graph, display_dashboard, open_in_editor,
    display_concept, export_mermaid_graph, console,
)


def _get_note_path(filename: str) -> Path:
    """Helper to find a note in the vault safely."""
    found = list(VAULT_PATH.rglob(f"*{filename}*.md"))
    if not found:
        print(f"[red]Could not find any note matching '{filename}'[/red]")
        raise typer.Exit()
    return found[0]


def register_commands(app: typer.Typer):

    @app.command()
    def add(category: str, value: list[str], at: str = None, remind: bool = False, tags: list[str] = None, files: list[str] = None, relates_to: int = None):
        """Manually add a structured event."""
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
    def edit(event_id: int, category: str = None, value: str = None, tags: list[str] = None, files: list[str] = None):
        """Edit an existing event."""
        try:
            edit_event(event_id, category, value, tags, files)
            print(f"[green]✔ Event {event_id} updated successfully![/green]")
        except Exception as e:
            print(f"[red]Error:[/red] {e}")

    @app.command()
    def export(tag: str = None, out: str = "timeline.md"):
        """Export timeline to markdown."""
        try:
            export_to_md(tag, out)
            print(f"[green]✔ Exported timeline to {out}[/green]")
        except Exception as e:
            print(f"[red]Failed to export:[/red] {e}")

    @app.command(name="list")
    def list_cmd(date: str = None):
        """List all chronological events."""
        display_events(list_events(date), "All Events")

    @app.command()
    def today():
        """View today's events."""
        display_events(show_today(), "Today's Events")

    @app.command()
    def search(query: str):
        """Search the event database."""
        display_events(search_events(query), f"Search Results for '{query}'")
        
    @app.command()
    def file(name: str):
        """See event history tied to a specific file."""
        display_events(get_file_history(name), f"History for '{name}'")
        
    @app.command()
    def stats():
        """View activity statistics."""
        display_stats(get_stats())

    @app.command()
    def delete(event_id: int):
        """Delete an event from the timeline."""
        remove_event(event_id)
        print(f"[red]✔ Event {event_id} deleted.[/red]")

    @app.command()
    def brain(keyword: str):
        """Full-text search inside your Markdown vault notes."""
        print(f"[dim]Scanning Second Brain for '{keyword}'...[/dim]")
        results = search_vault(keyword)
        if not results:
            print(f"[yellow]No notes found containing: '{keyword}'[/yellow]")
            return
        print(f"\n[bold cyan]🧠 Second Brain Results ({len(results)} found)[/bold cyan]")
        for filename, snippet in results.items():
            highlighted = snippet.replace(keyword, f"[bold green]{keyword}[/bold green]").replace(keyword.capitalize(), f"[bold green]{keyword.capitalize()}[/bold green]")
            print(Panel(f"[dim]...{highlighted}...[/dim]", title=f"[magenta]📄 {filename}[/magenta]", title_align="left"))
            
    @app.command()
    def concept(keyword: str):
        """Unify notes, events, and projects under a single Concept Node."""
        data = build_concept(keyword)
        display_concept(keyword, data)

    @app.command()
    def timeline(period: str = "week", tag: str = None):
        """View chronological timeline of events."""
        title_suffix = f" (#{tag})" if tag else ""
        display_timeline(get_timeline(period, tag), f"{period.capitalize()} Timeline{title_suffix}")

    @app.command()
    def dash():
        """Open your personal command center dashboard."""
        display_dashboard(get_stats(), show_today(), get_timeline("week"))
        
    @app.command()
    def note(title: str = None, category: str = None, tags: list[str] = None):
        """Open a distraction-free notebook directly in the terminal."""
        print("[bold cyan]📝 Sōzō Notebook[/bold cyan]")
        if not title:
            title = Prompt.ask("[bold yellow]What is the title of this note?[/bold yellow]") or f"Note {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        if not category:
            category = Prompt.ask("[bold yellow]Category (e.g., journal, ideas, recipe)[/bold yellow]", default="journal")
        if not tags:
            raw_tags = Prompt.ask("[bold yellow]Tags (comma separated, or press Enter to skip)[/bold yellow]", default="")
            tags = [t.strip() for t in raw_tags.split(",")] if raw_tags else []
                
        print(f"\n[dim]Opening Editor for '{title}'...[/dim]")
        print("[cyan]Write your thoughts, save (Ctrl+S), and close the window to auto-save.[/cyan]")
        content = click.edit()
        
        if content is None:
            print("[yellow]Note creation cancelled.[/yellow]")
            return
        try:
            filepath, final_tags = create_note(title, category, tags, content.strip())
            tag_str = f" [cyan]#{', #'.join(final_tags)}[/cyan]" if final_tags else ""
            print(f"[green]✔ Note saved securely:[/green] {title}{tag_str}")
        except Exception as e:
            print(f"[red]Error saving note:[/red] {e}")
            
    @app.command(name="notes")
    def list_notes():
        """View a table of contents of all your notes."""
        table = Table(title="📚 Your Sōzō Notebooks", show_lines=True)
        table.add_column("Date Created", style="dim")
        table.add_column("Title", style="cyan")
        table.add_column("Folder/Category", style="magenta")
        
        notes = list(VAULT_PATH.rglob("*.md"))
        if not notes:
            print("[yellow]Your notebook is currently empty. Try 'sozo note' to write something![/yellow]")
            return
        for note in sorted(notes, reverse=True):
            parts = note.stem.split("-", 1)
            date_str = parts[0] if len(parts) > 1 else "Unknown"
            title_str = parts[1].replace("-", " ").title() if len(parts) > 1 else note.stem
            table.add_row(date_str, title_str, note.parent.name)
        console.print(table)
            
    @app.command()
    def read(filename: str = typer.Argument(..., help="Part of the note's title to read")):
        """Read a note directly in your terminal."""
        filepath = _get_note_path(filename)
        with open(filepath, "r", encoding="utf-8") as f:
            console.print(f"\n[dim]Reading: {filepath.name}[/dim]\n")
            console.print(Markdown(f.read()))
            print()
    
    @app.command()
    def rewrite(filename: str = typer.Argument(..., help="Part of the filename to edit")):
        """Open an existing vault note to edit and update it."""
        filepath = _get_note_path(filename)
        print(f"[dim]Opening {filepath.name}...[/dim]")
        with open(filepath, "r", encoding="utf-8") as f:
            new_content = click.edit(f.read())
        if new_content is not None:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"[green]✔ Note updated:[/green] {filepath.name}")
        else:
            print("[dim]No changes made. Note closed.[/dim]")

    @app.command()
    def ingest(txt_file: str, title: str, category: str = "study", tags: list[str] = None):
        """Convert messy raw text into structured Markdown using AI."""
        try:
            with console.status(f"[bold magenta]Reading {txt_file} and querying AI...[/bold magenta]", spinner="bouncingBar"):
                filepath, final_tags = ingest_raw_file(txt_file, title, category, tags)
            tag_str = f" [cyan]#{', #'.join(final_tags)}[/cyan]" if final_tags else ""
            print(f"[green]✔ AI formatting complete:[/green] {title}{tag_str}")
            open_in_editor(filepath)
        except Exception as e:
            print(f"[red]Failed to ingest file:[/red] {e}")

    @app.command()
    def graph(export: bool = False):
        """Visualize the knowledge graph of your notes."""
        graph_data = build_knowledge_graph()
        if export:
            export_mermaid_graph(graph_data)
        else:
            display_graph(graph_data)
        
    @app.command()
    def log(text: list[str]):
        """Smart log using Natural Language and AI."""
        full_text = " ".join(text)
        if not full_text:
            print("[yellow]Please provide some text to log.[/yellow]")
            return
        try:
            with console.status("[bold cyan]🧠 Consulting AI to parse your log...[/bold cyan]", spinner="dots"):
                category, value, final_tags = log_natural_event(full_text)
            tag_str = f" [cyan]#{', #'.join(final_tags)}[/cyan]" if final_tags else ""
            print(f"[green]✔ Smart Logged:[/green] {category} → {value}{tag_str}")
        except Exception as e:
            print(f"[red]Error:[/red] {e}")
            
    @app.command()
    def kosmo():
        """Start the background reminder engine."""
        start_kosmo()

    @app.command()
    def manual():
        """Open the full manual in your text editor."""
        manual_path = Path(__file__).resolve().parent.parent.parent / "MANUAL.md"
        if not manual_path.exists():
            print("[red]MANUAL.md not found![/red]")
            return
        print("[green]Opening MANUAL.md...[/green]")
        open_in_editor(manual_path)