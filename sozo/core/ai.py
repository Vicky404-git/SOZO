import json
from groq import Groq
import time
from sozo.core.config import get_groq_api_key

def _get_client():
    api_key = get_groq_api_key()
    if not api_key:
        raise ValueError("GROQ_API_KEY is missing. Please add it to your .env file, or use sozo commit -m \"commit msg\".")
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
    
def _summarize_chunk(chunk: str) -> str:
    """Helper function to summarize a small piece of a massive diff."""
    client = _get_client()
    prompt = f"""
    Briefly summarize the changes in this git diff chunk. 
    Keep it under 2 sentences. Focus on what was added, modified, or deleted.
    
    Diff chunk:
    {chunk}
    """
    try:
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.1-8b-instant",
            temperature=0.2,
            max_tokens=100,
        )
        return response.choices[0].message.content.strip()
    except Exception:
        return "[Unreadable chunk]"

def generate_commit_message(diff: str) -> str:
    client = _get_client()
    
    # --- THE MAP-REDUCE CHUNKING ENGINE ---
    max_chunk_size = 12000
    
    if len(diff) > max_chunk_size:
        # 1. Map: Split the massive diff into manageable chunks
        chunks = [diff[i:i + max_chunk_size] for i in range(0, len(diff), max_chunk_size)]
        summaries = []
        
        for i, chunk in enumerate(chunks):
            # Cap at 5 chunks (60,000 chars) to prevent API rate limits on free tier
            if i >= 5: 
                summaries.append("... (diff too massive, remaining chunks ignored)")
                break
            
            summaries.append(f"- {i+1}: " + _summarize_chunk(chunk))
            time.sleep(1) # Prevent Groq API rate-limiting
            
        # 2. Reduce: Combine the summaries to pass to the final prompt
        diff_context = "COMBINED SUMMARIES OF MASSIVE CHANGES:\n" + "\n".join(summaries)
    else:
        # Normal flow for small diffs
        diff_context = f"Git diff:\n{diff}"

    # --- THE FINAL PROMPT ---
    prompt = f"""
    You are an expert software engineer.

    Write a high-quality conventional commit message describing the change in the provided git diff.

    Rules:
    - Use Conventional Commits format: type(scope): message
    - Allowed types: feat, fix, refactor, docs, style, test, chore, perf
    - Keep the subject line under 50 characters
    - Use imperative mood (e.g., "add", "fix", "update", not "added")
    - Do not include a period at the end
    - Be concise, clear, and professional
    - Focus only on the main change

    Output format:
    type: short description

    Output ONLY the commit message.
    No explanations.
    No markdown.
    No quotes.

    Git diff:
    {diff_context}
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
    
    
def generate_updated_docs(project_context: str, current_doc: str, doc_name: str) -> str:
    client = _get_client()
    prompt = f"""
    You are an expert technical writer. I am providing you with a structural skeleton of the project's source code and the current contents of '{doc_name}'.
    Your job is to update '{doc_name}' so it perfectly matches the project's current capabilities.
    
    Rules:
    1. Add sections for new features, functions, or capabilities found in the source code.
    2. Update descriptions, arguments, or endpoints for changed logic.
    3. Preserve the exact tone, style, and formatting of the original document.
    4. Do NOT output any markdown code blocks (like ```markdown), just output the raw text.
    5. Do NOT add conversational filler (e.g., "Here is the updated text...").
    6. Do NOT abbreviate or summarize. You MUST output the entire, full-length comprehensive document from start to finish.
    
    Project Source Skeleton (The Source of Truth):
    {project_context}
    
    Current {doc_name}:
    {current_doc}
    """
    try:
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            temperature=0.1, 
            max_tokens=3500, # Increased slightly to allow for full-length READMEs
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        raise RuntimeError(f"AI Doc Gen failed: {e}")