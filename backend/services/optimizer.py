
from datetime import datetime, timedelta

from models.optimization_engine import select_tasks_for_capacity


def format_time(value):
    """Format a datetime as a readable time."""
    return value.strftime("%I:%M %p").lstrip("0")


def generate_daily_plan(
    tasks,
    effective_hours,
    completed_task_ids=None,
    meeting_hours=0.0,
    start_time="09:00",
):
    """
    Generate a daily schedule using the optimization engine.

    effective_hours: work capacity before meetings.
    meeting_hours: hours reserved for meetings.
    """
    effective_hours = max(0.0, float(effective_hours))
    meeting_hours = max(0.0, float(meeting_hours))

    available_hours = max(
        0.0,
        effective_hours - meeting_hours,
    )

    result = select_tasks_for_capacity(
        tasks=tasks,
        available_hours=available_hours,
        completed_task_ids=completed_task_ids,
    )

    current_time = datetime.strptime(start_time, "%H:%M")
    schedule = []

    for task in result["tasks"]:
        duration = float(task["estimated_hours"])
        end_time = current_time + timedelta(hours=duration)

        schedule.append({
            "task_id": task.get("id", task.get("task_id")),
            "task_name": task.get(
                "name",
                task.get("title", "Untitled task"),
            ),
            "priority": task.get("priority", "Medium"),
            "estimated_hours": round(duration, 2),
            "delay_probability": float(
                task.get("delay_probability", 0.0)
            ),
            "score": task.get("score", 0),
            "start": format_time(current_time),
            "end": format_time(end_time),
        })

        current_time = end_time

    return {
        "effective_hours": round(effective_hours, 2),
        "meeting_hours": round(meeting_hours, 2),
        "available_hours": round(available_hours, 2),
        "planned_hours": result["planned_hours"],
        "remaining_hours": result["remaining_hours"],
        "tasks": schedule,
        "deferred_tasks": result["deferred_tasks"],
    }
