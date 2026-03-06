# 🌌 Sōzō (創造) — User Manual

Welcome to Sōzō. This is a local-first personal event engine. Sōzō bridges the gap between a daily logger, an Obsidian knowledge vault, and a Notion command center. 

## Core Philosophy
Everything you do is an **Event**. Sōzō doesn't just store files; it records *when* you did something, *why* you did it, and *what* it connects to.

---

## 1. The Command Center
Turn your terminal into a hacker workspace.

* **Open Dashboard:** `sozo dash`
  *(Splits your terminal into a Notion-style view showing Activity Stats, Today's Actions, and your Recent Timeline feed).*
* **View Timeline:** `sozo timeline` (or `sozo timeline month`)
  *(Outputs a beautifully formatted chronological tree of your events grouped by day).*

---

## 2. The Knowledge Vault (Obsidian Mode)
Sōzō features a hidden Markdown vault (`~/.sozo/vault/`) for your deep work, college lectures, and brainstorming.

* **Create a Note:** `sozo note "Deep Learning Lecture" -c study -t aiml`
  *(Instantly generates a formatted `.md` file in your vault, logs it to your timeline, and opens it in your default text editor).*
* **AI Note Ingestion:** `sozo ingest raw_notes.txt "Clean AI Notes" -c lecture`
  *(Takes your messy, unformatted `.txt` dumps and uses Llama 3 to structure them into beautiful Markdown before saving them to the vault).*
* **The Knowledge Graph:** `sozo graph`
  *(Scans your vault notes for Obsidian-style `[[wikilinks]]` and draws an ASCII tree of how your thoughts connect).*
  > **Pro-Tip:** Type `[[Another Idea]]` anywhere inside a Sōzō note to link them together!

---

## 3. Event Linking & Tracking
Record actions and string them together chronologically.

* **Basic Log:** `sozo add programming "Refactored the core engine"`
* **With Tags & Files:** `sozo add study "Read transformer paper" -t ai -f paper.pdf`
* **Bidirectional Linking:** `sozo add programming "Wrote the code for the idea" -r 5`
  *(Uses `-r` or `--relates-to` to link this new event directly back to Event #5).*
* **File History:** `sozo file "services.py"`
  *(See a timeline of every single event where you touched that specific file).*

---

## 4. Git & AI Workflows
Sōzō is fully aware of your local Git repositories. If you run Sōzō inside a repo, it tags events with the project name automatically.

* **The AI Auto-Committer:** `sozo commit`
  *(Reads your staged `git diff`, sends it to Groq's Llama 3 API to generate a conventional commit message, commits the code, and logs the changes directly to your Sōzō timeline).*
* **Manual Commit:** `sozo commit -m "fixed the login API"`
* **Git Passthrough:** `sozo git push origin main`
  *(Runs a normal git push, but secretly logs "Git Execute" to your timeline).*

---

## 5. Finding & Managing Data
* **Today's Events:** `sozo today`
* **All Events:** `sozo list` (or `sozo list "2026-03-05"`)
* **Search:** `sozo search "vector stores"`
* **Analytics:** `sozo stats`
* **Delete Event:** `sozo delete <ID>`
* **Export Timeline:** `sozo export -t aiml -o my_ai_timeline.md`

---

## 6. Reminders Engine (Kosmo)
Sōzō can run a background watcher to remind you of future events.

* **Set a Reminder:** `sozo add work "Deploy to production" --at "tomorrow 5pm" --remind`
* **Start the Watcher:** `sozo kosmo`
  *(Leave this running in a separate terminal tab. It will ping you when it's time).*