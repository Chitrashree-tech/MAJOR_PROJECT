from datetime import datetime, timedelta


PRIORITY_WEIGHT = {
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

        days_left = (
            deadline_date - datetime.today().date()
        ).days

        if days_left <= 0:
            return 100
        elif days_left <= 1:
            return 95
        elif days_left <= 3:
            return 85
        elif days_left <= 7:
            return 70
        elif days_left <= 14:
            return 50
        else:
            return 25

    except ValueError:
        return 0


def calculate_task_score(task):
    priority = PRIORITY_WEIGHT.get(
        task.get("priority", "Medium"),
        50
    )

    urgency = calculate_urgency(
        task.get("deadline")
    )

    dependency_count = task.get(
        "dependency_count",
        0
    )

    dependency_score = min(
        dependency_count * 10,
        100
    )

    score = (
        priority * 0.50
        + urgency * 0.35
        + dependency_score * 0.15
    )

    return round(score, 2)


def rank_tasks(tasks):
    ranked = []

    for task in tasks:
        task_copy = task.copy()

        task_copy["optimization_score"] = (
            calculate_task_score(task_copy)
        )

        ranked.append(task_copy)

    ranked.sort(
        key=lambda x: x["optimization_score"],
        reverse=True
    )

    return ranked


def generate_daily_plan(
    tasks,
    available_hours
):
    ranked_tasks = rank_tasks(tasks)

    selected_tasks = []
    total_hours = 0

    for task in ranked_tasks:

        estimated_hours = float(
            task.get(
                "estimated_hours",
                1
            )
        )

        if (
            total_hours + estimated_hours
            <= available_hours
        ):
            selected_tasks.append(task)

            total_hours += estimated_hours

    return {
        "tasks": selected_tasks,
        "available_hours": round(
            available_hours,
            2
        ),
        "planned_hours": round(
            total_hours,
            2
        ),
        "remaining_hours": round(
            available_hours - total_hours,
            2
        )
    }