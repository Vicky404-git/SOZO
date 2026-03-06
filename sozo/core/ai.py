import os
from pathlib import Path
from groq import Groq
from dotenv import load_dotenv

# Dynamically point to the root of the SOZO project folder
env_path = Path(__file__).resolve().parent.parent.parent / ".env"
load_dotenv(env_path)

def format_notes_to_markdown(raw_text: str) -> str:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError(f"GROQ_API_KEY is missing. Please add it to {env_path}")
    
    client = Groq(api_key=api_key)

    prompt = f"""
    You are an expert note-taker. Convert the following raw text into a beautifully formatted Markdown document.
    Follow these rules strictly:
    1. Use headings (##), bullet points, and bold text for key concepts.
    2. Fix any obvious typos, but do not change the core meaning.
    3. Output ONLY the markdown text. No conversational filler.

    Raw Notes:
    {raw_text}
    """

    try:
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.1-8b-instant",
            temperature=0.3,
            max_tokens=3000,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        raise RuntimeError(f"AI Formatting failed: {e}")
    
def generate_commit_message(diff: str) -> str:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError(f"GROQ_API_KEY is missing. Please add it to {env_path}")
    
    client = Groq(api_key=api_key)

    prompt = f"""
    You are an expert developer. Generate a concise, conventional commit message for the following git diff.
    Follow these rules strictly:
    1. Use conventional format (e.g., feat:, fix:, chore:, refactor:, docs:).
    2. Keep it under 50 characters if possible.
    3. Output ONLY the commit message. No explanations, no markdown formatting, no quotes, no yapping.

    Git Diff:
    {diff}
    """

    try:
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.1-8b-instant",  # Fast and free
            temperature=0.3,         # Low temperature for precise, predictable outputs
            max_tokens=50,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        raise RuntimeError(f"AI Generation failed: {e}")