import json
from groq import Groq
from sozo.core.config import get_groq_api_key

def _get_client():
    api_key = get_groq_api_key()
    if not api_key:
        raise ValueError("GROQ_API_KEY is missing. Please add it to your .env file.")
    return Groq(api_key=api_key)

def format_notes_to_markdown(raw_text: str) -> str:
    client = _get_client()
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
    client = _get_client()
    prompt = f"""
    You are an expert developer. Generate a concise, conventional commit message for the following git diff.
    Follow these rules strictly:
    1. Use conventional format (e.g., feat:, fix:, chore:, refactor:, docs:).
    2. Keep it under 50 characters if possible.
    3. Output ONLY the commit message. No explanations, no markdown formatting, no quotes, no yapping, in simple words.

    Git Diff:
    {diff}
    """
    try:
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.1-8b-instant",  
            temperature=0.3,         
            max_tokens=50,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        raise RuntimeError(f"AI Generation failed: {e}")
    
def parse_natural_language_event(text: str) -> dict:
    client = _get_client()
    prompt = f"""
    You are an AI assistant for a personal logging tool. 
    Extract the action from the following text and return it as a STRICT JSON object.
    Do not include any Markdown formatting, conversational filler, or code blocks. Just the raw JSON.
    
    Expected JSON format:
    {{
        "category": "a single word (e.g., study, health, programming, work, life)",
        "value": "a concise summary of the action (written in past tense)",
        "tags": ["tag1", "tag2"]
    }}
    
    Text: "{text}"
    """
    
    try:
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.1-8b-instant",
            temperature=0.1, # Keep it low so it's highly deterministic
            response_format={"type": "json_object"} # Forces the AI to return valid JSON
        )
        result = response.choices[0].message.content.strip()
        return json.loads(result)
    except Exception as e:
        raise RuntimeError(f"AI parsing failed: {e}")