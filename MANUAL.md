# Sōzō (創造) — User Manual

Welcome to Sōzō. This is a local-first personal event engine. Sōzō does not track everything automatically; instead, it records your intentional, meaningful actions on a timeline.

## Core Concept
Everything is an Event. An event consists of:
* **Time:** When it happened.
* **Category:** The area of your life (e.g., `study`, `programming`, `health`).
* **Value:** What exactly you did.
* **Tags:** Keywords to link thoughts together (like Obsidian).
* **Files:** Links to specific code, notes, or project files.

---

## Command Reference

### 1. Adding Events (`add`)
Record an action in your timeline. If you run this inside a Git repository, Sōzō will automatically detect the project name and tag it!

* **Basic:** `sozo add programming "fixed the database bug"`
* **With Tags:** `sozo add study "read transformer paper" -t ai -t machine-learning`
* **With Files:** `sozo add programming "refactored the CLI" -f sozo/cli/commands.py`
* **In the Past/Future:** `sozo add health "went for a run" --at "yesterday 6pm"`
* **With Reminder:** `sozo add work "call the client" --at "tomorrow 10am" --remind`

### 2. The Git Integration (`commit` & `git`)
Sōzō is fully integrated with Git. When you run Git commands through Sōzō, it automatically logs your actions to your timeline.

* **Auto-Commit:** `sozo commit`
  *(Sōzō will auto-stage your files, generate a placeholder commit message, push the commit, and log the exact changed files to your timeline).*
* **Custom Commit:** `sozo commit -m "fixed the login API"`
* **Git Passthrough:** `sozo git push origin main`
  *(Runs a normal git push, but logs "Git Execute" to Sōzō as an event).*

### 3. Viewing Your Timeline
* **Today's Events:** `sozo today`
* **Specific Date:** `sozo show "2026-03-04"` (or `sozo show yesterday`)
* **All Events:** `sozo list`

### 4. Finding Things (`search` & `stats`)
* **Search:** `sozo search ai` (Finds any event with "ai" in the category, value, or tags)
* **Analytics:** `sozo stats` (Shows you which categories you spend the most time on)
* **Calendar:** `sozo calendar` (Shows how many events you logged per day)

### 5. Exporting (`export`)
Export your timeline into a clean Markdown file to use in Notion, Obsidian, or GitHub.

* **Export All:** `sozo export` (Generates `timeline.md` in your current folder)
* **Export by Tag:** `sozo export -t aiml -o my_ai_notes.md`

### 6. Editing & Deleting
Every event has an ID (visible when you use `list`, `show`, or `today`).
* **Delete:** `sozo delete 5` (Deletes event ID 5)
* **Edit:** `sozo edit 5 --category "work" --value "updated meeting notes"`