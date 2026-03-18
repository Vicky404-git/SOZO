import os
import re
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict
from sozo.core.config import VAULT_PATH
import dateparser

from sozo.core.repos import (
    insert_event, fetch_all_events, fetch_events_by_date,
    search_events_in_db, fetch_category_stats, delete_event,
    fetch_events_in_range, fetch_file_history, fetch_event_by_id, update_event
)


# --------------------------------------------------
# DATETIME HELPERS
# --------------------------------------------------

def parse_datetime(input_str):
    if not input_str:
        return datetime.now()
    parsed = dateparser.parse(input_str)
    if not parsed:
        raise ValueError("Invalid date format")
    return parsed


# --------------------------------------------------
# PROJECT DETECTION
# --------------------------------------------------

def detect_project():
    current_dir = Path.cwd()
    for _ in range(3):
        if (current_dir / ".git").exists():
            return current_dir.name
        if current_dir.parent == current_dir:
            break
        current_dir = current_dir.parent
    return None


# --------------------------------------------------
# EVENT MANAGEMENT
# --------------------------------------------------

def add_event(category, value, at=None, remind=False, tags=None, files=None, relates_to=None):
    event_time = parse_datetime(at)
    now = datetime.now()
    tags_list = list(tags) if tags else []

    project = detect_project()
    if project and project not in tags_list:
        tags_list.append(project)

    tags_str = ",".join(tags_list)
    files_str = ",".join(files) if files else ""

    insert_event(
        event_time.isoformat(), category, value, now.isoformat(),
        int(remind), tags_str, files_str, relates_to,
    )
    return tags_list

def log_natural_event(text: str):
    from sozo.core.ai import parse_natural_language_event
    parsed_data = parse_natural_language_event(text)
    
    category = parsed_data.get("category", "log").lower()
    value = parsed_data.get("value", text)
    tags = parsed_data.get("tags", [])
    
    final_tags = add_event(category, value, tags=tags)
    return category, value, final_tags

def edit_event(event_id, category=None, value=None, tags=None, files=None):
    row = fetch_event_by_id(event_id)
    if not row:
        raise ValueError(f"Event {event_id} not found.")
    
    new_cat = category if category else row[2]
    new_val = value if value else row[3]
    new_tags = ",".join(tags) if tags else row[7]
    new_files = ",".join(files) if files else row[8]
    
    update_event(event_id, new_cat, new_val, new_tags, new_files)


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

def get_file_history(filename: str):
    return fetch_file_history(filename)


# --------------------------------------------------
# MARKDOWN EXPORT
# --------------------------------------------------

def export_to_md(tag=None, filename="timeline.md"):
    events = fetch_all_events()
    if tag:
        events = [e for e in events if e[5] and tag in e[5].split(",")]

    with open(filename, "w", encoding="utf-8") as f:
        f.write("# Sōzō Export\n")
        f.write(f"*Generated on {datetime.now().strftime('%Y-%m-%d %H:%M')}*\n\n")

        for e in events:
            date_part, time_part = e[1].split("T")
            f.write(f"### {date_part} | {time_part[:5]} - {e[2].capitalize()}\n")
            f.write(f"**Action:** {e[3]}\n")
            if e[5]:
                tags = ", ".join(["#" + t.strip() for t in e[5].split(",")])
                f.write(f"- **Tags:** {tags}\n")
            if e[6]:
                f.write(f"- **Files:** `{e[6]}`\n")
            f.write("\n---\n\n")


# --------------------------------------------------
# TIMELINE
# --------------------------------------------------

def get_timeline(period="week", tag=None):
    now = datetime.now()
    start_date = (now - timedelta(days=30 if period == "month" else 7)).date().isoformat()
    grouped = defaultdict(list)
    
    for event in fetch_events_in_range(start_date, now.date().isoformat(), tag):
        grouped[event[1].split("T")[0]].append(event)
        
    return grouped


# --------------------------------------------------
# VAULT HELPERS (SECOND BRAIN)
# --------------------------------------------------

def _save_to_vault(title, category, tags, content, action_desc):
    tags_list = list(tags) if tags else []
    project = detect_project()
    if project and project not in tags_list: 
        tags_list.append(project)
    
    subfolder = tags_list[0] if tags_list else "general"
    vault_path = VAULT_PATH / subfolder
    vault_path.mkdir(parents=True, exist_ok=True)

    safe_title = re.sub(r"[^a-zA-Z0-9]+", "-", title.lower()).strip("-")
    filename = f"{datetime.now().strftime('%Y%m%d')}-{safe_title}.md"
    filepath = vault_path / filename

    yaml_tags = f"[{', '.join([f'\"{t}\"' for t in tags_list])}]" if tags_list else "[]"
    iso_date = datetime.now().strftime('%Y-%m-%d %H:%M')

    yaml_frontmatter = f"""---
title: "{title}"
date: {iso_date}
category: {category}
tags: {yaml_tags}
---

# {title}

{content}"""

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(yaml_frontmatter)

    insert_event(datetime.now().isoformat(), category, f"{action_desc}: {title}",
                 datetime.now().isoformat(), 0, ",".join(tags_list), f"vault/{subfolder}/{filename}", None)
    return filepath, tags_list


def search_vault(keyword: str) -> dict:
    if not VAULT_PATH.exists():
        return {}
        
    results = {}
    keyword = keyword.lower()
    
    for filepath in VAULT_PATH.rglob("*.md"):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
                if keyword in content.lower():
                    lines = content.split('\n')
                    snippet = ""
                    for line in lines:
                        if keyword in line.lower():
                            snippet = line.strip()
                            break
                    results[filepath.name] = snippet
        except Exception:
            continue
            
    return results

# --------------------------------------------------
# NOTE CREATION
# --------------------------------------------------

def create_note(title: str, category: str, tags: list[str] = None, content: str = ""):
    return _save_to_vault(title, category, tags, content, "Created note")

def ingest_raw_file(txt_filepath: str, title: str, category: str, tags: list = None):
    from sozo.core.ai import format_notes_to_markdown
    path = Path(txt_filepath)

    if not path.exists():
        raise FileNotFoundError(f"Could not find the file: {txt_filepath}")

    with open(path, "r", encoding="utf-8") as f:
        raw_text = f.read()

    formatted_md = format_notes_to_markdown(raw_text)
    return _save_to_vault(title, category, tags, formatted_md, "AI Ingested")


# --------------------------------------------------
# KNOWLEDGE GRAPH
# --------------------------------------------------

def build_knowledge_graph():
    if not VAULT_PATH.exists():
        return {}

    graph = {}
    link_pattern = re.compile(r"\[\[(.*?)\]\]")

    for filepath in VAULT_PATH.rglob("*.md"):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
                links = link_pattern.findall(content)
                graph[filepath.stem] = links
        except Exception:
            continue

    return graph

# --------------------------------------------------
# CONCEPT ENGINE
# --------------------------------------------------

def build_concept(keyword: str) -> dict:
    events = search_events_in_db(keyword)
    notes = search_vault(keyword)
    
    concept_data = {
        "projects": [],
        "events": [],
        "notes": list(notes.keys())
    }
    
    for e in events:
        if e[2].lower() == "project":
            concept_data["projects"].append(e)
        else:
            concept_data["events"].append(e)
            
    return concept_data