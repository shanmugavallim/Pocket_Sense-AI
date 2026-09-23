import os
import joblib

MODEL_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "ml_models",
    "expense_prediction_model.pkl"
)


def predict_next_month_expense(month_index):

    model = joblib.load(MODEL_PATH)

    next_month = month_index + 1

    prediction = model.predict([[next_month]])

    return round(float(prediction[0]), 2)