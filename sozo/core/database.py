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

    # Migrations for Phase 2.5
    cursor.execute("PRAGMA table_info(events)")
    columns = [col[1] for col in cursor.fetchall()]
    
    if "tags" not in columns:
        cursor.execute("ALTER TABLE events ADD COLUMN tags TEXT DEFAULT ''")
    if "files" not in columns:
        cursor.execute("ALTER TABLE events ADD COLUMN files TEXT DEFAULT ''")

    conn.commit()
    conn.close()

initialize_database()