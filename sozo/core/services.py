import os
from pathlib import Path
from datetime import datetime
import dateparser
import subprocess
from sozo.core.repos import (
    insert_event, fetch_all_events, fetch_events_by_date,
    search_events_in_db, fetch_category_stats, delete_event
)

def parse_datetime(input_str):
    if not input_str:
        return datetime.now()
    parsed = dateparser.parse(input_str)
    if not parsed:
        raise ValueError("Invalid date format")
    return parsed

def detect_project():
    """Climbs up to 3 directories to find a .git folder and returns the project name."""
    current_dir = Path.cwd()
    for _ in range(3):
        if (current_dir / ".git").exists():
            return current_dir.name
        if current_dir.parent == current_dir:
            break
        current_dir = current_dir.parent
    return None

def add_event(category, value, at=None, remind=False, tags=None, files=None):
    event_time = parse_datetime(at)
    now = datetime.now()
    
    tags_list = list(tags) if tags else []
    
    # Auto-Project Detection
    project = detect_project()
    if project and project not in tags_list:
        tags_list.append(project)

    tags_str = ",".join(tags_list)
    files_str = ",".join(files) if files else ""
    
    insert_event(
        event_time.isoformat(), category, value, now.isoformat(), int(remind), tags_str, files_str
    )
    return tags_list

def export_to_md(tag=None, filename="timeline.md"):
    events = fetch_all_events()
    
    if tag:
        events = [e for e in events if e[5] and tag in e[5].split(",")]

    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"# Sōzō Export\n")
        f.write(f"*Generated on {datetime.now().strftime('%Y-%m-%d %H:%M')}*\n\n")
        
        for e in events:
            date_part, time_part = e[1].split("T")
            f.write(f"### {date_part} | {time_part[:5]} - {e[2].capitalize()}\n")
            f.write(f"**Action:** {e[3]}\n")
            if e[5]:
                f.write(f"- **Tags:** {', '.join(['#'+t.strip() for t in e[5].split(',')])}\n")
            if e[6]:
                f.write(f"- **Files:** `{e[6]}`\n")
            f.write("\n---\n\n")

# Pass-throughs
def list_events(date=None):
    if date:
        parsed = parse_datetime(date)
        return fetch_events_by_date(parsed.date().isoformat())
    return fetch_all_events()

def show_today():
    today = datetime.now().date().isoformat()
    return fetch_events_by_date(today)

def search_events(query):
    return search_events_in_db(query)

def get_stats():
    return fetch_category_stats()

def remove_event(event_id):
    delete_event(event_id)
    
def get_git_changes():
    """Gets a list of changed files for the auto-commit message."""
    try:
        # Check what is staged
        result = subprocess.run(["git", "diff", "--cached", "--name-only"], capture_output=True, text=True)
        files = [f for f in result.stdout.split('\n') if f]
        
        # If nothing is staged, stage everything and check again
        if not files:
            subprocess.run(["git", "add", "."])
            result = subprocess.run(["git", "diff", "--cached", "--name-only"], capture_output=True, text=True)
            files = [f for f in result.stdout.split('\n') if f]
            
        return files
    except Exception:
        return []

def execute_auto_commit(custom_msg=None):
    """Handles the commit process and prepares the AI integration point."""
    files = get_git_changes()
    
    if not files:
        raise ValueError("No changes found to commit.")

    # -------------------------------------------------------------
    # PHASE 3 AI INTEGRATION POINT
    # Later, we will send the `files` or `git diff` to an AI here.
    # For now, we use a basic file-listing string.
    # -------------------------------------------------------------
    if custom_msg:
        commit_msg = custom_msg
    else:
        file_list = ", ".join(files[:3]) + ("..." if len(files) > 3 else "")
        commit_msg = f"Update: {file_list}"
    
    # Run the actual git commit
    process = subprocess.run(["git", "commit", "-m", commit_msg], capture_output=True, text=True)
    
    if process.returncode != 0:
        raise RuntimeError(f"Git failed: {process.stderr}")
        
    # Log it to Sozo!
    project = detect_project()
    tags = ["git"]
    if project:
        tags.append(project)
        
    add_event("programming", f"Git Commit: {commit_msg}", tags=tags, files=files)
    return commit_msg, files