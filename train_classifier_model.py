import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import joblib

# Load training data
data = pd.read_csv("data/classification_expenses.csv")

# Convert category into numbers
category_mapping = {
    "Food": 0,
    "Transport": 1,
    "Education": 2,
    "Medicine": 3,
    "Shopping": 4,
    "Entertainment": 5,
    "Other": 6
}

data["category_code"] = data["category"].map(category_mapping)

# Input and output
X = data[["category_code", "amount"]]
y = data["label"]

# Create ML model
model = DecisionTreeClassifier(random_state=42)

# Train model
model.fit(X, y)

# Save model

joblib.dump(
    model,
    "ml_models/spending_classifier.pkl"
)

print("Spending classification model trained successfully!")
print("Model saved successfully!")