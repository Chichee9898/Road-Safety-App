import joblib
import os
import numpy as np

model_path = os.path.join('ml_models', 'flood_risk_model.pkl')
model = joblib.load(model_path)

def predict_risk(weather, incidents_nearby):
    # Convert weather and incident info into feature vector
    # Example: ["Rain", 3 accidents nearby] ➝ [1, 3]
    weather_map = {'Clear': 0, 'Rain': 1, 'Storm': 2, 'Flood': 3}
    weather_code = weather_map.get(weather, 0)
    features = np.array([[weather_code, incidents_nearby]])
    
    prediction = model.predict(features)
    return prediction[0]  # "low", "medium", "high"

