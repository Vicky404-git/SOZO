# 🌌 Sōzō in Action: A Day in the Life

Not sure how to actually use Sōzō?

You don't need to be a programmer. Whether you're a student, developer, or researcher, Sōzō records actions so you never lose context.

Here's how a typical day might look using Sōzō.

---

# 🌅 Morning — Quick Logging

Start your day by logging activities naturally.

### Smart Log a habit

```bash
sozo log "went for a 3 mile run and stretched"
```

Sōzō uses AI to automatically extract:

* category
* action
* tags

---

### Set a reminder

```bash
sozo add work "email professor about project" --at "3pm" --remind
```

---

### Start the reminder watcher

```bash
sozo kosmo
```

Kosmo runs in the background and alerts you when reminders are due.

---

# 🧠 Afternoon — Your Second Brain

### Create a quick note

```bash
sozo note "Faceless Channel Ideas" -c brainstorm -t youtube
```

This creates a Markdown file in your vault with YAML metadata.

---

### AI Note Ingestion

```bash
sozo ingest messy_notes.txt "DSA Concepts" -c study -t python
```

AI formats messy notes into structured Markdown.

---

### Search your vault

```bash
sozo brain "binary tree"
```

Searches inside your Markdown notes.

---

### View a Concept Node

```bash
sozo concept python
```

Shows:

* related notes
* related events
* related projects

---

### Check file history

```bash
sozo file services.py
```

Shows all events related to that file.

---

# 💻 Evening — Developer Workflow

### AI Auto Commit

```bash
sozo commit
```

Sōzō:

* reads git diff
* generates commit message
* commits changes
* logs event

---

### Push changes

```bash
sozo push
```

---

# 🌙 Night — Review Your Day

### Open dashboard

```bash
sozo dash
```

Displays:

* activity stats
* today's actions
* timeline preview

---

### View weekly timeline

```bash
sozo timeline week
```

---

### Fix a mistake

```bash
sozo edit 14 -v "updated description"
```

---

### Export timeline

```bash
sozo export -o timeline.md
```

---

### Visualize knowledge graph

```bash
sozo graph --export
```

---

# 📊 Useful Commands

| Command             | Purpose                    |
| ------------------- | -------------------------- |
| `sozo stats`        | show activity statistics   |
| `sozo today`        | show today's events        |
| `sozo list`         | list all events            |
| `sozo search QUERY` | search event database      |
| `sozo delete ID`    | delete event               |
| `sozo docs --sync`  | auto update docs using AI  |
| `sozo git status`   | run git command and log it |

---

Sōzō quietly builds a **chronological map of your life** while you work.
