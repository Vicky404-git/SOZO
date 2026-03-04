# 🌌 Sōzō (創造) — Life as Events

> **A local-first, CLI-based personal event engine. Git for your life activities.**

Most note-taking apps (Notion, Obsidian) are built around *pages* or *graphs*. **Sōzō** is built around **Time and Actions**. Sōzō doesn't just ask you to organize your work; it asks, *"What did you do today?"*

Instead of writing scattered journal entries, Sōzō lets you record meaningful actions in a timeline and connects them to knowledge, projects, and files using tags and Git integration.

---

## 🚀 Features

* **⚡ The Timeline Engine:** Every action is recorded as an "Event" (Timestamp, Category, Value).
* **🧠 Obsidian-Style Tags:** Link thoughts across different categories using `#tags`.
* **📂 Auto-Project Detection:** If you run Sōzō inside a Git repository, it automatically tags the event with the project name.
* **🔗 File Linking:** Connect your events directly to the physical files you edited on your hard drive.
* **🤖 The Auto-Committer:** Run `sozo commit` to instantly analyze your staged files, generate a placeholder commit message, and log the code change directly to your timeline.
* **🔒 100% Local & Private:** No servers, no accounts. Your data lives purely on your machine as an SQLite database.
* **📊 Analytics:** See where you spend your time (`sozo stats`).

---

## 🛠️ Installation

Clone the repository and install it globally using `pip`:

``` bash
git clone [https://github.com/Vicky404-git/SOZO.git](https://github.com/Vicky404-git/SOZO.git)
cd SOZO
pip install -e .
```
*Note: You can now type sozo from anywhere on your computer!*

## 📖 Quick Start
### Log an event:

``` bash
sozo add programming "Refactored the database schema" -t python -f core/database.py
```
### Auto-Commit your code & log it:

``` bash
sozo commit
```
### See what you did today:
``` bash
sozo today
```
### Find all your AI notes:
``` bash
sozo search ai
```
*For the complete guide, type sozo --help or sozo manual in your terminal.*

## 🗺️ Roadmap (Phase 3)
- AI Integration: Replacing the placeholder sozo commit generator with a local LLM that actually reads the git diff and writes human-like commit messages automatically.

- Background Daemon (DaemonV): Merging the reminder engine (kosmo) into a silent, background system process.