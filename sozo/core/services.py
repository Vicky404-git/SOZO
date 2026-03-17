import os
import re
import subprocess
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict
from sozo.core.config import VAULT_PATH

import dateparser

from sozo.core.repos import (
    insert_event,
    fetch_all_events,
    fetch_events_by_date,
    search_events_in_db,
    fetch_category_stats,
    delete_event,
    fetch_events_in_range,
    fetch_file_history,
)


# --------------------------------------------------
# DATETIME HELPERS
# --------------------------------------------------

def parse_datetime(input_str):
    """Parse human-friendly date input."""
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
    """
    Detect current git project name by scanning up to
    3 parent directories.
    """
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
        event_time.isoformat(),
        category,
        value,
        now.isoformat(),
        int(remind),
        tags_str,
        files_str,
        relates_to,
    )

    return tags_list

def log_natural_event(text: str):
    from sozo.core.ai import parse_natural_language_event
    
    # 1. Ask the AI to parse the sentence
    parsed_data = parse_natural_language_event(text)
    
    # 2. Extract the pieces (with safe defaults just in case)
    category = parsed_data.get("category", "log").lower()
    value = parsed_data.get("value", text)
    tags = parsed_data.get("tags", [])
    
    # 3. Save it to the database!
    final_tags = add_event(category, value, tags=tags)
    
    return category, value, final_tags

def edit_event(event_id, category=None, value=None, tags=None, files=None):
    from sozo.core.repos import fetch_event_by_id, update_event
    row = fetch_event_by_id(event_id)
    if not row:
        raise ValueError(f"Event {event_id} not found.")
    
    # Extract current values if new ones aren't provided
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
# GIT INTEGRATION
# --------------------------------------------------

