from rich.table import Table
from rich.console import Console
from rich import print
from rich.tree import Tree
from rich.layout import Layout
from rich.panel import Panel
from rich.align import Align
from datetime import datetime

console = Console()

def display_events(events, title):
    if not events:
        print(f"[yellow]No events found for: {title}[/yellow]")
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
        
        date_part, time_part = timestamp.split("T")
        time_only = time_part[:5]
        
        tag_display = ", ".join([f"#{t.strip()}" for t in tags.split(",") if t]) if tags else "-"
        file_display = files if files else "-"
        rel_display = f"→ #{relates_to}" if relates_to else "-"

        table.add_row(
            str(event_id), date_part, time_only, category, value,
            file_display, rel_display, tag_display, "✔" if remind else "",
        )

    console.print(table)

def display_stats(stats_data):
    if not stats_data:
        print("[yellow]No data to analyze yet.[/yellow]")
        return

    table = Table(title="Activity Stats")
    table.add_column("Category", style="magenta")
    table.add_column("Event Count", justify="right", style="green")

    for category, count in stats_data:
        table.add_row(category, str(count))

    console.print(table)

def display_timeline(grouped_events, title="Timeline"):
    if not grouped_events:
        print(f"[yellow]No events found for this {title.lower()}.[/yellow]")
        return

    print(f"\n[bold cyan]📅 {title}[/bold cyan]\n")

    for date_str, events in sorted(grouped_events.items()):
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        day_name = date_obj.strftime("%a") 

        print(f"[bold magenta]{day_name}[/bold magenta] [dim]({date_str})[/dim]")

        for event in events:
            _, timestamp, category, value, _, tags, files, relates_to = event
            time_part = timestamp.split("T")[1][:5]
            
            tag_str = f" [cyan]#{', #'.join([t.strip() for t in tags.split(',') if t])}[/cyan]" if tags else ""
            file_str = f" 📎 [dim]{files}[/dim]" if files else ""
            rel_str = f" 🔗 [magenta]→ #{relates_to}[/magenta]" if relates_to else ""

            print(f"  [dim][{time_part}][/dim] [green]{category}[/green] → {value}{tag_str}{file_str}{rel_str}")
        print()

def display_graph(graph_data):
    """Draws an Obsidian-style tree of connected notes."""
    if not graph_data:
        print("[yellow]No notes or [[wikilinks]] found in the vault.[/yellow]")
        return
        
    print("\n[bold cyan]🌌 Sōzō Knowledge Graph[/bold cyan]\n")
    root = Tree("📁 [bold magenta]Sōzō Vault[/bold magenta]")
    
    for note, links in graph_data.items():
        note_node = root.add(f"📄 [green]{note}[/green]")
        for link in links:
            note_node.add(f"🔗 [cyan]{link}[/cyan]")
            
    console.print(root)
    print()

def display_dashboard(stats, today_events, timeline_grouped):
    """Draws a Notion-style split-screen terminal dashboard."""
    layout = Layout()
    
    # Divide the terminal screen into sections
    layout.split_column(
        Layout(name="header", size=3),
        Layout(name="main")
    )
    layout["main"].split_row(
        Layout(name="left", ratio=1),
        Layout(name="right", ratio=2)
    )
    layout["right"].split_column(
        Layout(name="today", ratio=1),
        Layout(name="timeline", ratio=2)
    )
    
    # 1. Header
    layout["header"].update(Panel(Align.center("[bold cyan]🌌 Sōzō Command Center[/bold cyan]"), style="blue"))
    
    # 2. Stats Panel (Left)
    stats_str = ""
    if stats:
        for cat, count in stats:
            stats_str += f"[magenta]{cat}[/magenta]: [green]{count}[/green] events\n"
    else:
        stats_str = "[dim]No stats available yet.[/dim]"
    layout["left"].update(Panel(stats_str, title="[bold yellow]📊 Activity Stats[/bold yellow]", border_style="yellow"))
    
    # 3. Today Panel (Top Right)
    today_str = ""
    if today_events:
        for e in today_events:
            time_only = e[1].split("T")[1][:5]
            today_str += f"[dim][{time_only}][/dim] [green]{e[2]}[/green] → {e[3]}\n"
    else:
        today_str = "[dim]No events logged today.[/dim]"
    layout["today"].update(Panel(today_str, title="[bold cyan]⚡ Today's Actions[/bold cyan]", border_style="cyan"))
    
    # 4. Timeline Panel (Bottom Right)
    timeline_str = ""
    if timeline_grouped:
        # Show only the 3 most recent days to fit the dashboard
        for date_str in sorted(timeline_grouped.keys(), reverse=True)[:3]:
            day_name = datetime.strptime(date_str, "%Y-%m-%d").strftime("%a")
            timeline_str += f"\n[bold magenta]{day_name}[/bold magenta] [dim]({date_str})[/dim]\n"
            for e in timeline_grouped[date_str][:5]:  # Limit to 5 events per day so it doesn't overflow
                time_only = e[1].split("T")[1][:5]
                # Truncate value if it's too long
                val = e[3][:50] + "..." if len(e[3]) > 50 else e[3]
                timeline_str += f"  [dim][{time_only}][/dim] {e[2]} → {val}\n"
    else:
        timeline_str = "[dim]No recent timeline events.[/dim]"
    layout["timeline"].update(Panel(timeline_str, title="[bold blue]📅 Recent Timeline[/bold blue]", border_style="blue"))
    
    # Render the full dashboard
    console.print(layout)