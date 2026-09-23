import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib

# Load training data
data = pd.read_csv("data/expenses.csv")

# Input and output
X = data[["month"]]
y = data["total_expense"]

# Create ML model
model = LinearRegression()

# Train the model
model.fit(X, y)

# Save trained model
joblib.dump(model, "ml_models/expense_prediction_model.pkl")

print("ML model trained successfully!")
print("Model saved successfully!")