def get_git_diff():
    try:
        result = subprocess.run(
            ["git", "diff", "--cached"],
            capture_output=True,
            text=True,
            encoding="utf-8",
        )

        diff = result.stdout.strip()

        if not diff:
            subprocess.run(["git", "add", "."])
            result = subprocess.run(
                ["git", "diff", "--cached"],
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
            diff = result.stdout.strip()

        file_result = subprocess.run(
            ["git", "diff", "--cached", "--name-only"],
            capture_output=True,
            text=True,
            encoding="utf-8",
        )

        files = [f for f in file_result.stdout.split("\n") if f]
        return diff, files

    except Exception:
        return "", []


def execute_auto_commit(custom_msg=None):
    from sozo.core.ai import generate_commit_message
    diff, files = get_git_diff()

    if not files:
        raise ValueError("No changes found to commit.")

    if custom_msg:
        commit_msg = custom_msg
    else:
        # Pass the full, raw diff! The AI Map-Reduce engine handles the chunking now.
        commit_msg = generate_commit_message(diff)

    process = subprocess.run(
        ["git", "commit", "-m", commit_msg],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )

    if process.returncode != 0:
        raise RuntimeError(f"Git failed: {process.stderr}")

    project = detect_project()
    tags = ["git", "ai-commit"]
    if project:
        tags.append(project)

    add_event("programming", f"Git Commit: {commit_msg}", tags=tags, files=files)
    return commit_msg, files

def execute_release(version: str) -> str:
    from sozo.core.ai import generate_release_notes
    
    # 1. Find the last git tag to know where to start scanning
    try:
        last_tag_proc = subprocess.run(
            ["git", "describe", "--tags", "--abbrev=0"], 
            capture_output=True, text=True, encoding="utf-8" # <-- ADDED ENCODING
        )
        last_tag = last_tag_proc.stdout.strip()
    except Exception:
        last_tag = ""

    # 2. Get all commits since the last tag (or all commits if no tags exist)
    if last_tag:
        log_cmd = ["git", "log", f"{last_tag}..HEAD", "--oneline"]
    else:
        log_cmd = ["git", "log", "--oneline"]
        
    log_proc = subprocess.run(
        log_cmd, 
        capture_output=True, text=True, encoding="utf-8" # <-- ADDED ENCODING
    )
    commits = log_proc.stdout.strip()
    
    if not commits:
        raise ValueError("No new commits found to release since the last tag.")

    # 3. Ask the AI to write the Release Notes
    release_notes = generate_release_notes(commits, version)

    # 4. Create the Git Tag using the AI's notes as the message
    tag_proc = subprocess.run(
        ["git", "tag", "-a", version, "-m", release_notes], 
        capture_output=True, text=True, encoding="utf-8" # <-- ADDED ENCODING
    )
    if tag_proc.returncode != 0:
        raise RuntimeError(f"Failed to create git tag: {tag_proc.stderr}")

    # 5. Push the new tag to GitHub
    subprocess.run(
        ["git", "push", "origin", version], 
        capture_output=True, text=True, encoding="utf-8" # <-- ADDED ENCODING
    )
    
    # 6. Log it to Sōzō
    project = detect_project()
    tags = ["git", "release"]
    if project:
        tags.append(project)
        
    add_event("programming", f"Released version {version}", tags=tags)
    
    return release_notes

# --------------------------------------------------
# TIMELINE
# --------------------------------------------------

def get_timeline(period="week", tag=None):
    now = datetime.now()
    start_date = (now - timedelta(days=30 if period == "month" else 7)).date().isoformat()
    grouped = defaultdict(list)
    
    # Pass the tag directly into the SQL fetcher!
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

    # NEW: Format tags for YAML array (e.g., ["python", "aiml"])
    yaml_tags = f"[{', '.join([f'\"{t}\"' for t in tags_list])}]" if tags_list else "[]"
    iso_date = datetime.now().strftime('%Y-%m-%d %H:%M')

    # NEW: Official YAML Frontmatter
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
    """Full-text deep search of all Markdown files in the vault."""
    if not VAULT_PATH.exists():
        return {}
        
    results = {}
    keyword = keyword.lower()
    
    for filepath in VAULT_PATH.rglob("*.md"):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
                if keyword in content.lower():
                    # Extract a snippet around the keyword
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
    #vault_path = Path.home() / ".sozo" / "vault"
    if not VAULT_PATH.exists():
        return {}

    graph = {}
    link_pattern = re.compile(r"\[\[(.*?)\]\]")

    # FIX: Changed from .glob to .rglob so it scans inside all subfolders!
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
    """Gathers all notes, events, and projects related to a concept."""
    # 1. Get all database matches
    events = search_events_in_db(keyword)
    
    # 2. Get all vault matches
    notes = search_vault(keyword)
    
    concept_data = {
        "projects": [],
        "events": [],
        "notes": list(notes.keys())
    }
    
    # 3. Sort the database events into Projects vs Normal Events
    for e in events:
        # e[2] is the category column
        if e[2].lower() == "project":
            concept_data["projects"].append(e)
        else:
            concept_data["events"].append(e)
            
    return concept_data

# --------------------------------------------------
# AUTO DOCUMENTATION (UNIVERSAL PROJECT SYNC)
# --------------------------------------------------

def sync_documentation():
    from sozo.core.ai import generate_updated_docs
    import time
    from pathlib import Path
    
    # 1. Use the Current Working Directory (Where you ran the command!)
    root_dir = Path.cwd()
    
    # 2. The Universal Skeleton Extractor
    # Scans Python, Java, and JS/TS files to map the project's capabilities!
    skeleton = []
    valid_extensions = [".py", ".java", ".js", ".ts"]
    
    for filepath in root_dir.rglob("*"):
        if filepath.suffix not in valid_extensions:
            continue
            
        # Skip virtual environments, node_modules, and hidden folders
        if any(part.startswith('.') or part in ["venv", "env", "__pycache__", "node_modules", "build", "target"] for part in filepath.parts):
            continue
            
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                lines = f.readlines()
                
            file_context = [f"\n--- File: {filepath.name} ---"]
            for line in lines:
                stripped = line.strip()
                # Capture functions, classes, and decorators/annotations across languages
                if stripped.startswith(("def ", "class ", "@", "public ", "private ", "function ", "export ")):
                    file_context.append(stripped)
                    
            if len(file_context) > 1: # Only add if we found actual code structures
                skeleton.extend(file_context)
        except Exception:
            continue
            
    if not skeleton:
        raise FileNotFoundError(f"Could not find any code files in {root_dir.name} to read context from.")
        
    project_context = "\n".join(skeleton)
    
    # --- NEW: Cap the skeleton size to prevent Error 400 ---
    if len(project_context) > 12000:
        project_context = project_context[:12000] + "\n... [TRUNCATED DUE TO SIZE]"
    # ------------------------------
    
    docs_to_sync = ["README.md"]
    updated_files = []
    
    # 3. Loop through docs in the CURRENT folder
    for doc_name in docs_to_sync:
        doc_path = root_dir / doc_name
        if not doc_path.exists():
            continue
            
        with open(doc_path, "r", encoding="utf-8") as f:
            current_content = f.read()
            
        # Call the AI safely
        try:
            new_content = generate_updated_docs(project_context, current_content, doc_name)
        except Exception as e:
            print(f"\n[yellow]Skipping {doc_name} due to API rate limits. ({e})[/yellow]")
            continue
            
        # Cleanup markdown formatting
        if new_content.startswith("```markdown"):
            new_content = new_content.replace("```markdown", "", 1)
        if new_content.startswith("```"):
            new_content = new_content.replace("```", "", 1)
        if new_content.endswith("```"):
            new_content = new_content[:-3]
            
        # Safely overwrite the file
        with open(doc_path, "w", encoding="utf-8") as f:
            f.write(new_content.strip() + "\n")
            
        updated_files.append(doc_name)
        
        print(f"[dim]Synced {doc_name}... waiting 20s for Groq API cooldown...[/dim]")
        time.sleep(20) 
        
    # 4. Log the action to Sōzō!
    if updated_files:
        files_str = ",".join(updated_files)
        insert_event(
            datetime.now().isoformat(),
            "programming",
            f"Auto-synced documentation for project: {root_dir.name}",
            datetime.now().isoformat(),
            0,
            "docs,ai,SOZO",
            files_str,
            None
        )
        
    return updated_files