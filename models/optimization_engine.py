
from datetime import date, datetime


PRIORITY_WEIGHT = {
    "Critical": 100,
    "High": 75,
    "Medium": 50,
    "Low": 25,
}


def calculate_urgency(deadline):
    """Return urgency on a 0-100 scale."""
    if not deadline:
        return 25.0

    try:
        if isinstance(deadline, datetime):
            deadline_date = deadline.date()
        elif isinstance(deadline, date):
            deadline_date = deadline
        else:
            deadline_date = date.fromisoformat(str(deadline)[:10])

        days_left = (deadline_date - date.today()).days

        if days_left <= 0:
            return 100.0
        if days_left <= 1:
            return 95.0
        if days_left <= 3:
            return 85.0
        if days_left <= 7:
            return 70.0
        if days_left <= 14:
            return 50.0
        return 25.0

    except (ValueError, TypeError):
        return 25.0


def calculate_task_score(task):
    """
    Score a task using priority, urgency, low delay risk,
    and an optional trust score. Result is on a 0-100 scale.
    """
    priority_name = str(task.get("priority", "Medium")).title()
    priority = PRIORITY_WEIGHT.get(priority_name, 50)

    urgency = calculate_urgency(task.get("deadline"))

    delay_probability = float(
        task.get("delay_probability", 0.0)
    )
    delay_probability = min(1.0, max(0.0, delay_probability))

    # Trust score is optional and normalized to 0-1.
    trust = float(task.get("trust_score", 0.0))
    trust = min(1.0, max(0.0, trust))

    score = (
        0.35 * priority
        + 0.35 * urgency
        + 0.20 * (100 * (1 - delay_probability))
        + 0.10 * (100 * trust)
    )

    return round(score, 2)


def _task_id(task):
    return task.get("id", task.get("task_id"))


def _dependencies(task):
    deps = task.get("dependencies", [])
    if deps is None:
        return []
    if not isinstance(deps, (list, tuple, set)):
        deps = [deps]
    return list(deps)


def select_tasks_for_capacity(
    tasks,
    available_hours,
    completed_task_ids=None,
    time_resolution=0.1,
):
    """
    Select the highest-scoring combination using 0/1 Knapsack.

    Tasks are eligible only when every dependency is completed.
    Dependencies must refer to task IDs.

    Each task can be selected at most once.
    Durations use expected_hours when supplied, otherwise
    estimated_hours, otherwise 1 hour.
    """
    available_hours = max(0.0, float(available_hours))
    completed = set(completed_task_ids or [])

    all_tasks = [dict(task) for task in tasks]
    all_ids = {_task_id(task) for task in all_tasks}

    eligible = []
    deferred = []

    for task in all_tasks:
        task_id = _task_id(task)
        dependencies = _dependencies(task)

        # Do not schedule already-completed tasks.
        if task.get("status") == "completed" or task.get("completed") is True:
            continue

        # Also accept dependencies represented as completed task IDs.
        unresolved = [
            dep for dep in dependencies
            if dep not in completed
        ]

        if unresolved:
            task["deferred_reason"] = "Blocked by incomplete dependencies"
            task["blocked_by"] = unresolved
            deferred.append(task)
            continue

        duration = float(
            task.get(
                "expected_hours",
                task.get("estimated_hours", 1.0),
            )
        )

        if duration <= 0:
            task["deferred_reason"] = "Invalid task duration"
            deferred.append(task)
            continue

        task["estimated_hours"] = duration
        task["score"] = calculate_task_score(task)
        task["optimization_score"] = task["score"]

        if duration > available_hours:
            task["deferred_reason"] = "Exceeds available capacity"
            deferred.append(task)
            continue

        eligible.append(task)

    # Dynamic programming with discretized time capacity.
    # Each item is either selected once or not selected.
    resolution = float(time_resolution)
    if resolution <= 0:
        raise ValueError("time_resolution must be positive")

    capacity_units = int(available_hours / resolution)

    items = []
    for task in eligible:
        units = max(
            1,
            int(round(task["estimated_hours"] / resolution)),
        )
        items.append((task, units))

    # dp[c] = (total_score, tuple of selected item indexes)
    dp = [(0.0, ()) for _ in range(capacity_units + 1)]

    for index, (task, units) in enumerate(items):
        for c in range(capacity_units, units - 1, -1):
            previous_score, previous_items = dp[c - units]
            candidate_score = previous_score + task["score"]

            if candidate_score > dp[c][0]:
                dp[c] = (
                    candidate_score,
                    previous_items + (index,),
                )

    _, selected_indexes = max(dp, key=lambda result: result[0])
    selected_index_set = set(selected_indexes)

    selected = [
        task for index, (task, _) in enumerate(items)
        if index in selected_index_set
    ]

    selected_ids = {_task_id(task) for task in selected}

    # Any eligible task not chosen by the optimizer is deferred.
    for index, (task, _) in enumerate(items):
        if index not in selected_index_set:
            task["deferred_reason"] = "Not selected within capacity"
            deferred.append(task)

    selected.sort(
        key=lambda task: task["score"],
        reverse=True,
    )

    planned_hours = sum(
        task["estimated_hours"] for task in selected
    )

    return {
        "tasks": selected,
        "deferred_tasks": deferred,
        "available_hours": round(available_hours, 2),
        "total_hours": round(planned_hours, 2),
        "planned_hours": round(planned_hours, 2),
        "remaining_hours": round(
            max(0.0, available_hours - planned_hours), 2
        ),
        "selected_task_ids": list(selected_ids),
    }


def generate_daily_plan(tasks, available_hours, completed_task_ids=None):
    """Convenience wrapper for the optimization result."""
    return select_tasks_for_capacity(
        tasks=tasks,
        available_hours=available_hours,
        completed_task_ids=completed_task_ids,
    )
