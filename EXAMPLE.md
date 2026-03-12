# 🌌Sōzō in Action: A Day in the Life

Not sure how to actually use Sōzō? You don't need to be a programmer to use it. Whether you are a student, a writer, or a developer, Sōzō tracks your actions so you never lose your context.

Here is exactly how you might use Sōzō's AI and Second Brain features in a typical day.

---

## 🌅 Morning: The Basics
You wake up and start your day. Instead of writing a long diary entry or manually typing out categories and tags, you just talk to the AI.

**1. Smart Log a habit:**
```bash
sozo log "went for a 3 mile run and stretched for my health"
```
(Llama-3 automatically categorizes this as health, formats the action, and applies tags like #fitness behind the scenes).

**2. Set a reminder for later:**
You remember you need to email a client or professor later today.

```bash
sozo add work "Email Professor about the project" --at "3pm" --remind
```
**3. Start the Reminder Watcher:**
You open a new terminal tab and tell Sōzō to watch for your reminders. (It will ping you at 3 PM).

```bash
sozo kosmo
```
## 🧠 Afternoon: The Second Brain
You are studying, researching, or brainstorming. You need to write things down, but you want them connected to your timeline.

**4. Create a quick, dedicated Note:**
You have an idea for a project.

```bash
sozo note "Faceless Channel Ideas" -c brainstorm -t youtube
```
*(Sōzō creates 20260313-faceless-channel-ideas.md with official YAML frontmatter and opens it for you to write in).*

**5. AI Note Ingestion (The Magic Trick):**
You take some really messy, unformatted notes in a .txt file while watching a lecture. Let the AI clean it up.

```bash
sozo ingest messy_notes.txt "DSA Concepts" -c study -t python
```
*(Sōzō reads your messy text, uses AI to format it into beautiful Markdown, and saves it to your vault).*

**6. Deep Search your Brain:**
You know you wrote down something about "binary trees" a few weeks ago, but you can't remember where.

```bash
sozo brain "binary tree"
```
*(Sōzō does a full-text deep scan inside your Markdown vault and shows you the exact highlighted snippet).*

**7. View the Concept Node (Connecting the Dots):**
You want to see everything you've ever done related to Python.

```bash
sozo concept python
```
**(Sōzō generates a hierarchical tree showing every Python note you've written, every Python project you've committed, and every Python event you've logged. You can even CTRL+Click the notes to open them!)*

## 💻 Evening: The Developer Work
If you write code, Sōzō acts as your automated project manager.

**8. Check file history:**
You open a Python file and wonder when you last worked on it.

```bash
sozo file "services.py"
```
**9. The AI Auto-Commit & Smart Push:**
You finish writing some code. Instead of manually checking what you changed, writing a Git commit message, and pushing it, you just type:

```bash
sozo commit
sozo push
```
**(Sōzō asks the AI to write a perfect conventional commit message, commits your code, detects your Git branch, asks to push it to your remote repo, and logs everything to your timeline).**

## 🌙 Night: The Review
The day is over. It is time to see what you actually accomplished.

** 10. Open your Command Center:
Turn your terminal into a full-screen dashboard.

```bash
sozo dash
```
**11. View your chronological timeline:**
See a beautiful tree of everything you did this week.

```bash
sozo timeline week
```
**12. Oops, made a mistake:**
You realized you made a typo on Event #14 earlier today.

```bash
sozo edit 14 -v "Updated the value so it makes sense"
```
**13. Update the System:**
Before logging off, you check to see if there are any new Sōzō updates on GitHub.

```bash
sozo --update
```
**(Sōzō pulls the latest code and syncs dependencies instantly).**