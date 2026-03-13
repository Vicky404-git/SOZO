# Sōzō — Life as Events

> **A local-first, CLI-based personal event engine. Git for your life activities.**

Track life as events, not notes. Sōzō is a system that records meaningful actions and builds a chronological timeline of what you actually did. 

**Not a notes app. Not a task manager. Not a diary.**

Most productivity tools force people to write long notes, organize folders, or manage dashboards. But life doesn't work that way. People don't live in pages and tables. They do things. Sōzō records actions instead of documents. Think of it like **Git for your life timeline**.

---

## 🚀 The Core Idea
Everything in Sōzō is an **Event**. Over time, these events weave together to form a complete timeline of your work, learning, and projects.

* **Timestamp:** `2026-03-05 09:02`
* **Category:** `programming`
* **Value:** `implemented the Bidirectional Linking Engine`
* **Metadata:** `#python`, `#sozo`, `🔗 Linked to #14`

---

## ⚡ Features (The Second Brain & Autonomy Upgrades)

Sōzō has evolved from a simple logger into a deeply interconnected, AI-powered knowledge system:

* **Natural Language Logging:** Type normal sentences like `sozo log "studied LangChain for 2 hours"` and let the Llama-3 AI automatically extract the category, action, and tags.
* **The Concept Engine:** Run `sozo concept <keyword>` to instantly unify your disconnected notes, Git commits, and timeline events into a single, hierarchical Obsidian-style Concept Node.
* **Deep Brain Search:** Run `sozo brain <keyword>` to perform full-text regex scanning across your entire hidden Markdown vault.
* **The Knowledge Vault:** Use `sozo note` to automatically generate, format, and track Markdown files. Sōzō injects official YAML frontmatter so your notes are compatible with Obsidian and Notion.
* **AI Auto-Ingestion:** Dump raw, messy `.txt` thoughts into `sozo ingest`, and the Groq AI will instantly format it into clean Markdown and save it to your vault.
* **AI Git Workflows:** Run `sozo commit` to have Llama 3 read your staged code, write a conventional commit message, and log the changes. Then run `sozo push` for smart branch detection and automated remote syncing.
* **The Command Center:** Run `sozo dash` to turn your terminal into a Notion-style split-screen dashboard showing stats, today's actions, and your timeline feed.
* **Self-Updating:** Run `sozo --update` to automatically pull the latest codebase from GitHub and sync dependencies without needing to reinstall.
* **Timeline:** Run `sozo timeline` to view your events organized by week, month, or year. Use `--tag` to filter by specific tags.
* **Graph:** Run `sozo graph` to visualize your knowledge graph as a Mermaid.js network diagram. Use `--export` to save the graph as a 2D image.
* **File History:** Run `sozo file <name>` to view a list of events related to a specific file.
* **Smart Log (AI):** Run `sozo log` to log actions using natural language and AI.
* **Auto Docs:** Run `sozo docs` to auto-update your Markdown documentation files using AI.
* **Add Event:** Run `sozo add` to create a new event with customizable metadata, tags, and files. Use `--at` to specify a specific date and time, `--remind` to set a reminder, and `--tag` to assign tags.
* **Edit Event:** Run `sozo edit` to modify an existing event. Use `--category` to change the category, `--value` to update the value, and `--tag` to add or remove tags.
* **Delete Event:** Run `sozo delete` to remove an event by its ID.
* **Export Events:** Run `sozo export` to export events to a Markdown file. Use `--tag` to filter by specific tags and `--out` to specify the output file.
* **List Events:** Run `sozo list` to view a list of events. Use `--date` to filter by date.
* **Today's Events:** Run `sozo today` to view a list of events for the current day.
* **Search Events:** Run `sozo search` to search for events by keyword.
* **Stats:** Run `sozo stats` to view statistics about your events.
* **Kosmo Reminder Engine:** Run `sozo kosmo` to manage reminders and notifications.
* **Manual:** Run `sozo manual` to view the manual for Sōzō.
* **Commit:** Run `sozo commit` to commit changes to your Git repository. Use `--msg` to specify a custom commit message.
* **Push:** Run `sozo push` to push changes to your remote Git repository.
* **Git:** Run `sozo git` to manage your Git repository.
* **Note:** Run `sozo note` to create a new note with customizable metadata and tags.
* **Ingest:** Run `sozo ingest` to import raw text into your vault. Use `--title` to specify the title, `--category` to specify the category, and `--tag` to assign tags.

---

## 🛠️ Installation

### Clone the repository:
```bash
git clone [https://github.com/Vicky404-git/SOZO.git](https://github.com/Vicky404-git/SOZO.git)
cd SOZO
```
### Create and activate a virtual environment (Windows):

```Bash
python -m venv sozoenv
sozoenv\Scripts\activate
```
### Install the project (Editable Mode):

```Bash
pip install -e .
```
**Note for AI Features: Create a .env file in the root of the SOZO folder with GROQ_API_KEY=your_key_here to enable sozo log, sozo commit, and sozo ingest.**

## 📖 Quick Start & Example Workflow
### Open the Terminal Dashboard:

```Bash
sozo dash
```
### Log an action using natural language AI:

```Bash
sozo log "studied LangChain for 2 hours"
```
### Auto-format study notes with AI:

```Bash
sozo ingest raw_lecture.txt "Neural Networks Ch 1" -c study -t aiml
```
### View a unified Concept Node (Notes + Events + Projects):

```Bash
sozo concept python
```
### Search deep inside your vault notes:

```Bash
sozo brain "architecture"
```
### Auto-commit your code and push it:

``` Bash
sozo commit
sozo push
```
### Update Sōzō to the latest version:

``` Bash
sozo --update
```
**(For the complete guide, type sozo --help or sozo manual in your terminal).**

## 🗄️ Database Architecture
Sōzō uses a local, private SQLite database. No servers, no accounts.

**Table**: events

- id (INTEGER PRIMARY KEY)
- timestamp (TEXT)
- category (TEXT)
- value (TEXT)
- created_at (TEXT)
- remind (INTEGER)
- reminded (INTEGER)
- tags (TEXT)
- files (TEXT)
- relates_to (INTEGER)

## 🗺️ Roadmap
- **DaemonV Integration**: Moving the kosmo reminder engine into a silent, native Windows background service so it doesn't require an open terminal tab.

- **AI Semantic Search (Vector Space)**: Upgrading sozo brain from keyword search to local LangChain/FAISS vector embeddings so searching for "exhausted" finds logs about "pulling an all-nighter."

- **True Life Knowledge Graph**: Expanding the Mermaid.js graph visualization to map connections between Events → Projects → Concepts.

**Created by Vicky404** | GitHub Profile
