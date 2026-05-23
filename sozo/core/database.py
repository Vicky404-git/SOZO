import sqlite3
from sozo.core.config import DB_PATH

def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
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

    # Migrations
    cursor.execute("PRAGMA table_info(events)")
    columns = [col[1] for col in cursor.fetchall()]
    
    if "tags" not in columns:
        cursor.execute("ALTER TABLE events ADD COLUMN tags TEXT DEFAULT ''")
    if "files" not in columns:
        cursor.execute("ALTER TABLE events ADD COLUMN files TEXT DEFAULT ''")
    if "relates_to" not in columns:
        cursor.execute("ALTER TABLE events ADD COLUMN relates_to INTEGER DEFAULT NULL")
        
    # --- V2 TIMETABLE MIGRATIONS ---
    if "duration" not in columns:
        cursor.execute("ALTER TABLE events ADD COLUMN duration INTEGER DEFAULT NULL")
    if "deadline" not in columns:
        cursor.execute("ALTER TABLE events ADD COLUMN deadline TEXT DEFAULT NULL")
    if "priority" not in columns:
        cursor.execute("ALTER TABLE events ADD COLUMN priority INTEGER DEFAULT 2") # 1=High, 2=Med, 3=Low
    if "scheduled_start" not in columns:
        cursor.execute("ALTER TABLE events ADD COLUMN scheduled_start TEXT DEFAULT NULL")

    conn.commit()
    conn.close()

