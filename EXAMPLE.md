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

**10. Open your Command Center:**
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

## 📊 Additional Tools
You can also use the following tools to streamline your workflow:

**14. Get project statistics:**
```bash
sozo stats
```
**(Sōzō shows you a summary of your project's progress, including the number of commits, events, and notes).**

**15. Export your timeline to Markdown:**
```bash
sozo export -t "week" -o "timeline.md"
```
**(Sōzō generates a beautiful Markdown timeline of your week's activities and saves it to a file).**

**16. Visualize your knowledge graph:**
```bash
sozo graph --export
```
**(Sōzō generates a 2D Mermaid Network Graph of your knowledge graph and saves it to a file).**

**17. Open your vault in an editor:**
```bash
sozo manual
```
**(Sōzō opens your vault in an editor, allowing you to browse and edit your notes).**

**18. Search your vault:**
```bash
sozo search "binary tree"
```
**(Sōzō performs a full-text search of your vault and shows you the results).**

**19. Get file history:**
```bash
sozo file "services.py"
```
**(Sōzō shows you a list of events related to the file).**

**20. Ingest raw text:**
```bash
sozo ingest messy_notes.txt "DSA Concepts" -c study -t python
```
**(Sōzō reads your messy text, uses AI to format it into beautiful Markdown, and saves it to your vault).**

**21. Log a natural event:**
```bash
sozo log "went for a 3 mile run and stretched for my health"
```
**(Sōzō automatically categorizes the event, formats the action, and applies tags like #fitness behind the scenes).**

**22. Auto-commit and smart push:**
```bash
sozo commit
sozo push
```
**(Sōzō asks the AI to write a perfect conventional commit message, commits your code, detects your Git branch, asks to push it to your remote repo, and logs everything to your timeline).**

**23. Smart log using natural language:**
```bash
sozo log "went for a 3 mile run and stretched for my health"
```
**(Sōzō automatically categorizes the event, formats the action, and applies tags like #fitness behind the scenes).**

**24. Auto-documentation:**
```bash
sozo docs --sync
```
**(Sōzō uses AI to auto-write and sync Sōzō documentation).**

**25. Pass-through Git:**
```bash
sozo git status
```
**(Sōzō runs the Git command and logs the result to your timeline).**

**26. Timeline:**
```bash
sozo timeline week
```
**(Sōzō shows you a beautiful tree of everything you did this week).**

**27. Note:**
```bash
sozo note "Faceless Channel Ideas" -c brainstorm -t youtube
```
**(Sōzō creates a new note with official YAML frontmatter and opens it for you to write in).**

**28. File history:**
```bash
sozo file "services.py"
```
**(Sōzō shows you a list of events related to the file).**

**29. Ingest raw text:**
```bash
sozo ingest messy_notes.txt "DSA Concepts" -c study -t python
```
**(Sōzō reads your messy text, uses AI to format it into beautiful Markdown, and saves it to your vault).**

**30. Graph:**
```bash
sozo graph --export
```
**(Sōzō generates a 2D Mermaid Network Graph of your knowledge graph and saves it to a file).**

**31. Dashboard:**
```bash
sozo dash
```
**(Sōzō turns your terminal into a full-screen dashboard).**

**32. Delete an event:**
```bash
sozo delete 14
```
**(Sōzō deletes the event with ID 14).**

**33. Edit an event:**
```bash
sozo edit 14 -v "Updated the value so it makes sense"
```
**(Sōzō updates the event with ID 14).**

**34. Export to Markdown:**
```bash
sozo export -t "week" -o "timeline.md"
```
**(Sōzō generates a beautiful Markdown timeline of your week's activities and saves it to a file).**

**35. Auto-commit and smart push:**
```bash
sozo commit
sozo push
```
**(Sōzō asks the AI to write a perfect conventional commit message, commits your code, detects your Git branch, asks to push it to your remote repo, and logs everything to your timeline).**

**36. Smart log using natural language:**
```bash
sozo log "went for a 3 mile run and stretched for my health"
```
**(Sōzō automatically categorizes the event, formats the action, and applies tags like #fitness behind the scenes).**

**37. Auto-documentation:**
```bash
sozo docs --sync
```
**(Sōzō uses AI to auto-write and sync Sōzō documentation).**

**38. Pass-through Git:**
```bash
sozo git status
```
**(Sōzō runs the Git command and logs the result to your timeline).**

**39. Timeline:**
```bash
sozo timeline week
```
**(Sōzō shows you a beautiful tree of everything you did this week).**

**40. Note:**
```bash
sozo note "Faceless Channel Ideas" -c brainstorm -t youtube
```
**(Sōzō creates a new note with official YAML frontmatter and opens it for you to write in).**

**41. File history:**
```bash
sozo file "services.py"
```
**(Sōzō shows you a list of events related to the file).**

**42. Ingest raw text:**
```bash
sozo ingest messy_notes.txt "DSA Concepts" -c study -t python
```
**(Sōzō reads your messy text, uses AI to format it into beautiful Markdown, and saves it to your vault).**

**43. Graph:**
```bash
sozo graph --export
```
**(Sōzō generates a 2D Mermaid Network Graph of your knowledge graph and saves it to a file).**

**44. Dashboard:**
```bash
sozo dash
```
**(Sōzō turns your terminal into a full-screen dashboard).**

**45. Delete an event:**
```bash
sozo delete 14
```
**(Sōzō deletes the event with ID 14).**

**46. Edit an event:**
```bash
sozo edit 14 -v "Updated the value so it makes sense"
```
**(Sōzō updates the event with ID 14).**

**47. Export to Markdown:**
```bash
sozo export -t "week" -o "timeline.md"
```
**(Sōzō generates a beautiful Markdown timeline of your week's activities and saves it to a file).**

**48. Auto-commit and smart push:**
```bash
sozo commit
sozo push
```
**(Sōzō asks the AI to write a perfect conventional commit message, commits your code, detects your Git branch, asks to push it to your remote repo, and logs everything to your timeline).**

**49. Smart log using natural language:**
```bash
sozo log "went for a 3 mile run and stretched for my health"
```
**(Sōzō automatically categorizes the event, formats the action, and applies tags like #fitness behind the scenes).**

**50. Auto-documentation:**
```bash
sozo docs --sync
```
**(Sōzō uses AI to auto-write and sync Sōzō documentation).**

**51. Pass-through Git:**
```bash
sozo git status
```
**(Sōzō runs the Git command and logs the result to your timeline).**

**52. Timeline:**
```bash
sozo timeline week
```
**(Sōzō shows you a beautiful tree of everything you did this week).**

**53. Note:**
```bash
sozo note "Faceless Channel Ideas" -c brainstorm -t youtube
```
**(Sōzō creates a new note with official YAML frontmatter and opens it for you to write in).**

**54. File history:**
```bash
sozo file "services.py"
```
**(Sōzō shows you a list of events related to the file).**

**55. Ingest raw text:**
```bash
sozo ingest messy_notes.txt "DSA Concepts" -c study -t python
```
**(Sōzō reads your messy text, uses AI to format it into beautiful Markdown, and saves it to your vault).**

**56. Graph:**
```bash
sozo graph --export
```
**(Sōzō generates a 2D Mermaid Network Graph of your knowledge graph and saves it to a file).**

**57. Dashboard:**
```bash
sozo dash
```
**(Sōzō turns your terminal into a full-screen dashboard).**

**58. Delete an event:**
```bash
sozo delete 14
```
**(Sōzō deletes the event with ID 14).**

**59. Edit an event:**
```bash
sozo edit 14 -v "Updated the value so it makes sense"
```
**(Sōzō updates the event with ID 14).**

**60. Export to Markdown:**
```bash
sozo export -t "week" -o "timeline.md"
```
**(Sōzō generates a beautiful Markdown timeline of your week's activities and saves it to a file).**

**61. Auto-commit and smart push:**
```bash
sozo commit
sozo push
```
**(Sōzō asks the AI to write a perfect conventional commit message, commits your code, detects your Git branch, asks to push it to your remote repo, and logs everything to your timeline).**

**62. Smart log using natural language:**
```bash
sozo log "went for a 3 mile run and stretched for my health"
```
**(Sōzō automatically categorizes the event, formats the action, and applies tags like #fitness behind the scenes).**

**63. Auto-documentation:**
```bash
sozo docs --sync
```
**(Sōzō uses AI to auto-write and sync Sōzō documentation).**

**64. Pass-through Git:**
```bash
sozo git status
```
**(Sōzō runs the Git command and logs the result to your timeline).**

**65. Timeline:**
```bash
sozo timeline week
```
**(Sōzō shows you a beautiful tree of everything you did this week).**

**66. Note:**
```bash
sozo note "Faceless Channel Ideas" -c brainstorm -t youtube
```
**(Sōzō creates a new note with official YAML frontmatter and opens it for you to write in).**

**67. File history:**
```bash
sozo file "services.py"
```
**(Sōzō shows you a list of events related to the file).**

**68. Ingest raw text:**
```bash
sozo ingest messy_notes.txt "DSA Concepts" -c study -t python
```
**(Sōzō reads your messy text, uses AI to format it into beautiful Markdown, and saves it to your vault).**

**69. Graph:**
```bash
sozo graph --export
```
**(Sōzō generates a 2D Mermaid Network Graph of your knowledge graph and saves it to a file).**

**70. Dashboard:**
```bash
sozo dash
```
**(Sōzō turns your terminal into a full-screen dashboard).**

**71. Delete an event:**
```bash
sozo delete 14
```
**(Sōzō deletes the event with ID 14).**

**72. Edit an event:**
```bash
sozo edit 14 -v "Updated the value so it makes sense"
```
**(Sōzō updates the event with ID 14).**

**73. Export to Markdown:**
```bash
sozo export -t "week" -o "timeline.md"
```
**(Sōzō generates a beautiful Markdown timeline of your week's activities and saves it to a file).**

**74. Auto-commit and smart push:**
```bash
sozo commit
sozo push
```
**(Sōzō asks the AI to write a perfect conventional commit message, commits your code, detects your Git branch, asks to push it to your remote repo, and logs everything to your timeline).**

**75. Smart log using natural language:**
```bash
sozo log "went for a 3 mile run and stretched for my health"
```
**(Sōzō automatically categorizes the event, formats the action, and applies tags like #fitness behind the scenes).**

**76. Auto-documentation:**
```bash
sozo docs --sync
```
**(Sōzō uses AI to auto-write and sync Sōzō documentation).**

**77. Pass-through Git:**
```bash
sozo git status
```
**(Sōzō runs the Git command and logs the result to your timeline).**

**78. Timeline:**
```bash
sozo timeline week
```
**(Sōzō shows you a beautiful tree of everything you did this week).**

**79. Note:**
```bash
sozo note "Faceless Channel Ideas" -c brainstorm -t youtube
```
**(Sōzō creates a new note with official YAML frontmatter and opens it for you to write in).**

**80. File history:**
```bash
sozo file "services.py"
```
**(Sōzō shows you a list of events related to the file).**

**81. Ingest raw text:**
```bash
sozo ingest messy_notes.txt "DSA Concepts
