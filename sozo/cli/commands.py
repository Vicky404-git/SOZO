import typer
import subprocess
from pathlib import Path
from rich import print

from sozo.core.kosmo import start_kosmo
from sozo.core.services import (
    add_event,
    list_events,
    remove_event,
    show_today,
    search_events,
    get_stats,
    export_to_md,
)

from sozo.cli.utils import (
    display_events,
    display_stats,
    display_timeline,
    display_graph,
    display_dashboard,
    open_in_editor,
)

app = typer.Typer()


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
        from sozo.core.services import edit_event
        try:
            edit_event(event_id, category, value, tags, files)
            print(f"[green]✔ Event {event_id} updated successfully![/green]")
        except Exception as e:
            print(f"[red]Error:[/red] {e}")


    # ------------------------------------------------
    # EXPORT
    # ------------------------------------------------
    @app.command()
    def export(
        tag: str = typer.Option(None, "--tag", "-t"),
        out: str = typer.Option("timeline.md", "--out", "-o"),
    ):
        try:
            export_to_md(tag, out)
            print(f"[green]✔ Exported timeline to {out}[/green]")
        except Exception as e:
            print(f"[red]Failed to export:[/red] {e}")


    # ------------------------------------------------
    # LIST
    # ------------------------------------------------
    @app.command(name="list")
    def list_cmd(date: str = None):
        display_events(list_events(date), "All Events")


    # ------------------------------------------------
    # TODAY
    # ------------------------------------------------
    @app.command()
    def today():
        display_events(show_today(), "Today's Events")


    # ------------------------------------------------
    # SEARCH
    # ------------------------------------------------
    @app.command()
    def search(query: str):
        display_events(search_events(query), f"Search Results for '{query}'")


    # ------------------------------------------------
    # STATS
    # ------------------------------------------------
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
    # KOSMO
    # ------------------------------------------------
    @app.command()
    def kosmo():
        start_kosmo()


    # ------------------------------------------------
    # MANUAL
    # ------------------------------------------------
    @app.command()
    def manual():

        manual_path = Path(__file__).resolve().parent.parent.parent / "MANUAL.md"

        if not manual_path.exists():
            print("[red]MANUAL.md not found![/red]")
            return

        print("[green]Opening MANUAL.md...[/green]")
        open_in_editor(manual_path)


    # ------------------------------------------------
    # AUTO COMMIT
    # ------------------------------------------------
    @app.command()
    def commit(msg: str = typer.Option(None, "--msg", "-m")):

        from sozo.core.services import execute_auto_commit

        try:
            print("[dim]Analyzing changes...[/dim]")

            commit_msg, files = execute_auto_commit(msg)

            print("[green]✔ Committed successfully![/green]")
            print(f"📝 [bold]Message:[/bold] {commit_msg}")
            print(f"📎 [bold]Files:[/bold] {', '.join(files)}")
            print("[blue]✔ Logged to Sōzō timeline.[/blue]")

        except Exception as e:
            print(f"[red]Error:[/red] {e}")


    # ------------------------------------------------
    # PASS THROUGH GIT
    # ------------------------------------------------
    @app.command(context_settings={"allow_extra_args": True, "ignore_unknown_options": True})
    def git(ctx: typer.Context):

        from sozo.core.services import detect_project

        if not ctx.args:
            print("[yellow]Please provide git commands.[/yellow]")
            return

        command_str = " ".join(ctx.args)

        print(f"[dim]Running: git {command_str}[/dim]")
        
        result = subprocess.run(["git"] + list(ctx.args))
        
        if result.returncode == 0:

            project = detect_project()

            tags = ["git"]
            if project:
                tags.append(project)

            add_event("programming", f"Git Execute: git {command_str}", tags=tags)

            print("[blue]✔ Action logged to Sōzō[/blue]")


    # ------------------------------------------------
    # TIMELINE
    # ------------------------------------------------
    @app.command()
    def timeline(
        period: str = typer.Argument("week"),
        tag: str = typer.Option(None, "--tag", "-t", help="Filter timeline by tag")
    ):

        from sozo.core.services import get_timeline
        from sozo.cli.utils import display_timeline

        title_suffix = f" (#{tag})" if tag else ""
        display_timeline(get_timeline(period, tag), f"{period.capitalize()} Timeline{title_suffix}")

    # ------------------------------------------------
    # NOTE
    # ------------------------------------------------
    @app.command()
    def note(
        title: str,
        category: str = typer.Option("study", "--category", "-c"),
        tags: list[str] = typer.Option(None, "--tag", "-t"),
    ):

        from sozo.core.services import create_note

        try:
            print("[dim]Creating note...[/dim]")

            filepath, final_tags = create_note(title, category, tags)

            tag_str = f" [cyan]#{', #'.join(final_tags)}[/cyan]" if final_tags else ""

            print(f"[green]✔ Note created:[/green] {title}{tag_str}")

            open_in_editor(filepath)

        except Exception as e:
            print(f"[red]Error creating note:[/red] {e}")


    # ------------------------------------------------
    # FILE HISTORY
    # ------------------------------------------------
    @app.command()
    def file(name: str):

        from sozo.core.services import get_file_history

        display_events(get_file_history(name), f"History for '{name}'")


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

        from sozo.core.services import ingest_raw_file

        try:
            print("[dim]Reading file and querying AI...[/dim]")

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
    def graph():

        from sozo.core.services import build_knowledge_graph

        display_graph(build_knowledge_graph())


    # ------------------------------------------------
    # DASHBOARD
    # ------------------------------------------------
    @app.command()
    def graph(export: bool = typer.Option(False, "--export", "-e", help="Export as 2D Mermaid Network Graph")):
        from sozo.core.services import build_knowledge_graph
        from sozo.cli.utils import display_graph, export_mermaid_graph
        
        graph_data = build_knowledge_graph()
        if export:
            export_mermaid_graph(graph_data)
        else:
            display_graph(graph_data)