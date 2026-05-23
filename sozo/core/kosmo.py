import socket
import signal
import sys
import time
from datetime import datetime
from sozo.core.database import get_connection

DAEMONV_HOST = "localhost"
DAEMONV_PORT = 9333

def _daemonv_running() -> bool:
    """Check if DaemonV is reachable before trying to send."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            s.connect((DAEMONV_HOST, DAEMONV_PORT))
            return True
    except OSError:
        return False

def _send_to_daemonv(message: str) -> bool:
    """Send a reminder command to DaemonV's control server."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(2)
            s.connect((DAEMONV_HOST, DAEMONV_PORT))
            
            # Send the exact command Java expects
            s.sendall(f"NOTIFY {message}\n".encode("utf-8"))
            
            # Check if DaemonV actually understood the command
            response = s.recv(1024).decode("utf-8")
            if "Notification sent." in response:
                return True
            else:
                return False
    except (ConnectionRefusedError, TimeoutError, OSError):
        return False

def check_due_events():
    conn = get_connection()
    cursor = conn.cursor()
    now = datetime.now().isoformat()

    # V2 UPGRADE: Check both explicit reminders AND auto-scheduled tasks
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
        message = f"[{category.upper()}] {value}"
        
        # Try to send to DaemonV
        if _send_to_daemonv(message):
            # Success! Tell the terminal it sent the popup
            print(f"\n✨ Auto-Schedule Prompt: {message}")
        else:
            # Failure! Fall back to a standard terminal reminder
            print(f"\n🔔 Terminal Reminder: {message}")

        # Mark as reminded so it doesn't spam you
        cursor.execute(
            "UPDATE events SET reminded = 1 WHERE id = ?",
            (event_id,)
        )

    conn.commit()
    conn.close()

def start_kosmo(interval=30):
    # Graceful shutdown
    signal.signal(signal.SIGINT, lambda s, f: (
        print("\n👋 Kosmo stopped."), sys.exit(0)
    ))
    
    daemonv_status = "via DaemonV" if _daemonv_running() else "terminal fallback"
    print(f"🌌 Kosmo is watching your timeline... ({daemonv_status})")

    while True:
        check_due_events()
        time.sleep(interval)
