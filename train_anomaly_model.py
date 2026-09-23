import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib

# Load anomaly training data
data = pd.read_csv("data/anomaly_expenses.csv")

# Input data
X = data[["amount"]]

# Create ML model
model = IsolationForest(
    contamination=0.05,
    random_state=42
)

# Train model
model.fit(X)

# Save trained model
joblib.dump(
    model,
    "ml_models/anomaly_detection_model.pkl"
)

print("Anomaly detection model trained successfully!")
print("Model saved successfully!")