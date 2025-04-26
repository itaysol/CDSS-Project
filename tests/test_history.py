from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_history():
    body = {
        "patient_id": 1,
        "loinc_num": "789-8",
        "start": "2024-01-01T00:00:00Z",
        "end": "2024-02-01T00:00:00Z"
    }
    r = client.post("/history", json=body)
    assert r.status_code == 200
    assert isinstance(r.json(), list)