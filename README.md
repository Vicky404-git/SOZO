# Sōzō — Thought → Structure

> A local-first CLI system for turning **raw thoughts into structured reality**.

![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green)
![CLI](https://img.shields.io/badge/interface-CLI-grey)
![AI Powered](https://img.shields.io/badge/AI-Groq-orange)
![Local First](https://img.shields.io/badge/data-local--first-brightgreen)

---

## 🌘 What is Sōzō?

Sōzō (創造) means **creation**.

This is not a note-taking app.
Not a task manager.
Not a productivity dashboard.

Most tools store information.

**Sōzō transforms thinking.**

---

## 🧠 Core Philosophy

> Thoughts are chaotic.
> Clarity must be forced.

Sōzō treats life as **events + ideas + structure**.

Instead of writing long notes, you:

* log actions
* capture intent
* build structured knowledge over time

Think of it as:

> **Git for your life + an idea refinery engine**

---

## ⚡ Core Concepts

### 1. Events (Reality Layer)

Everything you do becomes an **event**.

```
sozo add programming "built CLI engine"
```

Over time, this creates a **timeline of actual work** — not plans.

---

### 2. Vault (Thought Layer)

Write distraction-free notes:

```
sozo note "Idea: AI Council"
```

Stored as clean Markdown with metadata.
Works seamlessly with tools like Obsidian.

---

### 3. Concept Engine (Connection Layer)

```
sozo concept ai
```

Unifies:

* events
* notes
* projects

Into a single **concept node**.

---

### 4. AI Layer (Optional)

Sōzō can:

* structure messy text
* generate commit messages
* convert thoughts → markdown
* parse natural language logs

But AI is **assistive, not central**.

---

## 🚀 Features

### 🧾 Event Logging

Track real actions instead of intentions.

```
sozo add study "read AI paper" --tag ai
```

---

### 🧠 Natural Language Logging

```
sozo log "studied transformers for 2 hours"
```

AI extracts:

* category
* structured action
* tags

---

### 📚 Knowledge Vault

```
sozo note "Neural Networks" -c study -t ai
```

* Markdown storage
* YAML metadata
* Obsidian-compatible

---

### 🔍 Deep Search

```
sozo brain "architecture"
```

Search across your entire vault.

---

### 🌌 Knowledge Graph

```
sozo graph
```

Visualize connections between notes.

Export:

```
sozo graph --export
```

---

### 📊 Command Center

```
sozo dash
```

Terminal dashboard showing:

* stats
* today’s actions
* recent timeline

---

### 📅 Timeline System

```
sozo timeline
```

Filter:

```
sozo timeline week --tag python
```

---

### 🧬 Concept Engine

```
sozo concept startup
```

Builds a unified view of:

* notes
* events
* projects

---

### 🤖 AI Tools

#### Smart Commit

```
sozo commit
```

#### Auto Docs

```
sozo docs --sync
```

#### AI Ingestion

```
sozo ingest notes.txt "Lecture"
```

---

### 🔧 Dev Integration

* Git wrapper (`sozo git`)
* Release system (`sozo release`)
* Auto logging of dev actions

---

### ⏰ Kosmo (Daemon Engine)

```
sozo kosmo
```

Background reminder system.

---

## 🧠 The Hidden Layer (Your Direction)

Sōzō is evolving into:

> A system that converts **ideas → structured blueprints**

Future direction includes:

* idea refinement engine
* thought auditing
* idea evolution tracking
* pattern detection

This is not just logging anymore.

---

## 🛠 Installation

```bash
git clone https://github.com/Vicky404-git/SOZO.git
cd SOZO

python -m venv sozoenv
source sozoenv/bin/activate   # or Windows equivalent

pip install -r requirements.txt
pip install -e .
```

---

## 🔑 AI Setup

Create `.env`:

```
GROQ_API_KEY=your_key_here
```

Used for:

* log
* commit
* ingest
* docs

---

## 🏗 Architecture

```
CLI (Typer)
   ↓
Commands
   ↓
Services
   ↓
Repository
   ↓
SQLite
```

Local-first. No cloud dependency.

---

## 🗄 Database

Single table: `events`

Tracks:

* time
* category
* value
* tags
* file links
* relations

---

## 🗺 Roadmap

* Idea Refinery Engine (Sōzō Core)
* Cycle Intelligence (Sōsei) (Probably/ or another repo )
* Semantic Search (FAISS)
* Full Knowledge Graph
* VS Code integration (probably)

---

## 👤 Author

**Vicky404**

GitHub:
https://github.com/Vicky404-git

---

## 🌒 Final Note

Sōzō is not about productivity.

It’s about:

> Understanding what you actually do,
> and turning thought into something real.

