
# utils/csv_utils.py
# Component: CSV storage utilities for Model 4 Adaptive Learning.
# Uses CSV files only; no database is required.

import os
from datetime import datetime

import pandas as pd


PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")

CSV_HEADERS = {
    "adaptive_learning_data.csv": [
        "user_id", "user_name", "date", "day_number", "day_of_week",
        "day_name", "week_number", "sleep_hours", "stress_level",
        "energy_level", "mood_score", "activity_level",
        "screen_time_hours", "available_hours_claimed", "meeting_hours",
        "blocker_reported", "raw_capacity_score", "true_capacity_score",
        "effective_work_hours", "tasks_assigned", "estimated_hours_total",
        "dominant_task_type", "tasks_completed", "actual_hours_total",
        "actual_completion_rate", "commits_today", "prs_merged",
        "issues_closed", "capacity_bias", "estimation_bias",
        "overload_threshold", "rolling_completion_rate", "trust_score",
        "reward"
    ],
    "daily_inputs.csv": [
        "id", "user_id", "date", "day_of_week", "day_name", "week_number",
        "sleep_hours", "stress_level", "energy_level", "mood_score",
        "activity_level", "screen_time_hours", "available_hours_claimed",
        "meeting_hours", "blocker_reported", "created_at"
    ],
    "daily_outcomes.csv": [
        "id", "user_id", "date", "tasks_completed", "actual_hours_total",
        "actual_completion_rate", "commits_today", "prs_merged",
        "issues_closed", "reward", "created_at"
    ],
    "user_profiles.csv": [
        "id", "user_id", "user_name", "date", "day_number",
        "capacity_bias", "estimation_bias", "overload_threshold",
        "rolling_completion_rate", "trust_score", "monday_multiplier",
        "tuesday_multiplier", "wednesday_multiplier", "thursday_multiplier",
        "friday_multiplier", "saturday_multiplier", "sunday_multiplier",
        "updated_at"
    ],
    "github_activity.csv": [
        "id", "user_id", "date", "event_type", "description",
        "linked_task", "repository", "progress_contribution", "created_at"
    ],
    "model_predictions.csv": [
        "id", "user_id", "date", "raw_capacity_score",
        "adjusted_capacity_score", "effective_work_hours",
        "tasks_assigned", "estimated_hours_total", "created_at"
    ]
}

os.makedirs(DATA_DIR, exist_ok=True)


def _path(filename):
    """Resolve a CSV filename inside the project's data directory."""
    if os.path.basename(filename) != filename:
        raise ValueError("Pass a filename, not a path.")
    if filename not in CSV_HEADERS:
        raise ValueError(f"Unsupported CSV filename: {filename}")
    return os.path.join(DATA_DIR, filename)


def initialize_csv_files():
    """Create required CSV files with headers if they do not exist."""
    for filename, headers in CSV_HEADERS.items():
        path = _path(filename)
        if not os.path.exists(path):
            pd.DataFrame(columns=headers).to_csv(path, index=False)


def read_csv(filename):
    """Read a CSV; return an empty DataFrame with headers if unavailable."""
    path = _path(filename)
    if not os.path.exists(path):
        return pd.DataFrame(columns=CSV_HEADERS[filename])
    try:
        return pd.read_csv(path)
    except pd.errors.EmptyDataError:
        return pd.DataFrame(columns=CSV_HEADERS[filename])


def write_csv(df, filename):
    """Write a DataFrame to the specified project CSV."""
    path = _path(filename)
    df.to_csv(path, index=False)


def append_row(row_dict, filename):
    """Append one row, preserving the file's predefined column order."""
    path = _path(filename)
    current = read_csv(filename)
    row = pd.DataFrame([row_dict]).reindex(
        columns=CSV_HEADERS[filename]
    )
    result = pd.concat([current, row], ignore_index=True)
    write_csv(result, filename)


def get_user_profile(user_id):
    """Return the latest saved adaptive profile for a user, or None."""
    df = read_csv("user_profiles.csv")
    if df.empty or "user_id" not in df.columns:
        return None

    matching = df[df["user_id"].astype(str) == str(user_id)]
    if matching.empty:
        return None

    if "updated_at" in matching.columns:
        matching = matching.sort_values("updated_at")
    elif "day_number" in matching.columns:
        matching = matching.sort_values("day_number")

    return matching.iloc[-1].to_dict()


def update_user_profile(user_id, profile_dict):
    """Append a new version of a user's profile to CSV."""
    row = dict(profile_dict)
    row["user_id"] = user_id
    row.setdefault("id", None)
    row.setdefault("updated_at", datetime.now().isoformat(timespec="seconds"))
    append_row(row, "user_profiles.csv")


def get_user_history(user_id, n_days):
    """Return the user's most recent n days of synthetic training history."""
    df = read_csv("adaptive_learning_data.csv")
    if df.empty:
        return df

    matching = df[df["user_id"].astype(str) == str(user_id)].copy()
    if "day_number" in matching.columns:
        matching = matching.sort_values("day_number")
    elif "date" in matching.columns:
        matching = matching.sort_values("date")

    return matching.tail(max(0, int(n_days))).reset_index(drop=True)


def save_daily_input(user_id, input_dict):
    """Save a morning check-in to daily_inputs.csv."""
    row = dict(input_dict)
    row["user_id"] = user_id
    row.setdefault("date", datetime.now().date().isoformat())
    row.setdefault("created_at", datetime.now().isoformat(timespec="seconds"))
    row.setdefault("id", None)
    append_row(row, "daily_inputs.csv")


def save_daily_outcome(user_id, outcome_dict):
    """Save an end-of-day outcome to daily_outcomes.csv."""
    row = dict(outcome_dict)
    row["user_id"] = user_id
    row.setdefault("date", datetime.now().date().isoformat())
    row.setdefault("created_at", datetime.now().isoformat(timespec="seconds"))
    row.setdefault("id", None)
    append_row(row, "daily_outcomes.csv")


initialize_csv_files()
