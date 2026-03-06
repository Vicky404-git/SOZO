import os
import sys
import subprocess
from datetime import datetime
from rich import print
from rich.table import Table
from rich.console import Console
from rich.tree import Tree
from rich.layout import Layout
from rich.panel import Panel
from rich.align import Align

console = Console()

# ---------------------------------------------------
# FILE UTILITIES
# ---------------------------------------------------

def open_in_editor(filepath):
    """Open a file in the system's default editor."""
    if sys.platform == "win32":
        os.startfile(filepath)
    elif sys.platform == "darwin":
        subprocess.call(["open", str(filepath)])
    else:
        subprocess.call(["xdg-open", str(filepath)])


# ---------------------------------------------------
# TIME & FORMATTING HELPERS
# ---------------------------------------------------

def extract_date(timestamp):
    return timestamp.split("T")[0]

def extract_time(timestamp):
    return timestamp.split("T")[1][:5]

def get_day_name(date_str):
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    return date_obj.strftime("%a")

def format_tags(tags):
    if not tags: return "-"
    return ", ".join([f"#{t.strip()}" for t in tags.split(",") if t.strip()])

def format_files(files):
    return files if files else "-"

def format_relation(relates_to):
    return f"→ #{relates_to}" if relates_to else "-"

def truncate_text(text, length=50):
    return text if len(text) <= length else text[:length] + "..."


# ---------------------------------------------------
# DASHBOARD TEXT FORMATTERS
# ---------------------------------------------------

def format_stats(stats):
    if not stats: return "[dim]No stats available yet.[/dim]"
    return "\n".join([f"[magenta]{cat}[/magenta]: [green]{count}[/green] events" for cat, count in stats])

def format_today_events(events):
    if not events: return "[dim]No events logged today.[/dim]"
    return "\n".join([f"[dim][{extract_time(e[1])}][/dim] [green]{e[2]}[/green] → {e[3]}" for e in events])

def format_timeline_preview(grouped_events, days=3, events_per_day=5):
    if not grouped_events: return "[dim]No recent timeline events.[/dim]"
    timeline_str = ""
    for date_str in sorted(grouped_events.keys(), reverse=True)[:days]:
        timeline_str += f"\n[bold magenta]{get_day_name(date_str)}[/bold magenta] [dim]({date_str})[/dim]\n"
        for e in grouped_events[date_str][:events_per_day]:
            timeline_str += f"  [dim][{extract_time(e[1])}][/dim] {e[2]} → {truncate_text(e[3])}\n"
    return timeline_str


# ---------------------------------------------------
# MAIN UI RENDERING (RICH)
# ---------------------------------------------------

def show_empty(message):
    print(f"[yellow]{message}[/yellow]")

def display_events(events, title):
    if not events:
        show_empty(f"No events found for: {title}")
        return

    table = Table(title=title, show_lines=True)
    table.add_column("ID", style="dim")
    table.add_column("Date", style="cyan")
    table.add_column("Time", style="cyan")
    table.add_column("Category", style="magenta")
    table.add_column("Value")
    table.add_column("Files", style="dim") 
    table.add_column("Links", style="magenta")
    table.add_column("Tags", style="blue")
    table.add_column("🔔", justify="center")

    for event in events:
        event_id, timestamp, category, value, remind, tags, files, relates_to = event
        table.add_row(
            str(event_id), extract_date(timestamp), extract_time(timestamp), category, value,
            format_files(files), format_relation(relates_to), format_tags(tags), "✔" if remind else "",
        )
    console.print(table)

def display_stats(stats_data):
    if not stats_data:
        show_empty("No data to analyze yet.")
        return

    table = Table(title="Activity Stats")
    table.add_column("Category", style="magenta")
    table.add_column("Event Count", justify="right", style="green")

    for category, count in stats_data:
        table.add_row(category, str(count))
    console.print(table)

def display_timeline(grouped_events, title="Timeline"):
    if not grouped_events:
        show_empty(f"No events found for this {title.lower()}.")
        return

    print(f"\n[bold cyan]📅 {title}[/bold cyan]\n")
    for date_str in sorted(grouped_events.keys()):
        print(f"[bold magenta]{get_day_name(date_str)}[/bold magenta] [dim]({date_str})[/dim]")
        for event in grouped_events[date_str]:
            _, timestamp, category, value, _, tags, files, relates_to = event
            
            tag_str = f" [cyan]{format_tags(tags)}[/cyan]" if tags else ""
            file_str = f" 📎 [dim]{files}[/dim]" if files else ""
            rel_str = f" 🔗 [magenta]{format_relation(relates_to)}[/magenta]" if relates_to else ""
            
            print(f"  [dim][{extract_time(timestamp)}][/dim] [green]{category}[/green] → {value}{tag_str}{file_str}{rel_str}")
        print()

def display_graph(graph_data):
    if not graph_data:
        show_empty("No notes or [[wikilinks]] found in the vault.")
        return
        
    print("\n[bold cyan]🌌 Sōzō Knowledge Graph[/bold cyan]\n")
    root = Tree("📁 [bold magenta]Sōzō Vault[/bold magenta]")
    
    for note, links in graph_data.items():
        note_node = root.add(f"📄 [green]{note}[/green]")
        for link in links:
            note_node.add(f"🔗 [cyan]{link}[/cyan]")
            
    console.print(root)
    print()
    
def export_mermaid_graph(graph_data, filename="network_graph.md"):
    if not graph_data:
        show_empty("No notes to graph.")
        return
        
    with open(filename, "w", encoding="utf-8") as f:
        f.write("```mermaid\n")
        f.write("graph TD;\n") # Top-Down Network Graph
        
        for note, links in graph_data.items():
            safe_note = note.replace(" ", "_").replace("-", "_")
            for link in links:
                safe_link = link.replace(" ", "_").replace("-", "_")
                f.write(f"    {safe_note}[{note}] --> {safe_link}[{link}];\n")
                
        f.write("```\n")
        
    print(f"[green]✔ Network graph exported to {filename}[/green]")
    print("[dim]Open this file in GitHub, Obsidian, or VSCode to see the 2D visualization.[/dim]")

def display_dashboard(stats, today_events, timeline_grouped):
    layout = Layout()
    layout.split_column(Layout(name="header", size=3), Layout(name="main"))
    layout["main"].split_row(Layout(name="left", ratio=1), Layout(name="right", ratio=2))
    layout["right"].split_column(Layout(name="today", ratio=1), Layout(name="timeline", ratio=2))
    
    layout["header"].update(Panel(Align.center("[bold cyan]🌌 Sōzō Command Center[/bold cyan]"), style="blue"))
    
    # Notice how clean this is by using your new formatters!
    layout["left"].update(Panel(format_stats(stats), title="[bold yellow]📊 Activity Stats[/bold yellow]", border_style="yellow"))
    layout["today"].update(Panel(format_today_events(today_events), title="[bold cyan]⚡ Today's Actions[/bold cyan]", border_style="cyan"))
    layout["timeline"].update(Panel(format_timeline_preview(timeline_grouped), title="[bold blue]📅 Recent Timeline[/bold blue]", border_style="blue"))
    
    console.print(layout)