# 🌌 Sōzō in Action — Real Workflow Example (Updated)

This is how you actually use Sōzō in daily life.

---

# 🌅 Morning — Start Fast

### Log your activity (natural language)

```
sozo log "went for a 3km run and stretched"
```

AI automatically extracts:

* category → health
* value → ran and stretched
* tags → fitness

---

### Add a reminder

```
sozo add work "email professor about thesis" --at "3pm" --remind
```

---

### Start reminder engine

```
sozo kosmo
```

This runs in the background and alerts you when events are due.

---

# 🧠 Afternoon — Build Your Second Brain

### Create a note

```
sozo note "Startup Ideas" -c ideas -t business
```

Opens your editor → write → save → auto-stored in vault.

---

### Ingest messy notes using AI

```
sozo ingest raw.txt "Clean Notes" -c study -t ai
```

AI converts raw text → structured Markdown.

---

### Search your brain

```
sozo brain "vector database"
```

Searches inside all Markdown files.

---

### Explore a concept

```
sozo concept python
```

Shows:

* related notes
* related events
* related projects

---

### View file history

```
sozo file services.py
```

---

# 💻 Evening — Developer Mode

### Auto commit with AI

```
sozo commit
```

Sōzō:

* reads git diff
* generates commit message
* commits
* logs event

---

### Push changes

```
sozo push
```

---

### Run git commands (tracked)

```
sozo git status
sozo git pull
```

All actions are logged automatically.

---

# 🚀 Release Workflow

### Create release

```
sozo release v1.0.0
```

Sōzō:

* scans commits
* generates release notes (AI)
* creates git tag
* pushes to GitHub
* logs event

---

### Undo release

```
sozo unrelease v1.0.0
```

---

# 🌙 Night — Reflect & Review

### Open dashboard

```
sozo dash
```

Shows:

* stats
* today's actions
* timeline preview

---

### View timeline

```
sozo timeline week
```

---

### Fix a mistake

```
sozo edit 14 -v "updated description"
```

---

### Delete wrong entry

```
sozo delete 14
```

---

### Export your timeline

```
sozo export -o timeline.md
```

---

### Visualize knowledge graph

```
sozo graph --export
```

Open in:

* GitHub
* Obsidian
* VS Code

---

# ⚡ Power Moves

### Multi-log in one command

```
sozo log "fixed API bug" "optimized query" "pushed update"
```

---

### Link events together

```
sozo add programming "refactored services layer" --relates-to 21
```

---

### Tag-based timeline

```
sozo timeline week --tag ai
```

---

### Search everything

```
sozo search python
```

---

# 🧠 Mental Model

You are not writing notes.

You are **recording actions**.

Over time:

* events → timeline
* timeline → patterns
* patterns → insight

---

# 🔥 End Result

Sōzō becomes:

* your memory
* your progress tracker
* your developer log
* your second brain

---

# 🧩 Final Thought

Use Sōzō like Git:

You don’t log everything.

You log **meaningful actions**.

---

👉 Build your timeline. One event at a time.
