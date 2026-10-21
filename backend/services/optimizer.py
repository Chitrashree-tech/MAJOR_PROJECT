from .task_engine import select_tasks_for_capacity


def generate_daily_plan(
    tasks,
    effective_hours
):
    result = select_tasks_for_capacity(
        tasks,
        effective_hours
    )

    selected_tasks = result["tasks"]

    current_hour = 9.0

    schedule = []

    for task in selected_tasks:

        hours = float(
            task.get("estimated_hours", 1)
        )

        start_hour = current_hour
        end_hour = current_hour + hours

        schedule.append(
            {
                "task_id": task.get("id"),
                "task_name": task.get("name"),
                "priority": task.get("priority"),
                "estimated_hours": hours,
                "start": format_time(start_hour),
                "end": format_time(end_hour),
                "score": task.get("score", 0)
            }
        )

        current_hour = end_hour

    return {
        "effective_hours": effective_hours,
        "planned_hours": result["total_hours"],
        "remaining_hours": result["remaining_hours"],
        "tasks": schedule
    }


def format_time(decimal_hour):

    hour = int(decimal_hour)
    minutes = int(
        (decimal_hour - hour) * 60
    )

    period = "AM"

    if hour >= 12:
        period = "PM"

    display_hour = hour

    if display_hour > 12:
        display_hour -= 12

    if display_hour == 0:
        display_hour = 12

    return (
        f"{display_hour}:"
        f"{minutes:02d} "
        f"{period}"
    )