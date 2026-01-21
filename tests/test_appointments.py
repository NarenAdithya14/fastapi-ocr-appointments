from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_create_appointment_valid():
    response = client.post("/appointments", json={
        "text": "Schedule a meeting with John Doe on March 10th at 3 PM."
    })
    assert response.status_code == 200
    assert "appointment_id" in response.json()

def test_create_appointment_invalid_text():
    response = client.post("/appointments", json={
        "text": ""
    })
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "Text must not be empty."

def test_create_appointment_ambiguous_date():
    response = client.post("/appointments", json={
        "text": "Let's meet next week."
    })
    assert response.status_code == 400
    assert response.json()["detail"] == "Ambiguous date provided."

def test_create_appointment_no_text():
    response = client.post("/appointments", json={})
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "Field required."