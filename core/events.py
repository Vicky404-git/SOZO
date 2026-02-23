from datetime import datetime
import dateparser
from .database import get_connection


def parse_datetime(dt: str | None):
    if dt is None:
        return datetime.now()

    parsed = dateparser.parse(dt)

    if parsed is None:
        raise ValueError(
            "Invalid date. Try formats like '2026-03-03 18:00', "
            "'tomorrow 5pm', '3 march', 'next monday 7am'."
        )

    return parsed


def add_event(category, value, at=None, remind=False):
    conn = get_connection()
    cursor = conn.cursor()

    event_time = parse_datetime(at)
    now = datetime.now()

    cursor.execute(
        """
        INSERT INTO events (timestamp, category, value, created_at, remind)
        VALUES (?, ?, ?, ?, ?)
        """,
        (event_time.isoformat(), category, value, now.isoformat(), int(remind)),
    )

    conn.commit()
    conn.close()


def get_events_by_date(date_str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT timestamp, category, value
        FROM events
        WHERE date(timestamp) = ?
        ORDER BY timestamp ASC
    """, (date_str,))

    rows = cursor.fetchall()
    conn.close()
    return rows


def get_calendar_summary():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT date(timestamp), COUNT(*)
        FROM events
        GROUP BY date(timestamp)
        ORDER BY date(timestamp) DESC
    """)

    rows = cursor.fetchall()
    conn.close()
    return rows