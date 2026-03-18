import typer
import subprocess
from rich import print
from rich.panel import Panel
from rich.markdown import Markdown

from sozo.cli.utils import console
from sozo.core.services import detect_project, add_event

# ----------------------------------------------------
# IMPORT FROM THE NEW DEV SERVICES
# ----------------------------------------------------
from sozo.core.dev_services import (
    execute_auto_commit,
    execute_release, 
    undo_release, 
    sync_documentation
)
# ================================================
# DEVELOPER HELPERS
# ================================================

def _log_git_action(message: str):
    """Helper to detect projects and log git commands."""
    project = detect_project()
    tags = ["git"]
    if project:
        tags.append(project)
    add_event("programming", message, tags=tags)


# ================================================
# DEVELOPER COMMANDS REGISTRY
# ================================================

def register_dev_commands(app: typer.Typer):

    # ------------------------------------------------
    # AUTO COMMIT
    # ------------------------------------------------
    @app.command()
    def commit(msg: str = typer.Option(None, "--msg", "-m")):
        """AI tool to automatically summarize and commit changes."""
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
        if not version.startswith("v"):
            version = f"v{version}"

        try:
            with console.status(f"[bold cyan]Scanning git history and writing release notes for {version}...[/bold cyan]", spinner="dots"):
                notes = execute_release(version)

            print(f"\n[green]✔ Successfully created and pushed tag {version}![/green]\n")
            console.print(Panel(Markdown(notes), title=f"[bold blue]📦 Release Notes: {version}[/bold blue]", border_style="blue"))
            print("\n[dim]✔ Action logged to Sōzō timeline.[/dim]")
        except Exception as e:
            print(f"[red]Error:[/red] {e}")
            
    # ------------------------------------------------
    # UNDO RELEASE
    # ------------------------------------------------
    @app.command()
    def unrelease(version: str = typer.Argument(..., help="Version number to undo (e.g., v0.3.0)")):
        """Undo a release: delete local/remote tags and scrub Sōzō logs."""
        if not version.startswith("v"):
            version = f"v{version}"

        try:
            with console.status(f"[bold red]Rolling back release {version}...[/bold red]", spinner="dots"):
                undo_release(version)

            print(f"\n[green]✔ Successfully scrubbed {version} from Git and GitHub![/green]")
            print("[dim]✔ Event removed from Sōzō timeline.[/dim]")
        except Exception as e:
            print(f"[red]Error:[/red] {e}")

    # ------------------------------------------------
    # PASS THROUGH GIT
    # ------------------------------------------------
    @app.command(context_settings={"allow_extra_args": True, "ignore_unknown_options": True})
    def git(ctx: typer.Context):
        """Pass commands straight to git while logging them to Sōzō."""
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
    # AUTO DOCS
    # ------------------------------------------------
    @app.command()
    def docs(sync: bool = typer.Option(False, "--sync", "-s", help="Auto-update markdown docs using AI")):
        """AI tool to auto-write and sync project documentation."""
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