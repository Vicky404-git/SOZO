import os
import re
import subprocess
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict

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

        truncated_diff = diff[:30000] if len(diff) > 30000 else diff
        commit_msg = generate_commit_message(truncated_diff)

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


# --------------------------------------------------
# TIMELINE
# --------------------------------------------------

def get_timeline(period="week"):

    now = datetime.now()

    if period == "month":
        start_date = (now - timedelta(days=30)).date().isoformat()
    else:
        start_date = (now - timedelta(days=7)).date().isoformat()

    end_date = now.date().isoformat()

    events = fetch_events_in_range(start_date, end_date)

    grouped = defaultdict(list)

    for event in events:

        date_part = event[1].split("T")[0]
        grouped[date_part].append(event)

    return grouped


# --------------------------------------------------
# VAULT HELPERS (DRY)
# --------------------------------------------------

def _save_to_vault(title, category, tags, content, action_desc):

    vault_path = Path.home() / ".sozo" / "vault"
    vault_path.mkdir(parents=True, exist_ok=True)

    safe_title = re.sub(r"[^a-zA-Z0-9]+", "-", title.lower()).strip("-")

    date_prefix = datetime.now().strftime("%Y%m%d")

    filename = f"{date_prefix}-{safe_title}.md"
    filepath = vault_path / filename

    tags_list = list(tags) if tags else []

    project = detect_project()

    if project and project not in tags_list:
        tags_list.append(project)

    tags_str = ", ".join([f"#{t}" for t in tags_list]) if tags_list else ""

    with open(filepath, "w", encoding="utf-8") as f:

        f.write(f"# {title}\n\n")
        f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")

        if tags_str:
            f.write(f"**Tags:** {tags_str}\n")

        f.write("\n---\n\n")

        if content:
            f.write(content)

    insert_event(
        datetime.now().isoformat(),
        category,
        f"{action_desc}: {title}",
        datetime.now().isoformat(),
        0,
        ",".join(tags_list),
        f"vault/{filename}",
        None,
    )

    return filepath, tags_list


# --------------------------------------------------
# NOTE CREATION
# --------------------------------------------------

def create_note(title: str, category: str, tags: list[str] = None):
    return _save_to_vault(title, category, tags, "", "Created note")


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

    vault_path = Path.home() / ".sozo" / "vault"

    if not vault_path.exists():
        return {}

    graph = {}

    link_pattern = re.compile(r"\[\[(.*?)\]\]")

    for filepath in vault_path.glob("*.md"):

        try:

            with open(filepath, "r", encoding="utf-8") as f:

                content = f.read()
                links = link_pattern.findall(content)

                graph[filepath.stem] = links

        except Exception:
            continue

    return graph