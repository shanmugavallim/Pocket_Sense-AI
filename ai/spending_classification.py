import os
import joblib

MODEL_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "ml_models",
    "spending_classifier.pkl"
)

CATEGORY_MAPPING = {
    "food": 0,
    "transport": 1,
    "education": 2,
    "medicine": 3,
    "shopping": 4,
    "entertainment": 5,
    "other": 6
}


def classify_spending(category, amount):

    model = joblib.load(MODEL_PATH)

    category_code = CATEGORY_MAPPING.get(
        category.lower(),
        6
    )

    prediction = model.predict([
        [category_code, amount]
    ])

    return prediction[0]