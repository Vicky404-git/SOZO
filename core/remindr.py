from datetime import datetime
from .database import get_connection


def get_upcoming_events():
    conn = get_connection()
    cursor = conn.cursor()

    now = datetime.now().isoformat()

    cursor.execute("""
        SELECT id, timestamp, category, value
        FROM events
        WHERE timestamp <= ?
        AND reminded = 0
    """, (now,))

    rows = cursor.fetchall()
    conn.close()
    return rows


def mark_as_reminded(event_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE events SET reminded = 1 WHERE id = ?",
        (event_id,),
    )

    conn.commit()
    conn.close()