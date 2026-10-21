
from pathlib import Path
import joblib
import pandas as pd


# Locate the saved model files
BASE_DIR = Path(__file__).resolve().parent
MODEL_DIR = BASE_DIR / "task_model_artifacts"

difficulty_model = joblib.load(
    MODEL_DIR / "difficulty_model_v2.joblib"
)

duration_model = joblib.load(
    MODEL_DIR / "duration_model_v2.joblib"
)

delay_model = joblib.load(
    MODEL_DIR / "delay_model_v2.joblib"
)


def predict_task(task: dict) -> dict:
    """
    Predict task difficulty, duration, and delay risk.

    The feature names must match those used during training.
    """

    title = task.get("title", "")
    description = task.get("description", "")
    components = task.get("components_text", "")

    row = {
        "model_text": (
            f"{title} {description} {components}"
        ),
        "Type": task.get("type", "Task"),
        "Priority": task.get("priority", "Medium"),
        "Project_ID": str(task.get("project_id", "unknown")),
        "Story_Point": task.get("story_point"),
        "Comment_Count": task.get("comment_count", 0),
        "Link_Count": task.get("link_count", 0),
        "Created_Month": task.get("created_month", 10),
        "Created_Year": task.get("created_year", 2026),
    }

    X = pd.DataFrame([row])

    difficulty = difficulty_model.predict(X)[0]
    duration = float(duration_model.predict(X)[0])

    delay_probability = None

    if hasattr(delay_model, "predict_proba"):
        probabilities = delay_model.predict_proba(X)[0]
        classes = list(delay_model.classes_)

        # Find the probability of the positive/delay class.
        # Verify the positive label in your training cell.
        positive_labels = [
            label for label in classes
            if str(label).lower() in {"1", "true", "delayed", "delay"}
        ]

        if positive_labels:
            index = classes.index(positive_labels[0])
            delay_probability = float(probabilities[index])

    return {
        "difficulty": str(difficulty),
        "expected_duration_days": round(max(0, duration), 2),
        "delay_probability": (
            round(delay_probability, 4)
            if delay_probability is not None else None
        ),
    }
