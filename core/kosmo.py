import time
from datetime import datetime
from .database import get_connection


def check_due_events():
    conn = get_connection()
    cursor = conn.cursor()

    now = datetime.now().isoformat()

    cursor.execute("""
        SELECT id, category, value
        FROM events
        WHERE timestamp <= ?
        AND remind = 1
        AND reminded = 0
    """, (now,))

    rows = cursor.fetchall()

    for event_id, category, value in rows:
        print(f"\n🔔 Reminder: {category} → {value}")
        cursor.execute(
            "UPDATE events SET reminded = 1 WHERE id = ?",
            (event_id,)
        )

    conn.commit()
    conn.close()


def start_kosmo(interval=30):
    print("🌌 Kosmo is watching your timeline...")

    while True:
        check_due_events()
        time.sleep(interval)