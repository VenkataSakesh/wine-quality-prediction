from fastapi import FastAPI
import joblib
import numpy as np
from prometheus_client import Counter, Histogram, generate_latest
from fastapi.responses import Response
from typing import List
app = FastAPI()
model = joblib.load("wine_model.pkl")

# Metrics
REQUEST_COUNT = Counter("request_count", "Total number of requests")
PREDICTION_HIST = Histogram("prediction_hist", "Distribution of predictions")

@app.get("/")
def home():
    REQUEST_COUNT.inc()
    return {"message": "Wine Quality Prediction API is running!"}

@app.post("/predict")
def predict(features: List[float]):
    REQUEST_COUNT.inc()
    prediction = model.predict([np.array(features)])
    PREDICTION_HIST.observe(prediction[0])
    return {"quality": int(prediction[0])}

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type="text/plain")
if __name__ == "__main__":
    # Sample input with 13 features from the wine dataset
    sample_input = [13.2, 2.77, 2.51, 18.5, 100.0, 2.6, 2.76, 0.26, 1.28, 5.3, 1.02, 3.17, 830.0]
    prediction = predict(sample_input)
    print("Predicted Wine Class:", prediction)

