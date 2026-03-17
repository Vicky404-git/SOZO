import typer
import subprocess
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
from sozo.core.services import *
from sozo.cli.utils import *

app = typer.Typer()


# ================================================
# CLI HELPERS (DRY PRINCIPLES)
# ================================================

def _get_note_path(filename: str) -> Path:
    """Helper to find a note in the vault safely."""
    found = list(VAULT_PATH.rglob(f"*{filename}*.md"))
    if not found:
        print(f"[red]Could not find any note matching '{filename}'[/red]")
        raise typer.Exit()
    return found[0]

def _log_git_action(message: str):
    """Helper to detect projects and log git commands."""
    project = detect_project()
    tags = ["git"]
    if project:
        tags.append(project)
    add_event("programming", message, tags=tags)


def register_commands(app: typer.Typer):

    # ------------------------------------------------
    # ADD EVENT
    # ------------------------------------------------
    @app.command()
    def add(
        category: str,
        value: list[str],
        at: str = typer.Option(None, "--at"),
        remind: bool = typer.Option(False, "--remind"),
        tags: list[str] = typer.Option(None, "--tag", "-t"),
        files: list[str] = typer.Option(None, "--file", "-f"),
        relates_to: int = typer.Option(None, "--relates-to", "-r"),
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
            
    # -----------------------------------------------
    # EDIT EVENT
    # -----------------------------------------------
    @app.command()
    def edit(
        event_id: int,
        category: str = typer.Option(None, "--category", "-c"),
        value: str = typer.Option(None, "--value", "-v"),
        tags: list[str] = typer.Option(None, "--tag", "-t"),
        files: list[str] = typer.Option(None, "--file", "-f"),
    ):
        try:
            edit_event(event_id, category, value, tags, files)
            print(f"[green]✔ Event {event_id} updated successfully![/green]")
        except Exception as e:
            print(f"[red]Error:[/red] {e}")


    # ------------------------------------------------
    # EXPORT
    # ------------------------------------------------
    @app.command()
    def export(tag: str = typer.Option(None, "--tag", "-t"), out: str = typer.Option("timeline.md", "--out", "-o")):
        try:
            export_to_md(tag, out)
            print(f"[green]✔ Exported timeline to {out}[/green]")
        except Exception as e:
            print(f"[red]Failed to export:[/red] {e}")


    # ------------------------------------------------
    # LIST / TODAY / SEARCH / FILE / STATS
    # ------------------------------------------------
    @app.command(name="list")
    def list_cmd(date: str = None):
        display_events(list_events(date), "All Events")

    @app.command()
    def today():
        display_events(show_today(), "Today's Events")

    @app.command()
    def search(query: str):
        display_events(search_events(query), f"Search Results for '{query}'")
        
    @app.command()
    def file(name: str):
        display_events(get_file_history(name), f"History for '{name}'")
        
    @app.command()
    def stats():
        display_stats(get_stats())


    # ------------------------------------------------
    # DELETE
    # ------------------------------------------------
    @app.command()
    def delete(event_id: int):
        remove_event(event_id)
        print(f"[red]✔ Event {event_id} deleted.[/red]")


    # ------------------------------------------------
    # BRAIN SEARCH (DEEP VAULT SEARCH)
    # ------------------------------------------------
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
            highlighted_snippet = snippet.replace(keyword, f"[bold green]{keyword}[/bold green]")
            highlighted_snippet = highlighted_snippet.replace(keyword.capitalize(), f"[bold green]{keyword.capitalize()}[/bold green]")
            print(Panel(f"[dim]...{highlighted_snippet}...[/dim]", title=f"[magenta]📄 {filename}[/magenta]", title_align="left"))
            
    # ------------------------------------------------
    # CONCEPT ENGINE
    # ------------------------------------------------
    @app.command()
    def concept(keyword: str):
        """Unify notes, events, and projects under a single Concept Node."""
        data = build_concept(keyword)
        display_concept(keyword, data)


    # ------------------------------------------------
    # AUTO COMMIT
    # ------------------------------------------------
    @app.command()
    def commit(msg: str = typer.Option(None, "--msg", "-m")):
        try:
            with console.status("[bold cyan]Analyzing changes and consulting AI...[/bold cyan]", spinner="dots"):
                commit_msg, files = execute_auto_commit(msg)

            print("[green]✔ Committed successfully![/green]")
            print(f"📝 [bold]Message:[/bold] {commit_msg}")
            print(f"📎 [bold]Files:[/bold] {', '.join(files)}")
            print("[blue]✔ Logged to Sōzō timeline.[/blue]")
        except Exception as e:
            print(f"[red]Error:[/red] {e}")
            

    # ------------------------------------------------
    # SMART PUSH
    # ------------------------------------------------
    @app.command()
    def push():
        """Smart git push with branch confirmation."""
        try:
            result = subprocess.run(["git", "branch", "--show-current"], capture_output=True, text=True, check=True)
            current_branch = result.stdout.strip() or "master"
        except Exception:
            print("[red]Error: Not inside a valid git repository.[/red]")
            return

        is_default = current_branch in ["main", "master"]
        prompt_msg = f"Push to {current_branch} right?" if is_default else f"Push to current branch '{current_branch}'?"
        
        if typer.confirm(prompt_msg, default=True):
            target_branch = current_branch
        else:
            target_branch = typer.prompt("Enter the branch name to push to")

        print(f"\n[dim]Executing: git push origin {target_branch}[/dim]")
        push_result = subprocess.run(["git", "push", "origin", target_branch])
        
        if push_result.returncode == 0:
            _log_git_action(f"Git Push: origin {target_branch}")
            print("[blue]✔ Push logged to Sōzō timeline.[/blue]")
        else:
            print("[red]✖ Git push failed. Check your remote and permissions.[/red]")

    # ------------------------------------------------
    # RELEASE
    # ------------------------------------------------
    @app.command()
    def release(version: str = typer.Argument(..., help="Version number (e.g., v1.0.0)")):
        """Generate AI release notes, tag the repo, and push."""
        # Ensure the version starts with a 'v' (best practice)
        if not version.startswith("v"):
            version = f"v{version}"

        try:
            with console.status(f"[bold cyan]Scanning git history and writing release notes for {version}...[/bold cyan]", spinner="dots"):
                notes = execute_release(version)

            print(f"\n[green]✔ Successfully created and pushed tag {version}![/green]\n")
            
            # Print the AI's release notes beautifully in the terminal
            console.print(Panel(Markdown(notes), title=f"[bold blue]📦 Release Notes: {version}[/bold blue]", border_style="blue"))
            print("\n[dim]✔ Action logged to Sōzō timeline.[/dim]")
        except Exception as e:
            print(f"[red]Error:[/red] {e}")

    # ------------------------------------------------
    # PASS THROUGH GIT
    # ------------------------------------------------
    @app.command(context_settings={"allow_extra_args": True, "ignore_unknown_options": True})
    def git(ctx: typer.Context):
        if not ctx.args:
            print("[yellow]Please provide git commands.[/yellow]")
            return

        command_str = " ".join(ctx.args)
        print(f"[dim]Running: git {command_str}[/dim]")
        
        result = subprocess.run(["git"] + list(ctx.args))
        if result.returncode == 0:
            _log_git_action(f"Git Execute: git {command_str}")
            print("[blue]✔ Action logged to Sōzō[/blue]")


    # ------------------------------------------------
    # TIMELINE & DASHBOARD
    # ------------------------------------------------
    @app.command()
    def timeline(period: str = typer.Argument("week"), tag: str = typer.Option(None, "--tag", "-t")):
        title_suffix = f" (#{tag})" if tag else ""
        display_timeline(get_timeline(period, tag), f"{period.capitalize()} Timeline{title_suffix}")

    @app.command()
    def dash():
        display_dashboard(get_stats(), show_today(), get_timeline("week"))
        

    # ------------------------------------------------
    # NOTE (UI EDITOR & GUIDED CREATOR)
    # ------------------------------------------------
    @app.command()
    def note(
        title: str = typer.Argument(None, help="Optional title of the note"),
        category: str = typer.Option(None, "--category", "-c"),
        tags: list[str] = typer.Option(None, "--tag", "-t"),
    ):
        print("[bold cyan]📝 Sōzō Notebook[/bold cyan]")
        
        if not title:
            title = Prompt.ask("[bold yellow]What is the title of this note?[/bold yellow]")
            if not title:
                title = f"Note {datetime.now().strftime('%Y-%m-%d %H:%M')}"
                
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
            
    # ------------------------------------------------
    # BOOKSHELF & NOTE MANAGEMENT
    # ------------------------------------------------
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
            md_content = f.read()
            
        console.print(f"\n[dim]Reading: {filepath.name}[/dim]\n")
        console.print(Markdown(md_content))
        print()
    
    @app.command()
    def rewrite(filename: str = typer.Argument(..., help="Part of the filename to edit")):
        """Open an existing vault note to edit and update it."""
        filepath = _get_note_path(filename)
        print(f"[dim]Opening {filepath.name}...[/dim]")
        
        with open(filepath, "r", encoding="utf-8") as f:
            current_content = f.read()
            
        new_content = click.edit(current_content)
        if new_content is not None:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"[green]✔ Note updated:[/green] {filepath.name}")
        else:
            print("[dim]No changes made. Note closed.[/dim]")


    # ------------------------------------------------
    # INGEST RAW TEXT
    # ------------------------------------------------
    @app.command()
    def ingest(
        txt_file: str = typer.Argument(...),
        title: str = typer.Argument(...),
        category: str = typer.Option("study", "--category", "-c"),
        tags: list[str] = typer.Option(None, "--tag", "-t"),
    ):
        try:
            with console.status(f"[bold magenta]Reading {txt_file} and querying AI...[/bold magenta]", spinner="bouncingBar"):
                filepath, final_tags = ingest_raw_file(txt_file, title, category, tags)

            tag_str = f" [cyan]#{', #'.join(final_tags)}[/cyan]" if final_tags else ""
            print(f"[green]✔ AI formatting complete:[/green] {title}{tag_str}")
            open_in_editor(filepath)
        except Exception as e:
            print(f"[red]Failed to ingest file:[/red] {e}")

    # ------------------------------------------------
    # GRAPH
    # ------------------------------------------------
    @app.command()
    def graph(export: bool = typer.Option(False, "--export", "-e", help="Export as 2D Mermaid Network Graph")):
        graph_data = build_knowledge_graph()
        if export:
            export_mermaid_graph(graph_data)
        else:
            display_graph(graph_data)
        
    # ------------------------------------------------
    # SMART LOG (AI)
    # ------------------------------------------------
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
            
    # ------------------------------------------------
    # AUTO DOCS
    # ------------------------------------------------
    @app.command()
    def docs(sync: bool = typer.Option(False, "--sync", "-s", help="Auto-update markdown docs using AI")):
        """AI tool to auto-write and sync Sōzō documentation."""
        if not sync:
            print("[yellow]Use 'sozo docs --sync' to auto-update your documentation files based on current code.[/yellow]")
            return
            
        try:
            with console.status("[bold magenta]🤖 AI is reading your code and rewriting docs...[/bold magenta]", spinner="point"):
                updated = sync_documentation()
                
            if updated:
                print(f"[green]✔ Successfully updated:[/green] {', '.join(updated)}")
                print("[blue]✔ Action logged to Sōzō timeline.[/blue]")
            else:
                print("[yellow]No documentation files found to update.[/yellow]")
        except Exception as e:
            print(f"[red]Error syncing docs:[/red] {e}")

    # ------------------------------------------------
    # MISC
    # ------------------------------------------------
    @app.command()
    def kosmo():
        start_kosmo()

    @app.command()
    def manual():
        manual_path = Path(__file__).resolve().parent.parent.parent / "MANUAL.md"
        if not manual_path.exists():
            print("[red]MANUAL.md not found![/red]")
            return
        print("[green]Opening MANUAL.md...[/green]")
        open_in_editor(manual_path)