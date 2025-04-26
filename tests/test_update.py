from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_update():
    body = {
        "patient_id": 1,
        "loinc_num": "789-8",
        "taken_at": "2024-01-02T08:00:00Z",
        "new_value": 9100
    }
    r = client.post("/update", json=body)
    assert r.status_code == 200
    assert "newValue" in r.json()