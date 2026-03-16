from sozo.core.database import get_connection

def _run_query(query: str, params=(), fetch_all=False, fetch_one=False, commit=False):
    """Master helper to eliminate SQLite boilerplate."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    
    result = None
    if fetch_all:
        result = cursor.fetchall()
    elif fetch_one:
        result = cursor.fetchone()
        
    if commit:
        conn.commit()
        
    conn.close()
    return result

# --- REFACTORED COMMANDS ---

def insert_event(timestamp, category, value, created_at, remind, tags, files, relates_to=None):
    _run_query(
        "INSERT INTO events (timestamp, category, value, created_at, remind, tags, files, relates_to) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (timestamp, category, value, created_at, remind, tags, files, relates_to),
        commit=True
    )

def fetch_all_events():
    return _run_query("SELECT id, timestamp, category, value, remind, tags, files, relates_to FROM events ORDER BY timestamp ASC", fetch_all=True)

def fetch_events_by_date(date):
    return _run_query("SELECT id, timestamp, category, value, remind, tags, files, relates_to FROM events WHERE date(timestamp) = ? ORDER BY timestamp ASC", (date,), fetch_all=True)

def search_events_in_db(query):
    search_term = f"%{query}%"
    return _run_query("SELECT id, timestamp, category, value, remind, tags, files, relates_to FROM events WHERE category LIKE ? OR value LIKE ? OR tags LIKE ? OR files LIKE ? ORDER BY timestamp DESC", (search_term, search_term, search_term, search_term), fetch_all=True)

def fetch_category_stats():
    return _run_query("SELECT category, COUNT(*) as count FROM events GROUP BY category ORDER BY count DESC", fetch_all=True)

def delete_event(event_id):
    _run_query("DELETE FROM events WHERE id = ?", (event_id,), commit=True)
    
def fetch_events_in_range(start_date, end_date, tag=None):
    if tag:
        return _run_query("SELECT id, timestamp, category, value, remind, tags, files, relates_to FROM events WHERE date(timestamp) >= ? AND date(timestamp) <= ? AND tags LIKE ? ORDER BY timestamp ASC", (start_date, end_date, f"%{tag}%"), fetch_all=True)
    return _run_query("SELECT id, timestamp, category, value, remind, tags, files, relates_to FROM events WHERE date(timestamp) >= ? AND date(timestamp) <= ? ORDER BY timestamp ASC", (start_date, end_date), fetch_all=True)

def fetch_file_history(filename):
    search_term = f"%{filename}%"
    return _run_query("SELECT id, timestamp, category, value, remind, tags, files, relates_to FROM events WHERE files LIKE ? OR tags LIKE ? ORDER BY timestamp DESC", (search_term, search_term), fetch_all=True)

def fetch_event_by_id(event_id):
    return _run_query("SELECT * FROM events WHERE id = ?", (event_id,), fetch_one=True)

def update_event(event_id, category, value, tags, files):
    _run_query("UPDATE events SET category = ?, value = ?, tags = ?, files = ? WHERE id = ?", (category, value, tags, files, event_id), commit=True)