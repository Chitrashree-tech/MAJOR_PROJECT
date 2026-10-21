
from pathlib import Path

import joblib
import pandas as pd


class BehavioralCapacityModel:
    """
    Loads the trained behavioral stress classifier and converts
    its elevated-stress probability into a provisional capacity score.
    """

    def __init__(self, model_path=None, reference_hours=8.0):
        project_models_dir = Path(__file__).resolve().parent

        if model_path is None:
            model_path = (
                project_models_dir
                / "behavioral_stress_model.joblib"
            )

        self.model_path = Path(model_path)
        self.reference_hours = float(reference_hours)

        if not self.model_path.exists():
            raise FileNotFoundError(
                f"Trained behavioral model not found: "
                f"{self.model_path}"
            )

        self.model = joblib.load(self.model_path)

        self.feature_columns = [
            "Student_Type",
            "Sleep_Hours",
            "Study_Hours",
            "Social_Media_Hours",
            "Exam_Pressure",
            "Month",
        ]

    def predict_capacity(self, user_data):
        """
        user_data: dictionary containing the six required input features.

        Returns predicted stress class, stress probability,
        capacity proxy, and estimated effective work hours.
        """

        missing = [
            col for col in self.feature_columns
            if col not in user_data
        ]

        if missing:
            raise ValueError(
                f"Missing required features: {missing}"
            )

        input_df = pd.DataFrame(
            [{col: user_data[col]
              for col in self.feature_columns}]
        )

        # Predict binary stress class and elevated-stress probability
        predicted_stress = int(self.model.predict(input_df)[0])

        probabilities = self.model.predict_proba(input_df)[0]
        classes = list(self.model.classes_)

        # Find the probability corresponding to class 1 explicitly
        positive_class_index = classes.index(1)
        stress_probability = float(
            probabilities[positive_class_index]
        )

        # Prototype conversion: stress probability -> capacity proxy
        capacity_score = 1.0 - stress_probability

        effective_hours = (
            capacity_score * self.reference_hours
        )

        return {
            "predicted_stress_level": predicted_stress,
            "stress_probability": round(stress_probability, 4),
            "capacity_score": round(capacity_score, 4),
            "reference_hours": self.reference_hours,
            "effective_work_hours": round(effective_hours, 2),
            "capacity_is_validated": False,
        }


if __name__ == "__main__":
    behavioral_model = BehavioralCapacityModel()

    example_student = {
        "Student_Type": "college",
        "Sleep_Hours": 6.5,
        "Study_Hours": 4.0,
        "Social_Media_Hours": 2.0,
        "Exam_Pressure": 5.0,
        "Month": 10,
    }

    result = behavioral_model.predict_capacity(
        example_student
    )

    print("Behavioral Model Prediction")
    for key, value in result.items():
        print(f"{key}: {value}")
