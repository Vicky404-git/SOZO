import subprocess
import time
from pathlib import Path
from datetime import datetime

from sozo.core.repos import search_events_in_db, delete_event, insert_event
from sozo.core.services import detect_project, add_event
from sozo.core.ai import (
    generate_commit_message,
    generate_release_notes,
    generate_updated_docs
)

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
    diff, files = get_git_diff()

    if not files:
        raise ValueError("No changes found to commit.")

    if custom_msg:
        commit_msg = custom_msg
    else:
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
    try:
        last_tag_proc = subprocess.run(
            ["git", "describe", "--tags", "--abbrev=0"], 
            capture_output=True, text=True, encoding="utf-8"
        )
        last_tag = last_tag_proc.stdout.strip()
    except Exception:
        last_tag = ""

    if last_tag:
        log_cmd = ["git", "log", f"{last_tag}..HEAD", "--oneline"]
    else:
        log_cmd = ["git", "log", "--oneline"]
        
    log_proc = subprocess.run(
        log_cmd, 
        capture_output=True, text=True, encoding="utf-8"
    )
    commits = log_proc.stdout.strip()
    
    if not commits:
        raise ValueError("No new commits found to release since the last tag.")

    release_notes = generate_release_notes(commits, version)

    tag_proc = subprocess.run(
        ["git", "tag", "-a", version, "-m", release_notes], 
        capture_output=True, text=True, encoding="utf-8"
    )
    if tag_proc.returncode != 0:
        raise RuntimeError(f"Failed to create git tag: {tag_proc.stderr}")

    subprocess.run(
        ["git", "push", "origin", version], 
        capture_output=True, text=True, encoding="utf-8"
    )
    
    project = detect_project()
    tags = ["git", "release"]
    if project:
        tags.append(project)
        
    add_event("programming", f"Released version {version}", tags=tags)
    
    return release_notes


def undo_release(version: str):
    local_proc = subprocess.run(["git", "tag", "-d", version], capture_output=True, text=True, encoding="utf-8")
    remote_proc = subprocess.run(["git", "push", "--delete", "origin", version], capture_output=True, text=True, encoding="utf-8")
    
    events = search_events_in_db(f"Released version {version}")
    for event in events:
        if event[5] and "release" in event[5]:
            delete_event(event[0])
            
    return local_proc.returncode == 0 or remote_proc.returncode == 0


# --------------------------------------------------
# AUTO DOCUMENTATION
# --------------------------------------------------

def sync_documentation():
    root_dir = Path.cwd()
    skeleton = []
    valid_extensions = [".py", ".java", ".js", ".ts"]
    
    valid_files = []
    for filepath in root_dir.rglob("*"):
        if filepath.suffix not in valid_extensions:
            continue
        if any(part.startswith('.') or part in ["venv", "env", "__pycache__", "node_modules", "build", "target"] for part in filepath.parts):
            continue
        valid_files.append(filepath)
        
    valid_files.sort(key=lambda p: 0 if p.stem.lower() in ["commands", "cli", "app", "main"] else 1)
    
    for filepath in valid_files:
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                lines = f.readlines()
                
            file_context = [f"\n--- File: {filepath.name} ---"]
            for line in lines:
                stripped = line.strip()
                if stripped.startswith(("def ", "class ", "@", "public ", "private ", "function ", "export ")):
                    file_context.append(stripped)
                    
            if len(file_context) > 1:
                skeleton.extend(file_context)
        except Exception:
            continue
            
    if not skeleton:
        raise FileNotFoundError(f"Could not find any code files in {root_dir.name} to read context from.")
        
    project_context = "\n".join(skeleton)
    
    if len(project_context) > 12000:
        project_context = project_context[:12000] + "\n... [TRUNCATED DUE TO SIZE]"
    
    docs_to_sync = ["README.md"]
    updated_files = []
    
    for doc_name in docs_to_sync:
        doc_path = root_dir / doc_name
        if not doc_path.exists():
            continue
            
        with open(doc_path, "r", encoding="utf-8") as f:
            current_content = f.read()
            
        try:
            new_content = generate_updated_docs(project_context, current_content, doc_name)
        except Exception as e:
            print(f"\n[yellow]Skipping {doc_name} due to API rate limits. ({e})[/yellow]")
            continue
            
        if new_content.startswith("```markdown"):
            new_content = new_content.replace("```markdown", "", 1)
        if new_content.startswith("```"):
            new_content = new_content.replace("```", "", 1)
        if new_content.endswith("```"):
            new_content = new_content[:-3]
            
        with open(doc_path, "w", encoding="utf-8") as f:
            f.write(new_content.strip() + "\n")
            
        updated_files.append(doc_name)
        print(f"[dim]Synced {doc_name}... waiting 20s for Groq API cooldown...[/dim]")
        time.sleep(20) 
        
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