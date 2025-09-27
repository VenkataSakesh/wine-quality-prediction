from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert "Wine Quality" in response.json()["message"]

def test_predict():
    response = client.post("/predict", json=[13.0, 2.5, 2.3, 15.6, 120.0, 2.8, 2.6, 0.3, 1.56, 5.1, 1.04, 3.0, 800.0])
    assert response.status_code == 200
    assert "quality" in response.json()
