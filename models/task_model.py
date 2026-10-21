
from pathlib import Path

import joblib
import numpy as np
import pandas as pd


MODEL_DIR = Path(__file__).resolve().parent / "task_model_artifacts"

# Load trained models
difficulty_model = joblib.load(
    MODEL_DIR / "difficulty_model.joblib"
)

duration_model = joblib.load(
    MODEL_DIR / "duration_model.joblib"
)

delay_model = joblib.load(
    MODEL_DIR / "delay_model.joblib"
)


def predict_task(
    title: str,
    description: str = "",
    task_type: str = "Unknown",
    priority: str = "Unknown",
    project_id: str = "Unknown",
    story_point: float = 0,
    comment_count: int = 0,
    link_count: int = 0,
    created_month: int = 1,
    created_year: int = 2026,
):
    features = pd.DataFrame([{
        "model_text": f"{title} {description}",
        "Type": task_type or "Unknown",
        "Priority": priority or "Unknown",
        "Project_ID": str(project_id or "Unknown"),
        "Story_Point": story_point,
        "Comment_Count": comment_count,
        "Link_Count": link_count,
        "Created_Month": created_month,
        "Created_Year": created_year,
    }])

    difficulty = difficulty_model.predict(features)[0]

    # Duration model was trained using log1p(duration in days)
    predicted_log_duration = duration_model.predict(features)[0]
    duration_days = max(
        0.0,
        float(np.expm1(predicted_log_duration))
    )

    delay_prediction = delay_model.predict(features)[0]

    delay_probability = None

    if hasattr(delay_model, "predict_proba"):
        probabilities = delay_model.predict_proba(features)[0]
        classes = list(delay_model.classes_)

        for index, label in enumerate(classes):
            if str(label).lower() in {
                "1", "true", "yes", "delay", "delayed", "high"
            }:
                delay_probability = float(probabilities[index])
                break

    return {
        "difficulty": str(difficulty),
        "predicted_duration_days": round(duration_days, 2),
        "delay_risk": str(delay_prediction),
        "delay_probability": (
            round(delay_probability, 4)
            if delay_probability is not None
            else None
        ),
    }
