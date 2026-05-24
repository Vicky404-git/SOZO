# sozo/core/kosmo.py
# Kosmo — Temporal orchestration engine for Sōzō
# Handles: reminders, scheduling, DaemonV bridge

import socket
import signal
import sys
import time
import datetime
from sozo.core.database import get_connection
from sozo.core.repos import _run_query

DAEMONV_HOST = "localhost"
DAEMONV_PORT = 9333

# Default working hours (configurable later)
START_HOUR = 9
END_HOUR = 17


# =========================================================
# DAEMONV BRIDGE
# =========================================================

def _daemonv_running() -> bool:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            s.connect((DAEMONV_HOST, DAEMONV_PORT))
            return True
    except OSError:
        return False


def _send_to_daemonv(message: str) -> bool:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(2)
            s.connect((DAEMONV_HOST, DAEMONV_PORT))
            s.sendall(f"NOTIFY {message}\n".encode("utf-8"))
            response = s.recv(1024).decode("utf-8")
            return "Notification sent." in response
    except (ConnectionRefusedError, TimeoutError, OSError):
        return False


# =========================================================
# SCHEDULER
# =========================================================

def _get_next_valid_time(current_time: datetime.datetime) -> datetime.datetime:
    """Push time into the next valid working window."""
    if current_time.hour >= END_HOUR:
        next_day = current_time + datetime.timedelta(days=1)
        return next_day.replace(hour=START_HOUR, minute=0, second=0, microsecond=0)
    elif current_time.hour < START_HOUR:
        return current_time.replace(hour=START_HOUR, minute=0, second=0, microsecond=0)
    return current_time


def auto_schedule_tasks() -> list:
    """
    Find all unscheduled tasks with a duration and slot them
    sequentially into working hours (9-5).
    Returns list of (value, scheduled_start_iso, deadline_warning).
    """
    pending = _run_query(
        """SELECT id, value, duration, deadline, priority
           FROM events
           WHERE duration IS NOT NULL AND scheduled_start IS NULL
           ORDER BY priority ASC""",
        fetch_all=True
    )

    if not pending:
        return []

    now = datetime.datetime.now()

    # Start from end of last scheduled block, or right now
    last_scheduled = _run_query(
        """SELECT scheduled_start, duration FROM events
           WHERE scheduled_start >= ?
           ORDER BY scheduled_start DESC LIMIT 1""",
        (now.isoformat(),),
        fetch_one=True
    )

    if last_scheduled and last_scheduled[0]:
        last_start = datetime.datetime.fromisoformat(last_scheduled[0])
        current_slot = last_start + datetime.timedelta(minutes=last_scheduled[1])
    else:
        current_slot = now

    current_slot = _get_next_valid_time(current_slot)

    results = []

    for task in pending:
        task_id, value, duration, deadline_str, priority = task

        # If task bleeds past END_HOUR, push to next morning
        end_slot = current_slot + datetime.timedelta(minutes=duration)
        if end_slot.hour >= END_HOUR:
            current_slot = _get_next_valid_time(
                current_slot.replace(hour=END_HOUR, minute=0, second=0, microsecond=0)
            )

        start_iso = current_slot.isoformat()

        _run_query(
            "UPDATE events SET scheduled_start = ? WHERE id = ?",
            (start_iso, task_id),
            commit=True
        )

        # Check if task will breach its deadline
        warning = False
        if deadline_str:
            try:
                deadline_dt = datetime.datetime.fromisoformat(deadline_str)
                if current_slot + datetime.timedelta(minutes=duration) > deadline_dt:
                    warning = True
            except ValueError:
                pass

        results.append((value, start_iso, warning))

        current_slot = _get_next_valid_time(
            current_slot + datetime.timedelta(minutes=duration)
        )

    return results


# =========================================================
# KOSMO ENGINE
# =========================================================

class KosmoEngine:
    """
    Temporal orchestration engine for Sōzō.
    Bridges the SOZO timeline with DaemonV notifications.
    """

    def __init__(self, interval: int = 30):
        self.interval = interval

    def run(self):
        signal.signal(signal.SIGINT, self._shutdown)

        status = "DaemonV connected" if _daemonv_running() else "terminal fallback"
        print(f"🌌 Kosmo awakened ({status})")

        while True:
            self.check_due_events()
            time.sleep(self.interval)

    def check_due_events(self):
        """Fire reminders for due events AND auto-scheduled task prompts."""
        conn = get_connection()
        cursor = conn.cursor()
        now = datetime.datetime.now().isoformat()

        cursor.execute("""
            SELECT id, category, value
            FROM events
            WHERE (
                (timestamp <= ? AND remind = 1)
                OR
                (scheduled_start <= ? AND scheduled_start IS NOT NULL)
            )
            AND reminded = 0
        """, (now, now))

        rows = cursor.fetchall()

        for event_id, category, value in rows:
            message = f"{category} → {value}"
            self.send_nudge(message)
            cursor.execute(
                "UPDATE events SET reminded = 1 WHERE id = ?",
                (event_id,)
            )

        conn.commit()
        conn.close()

    def send_nudge(self, message: str):
        """Send via DaemonV desktop notification, fall back to terminal."""
        if _send_to_daemonv(message):
            print(f"✨ DaemonV: {message}")
        else:
            print(f"🔔 Reminder: {message}")

    def _shutdown(self, signum, frame):
        print("\n👋 Kosmo entering silence.")
        sys.exit(0)


# =========================================================
# ENTRYPOINTS
# =========================================================

def start_kosmo(interval: int = 30):
    """Called by: sozo kosmo"""
    KosmoEngine(interval).run()
