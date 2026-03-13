# Sōzō — Life as Events

> **A local-first, CLI-based personal event engine. Git for your life activities.**

![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green)
![CLI](https://img.shields.io/badge/interface-CLI-grey)
![AI Powered](https://img.shields.io/badge/AI-Groq%20-orange)
![Local First](https://img.shields.io/badge/data-local--first-brightgreen)

Track life as **events**, not notes. Sōzō records meaningful actions and builds a chronological timeline of what you actually did.

**Not a notes app. Not a task manager. Not a diary.**

Most productivity tools force people to write long notes, organize folders, or manage dashboards. But life doesn't work that way. People don't live in pages and tables. They do things.

Sōzō records **actions instead of documents**.

Think of it like **Git for your life timeline.**

---

# 🚀 The Core Idea

Everything in Sōzō is an **Event**.

Over time, these events weave together to form a complete timeline of your work, learning, and projects.

Example event:

```
Timestamp: 2026-03-05 09:02
Category: programming
Value: implemented the Bidirectional Linking Engine
Metadata: #python #sozo 🔗 linked to #14
```

Each event becomes part of your **life timeline database**.

---

# ⚡ Features

Sōzō has evolved from a simple logger into a **local-first AI knowledge system**.

### Natural Language Logging

Write normal sentences and let AI convert them into structured events.

```
sozo log "studied LangChain for 2 hours"
```

AI extracts:

* category
* action
* tags

---

### Concept Engine

Unify notes, events, and projects into a **single concept node**.

```
sozo concept python
```

Shows connections between:

* notes
* projects
* events

---

### Deep Brain Search

Search inside your **entire Markdown vault**.

```
sozo brain "architecture"
```

---

### Knowledge Vault

Create Markdown notes with automatic YAML frontmatter.

```
sozo note "Neural Networks Basics" -c study -t aiml
```

Compatible with:

* Obsidian
* Notion
* any Markdown system

---

### AI Auto-Ingestion

Convert messy raw text into structured Markdown.

```
sozo ingest lecture.txt "Transformers Notes" -c study -t ai
```

AI automatically formats the content.

---

### AI Git Workflows

Auto-generate commit messages from your Git diffs.

```
sozo commit
```

Then push:

```
sozo push
```

Sōzō logs the commit to your event timeline.

---

### Command Center Dashboard

Turn your terminal into a **personal activity dashboard**.

```
sozo dash
```

Shows:

* activity stats
* today's actions
* recent timeline

---

### Timeline View

See your activity history.

```
sozo timeline
```

Filter by tag:

```
sozo timeline week --tag python
```

---

### Knowledge Graph

Visualize note relationships.

```
sozo graph
```

Export as Mermaid graph:

```
sozo graph --export
```

---

### File History

View timeline events related to a file.

```
sozo file main.py
```

---

### Smart Git Command Wrapper

Run git commands through Sōzō and log them automatically.

```
sozo git status
sozo git pull
```

---

### Auto Documentation (AI)

Update project documentation automatically.

```
sozo docs --sync
```

AI scans the project code and rewrites docs.

---

# 📦 Event Commands

### Add Event

```
sozo add programming "built CLI tool"
```

Options:

```
--at        specify time
--remind    set reminder
--tag       add tags
--file      attach files
--relates-to link events
```

Example:

```
sozo add study "read AI paper" --tag ai --tag research
```

---

### Edit Event

```
sozo edit 12 --value "updated algorithm"
```

---

### Delete Event

```
sozo delete 12
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

### Today's Events

```
sozo today
```

---

### Search Events

```
sozo search "python"
```

---

### Activity Stats

```
sozo stats
```

---

### Export Timeline

```
sozo export
```

Filter by tag:

```
sozo export --tag ai
```

---

# ⏰ Reminder Engine (Kosmo)

Run the reminder daemon:

```
sozo kosmo
```

Kosmo watches your timeline and triggers reminders when events are due.

---

# 🔄 Self Updating

Update Sōzō from GitHub:

```
sozo --update
```

This will:

* pull latest code
* install new dependencies

---

# 📖 Manual

Open the full manual:

```
sozo manual
```

Or:

```
sozo --help
```

---

# 🛠 Installation

### Clone repository

```
git clone https://github.com/Vicky404-git/SOZO.git
cd SOZO
```

---

### Create virtual environment

```
python -m venv sozoenv
```

Activate:

Windows

```
sozoenv\Scripts\activate
```

Linux / Mac

```
source sozoenv/bin/activate
```

---

### Install dependencies

```
pip install -r requirements.txt
```

Install project:

```
pip install -e .
```

---

### Setup AI features

Create `.env` in project root:

```
GROQ_API_KEY=your_key_here
```

Required for:

* `sozo log`
* `sozo commit`
* `sozo ingest`
* `sozo docs`

---

# 🏗 Architecture

Sōzō follows a layered architecture.

    ┌─────────────┐
    │   CLI App   │
    │   (Typer)   │
    └──────┬──────┘
           │
    ┌──────▼──────┐
    │   Commands   │
    │  CLI Logic   │
    └──────┬──────┘
           │
    ┌──────▼──────┐
    │   Services   │
    │ Business API │
    └──────┬──────┘
           │
    ┌──────▼──────┐
    │ Repository   │
    │ DB Queries   │
    └──────┬──────┘
           │
    ┌──────▼──────┐
    │   SQLite DB  │
    └─────────────┘


---

# 🗄 Database Architecture

SQLite table: **events**

| Column     | Type                |
| ---------- | ------------------- |
| id         | INTEGER PRIMARY KEY |
| timestamp  | TEXT                |
| category   | TEXT                |
| value      | TEXT                |
| created_at | TEXT                |
| remind     | INTEGER             |
| reminded   | INTEGER             |
| tags       | TEXT                |
| files      | TEXT                |
| relates_to | INTEGER             |

---

# 🗺 Roadmap

### DaemonV Integration

Turn the reminder engine into a background OS service.

---

### AI Semantic Search

Upgrade keyword search to vector embeddings using FAISS.

---

### Life Knowledge Graph

Expand the graph system to map relationships between:

```
Events → Projects → Concepts
```

---

# 👤 Author

**Vicky404**

GitHub:
https://github.com/Vicky404-git
