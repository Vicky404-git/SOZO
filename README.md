# 🌌 Sōzō — Thought → Structure

> A local-first CLI system for turning raw thoughts, actions, and ideas into structured knowledge.

![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green)
![CLI](https://img.shields.io/badge/interface-CLI-grey)
![AI Powered](https://img.shields.io/badge/AI-Groq-orange)
![Local First](https://img.shields.io/badge/data-local--first-brightgreen)

---

# 🧠 What is Sōzō?

Sōzō (創造) means:

> creation  
> imagination  
> bringing ideas into reality

Sōzō is not:
- a productivity app
- a task manager
- a notes app
- a self-improvement tracker

Most software stores information.

Sōzō structures thought.

---

# 🌘 Core Philosophy

> Thoughts are chaotic.  
> Clarity must be created.

Sōzō helps you:
- capture meaningful actions
- preserve important thoughts
- connect ideas together
- build a searchable memory system

Instead of managing pages and folders,
you build a living timeline of:
- work
- learning
- ideas
- projects
- reflections

Think of it like:

> Git for your thinking.

---

# ⚡ Core Systems

## 🧾 Event System

Everything becomes an event.

```
sozo add programming "built markdown parser"
```


Over time:

```text
events → timeline → patterns → insight
```

---

## 🧠 Vault System

Create distraction-free notes directly from terminal.

```
sozo note "AI Council Idea"
```

Notes are:

* stored locally
* markdown-based
* YAML powered
* Obsidian compatible

---

## 🌌 Concept Engine

```
sozo concept ai
```

Unifies:

* notes
* events
* related ideas

Into a single concept node.

---

## 🔍 Brain Search

```
sozo brain "vector database"
```

Search your entire vault instantly.

---

## 🌐 Knowledge Graph

```
sozo graph
```


Visualize relationships between thoughts.

Export Mermaid graph:

```
sozo graph --export
```

---

## 🤖 AI Assistance

AI in Sōzō is assistive — not central.

It helps:

* structure raw notes
* parse natural language
* clean messy thoughts
* transform text into readable markdown

---

# 🚀 Features

## Smart Logging

```
sozo log "studied transformers for 2 hours"
```

AI extracts:

* category
* action
* tags

---

## Timeline View

```
sozo timeline
sozo timeline week
```

Filter:

```
sozo timeline month --tag ai
```

---

## Dashboard

```
sozo dash
```

Shows:

* activity stats
* today's actions
* timeline preview

---

## Notes

### Create

```
sozo note "Startup Ideas"
```

### Read

```
sozo read startup
```

### Rewrite

```
sozo rewrite startup
```

### List Notes

```
sozo notes
```

---

## AI Ingestion

Convert raw text into structured markdown.

```
sozo ingest raw.txt "Clean Notes"
```

---

## File History

```bash
sozo file services.py
```

---

## Export Timeline

```
sozo export -o timeline.md
```

---

## Reminder Engine — Kosmo

```
sozo kosmo
```

Background event reminder system.

---

# 🧩 Example Workflow

Morning:

```
sozo log "went for a run"
```

Afternoon:

```
sozo note "Research Ideas"
```

Night:

```
sozo timeline week
```

Over time,
Sōzō becomes:

* your memory
* your second brain
* your idea archive
* your reflection system

---

# 🛠 Installation

## Clone Repository

```
git clone https://github.com/Vicky404-git/SOZO.git
cd SOZO
```

---

## Create Virtual Environment

```
python -m venv sozoenv
```

Linux/macOS:

```
source sozoenv/bin/activate
```

Windows:

```
sozoenv\Scripts\activate
```

---

## Install Dependencies

```
pip install -r requirements.txt
pip install -e .
```

---

# 🔑 AI Setup

Create `.env` in root directory:

```env
GROQ_API_KEY=your_api_key
```

Required for:

* `sozo log`
* `sozo ingest`

---

# 🏗 Architecture

```text
CLI
 ↓
Commands
 ↓
Services
 ↓
Repository Layer
 ↓
SQLite Database
```

Local-first by design.

No cloud dependency.

Your data stays yours.

---

# 🗄 Database

SQLite table: `events`

Tracks:

* timestamps
* categories
* tags
* linked files
* relations

---

# 🗺 Roadmap

## Sōzō v2

Planned systems:

* Idea Refinery Engine
* Thought Structuring AI
* Semantic Search
* Pattern Detection
* Idea Evolution Tracking
* Reflection Layer

---

# 🌒 Ecosystem

Sōzō is focused on:

> thought + structure + memory

Developer tooling is being moved into a separate experimental project:

---

# 👤 Author

**Vicky404**

GitHub:
[https://github.com/Vicky404-git](https://github.com/Vicky404-git)

---

# 🌌 Final Thought

You do not need to remember everything.

You only need a system
that helps you reconnect the dots later.

Sōzō exists for that.

```
```

