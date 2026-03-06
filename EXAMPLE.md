# 🌌 Sozo in Action: A Day in the Life

Not sure how to actually use Sozo? You don't need to be a programmer to use it. Whether you are a student, a writer, or a developer, Sozo tracks your actions so you never lose your context.

Here is exactly how you might use every single command in a typical day.

---

## 🌅 Morning: The Basics
You wake up and start your day. Instead of writing a long diary entry, you just log your actions.

**1. Log a simple habit:**
```bash
sozo add health "Morning run and stretched" -t fitness
```
2. Set a reminder for later:
You remember you need to email a client or professor later today.

``` bash
sozo add work "Email Professor about the project" --at "3pm" --remind
```
3. Start the Reminder Watcher:
You open a new terminal tab and tell Sozo to watch for your reminders. (It will ping you at 3 PM).

``` bash
sozo kosmo
```
## 🧠 Afternoon: The Knowledge Vault
You are studying, researching, or brainstorming. You need to write things down, but you want them connected to your timeline.

4. Create a quick, dedicated Note:
You have an idea for a project or anything.

``` Bash
sozo note "Proj Ideas" -c brainstorm -t youtube
```
(Sozo instantly creates 20260305-faceless-channel-ideas.md and opens it for you to write in).

5. AI Note Ingestion (The Magic Trick):
You take some really messy, unformatted notes in a .txt file while watching a lecture or reading a book . Let the AI clean it up.

``` bash
sozo ingest messy_notes.txt "DSA Concepts" -c reading -t dsa
```
(Sozo reads your messy text, uses AI to format it into beautiful Markdown, and saves it to your vault).

6. Connect your thoughts (Bidirectional Linking):
Later, you take an action based on that brainstorm note you wrote earlier (let's say it was Event ID #12).

``` bash
sozo add project "Created the graph func" -r 12
```
(Now, this action is permanently linked to your original brainstorm).

7. See the connections:
To see how your ideas are connecting, just run:

``` bash
sozo graph
```
💻 Evening: The Developer Work
If you write code, Sozo acts as your automated project manager.

8. Check file history:
You open a Python file and wonder when you last worked on it.

``` bash
sozo file "services.py"
```
9. The AI Auto-Commit:
You finish writing some code. Instead of manually checking what you changed and writing a Git commit message, you just type:

``` bash
sozo commit
```
(Sozo reads your code changes, asks the AI to write a perfect commit message, pushes the commit, and logs the files you changed to your timeline).

## 🌙 Night: The Review
The day is over. It is time to see what you actually accomplished.

10. Open your Command Center:
Turn your terminal into a full-screen dashboard.

``` bash
sozo dash
```
11. View your chronological timeline:
See a beautiful tree of everything you did this week, grouped by day.

```bash
sozo timeline week
```
12. Search for something specific:
You forgot when you worked on a specific game server setup.

``` bash
sozo search "minecraft"
```
13. Oops, made a mistake:
You accidentally logged something twice (let's say Event ID #4).

``` bash
sozo delete 4
```
14. Export your data:
You want to back up all your "AI" related logs to a single file to share with a friend.

``` bash
sozo export -t ai -o my_ai_journey.md
```