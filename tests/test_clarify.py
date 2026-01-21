from fastapi.testclient import TestClient
from src.main import app


client = TestClient(app)


def test_clarify_merge():
    pipeline = {"ocr": {"raw_text": "Book dentist next Friday at 3pm", "confidence": 0.9}}
    appointment = {"department": None, "date": None, "time": None, "tz": "Asia/Kolkata"}
    payload = {"pipeline": pipeline, "appointment": appointment, "corrections": {"department": "Dentistry", "date": "2025-09-26", "time": "15:00"}}

    resp = client.post("/appointments/clarify", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ok"
    assert data["appointment"]["department"] == "Dentistry"
    assert data["appointment"]["date"] == "2025-09-26"
    assert data["appointment"]["time"] == "15:00"
