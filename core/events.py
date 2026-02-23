from datetime import datetime
from .database import get_connection

def add_event(category: str, value: str):
    conn = get_connection()
    cursor = conn.cursor()

    timestamp = datetime.now().isoformat()

    cursor.execute(
        "INSERT INTO events (timestamp, category, value) VALUES (?, ?, ?)",
        (timestamp, category, value),
    )

    conn.commit()
    conn.close()

def get_today_events():
    conn = get_connection()
    cursor = conn.cursor()

    today_date = datetime.now().date().isoformat()

    cursor.execute(
        "SELECT timestamp, category, value FROM events WHERE date(timestamp) = ? ORDER BY timestamp ASC",
        (today_date,),
    )

    rows = cursor.fetchall()
    conn.close()

    return rows