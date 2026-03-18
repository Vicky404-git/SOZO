# 🌌 Sōzō — User Manual (Updated)

Welcome to **Sōzō** — a local-first CLI system that turns your life into a **timeline of events**.

---

# 🧠 Core Idea

Everything is an **Event**.

Sōzō records:

* what you did
* when it happened
* how it connects

This builds a **searchable life database**.

---

# ⚡ Command Center

### Dashboard

```
sozo dash
```

Shows:

* stats
* today's events
* timeline preview

---

### Timeline

```
sozo timeline
sozo timeline week
sozo timeline month --tag python
```

---

### Stats

```
sozo stats
```

---

# ✍️ Event System

### Add Event

```
sozo add CATEGORY "VALUE"
```

Options:

```
--at TIME
--remind
-t TAG
-f FILE
--relates-to ID
```

---

### Edit Event

```
sozo edit <id> -v "new value"
```

---

### Delete Event

```
sozo delete <id>
```

---

### Search Events

```
sozo search python
```

---

### Today

```
sozo today
```

---

# 🤖 AI Smart Logging

### Natural Language Logging

```
sozo log "studied transformers for 2 hours"
```

AI extracts:

* category
* action
* tags

---

# 🧠 Second Brain (Vault)

Stored at:

```
~/.sozo/vault/
```

---

### Create Note

```
sozo note "Title" -c category -t tag
```

---

### Read Note

```
sozo read keyword
```

---

### Rewrite Note

```
sozo rewrite keyword
```

---

### List Notes

```
sozo notes
```

---

### AI Ingest

```
sozo ingest file.txt "Title"
```

---

### Brain Search

```
sozo brain keyword
```

---

### Concept Engine

```
sozo concept python
```

---

### Knowledge Graph

```
sozo graph
sozo graph --export
```

---

# 🧬 Git + AI Workflows

### Auto Commit

```
sozo commit
```

* reads diff
* generates message
* commits
* logs event

---

### Manual Commit

```
sozo commit -m "message"
```

---

### Smart Push

```
sozo push
```

---

### Git Passthrough

```
sozo git status
```

---

### Release

```
sozo release v1.0.0
```

* generates release notes
* tags repo
* pushes
* logs event

---

### Undo Release

```
sozo unrelease v1.0.0
```

---

# 📁 File Tracking

### File History

```
sozo file services.py
```

---

# 📤 Export

```
sozo export -o timeline.md
sozo export --tag python
```

---

# ⚙️ System

### Manual

```
sozo --help
```

Displays this manual in terminal 

---

### Update Sōzō

```
sozo --update
```

* pulls latest code
* installs dependencies 

---

### Reminder Engine (Kosmo)

```
sozo kosmo
```

Runs background watcher for reminders 

---

### Docs Sync (AI)

```
sozo docs --sync
```

AI rewrites project documentation based on source code 

---

# 🧩 Architecture Overview

CLI → Commands → Services → Repos → SQLite 

---

# 🗄 Database

SQLite table: `events`

Stores:

* timestamp
* category
* value
* tags
* files
* relations 

---

# 🧠 Philosophy

Sōzō is not:

* a notes app
* a task manager

It is:

👉 **Git for your life timeline**

---

# 🔚

Use Sōzō daily.

Your future self will thank you.
