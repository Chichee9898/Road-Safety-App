# train_flood_model.py

import os
import numpy as np
from sklearn.tree import DecisionTreeClassifier
import joblib

print("Script is running...")
# Create sample training data
X = np.array([
    [10, 1, 2],
    [20, 2, 4],
    [30, 3, 7],
    [35, 2, 8],
    [50, 3, 10],
])

y = ["Low", "Medium", "Medium", "High", "High"]

# Train a decision tree model
model = DecisionTreeClassifier()
model.fit(X, y)

# Save the model to a directory
os.makedirs("ml_models", exist_ok=True)
joblib.dump(model, "ml_models/flood_risk_model.pkl")

print("✅ Model trained and saved to ml_models/flood_risk_model.pkl")
