from datetime import datetime


PRIORITY_SCORE = {
    "Critical": 100,
    "High": 75,
    "Medium": 50,
    "Low": 25
}


def calculate_urgency(deadline):
    if not deadline:
        return 0

    try:
        deadline_date = datetime.strptime(
            deadline,
            "%Y-%m-%d"
        ).date()

        days_remaining = (
            deadline_date - datetime.today().date()
        ).days

        if days_remaining <= 0:
            return 100

        if days_remaining <= 2:
            return 90

        if days_remaining <= 5:
            return 70

        if days_remaining <= 10:
            return 50

        return 25

    except ValueError:
        return 0


def calculate_task_score(task):
    priority = PRIORITY_SCORE.get(
        task.get("priority", "Medium"),
        50
    )

    urgency = calculate_urgency(
        task.get("deadline")
    )

    dependency_score = (
        task.get("dependency_count", 0) * 10
    )

    return (
        priority * 0.5
        + urgency * 0.35
        + dependency_score * 0.15
    )


def rank_tasks(tasks):
    ranked_tasks = []

    for task in tasks:

        task_copy = task.copy()

        task_copy["score"] = round(
            calculate_task_score(task_copy),
            2
        )

        ranked_tasks.append(
            task_copy
        )

    ranked_tasks.sort(
        key=lambda task: task["score"],
        reverse=True
    )

    return ranked_tasks


def select_tasks_for_capacity(
    tasks,
    available_hours
):
    ranked_tasks = rank_tasks(tasks)

    selected = []
    total_hours = 0

    for task in ranked_tasks:

        hours = float(
            task.get("estimated_hours", 1)
        )

        if total_hours + hours <= available_hours:

            selected.append(task)
            total_hours += hours

    return {
        "tasks": selected,
        "total_hours": round(total_hours, 2),
        "remaining_hours": round(
            available_hours - total_hours,
            2
        )
    }