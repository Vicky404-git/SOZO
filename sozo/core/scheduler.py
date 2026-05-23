import datetime
from sozo.core.repos import _run_query

# Default Working Hours (We can make this customizable later)
START_HOUR = 9
END_HOUR = 17

def _get_next_valid_time(current_time):
    """Pushes time to the next working window if outside hours."""
    if current_time.hour >= END_HOUR:
        # Move to next day 9 AM
        next_day = current_time + datetime.timedelta(days=1)
        return next_day.replace(hour=START_HOUR, minute=0, second=0, microsecond=0)
    elif current_time.hour < START_HOUR:
        return current_time.replace(hour=START_HOUR, minute=0, second=0, microsecond=0)
    return current_time

def auto_schedule_tasks():
    """Finds all unscheduled tasks and slots them into available working hours."""
    
    # 1. Fetch un-scheduled tasks that have a duration requirement
    pending = _run_query(
        """SELECT id, value, duration, deadline, priority 
           FROM events 
           WHERE duration IS NOT NULL AND scheduled_start IS NULL 
           ORDER BY priority ASC""",
        fetch_all=True
    )
    
    if not pending:
        return []

    # 2. Get the end time of the last scheduled task, or start from right now
    now = datetime.datetime.now()
    last_scheduled = _run_query(
        "SELECT scheduled_start, duration FROM events WHERE scheduled_start >= ? ORDER BY scheduled_start DESC LIMIT 1",
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

    # 3. Stack tasks sequentially into the calendar
    for task in pending:
        task_id, value, duration, deadline_str, priority = task
        
        # If the task bleeds past 5 PM, push it to 9 AM the next morning
        end_slot = current_slot + datetime.timedelta(minutes=duration)
        if end_slot.hour >= END_HOUR or (end_slot.hour == END_HOUR and end_slot.minute > 0):
            current_slot = _get_next_valid_time(current_slot.replace(hour=END_HOUR))
        
        start_iso = current_slot.isoformat()
        
        # Update Sōzō Database
        _run_query("UPDATE events SET scheduled_start = ? WHERE id = ?", (start_iso, task_id), commit=True)
        
        # Deadline Check (The ultimate warning system)
        warning = False
        if deadline_str:
            try:
                deadline_dt = datetime.datetime.fromisoformat(deadline_str)
                if current_slot + datetime.timedelta(minutes=duration) > deadline_dt:
                    warning = True
            except ValueError:
                pass # Fallback if user typed bad date string
        
        results.append((value, start_iso, warning))
        
        # Move the time cursor forward for the next task
        current_slot = current_slot + datetime.timedelta(minutes=duration)
        current_slot = _get_next_valid_time(current_slot)

    return results
