from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
from prometheus_client import Counter, Histogram, generate_latest
from fastapi.responses import Response

class Features(BaseModel):
    features: List[float]

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
def predict(data: Features):
    REQUEST_COUNT.inc()
    prediction = model.predict([np.array(data.features)])
    PREDICTION_HIST.observe(prediction[0])
    return {"quality": int(prediction[0])}

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type="text/plain")
