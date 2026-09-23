import os
import joblib

MODEL_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "ml_models",
    "anomaly_detection_model.pkl"
)


def detect_unusual_spending(expenses):
    model = joblib.load(MODEL_PATH)

    unusual = []

    for expense in expenses:

        prediction = model.predict([[expense.amount]])

        if prediction[0] == -1:
            unusual.append(
                f"Unusual spending detected: "
                f"{expense.title} - ₹{expense.amount}"
            )

    return unusual