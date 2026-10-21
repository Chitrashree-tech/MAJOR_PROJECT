from statistics import mean


class AdaptiveLearning:

    def __init__(self):
        self.history = []

    def add_feedback(
        self,
        predicted_hours,
        actual_hours,
        completed,
        rating=None
    ):
        record = {
            "predicted_hours": predicted_hours,
            "actual_hours": actual_hours,
            "completed": completed,
            "rating": rating
        }

        self.history.append(record)

    def calculate_error(
        self,
        predicted_hours,
        actual_hours
    ):
        if predicted_hours == 0:
            return 0

        return (
            actual_hours - predicted_hours
        ) / predicted_hours

    def average_error(self):

        if not self.history:
            return 0

        errors = []

        for record in self.history:

            error = self.calculate_error(
                record["predicted_hours"],
                record["actual_hours"]
            )

            errors.append(error)

        return mean(errors)

    def adjustment_factor(self):

        if not self.history:
            return 1.0

        error = self.average_error()

        # If actual work consistently takes longer,
        # increase future estimates.
        factor = 1 + error

        return max(
            0.75,
            min(factor, 1.50)
        )

    def adjust_estimate(
        self,
        predicted_hours
    ):
        factor = self.adjustment_factor()

        return round(
            predicted_hours * factor,
            2
        )

    def get_learning_summary(self):

        return {
            "feedback_records": len(
                self.history
            ),
            "average_error": round(
                self.average_error(),
                3
            ),
            "adjustment_factor": round(
                self.adjustment_factor(),
                3
            )
        }