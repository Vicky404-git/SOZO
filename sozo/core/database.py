import sqlite3
from pathlib import Path

DB_PATH = Path.home() / ".sozo" / "sozo.db"

def get_connection():
    DB_PATH.parent.mkdir(exist_ok=True)
    return sqlite3.connect(DB_PATH)

def initialize_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            category TEXT NOT NULL,
            value TEXT NOT NULL,
            created_at TEXT NOT NULL,
            remind INTEGER DEFAULT 0,
            reminded INTEGER DEFAULT 0
        )
    """)
    
def fetch_event_by_id(event_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM events WHERE id = ?", (event_id,))
    row = cursor.fetchone()
    conn.close()
    return row

def update_event(event_id, category, value, tags, files):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE events 
        SET category = ?, value = ?, tags = ?, files = ?
        WHERE id = ?
        """,
        (category, value, tags, files, event_id)
    )
    conn.commit()
    conn.close()

    # Migrations for Phase 2.5 & Phase 4
    cursor.execute("PRAGMA table_info(events)")
    columns = [col[1] for col in cursor.fetchall()]
    
    if "tags" not in columns:
        cursor.execute("ALTER TABLE events ADD COLUMN tags TEXT DEFAULT ''")
    if "files" not in columns:
        cursor.execute("ALTER TABLE events ADD COLUMN files TEXT DEFAULT ''")
    if "relates_to" not in columns:
        cursor.execute("ALTER TABLE events ADD COLUMN relates_to INTEGER DEFAULT NULL")

    conn.commit()
    conn.close()

initialize_database()