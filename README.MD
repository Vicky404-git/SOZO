# Sozo — Life as Events

> **A local-first, CLI-based personal event engine. Git for your life activities.**

Track life as events, not notes. Sozo is a system that records meaningful actions and builds a chronological timeline of what you actually did. 

**Not a notes app. Not a task manager. Not a diary.**

Most productivity tools force people to write long notes, organize folders, or manage dashboards. But life doesn't work that way. People don't live in pages and tables. They do things. Sozo records actions instead of documents. Think of it like **Git for your life timeline**.

---

## 🚀 The Core Idea
Everything in Sozo is an **Event**. Over time, these events weave together to form a complete timeline of your work, learning, and projects.

* **Timestamp:** `2026-03-05 09:02`
* **Category:** `programming`
* **Value:** `implemented the Bidirectional Linking Engine`
* **Metadata:** `#python`, `#sozo`, `🔗 Linked to #14`

---

## ⚡ Features (The Second Brain Upgrades)

Sozo has evolved from a simple logger into a deeply interconnected knowledge system:

* **The Command Center:** Run `sozo dash` to turn your terminal into a Notion-style split-screen dashboard showing stats, today's actions, and your timeline feed.
* **The Knowledge Vault:** Use `sozo note` to automatically generate, format, and track Markdown files in a hidden local vault.
* **AI Auto-Ingestion:** Dump raw, messy `.txt` thoughts into `sozo ingest`, and the Groq AI will instantly format it into clean Markdown and save it to your vault.
* **Obsidian-Style Graph:** Use `[[wikilinks]]` inside your notes, then run `sozo graph` to render an ASCII tree mapping how all your thoughts connect.
* **Bidirectional Timeline Linking:** Use the `-r` flag to visually link today's code commit back to a brainstorming note you wrote three weeks ago.
* **AI Git Auto-Committer:** Run `sozo commit` to have Llama 3 read your staged code, write a conventional commit message, and log the changes to your timeline.
* **Auto-Context:** Sozo detects your Git repositories and links physical files to your events automatically.

---

## 🛠️ Installation

Clone the repository:
```bash
git clone [https://github.com/Vicky404-git/SOZO.git](https://github.com/Vicky404-git/SOZO.git)
cd SOZO

```

Create and activate a virtual environment (Windows):

Bash

```
python -m venv sozoenv
sozoenv\Scripts\activate

```

Install the project:

Bash

```
pip install -e .

```

_Note for AI Features: Create a `.env` file in the root of the `SOZO` folder with `GROQ_API_KEY=your_key_here` to enable `sozo commit` and `sozo ingest`._

----------

## 📖 Quick Start & Example Workflow

**Open the Terminal Dashboard:**

Bash

```
sozo dash

```

**Log an action linked to a previous idea:**

Bash

```
sozo add programming "built the graph scanner" -t python -f core/services.py -r 14

```

**Auto-format study notes with AI:**

Bash

```
sozo ingest raw_lecture.txt "Neural Networks Ch 1" -c study -t aiml

```

**View your Knowledge Graph:**

Bash

```
sozo graph

```

**Auto-commit your code and log it:**

Bash

```
sozo commit

```

_(For the complete guide, type `sozo --help` or `sozo manual` in your terminal)._

----------

## 🗄️ Database Architecture

Sozo uses a local, private SQLite database. No servers, no accounts.

**Table:** `events`

-   `id` (INTEGER PRIMARY KEY)
    
-   `timestamp` (TEXT)
    
-   `category` (TEXT)
    
-   `value` (TEXT)
    
-   `created_at` (TEXT)
    
-   `remind` (INTEGER)
    
-   `reminded` (INTEGER)
    
-   `tags` (TEXT)
    
-   `files` (TEXT)
    
-   `relates_to` (INTEGER)
    

----------

## 🗺️ Roadmap

-   **DaemonV Integration:** Moving the `kosmo` reminder engine into a silent, native background service so it doesn't require an open terminal tab.
    
-   **Natural Language Processing:** `sozo log studied transformers for 2h` -> auto-parses category, value, and duration.
    

----------

**Created by Vicky404** [GitHub Profile](https://github.com/Vicky404-git)