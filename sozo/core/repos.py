from sozo.core.database import get_connection

def insert_event(timestamp, category, value, created_at, remind, tags, files):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO events (timestamp, category, value, created_at, remind, tags, files)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (timestamp, category, value, created_at, remind, tags, files),
    )
    conn.commit()
    conn.close()

def fetch_all_events():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, timestamp, category, value, remind, tags, files
        FROM events ORDER BY timestamp ASC
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows

def fetch_events_by_date(date):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, timestamp, category, value, remind, tags, files
        FROM events WHERE date(timestamp) = ? ORDER BY timestamp ASC
    """, (date,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def search_events_in_db(query):
    conn = get_connection()
    cursor = conn.cursor()
    search_term = f"%{query}%"
    cursor.execute("""
        SELECT id, timestamp, category, value, remind, tags, files
        FROM events 
        WHERE category LIKE ? OR value LIKE ? OR tags LIKE ? OR files LIKE ?
        ORDER BY timestamp DESC
    """, (search_term, search_term, search_term, search_term))
    rows = cursor.fetchall()
    conn.close()
    return rows

def fetch_category_stats():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT category, COUNT(*) as count FROM events GROUP BY category ORDER BY count DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows

def delete_event(event_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM events WHERE id = ?", (event_id,))
    conn.commit()
    conn.close()