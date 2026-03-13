# 🌌 Sōzō (創造) — User Manual

Welcome to **Sōzō**.

Sōzō is a **local-first personal event engine**. It bridges the gap between a daily activity logger, an Obsidian-style knowledge vault, and a terminal command center.

Everything you do becomes part of a **chronological timeline of events**.

---

# Core Philosophy

Everything you do is an **Event**.

Sōzō doesn't just store files. It records:

* **when** something happened
* **what** you did
* **how it connects** to other work

Over time, these events form a complete **life timeline database**.

---

# 1. The Command Center

Turn your terminal into a **personal activity dashboard**.

### Open Dashboard

```
sozo dash
```

Displays:

* Activity statistics
* Today's events
* Recent timeline preview

---

### View Timeline

```
sozo timeline
```

Or filter by time:

```
sozo timeline week
sozo timeline month
```

Filter by tag:

```
sozo timeline week --tag python
```

This displays events grouped by day in chronological order.

---

### Edit an Event

```
sozo edit <ID> [-c CATEGORY] [-v VALUE] [-t TAG] [-f FILE]
```

Example:

```
sozo edit 14 -v "updated project description"
```

Allows you to modify past events.

---

### Delete an Event

```
sozo delete <ID>
```

Removes the event permanently from the database.

---

# 2. Smart Logging (Natural Language)

You don't need to manually define categories or tags.

### AI Smart Log

```
sozo log "studied LangChain vector stores for 2 hours"
```

Sōzō uses AI to:

* detect category
* format the action
* generate relevant tags

---

### Multi-Sentence Logging

```
sozo log "implemented graph engine" "fixed CLI bugs"
```

Multiple actions can be logged at once.

---

# 3. The Second Brain

Sōzō includes a hidden Markdown vault:

```
~/.sozo/vault/
```

All notes contain **YAML frontmatter** and are compatible with tools like:

* Obsidian
* Notion
* Markdown editors

---

### Concept Engine

```
sozo concept python
```

Displays a hierarchical node connecting:

* notes
* projects
* timeline events

---

### Deep Brain Search

```
sozo brain "architecture"
```

Performs a **full-text search inside vault notes**.

---

### Create a Note

```
sozo note "Deep Learning Lecture" -c study -t ai
```

Creates a Markdown note and opens it in your editor.

---

### AI Note Ingestion

```
sozo ingest messy_notes.txt "Clean AI Notes" -c study -t ai
```

Sōzō uses AI to convert messy text into structured Markdown.

---

### Knowledge Graph

```
sozo graph
```

Scans notes for `[[wikilinks]]` and displays relationships.

Export a graph:

```
sozo graph --export
```

This generates a **Mermaid network diagram**.

---

# 4. Git & AI Workflows

Sōzō integrates directly with Git repositories.

If run inside a repo, events are automatically tagged with the **project name**.

---

### AI Auto Commit

```
sozo commit
```

Sōzō:

1. reads your staged `git diff`
2. generates a commit message with AI
3. commits the changes
4. logs the commit to your timeline

---

### Manual Commit Message

```
sozo commit -m "fix login API bug"
```

---

### Smart Push

```
sozo push
```

Sōzō detects your current branch and pushes to the remote repository.

---

### Git Passthrough

```
sozo git status
sozo git pull
sozo git checkout dev
```

Runs git commands while logging activity.

---

# 5. Manual Event Tracking

When you want full control over event creation.

### Add Event

```
sozo add CATEGORY "VALUE" [--at TIME] [--remind] [-t TAG] [-f FILE] [--relates-to EVENT_ID]
```

Example:

```
sozo add study "read transformer paper" --tag ai
```

Options:

| Option                  | Description           |
| ----------------------- | --------------------- |
| `--at TIME`             | schedule event time   |
| `--remind`              | enable reminder       |
| `-t TAG`                | attach tags           |
| `-f FILE`               | attach related files  |
| `--relates-to EVENT_ID` | link to another event |

---

### File History

```
sozo file services.py
```

Displays all timeline events associated with that file.

---

# 6. Finding & Managing Data

### Today's Events

```
sozo today
```

---

### List Events

```
sozo list
```

Filter by date:

```
sozo list 2026-03-10
```

---

### Search Database

```
sozo search python
```

Searches inside the **event database**.

Use `sozo brain` to search inside vault files.

---

### Activity Statistics

```
sozo stats
```

Shows event counts by category.

---

### Export Timeline

```
sozo export -o timeline.md
```

Export events to a Markdown file.

Filter by tag:

```
sozo export --tag python
```

---

# 7. System & Maintenance

### Self Update

```
sozo --update
```

Updates Sōzō from GitHub and installs new dependencies.

---

### Reminder Engine (Kosmo)

```
sozo kosmo
```

Runs a background watcher for scheduled events.

Example reminder event:

```
sozo add work "email professor" --at "3pm" --remind
```

---

### Manual

```
sozo manual
```

Opens the **MANUAL.md** file in your editor.

---

### Documentation Sync (AI)

```
sozo docs --sync
```

Automatically updates project documentation.

---

# 8. Additional Useful Commands

| Command         | Purpose                              |
| --------------- | ------------------------------------ |
| `sozo dash`     | open dashboard                       |
| `sozo timeline` | view activity timeline               |
| `sozo note`     | create markdown note                 |
| `sozo ingest`   | convert raw text to structured notes |
| `sozo graph`    | visualize knowledge graph            |
| `sozo commit`   | AI-generated commit                  |
| `sozo push`     | push git branch                      |
| `sozo git`      | run git commands                     |
| `sozo stats`    | show usage statistics                |

---

# Final Thought

Sōzō quietly builds a **structured memory of your work and life**.

Instead of writing long notes, you simply **do things** — and Sōzō records them as events.
