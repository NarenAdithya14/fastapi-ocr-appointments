import base64
from fastapi.testclient import TestClient
from src.main import app
from src.services.ocr_service import OCRService


client = TestClient(app)


def test_image_base64_path_monkeypatched(monkeypatch):
    # Monkeypatch OCRService to avoid depending on pytesseract during tests
    def fake_extract(self, b):
        return {"raw_text": "book dentist March 10th at 3 PM", "confidence": 0.9}

    monkeypatch.setattr(OCRService, "extract_text_from_bytes", fake_extract)

    payload = {"image_base64": base64.b64encode(b"dummy").decode("utf-8")}
    response = client.post("/appointments", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "appointment" in data
    assert data["appointment"]["department"] == "Dentistry"
    assert data["appointment"]["date"] == "2023-03-10"
    assert data["appointment"]["time"] == "15:00"
