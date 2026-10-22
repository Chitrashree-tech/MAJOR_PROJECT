
import os
import joblib
import numpy as np
import pandas as pd
from datetime import date, datetime

from utils.csv_utils import (
    get_user_profile,
    update_user_profile,
)


class AdaptiveLearner:
    """Updates user profiles and adapts workload recommendations over time."""

    def __init__(self):
        self.user_profiles = {}

        self.project_root = os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        )
        self.data_dir = os.path.join(self.project_root, "data")
        self.models_dir = os.path.join(self.project_root, "models")

        self.learning_rate = 0.15

        self.weekday_names = [
            "Monday", "Tuesday", "Wednesday", "Thursday",
            "Friday", "Saturday", "Sunday"
        ]

        self.default_multipliers = {
            "Monday": 0.78,
            "Tuesday": 0.92,
            "Wednesday": 1.00,
            "Thursday": 0.90,
            "Friday": 0.72,
            "Saturday": 0.55,
            "Sunday": 0.50,
        }

    # ---------------------------------------------------------
    # PROFILE MANAGEMENT
    # ---------------------------------------------------------

    def get_default_profile(self, user_id):
        """Return the initial profile for a new user."""

        return {
            "user_id": user_id,
            "user_name": str(user_id),
            "capacity_bias": 0.0,
            "estimation_bias": 1.0,
            "overload_threshold": 6,
            "avg_completion_rate": 0.70,
            "rolling_completion_rate": 0.70,
            "trust_score": 0.50,
            "days_tracked": 0,
            "day_multipliers": self.default_multipliers.copy(),
        }

    def _get_profile(self, user_id):
        """Load a profile from memory or CSV, or create a default."""

        key = str(user_id)

        if key in self.user_profiles:
            return self.user_profiles[key]

        profile = None

        try:
            profile = get_user_profile(user_id)
        except (TypeError, ValueError, KeyError, FileNotFoundError):
            profile = None

        if profile:
            profile = self._profile_from_row(user_id, profile)
        else:
            profile = self.get_default_profile(user_id)

        self.user_profiles[key] = profile
        return profile

    def _profile_from_row(self, user_id, row):
        """Convert a CSV profile row into the internal profile format."""

        profile = self.get_default_profile(user_id)

        for field in [
            "user_name",
            "capacity_bias",
            "estimation_bias",
            "overload_threshold",
            "rolling_completion_rate",
            "trust_score",
        ]:
            if field in row and pd.notna(row[field]):
                try:
                    if field == "user_name":
                        profile[field] = str(row[field])
                    elif field == "overload_threshold":
                        profile[field] = int(float(row[field]))
                    else:
                        profile[field] = float(row[field])
                except (TypeError, ValueError):
                    pass

        profile["avg_completion_rate"] = profile[
            "rolling_completion_rate"
        ]

        if "days_tracked" in row and pd.notna(row["days_tracked"]):
            try:
                profile["days_tracked"] = int(float(row["days_tracked"]))
            except (TypeError, ValueError):
                pass
        elif "day_number" in row and pd.notna(row["day_number"]):
            try:
                profile["days_tracked"] = int(float(row["day_number"]))
            except (TypeError, ValueError):
                pass

        for day in self.weekday_names:
            column = f"{day.lower()}_multiplier"
            if column in row and pd.notna(row[column]):
                try:
                    profile["day_multipliers"][day] = float(row[column])
                except (TypeError, ValueError):
                    pass

        return profile

    def load_profile_from_csv(self, user_id):
        """Reload the user's latest saved profile."""

        try:
            row = get_user_profile(user_id)
        except (TypeError, ValueError, KeyError, FileNotFoundError):
            row = None

        if not row:
            return self.get_default_profile(user_id)

        profile = self._profile_from_row(user_id, row)
        self.user_profiles[str(user_id)] = profile
        return profile

    def _save_profile(self, user_id, profile):
        """Persist the profile through the project's CSV utility."""

        today = date.today().isoformat()
        multipliers = profile["day_multipliers"]

        row = {
            "user_id": user_id,
            "user_name": profile.get("user_name", str(user_id)),
            "date": today,
            "day_number": profile["days_tracked"],
            "capacity_bias": profile["capacity_bias"],
            "estimation_bias": profile["estimation_bias"],
            "overload_threshold": profile["overload_threshold"],
            "rolling_completion_rate": profile["rolling_completion_rate"],
            "trust_score": profile["trust_score"],
        }

        for day in self.weekday_names:
            row[f"{day.lower()}_multiplier"] = multipliers[day]

        try:
            update_user_profile(user_id, row)
        except TypeError:
            # Supports utilities whose update function accepts only a row.
            update_user_profile(row)

    # ---------------------------------------------------------
    # DAILY LEARNING
    # ---------------------------------------------------------

    def update(self, user_id, day_data):
        """
        Update a profile using observed end-of-day results.

        Expected keys:
        predicted_capacity, actual_completion_rate, tasks_assigned,
        tasks_completed, sleep, stress, energy, day_of_week,
        estimated_hours, actual_hours.
        """

        profile = self._get_profile(user_id)
        lr = self.learning_rate

        predicted_capacity = float(
            day_data.get("predicted_capacity", 0.0) or 0.0
        )
        completion_rate = float(
            day_data.get("actual_completion_rate", 0.0) or 0.0
        )
        tasks_assigned = int(day_data.get("tasks_assigned", 0) or 0)
        tasks_completed = int(day_data.get("tasks_completed", 0) or 0)

        estimated_hours = float(
            day_data.get("estimated_hours", 0.0) or 0.0
        )
        actual_hours = float(
            day_data.get("actual_hours", 0.0) or 0.0
        )

        completion_rate = float(np.clip(completion_rate, 0.0, 1.0))
        predicted_capacity = float(
            np.clip(predicted_capacity, 0.0, 1.0)
        )

        # 1. Learn capacity bias from the difference between
        # predicted capacity and observed completion.
        capacity_error = completion_rate - predicted_capacity
        profile["capacity_bias"] = float(
            np.clip(
                profile["capacity_bias"] + lr * capacity_error,
                -0.5,
                0.5,
            )
        )

        # 2. Adjust the task-count threshold according to overload.
        if tasks_assigned > 0:
            if completion_rate < 0.50:
                profile["overload_threshold"] = max(
                    1, profile["overload_threshold"] - 1
                )
            elif completion_rate >= 0.90:
                profile["overload_threshold"] = min(
                    20, profile["overload_threshold"] + 1
                )

        # 3. Learn whether task-time estimates are too high or low.
        if estimated_hours > 0 and actual_hours > 0:
            observed_ratio = actual_hours / estimated_hours
            observed_ratio = float(np.clip(observed_ratio, 0.5, 2.0))

            profile["estimation_bias"] = float(
                np.clip(
                    (1 - lr) * profile["estimation_bias"]
                    + lr * observed_ratio,
                    0.5,
                    2.0,
                )
            )

        # 4. Update the weekday multiplier.
        day = day_data.get("day_of_week")

        if isinstance(day, (int, np.integer)):
            day = self.weekday_names[int(day) % 7]
        elif isinstance(day, str):
            day = day.capitalize()

        if day in profile["day_multipliers"]:
            target_multiplier = float(
                np.clip(0.5 + completion_rate * 0.5, 0.5, 1.0)
            )

            current = profile["day_multipliers"][day]
            profile["day_multipliers"][day] = float(
                np.clip(
                    (1 - lr) * current + lr * target_multiplier,
                    0.3,
                    1.2,
                )
            )

        # 5. Update rolling completion rate.
        previous_rate = profile["rolling_completion_rate"]
        profile["rolling_completion_rate"] = float(
            (1 - lr) * previous_rate + lr * completion_rate
        )
        profile["avg_completion_rate"] = profile[
            "rolling_completion_rate"
        ]

        # 6. Update trust in predictions using observed accuracy.
        prediction_accuracy = 1.0 - abs(capacity_error)
        profile["trust_score"] = float(
            np.clip(
                (1 - lr) * profile["trust_score"]
                + lr * prediction_accuracy,
                0.0,
                1.0,
            )
        )

        profile["days_tracked"] += 1
        profile["user_name"] = day_data.get(
            "user_name", profile.get("user_name", str(user_id))
        )

        self.user_profiles[str(user_id)] = profile
        self._save_profile(user_id, profile)

        return profile

    # ---------------------------------------------------------
    # ADAPTIVE WORKLOAD METHODS
    # ---------------------------------------------------------

    def get_adjusted_capacity(self, user_id, raw_capacity, day_of_week):
        """Apply personal capacity bias, weekday pattern and trust."""

        profile = self._get_profile(user_id)

        capacity = float(raw_capacity) + profile["capacity_bias"]

        if isinstance(day_of_week, (int, np.integer)):
            day = self.weekday_names[int(day_of_week) % 7]
        else:
            day = str(day_of_week).capitalize()

        multiplier = profile["day_multipliers"].get(day, 1.0)

        # Low trust reduces the strength of personalization.
        personalization_strength = 0.5 + 0.5 * profile["trust_score"]
        adjusted = 0.5 + (capacity * multiplier - 0.5) * (
            personalization_strength
        )

        return float(np.clip(adjusted, 0.1, 1.0))

    def get_adjusted_task_time(self, user_id, model2_estimate):
        """Adjust Model 2's task-time estimate using learned bias."""

        profile = self._get_profile(user_id)
        return max(0.0, float(model2_estimate) * profile["estimation_bias"])

    def get_max_tasks(self, user_id):
        """Return the user's current recommended task-count threshold."""

        profile = self._get_profile(user_id)
        return int(profile["overload_threshold"])

    # ---------------------------------------------------------
    # NEXT-DAY RANDOM FOREST PREDICTION
    # ---------------------------------------------------------

    def predict_next_day(self, user_id, today_features_dict):
        """Predict next-day completion rate using the trained Model 4 RF."""

        model_path = os.path.join(
            self.models_dir, "model4_adaptive.pkl"
        )
        scaler_path = os.path.join(
            self.models_dir, "model4_scaler.pkl"
        )
        features_path = os.path.join(
            self.models_dir, "model4_features.pkl"
        )

        if not all(
            os.path.exists(path)
            for path in [model_path, scaler_path, features_path]
        ):
            raise FileNotFoundError(
                "Model 4 artifacts are missing. Place model4_adaptive.pkl, "
                "model4_scaler.pkl and model4_features.pkl in the models/ "
                "directory."
            )

        model = joblib.load(model_path)
        scaler = joblib.load(scaler_path)
        feature_names = joblib.load(features_path)

        profile = self._get_profile(user_id)

        values = {
            "sleep_hours": today_features_dict.get("sleep_hours",
                               today_features_dict.get("sleep", 7.0)),
            "stress_level": today_features_dict.get("stress_level",
                               today_features_dict.get("stress", 5.0)),
            "energy_level": today_features_dict.get("energy_level",
                               today_features_dict.get("energy", 5.0)),
            "mood_score": today_features_dict.get("mood_score", 5.0),
            "activity_level": today_features_dict.get("activity_level", 5.0),
            "day_of_week": today_features_dict.get(
                "day_of_week", datetime.today().weekday()
            ),
            "week_number": today_features_dict.get("week_number", 1),
            "tasks_assigned": today_features_dict.get("tasks_assigned", 0),
            "estimated_hours_total": today_features_dict.get(
                "estimated_hours_total",
                today_features_dict.get("estimated_hours", 0.0),
            ),
            "capacity_bias": profile["capacity_bias"],
            "estimation_bias": profile["estimation_bias"],
            "rolling_completion_rate": profile["rolling_completion_rate"],
            "trust_score": profile["trust_score"],
            "commits_today": today_features_dict.get("commits_today", 0),
            "meeting_hours": today_features_dict.get("meeting_hours", 0.0),
            "blocker_reported": today_features_dict.get(
                "blocker_reported", 0
            ),
        }

        input_df = pd.DataFrame(
            [[values.get(name, 0.0) for name in feature_names]],
            columns=feature_names,
        )

        scaled_input = scaler.transform(input_df)
        prediction = float(model.predict(scaled_input)[0])

        return float(np.clip(prediction, 0.0, 1.0))

    # ---------------------------------------------------------
    # PROFILE INSIGHTS
    # ---------------------------------------------------------

    def get_profile_summary(self, user_id):
        """Return profile values and human-readable insights."""

        profile = self._get_profile(user_id)

        capacity_bias = profile["capacity_bias"]
        estimation_bias = profile["estimation_bias"]
        completion = profile["rolling_completion_rate"]

        if capacity_bias > 0.05:
            capacity_insight = "Observed completion is generally above predictions."
        elif capacity_bias < -0.05:
            capacity_insight = "Observed completion is generally below predictions."
        else:
            capacity_insight = "Capacity predictions are reasonably aligned."

        percentage = (estimation_bias - 1.0) * 100

        if percentage > 5:
            estimation_insight = (
                f"Task durations tend to be underestimated by about "
                f"{percentage:.1f}%."
            )
        elif percentage < -5:
            estimation_insight = (
                f"Task durations tend to be overestimated by about "
                f"{abs(percentage):.1f}%."
            )
        else:
            estimation_insight = "Task-time estimates are reasonably aligned."

        multipliers = profile["day_multipliers"]
        peak_day = max(multipliers, key=multipliers.get)

        return {
            "user_id": user_id,
            "days_tracked": profile["days_tracked"],
            "capacity_bias": round(capacity_bias, 3),
            "estimation_bias": round(estimation_bias, 3),
            "overload_threshold": profile["overload_threshold"],
            "rolling_completion_rate": round(completion, 3),
            "trust_score": round(profile["trust_score"], 3),
            "peak_weekday": peak_day,
            "capacity_insight": capacity_insight,
            "estimation_insight": estimation_insight,
        }
