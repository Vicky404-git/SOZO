# 🌌 Sōzō (創造) — User Manual

Welcome to Sōzō. This is a local-first personal event engine. Sōzō bridges the gap between a daily logger, an Obsidian knowledge vault, and a Notion command center. 

## Core Philosophy
Everything you do is an **Event**. Sōzō doesn't just store files; it records *when* you did something, *why* you did it, and *what* it connects to.

---

## 1. The Command Center
Turn your terminal into a hacker workspace.

* **Open Dashboard:** `sozo dash`
  *(Splits your terminal into a Notion-style view showing Activity Stats, Today's Actions, and your Recent Timeline feed).*
* **View Timeline:** `sozo timeline` (or `sozo timeline month` / `sozo timeline week -t aiml`)
  *(Outputs a beautifully formatted chronological tree of your events grouped by day. Can be filtered by tag).*
* **Edit an Event:** `sozo edit <ID> [-c CATEGORY] [-v VALUE] [-t TAG] [-f FILE]`
  *(Fix typos or update categories, values, tags, and files of past events).*
* **Delete an Event:** `sozo delete <ID>`
  *(Permanently removes an event from your database).*

---

## 2. Smart Logging (Natural Language)
You don't need to manually type out tags and categories anymore. Sōzō has a brain.

* **AI Smart Log:** `sozo log "studied LangChain vector stores for 2 hours"`
  *(Sends your plain English sentence to Llama-3. The AI automatically figures out the category, formats the action, extracts the tags, and saves it perfectly to your timeline).*

---

## 3. The Second Brain (Knowledge Vault & Concepts)
Sōzō features a hidden, deeply interconnected Markdown vault (`~/.sozo/vault/`). All notes are generated with official YAML frontmatter, making them 100% compatible with Obsidian and Notion.

* **The Concept Engine:** `sozo concept "python"`
  *(Unifies your entire life. Instantly gathers every Markdown note, Git commit, and logged event related to "python" and renders them as a hierarchical, clickable tree).*
* **Deep Brain Search:** `sozo brain "architecture"`
  *(Performs a full-text regex scan deep inside the actual content of your Markdown vault notes, returning highlighted snippets of where the word was found).*
* **Create a Note:** `sozo note "Deep Learning Lecture" [-c CATEGORY] [-t TAG]`
  *(Generates a YAML-formatted `.md` file in an auto-organized subfolder, logs it to your timeline, and opens your editor).*
* **AI Note Ingestion:** `sozo ingest RAW_FILE.TXT "Clean AI Notes" [-c CATEGORY] [-t TAG]`
  *(Takes messy, unformatted `.txt` dumps and uses Llama-3 to structure them into beautiful Markdown before saving).*
* **The Knowledge Graph:** `sozo graph` (or `sozo graph --export`)
  *(Scans your vault notes for Obsidian-style `[[wikilinks]]` and draws an ASCII tree of how your thoughts connect. Use `--export` to generate a 2D interactive network graph).*

---

## 4. Git & AI Workflows
Sōzō is fully aware of your local Git repositories. If you run Sōzō inside a repo, it tags events with the project name automatically.

* **The AI Auto-Committer:** `sozo commit [-m MESSAGE]`
  *(Reads your staged `git diff`, sends it to Groq to generate a conventional commit message, commits the code, and logs the changes directly to your timeline).*
* **Smart Push:** `sozo push`
  *(Detects your current branch, asks for confirmation, pushes to the remote repository, and logs the execution).*
* **Manual Commit:** `sozo commit -m "fixed the login API"`
* **Git Passthrough:** `sozo git [COMMAND]`
  *(Runs normal git commands, but secretly logs "Git Execute" to your timeline).*

---

## 5. Manual Event Tracking
For when you want complete, rigid control over your logs.

* **Basic Log:** `sozo add CATEGORY "VALUE" [-a AT] [-r RELATES_TO] [-t TAG] [-f FILE]`
  *(Creates a new event with the specified category, value, and tags).*
* **With Tags & Files:** `sozo add CATEGORY "VALUE" [-t TAG] [-f FILE]`
  *(Creates a new event with the specified category, value, tags, and files).*
* **Bidirectional Linking:** `sozo add CATEGORY "VALUE" [-r RELATES_TO]`
  *(Uses `-r` or `--relates-to` to link this new event directly back to Event #RELATES_TO).*
* **File History:** `sozo file FILENAME`
  *(See a timeline of every single event where you touched that specific file).*

---

## 6. Finding & Managing Data
* **Today's Events:** `sozo today`
* **All Events:** `sozo list` (or `sozo list DATE`)
* **Database Search:** `sozo search QUERY`
  *(Searches your SQLite database timeline. Use `sozo brain` to search inside files).*
* **Analytics:** `sozo stats`
* **Export Timeline:** `sozo export [-t TAG] [-o OUTPUT_FILE]`
  *(Exports your timeline to a Markdown file, optionally filtered by tag).*

---

## 7. System & Maintenance
* **Self-Updater:** `sozo --update`
  *(Automatically pulls the latest Sōzō codebase from GitHub and syncs any new dependencies without needing to reinstall).*
* **Reminders (Kosmo):** `sozo kosmo`
  *(Start the background watcher in a separate terminal tab. It will ping you when a future event, created via `sozo add --at "3pm" --remind`, is due).*
* **Manual:** `sozo manual`
  *(Opens the MANUAL.md file in your default editor).*
