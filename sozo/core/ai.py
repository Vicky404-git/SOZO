import json
import time
from groq import Groq
from sozo.core.config import get_groq_api_key

# ---------- Core Client ----------

def _client():
    api_key = get_groq_api_key()
    if not api_key:
        raise ValueError(
            "GROQ_API_KEY missing. Add it to .env or use sozo commit."
        )
    return Groq(api_key=api_key)


def _ai(prompt: str, *, model="llama-3.1-8b-instant", temp=0.3, tokens=1000, fmt=None):
    """Generic LLM executor."""
    kwargs = {
        "messages": [{"role": "user", "content": prompt}],
        "model": model,
        "temperature": temp,
        "max_tokens": tokens,
    }
    
    # Safely attach the JSON formatter only if requested
    if fmt:
        kwargs["response_format"] = fmt
        
    try:
        res = _client().chat.completions.create(**kwargs)
        return res.choices[0].message.content.strip()
    except Exception as e:
        raise RuntimeError(f"AI call failed: {e}")


# ---------- Notes Formatter ----------

def format_notes_to_markdown(text: str) -> str:
    prompt = f"""
Convert the raw notes into clean Markdown.

Rules:
- Use headings (##), bullets, bold for key ideas
- Fix obvious typos
- Output ONLY markdown

Raw Notes:
{text}
"""
    return _ai(prompt, tokens=3000)


# ---------- Diff Chunk Summarizer ----------

def _summarize_chunk(chunk: str) -> str:
    try:
        return _ai(
            f"Summarize this git diff in <=2 sentences:\n\n{chunk}",
            temp=0.2,
            tokens=100,
        )
    except Exception:
        return "[Unreadable chunk]"


# ---------- Commit Message Generator ----------

def generate_commit_message(diff: str) -> str:
    max_chunk = 12000

    if len(diff) > max_chunk:
        chunks = [diff[i:i + max_chunk] for i in range(0, len(diff), max_chunk)]
        summaries = []

        for i, chunk in enumerate(chunks[:5]):
            summaries.append(f"- {i+1}: {_summarize_chunk(chunk)}")
            time.sleep(1)

        if len(chunks) > 5:
            summaries.append("... (remaining chunks ignored)")

        context = "COMBINED DIFF SUMMARY:\n" + "\n".join(summaries)
    else:
        context = diff

    prompt = f"""
Write a Conventional Commit message for this change.

Rules:
- format: type(scope): message
- types: feat, fix, refactor, docs, style, test, chore, perf
- subject < 50 chars
- imperative mood
- no period

Diff:
{context}

Output ONLY the commit message.
"""

    return _ai(prompt, tokens=50)


# ---------- Natural Language Event Parser ----------

def parse_natural_language_event(text: str) -> dict:
    prompt = f"""
Extract structured JSON from this text.

Format:
{{
  "category": "single word",
  "value": "past tense summary",
  "tags": ["tag1","tag2"]
}}

Text: "{text}"
"""

    result = _ai(
        prompt,
        temp=0.1,
        fmt={"type": "json_object"},
    )

    return json.loads(result)


# ---------- Documentation Updater ----------

def generate_updated_docs(context: str, doc: str, name: str) -> str:
    prompt = f"""
Update '{name}' so it matches the project source.

Rules:
- Add missing features
- Update changed logic
- Preserve formatting
- Output full document
- No markdown code blocks
- No filler text

Project Source:
{context}

Current {name}:
{doc}
"""

    return _ai(
        prompt,
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        temp=0.1,
        tokens=3500,
    )